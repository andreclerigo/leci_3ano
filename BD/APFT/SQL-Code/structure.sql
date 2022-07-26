CREATE SCHEMA AltoRendimento;
GO

CREATE TABLE Atleta (
    n_inscricao INTEGER IDENTITY(1, 1) NOT NULL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    data_nasc DATE NOT NULL,
    modalidade VARCHAR(15) NOT NULL CHECK (modalidade IN('natacão', 'judo', 'ténis', 'basquetebol', 'atletismo', 'voleibol', 'badminton', 'rugby')),
	idade AS FLOOR( DATEDIFF(hour, data_nasc, GETDATE() ) / 8766),      /* Calcular idade a partir da data de nasicmento*/
	 /* Quando o atleta é criado, o seu estado de saude é indefinido (mesmo se especificado outro), e por isso, necessita de uma consulta */
    estado_saude VARCHAR(10) NOT NULL DEFAULT 'indefinido' CHECK (estado_saude IN('apto', 'inapto', 'indefinido')),
    CHECK (data_nasc <=  CAST( DATEADD(year, -14, GETDATE()) AS Date )) /* Atleta tem que ter pelo menos 14 anos */
);

CREATE TABLE Estabelecimento (
    id INTEGER IDENTITY(1, 1) NOT NULL PRIMARY KEY,
    hora_aberto TIME NOT NULL CHECK (hora_aberto >= '05:00'),
    hora_fechado TIME NOT NULL CHECK ('23:30' >= hora_fechado),
    data_manutencao DATE NOT NULL,								/* No dia da data de manutenção (dia-da-semana), não é possível marcar treinos */
    lotacao INTEGER NOT NULL,
    CHECK (lotacao >= 0),
    CHECK (hora_aberto < hora_fechado),
);

CREATE TABLE Piscina (
    id INTEGER PRIMARY KEY,
    temp_agua FLOAT NOT NULL,
    CHECK (temp_agua >= 20 AND temp_agua <= 30),
    FOREIGN KEY (id) REFERENCES Estabelecimento(id) ON DELETE CASCADE,
);

CREATE TABLE Ginasio (
    id INTEGER NOT NULL PRIMARY KEY,
    qtd_aparelhos INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES Estabelecimento(id) ON DELETE CASCADE,
);

CREATE TABLE Pista (
    id INTEGER NOT NULL PRIMARY KEY,
    tipo_solo VARCHAR(15) NOT NULL CHECK (tipo_solo IN('esteira', 'argila', 'areia', 'sintética', 'asfalto')),
    FOREIGN KEY (id) REFERENCES Estabelecimento(id) ON DELETE CASCADE,
);

CREATE TABLE Empregado (
    n_func INTEGER IDENTITY(1, 1) NOT NULL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    salario FLOAT NOT NULL,
    nif INTEGER NOT NULL UNIQUE,
    CHECK (nif >= 100000000 AND nif <= 499999999), -- NIF acima de 500000000 são de empresas
    CHECK (salario >= 705)
);

CREATE TABLE Treinador (
    n_func INTEGER NOT NULL PRIMARY KEY,
    modalidade VARCHAR(15) NOT NULL CHECK (modalidade IN('natacão', 'judo', 'ténis', 'basquetebol', 'atletismo', 'voleibol', 'badminton', 'rugby')),
    FOREIGN KEY (n_func) REFERENCES Empregado(n_func) ON DELETE CASCADE,
);

CREATE TABLE Secretariado (
    n_func INTEGER NOT NULL PRIMARY KEY,
    id_estabelecimento INTEGER,
    FOREIGN KEY (id_estabelecimento) REFERENCES Estabelecimento(id) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (n_func) REFERENCES Empregado(n_func) ON DELETE CASCADE,
);

CREATE TABLE Emp_Saude (
    n_func INTEGER NOT NULL PRIMARY KEY,
    especialidade VARCHAR(15) NOT NULL CHECK (especialidade IN('fisioterapia', 'medicina geral', 'cardiologia', 'oftalmologia', 'nutricão')),
    FOREIGN KEY (n_func) REFERENCES Empregado(n_func) ON DELETE CASCADE,
);

CREATE TABLE Reserva (
    num_reserva INTEGER IDENTITY(1, 1) NOT NULL PRIMARY KEY,
    n_func_treinador INTEGER,
    n_insc_atleta INTEGER NOT NULL,
    data_reserva DATE NOT NULL CHECK (data_reserva >= GETDATE()),
    hora_inicio TIME NOT NULL,
    duracao TIME NOT NULL CHECK (duracao <= '6:00:00'),
	hora_fim AS (DATEADD(MINUTE, (DATEDIFF(MINUTE, 0, duracao)), hora_inicio)),
    id_estabelecimento INTEGER NOT NULL,
	FOREIGN KEY (id_estabelecimento) REFERENCES Estabelecimento(id),
    FOREIGN KEY (n_insc_atleta) REFERENCES Atleta(n_inscricao) ON DELETE CASCADE,
    FOREIGN KEY (n_func_treinador) REFERENCES Treinador(n_func) ON DELETE CASCADE
);

CREATE TABLE Sessao_Treino (
    num_reserva INTEGER NOT NULL PRIMARY KEY,
    avaliacao INTEGER CHECK (avaliacao >= 0 AND avaliacao <= 20), --melhor tempo/score da modalidade no centro de alto rendimento tem nota 20
    FOREIGN KEY (num_reserva) REFERENCES Reserva(num_reserva) ON DELETE CASCADE,
);

CREATE TABLE Consulta(
    id_consulta INTEGER IDENTITY(1, 1) NOT NULL PRIMARY KEY,
    n_func_emp INTEGER NOT NULL,
    n_insc_atleta INTEGER NOT NULL,
    data_consulta DATE NOT NULL,				/* Para efeitos de teste, podemos adicionar consultas com datas passadas */
    estado_saude VARCHAR(10) NOT NULL CHECK (estado_saude IN ('apto', 'inapto')),
    FOREIGN KEY (n_func_emp) REFERENCES Emp_Saude(n_func),
    FOREIGN KEY (n_insc_atleta) REFERENCES Atleta(n_inscricao)
);

/* TO DO
Insertion consulta, reserva, sessao_treino
*/

/* IDEIAS E CENAS 
View para ver o estado de saude do atleta (ir à tabela das consultas ver qual foi a ultima dele, o estado dele 
e há quanto tempo foi, se for acima de X meses ou um estado mau, então tem que ser avaliado novamente)

Restringir o estado do atleta com um enum (lesionado, apto)
Fazer um ENUM para modalidades
Funcao calculo da idade idade 

Times dos horários ficarem em formato HH:mm sempre
*/

/* DUVIDAS PROFESSOR 
Deixar dar update a uma consulta já feita, apenas registada?
*/