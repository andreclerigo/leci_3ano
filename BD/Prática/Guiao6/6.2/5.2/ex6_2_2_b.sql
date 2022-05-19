-- insert dataset info

INSERT INTO GESTSTOCK.tipo_fornecedor(codigo,designacao)VALUES(101,'Carnes')
INSERT INTO GESTSTOCK.tipo_fornecedor(codigo,designacao)VALUES(102,'Laticinios')
INSERT INTO GESTSTOCK.tipo_fornecedor(codigo,designacao)VALUES(103,'Frutas e Legumes')
INSERT INTO GESTSTOCK.tipo_fornecedor(codigo,designacao)VALUES(104,'Mercearia')
INSERT INTO GESTSTOCK.tipo_fornecedor(codigo,designacao)VALUES(105,'Bebidas')
INSERT INTO GESTSTOCK.tipo_fornecedor(codigo,designacao)VALUES(106,'Peixe')
INSERT INTO GESTSTOCK.tipo_fornecedor(codigo,designacao)VALUES(107,'Detergentes')
INSERT INTO GESTSTOCK.fornecedor(nif,nome,fax,endereco,condpag,tipo)VALUES(509111222,'LactoSerrano',234872372,NULL,60,102)
INSERT INTO GESTSTOCK.fornecedor(nif,nome,fax,endereco,condpag,tipo)VALUES(509121212,'FrescoNorte',221234567,'Rua do Complexo Grande - Edf 3',90,102)
INSERT INTO GESTSTOCK.fornecedor(nif,nome,fax,endereco,condpag,tipo)VALUES(509294734,'PinkDrinks',2123231732,'Rua Poente 723',30,105)
INSERT INTO GESTSTOCK.fornecedor(nif,nome,fax,endereco,condpag,tipo)VALUES(509827353,'LactoSerrano',234872372,NULL,60,102)
INSERT INTO GESTSTOCK.fornecedor(nif,nome,fax,endereco,condpag,tipo)VALUES(509836433,'LeviClean',229343284,'Rua Sol Poente 6243',30,107)
INSERT INTO GESTSTOCK.fornecedor(nif,nome,fax,endereco,condpag,tipo)VALUES(509987654,'MaduTex',234873434,'Estrada da Cincunvalacao 213',30,104)
INSERT INTO GESTSTOCK.fornecedor(nif,nome,fax,endereco,condpag,tipo)VALUES(590972623,'ConservasMac',234112233,'Rua da Recta 233',30,104)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10001,'Bife da Pa',8.75,23,125)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10002,'Laranja Algarve',1.25,23,1000)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10003,'Pera Rocha',1.45,23,2000)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10004,'Secretos de Porco Preto',10.15,23,342)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10005,'Vinho Rose Plus',2.99,13,5232)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10006,'Queijo de Cabra da Serra',15.00,23,3243)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10007,'Queijo Fresco do Dia',0.65,23,452)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10008,'Cerveja Preta Artesanal',1.65,13,937)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10009,'Lixivia de Cor',1.85,23,9382)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10010,'Amaciador Neutro',4.05,23,932432)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10011,'Agua Natural',0.55,6,919323)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10012,'Pao de Leite',0.15,6,5434)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10013,'Arroz Agulha',1.00,13,7665)
INSERT INTO GESTSTOCK.produto(codigo,nome,preco,iva,unidades)VALUES(10014,'Iogurte Natural',0.40,13,998)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(1,'2015-03-03',509111222)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(2,'2015-03-04',509121212)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(3,'2015-03-05',509987654)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(4,'2015-03-06',509827353)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(5,'2015-03-07',509294734)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(6,'2015-03-08',509836433)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(7,'2015-03-09',509121212)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(8,'2015-03-10',509987654)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(9,'2015-03-11',509836433)
INSERT INTO GESTSTOCK.encomenda(numero,data,fornecedor)VALUES(10,'2015-03-12',509987654)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(1,10001,200)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(1,10004,300)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(2,10002,1200)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(2,10003,3200)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(3,10013,900)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(4,10006,50)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(4,10007,40)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(4,10014,200)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(5,10005,500)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(5,10008,10)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(5,10011,1000)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(6,10009,200)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(6,10010,200)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(7,10003,1200)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(8,10013,350)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(9,10009,100)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(9,10010,300)
INSERT INTO GESTSTOCK.item(numEnc,codProd,unidades)VALUES(10,10012,200)