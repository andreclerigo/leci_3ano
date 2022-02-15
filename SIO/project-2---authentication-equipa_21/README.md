# project-2---authentication-equipa_21
## Description
### UAP
A nossa UAP consiste num serviço que permite vários utilizadores guardar credenciais (vault) e consequentemente autenticar as suas contas em vários serviços. O vault da UAP guarda as vários pares de credencias associados a um DNS, esta informação é sempre guardada num ficheiro .json associado a cada utilizador sendo permitido que um utilizador tenha várias credenciais para um dado DNS desque não tenham o mesmo username.<br>
É possivel registar um novo utilizador na UAP inserindo o seu username e password, esses dados são utilizados para posteriormente realizar o login no vault da UAP e no secure login do SIO Forum. No vault da UAP é possivel registar várias credencias inserindo o DNS, o username desejado e a respetiva palavra-passe.

#### Encriptação
A encriptação das credenciais funciona de maneira muito simples. Na hora da encriptação do ficheiro .json que está associado a todos os utilizadores da UAP é gerado um random salt e um nonce, o salt é usado para a Key Derivation Function (PBKDF2) que vair gerar a key a partir da hashed password do utilizador na UAP, o nonce vai ser usado para fazer uma cifra de ChaCha20 que posteriormente é usada para encriptar o ficheiro .json. É também gerado um HMAC do criptograma para o controlo de integridade do mesmo. O ficheiro cifrado vai ser constituido por nonce, salt, assinatura HMAC e criptograma.<br>
No processo de desencriptação os elementos de nonce e salt são retirados para gerar a mesma key e a mesma cifra (dado que se sabe qual é a hashed password), antes de desencriptar comparamos o HMAC esperado com o HMAC que é inserido no ínicio do ficheiro cifrado, caso estes não sejam coincidentes um erro é gerado e o processo é interrompido, caso o HMAC esteja correto, usamos a cifra gerada em ChaCha20 para desencriptar os dados, ficando com um objeto json das credenciais.
O processo de desencriptação acontece sempre que o utilizador dá login na UAP dando load do json em formato dicionário para uma váriavel guardar em session no cherrypy (mantendo assim o .json sempre encriptado). O processo de encriptação acontece sempre que as credenciais são alteradas, isto é, quando se adiciona e remove crendenciais, mas também quando se altera a password do utilizador na UAP (isto porque o processo de encriptação das credenciais está profundamente ligado com a password do utilizador na UAP).

### Protocolo E-CHAP

Os pacotes que seguem o nosso protocolo E-CHAP tem o seguinte formato:
|-----| Header |------| Data|
| -- | -- | -- | -- |
| Code | Identifier | Length | Data |
| 1 byte | 1 byte | 2 bytes | N bytes |

#### Codes
Os códigos dos nossos pacotes são reconhecidos de seguinte modo:

| Valor | Código |
| -- | -- |
| 0x00 | AUTHENTICATION_REQUEST |
| 0x01 | CHALLENGE |
| 0x02 | REQUEST |
| 0x03 | SUCCESS |
| 0x04 | FAILURE |

#### Identifier
O identificador é um número aleatório entre 0 e 255 que identificam os pacotes para um exchange entre peer e autenticador, isto serve para mais facilmente se identificar uma conversa e verificar se um pacote não foi alterado.

#### Length
A length é o valor em bytes dos dados enviados no pacote mais o valor do header do pacote (que neste caso é sempre 4).

#### Data
Os dados é efetivamente o que vai ser enviado no pacote, normalmente será um valor de 1byte que representa o bit trocado na mensagem, mas pode também ser o valor de 32, 64, ... bytes para se trocar informação como o salt, challenge, identidades e etc.

