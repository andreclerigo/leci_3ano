-- Create Databases

CREATE SCHEMA GESTSTOCK;
GO
--CREATE DATABASE GESTSTOCK;

CREATE TABLE GESTSTOCK.tipo_fornecedor(
	codigo INT NOT NULL CHECK(codigo> 0),
	designacao	VARCHAR(20),
	PRIMARY KEY(codigo),
	UNIQUE(codigo),
);

CREATE TABLE GESTSTOCK.fornecedor(
	nif INT NOT NULL CHECK(nif> 0),	
	nome VARCHAR(15),
	fax INT,	
	endereco VARCHAR(40),
	condpag VARCHAR(20),
	tipo INT,
	PRIMARY KEY(nif),
	UNIQUE(nif),
	FOREIGN KEY(tipo) REFERENCES GESTSTOCK.tipo_fornecedor(codigo)
);

CREATE TABLE GESTSTOCK.produto(
	codigo INT NOT NULL CHECK(codigo> 0),	
	nome VARCHAR(30) NOT NULL,
	preco SMALLMONEY NOT NULL CHECK(preco> 0),	
	iva INT DEFAULT 23,
	unidades INT CHECK(unidades> 0),
	PRIMARY KEY(codigo),
	UNIQUE(codigo)
);

CREATE TABLE GESTSTOCK.encomenda(
	numero INT NOT NULL CHECK(numero> 0),	
	[data] DATE,
	fornecedor INT,
	PRIMARY KEY(numero),
	UNIQUE(numero),
	FOREIGN KEY(fornecedor) REFERENCES GESTSTOCK.fornecedor(nif)
);

CREATE TABLE GESTSTOCK.item(
	numEnc INT,	
	codProd INT,
	unidades INT,
	FOREIGN KEY(numEnc) REFERENCES GESTSTOCK.encomenda(numero),
	FOREIGN KEY(codProd) REFERENCES GESTSTOCK.produto(codigo),
);