#### Processo
No protocolo E-CHAP é feita troca de pacotes entre o peer (UAP) e o autenticador (SIO Forum) por forma a garantir confianaça entre ambos. 
1. O peer envia um `AUTHENTICATION_REQUEST` com o username que quer autenticar e o nome do serviço (UAP).
2. O autenticador recebe o pacote e verifica se este é um `AUTHENTICATION_REQUEST`, se sim, dá parse dos dados. Caso isto não esteja correto a comunicação é abortada.
3. O autenticador verifica se o username existe na base de dados, se sim, vai buscar a hashed password e o salt usado para essa hash. Caso o utilizador na exista na base de dados, um valor de hash e salt random são gerados.
4. O autenticador cria um Challenge, um Identifier para a conversa e envia uma pacote com o código `CHALLENGE` que nos dados contém o valor do Challenge gerado, o valor do salt usado e o nome do serviço (localhost).
5. O autenticador, com o valor do Challenge e da hash password, cria uma chave com PBKDF2.
6. O peer recebe o pacote e verifica se este é um `CHALLENGE`, se sim, dá parse dos dados. Caso isto não esteja correto a comunicação é abortada.
7. Com o valor do salt cria a mesma hash password que o autenticador tem do seu lado e com o Challenge gera a mesma chave que o autenticador tem do seu lado.<br>
Ambos os lados possuem uma flag de erros que é inicializada a True (não há erros).
9. O peer gera um pacote de resposta com o código `RESPONSE` e nos dados segue o bit 0(n) da sua chave e o nome do serviço (UAP). Caso a Flag esteja a False, o valor de bit enviado é random.
10. O autenticador recebe o pacote, se a sua Flag estiver a True, este verifica se os dados estão corretos (Código esperado, Identifier esperado, Identity esperada, e valor do bit esperado para essa posição). Se os valores não forem os esperados a Flag é posta a False.
11. Se os dados tiverem corretos o valor do seguinte bit é retirado da sua chave e o autenticador envia um pacote com o código `RESPONSE` e nos dados segue o bit 1 (n+1) da sua chave e nome do serviço (localhost). Caso a Flag esteja a False, o valor de bit enviado é random.
12. O peer recebe o pacote, se a sua Flag estiver a True, este verifica se os dados estão corretos (Código esperado, Identifier esperado, Identity esperada, e valor do bit esperado para essa posição). Caso a Flag esteja a False, o valor de bit enviado é random.
13. O processo 8 a 11 é repetido mais 63 vezes incrementado a posição do bit a ser enviada, de modo a que cada uma das entidades envie 64 bits, tendo sido no total verificado 128 bits da chave (16 bytes) de um total de 32 bytes que as chaves vão ter.

#### Token
Depois do processo de autenticação estar completo e não haver qualquer erro por ambas as partes (valor da flag a True), o autenticador (SIO Forum) envia um último pacote ao peer (UAP) com o código `SUCCESS` e um salt. Vistos que ambas as entidades têm confiança uma na outra, sabem que ambas têm a mesma hashed password, com o novo salt tanto o autenticador como o peer geram uma key, o autenticador mete essa key (em formato string) na sua base de dados e associada ao utilizador que fez o pedido de autenticação, a UAP vai redirecionar o utilizador para o login do autenticador dando um parametro adicional (?token=) à página, esse token é a key que a UAP gerou com o novo sal (em formato string).<br>
Finalmente, quando SIO Forum vê que alguém está a fazer um login com o token, o serviço vai verificar se esse token existe na base de dados, e se sim, a quem é que está associado.<br>
Caso isto seja verdade duas coisas acontecem:
1. O utilizador é logged in no serviço
2. O token utilizado é rescrito com o valor NULL na base de dados, de modo a que aquele token em especifico nunca mais seja possível de ser usado

Caso o token esteja incorreto uma página de erro genérica é mostrada ao utilizador.

Se o processo de autenticação não for válido o autenticador manda uma mensagem de erro para o peer com o código `FAILURE` e nada acontece.
### Contas
As contas que existem na UAP são:

1. username: andre | password: clerigo  
    Dentro desta conta UAP existem as seguintes credenciais para o SIO Forum (localhost:8080 ou 127.0.0.1:8080)
    - username: CSGOd | password: pass4 ✅ (Utilizador existe no SIO Forum)
    - username: user | password: pass ❌ (Utilizador não existe no SIO Forum)
    - username: Hugito | password: pass2 ✅

2. username: user | password: user  
    Dentro desta conta UAP existem as seguintes credenciais para o SIO Forum (localhost:8080 ou 127.0.0.1:8080)
    - username: Tiagura | password: pass1 ✅
    - username: Rager | password: wrong ❌ (Utilizador existe no SIO Forum mas password está errada)
## How to run
1. Crie um virtual environment:
```bash
python3 -m venv venv
```

2. Ative o virtual environment (precisa de repetir este passo sempre que começar uma nossa sessão/terminal):
```bash
source venv/bin/activate
```

3. Instale os requisitos:
```bash
pip install -r requirements.txt
```

4. Corra o servidor:
```bash
python3 app_auth.py
```

4. Corra a UAP:
```bash
cd uap/
python3 uap.py
```

5. Aceda à UAP:

    http://127.0.0.1:8081/
    
6. Insira credenciais na UAP para o(s) DNS 127.0.0.1:8080 e localhost:8080

7. Aceda ao Website:

    http://127.0.0.1:8080/

8. Clique em Secure Login e insira as credenciais da sua UAP

## Authors
[André Clérigo](https://github.com/andreclerigo), 98485  
[Cláudio Asensio](https://github.com/ClaudioAsensio), 98433  
[Hugo Domingos](https://github.com/Hugo-Domingos), 98502  
[Tiago Marques](https://github.com/Tiagura), 98459  

## Grade
18,5
