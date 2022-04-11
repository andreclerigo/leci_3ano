CREATE TABLE EMPRESA (
	nome VARCHAR(30) NOT NULL,
	NIF INT NOT NULL CHECK(NIF > 0 AND NIF < 999999),
	PRIMARY KEY (NIF)
);

CREATE TABLE PRODUTO (
	codigo INT NOT NULL CHECK (codigo > 0),
	empresa_NIF INT NOT NULL,
	nome VARCHAR(30) NOT NULL,
	iva float NOT NULL CHECK (iva >= 0),
	preco float NOT NULL CHECK (preco >= 0),
	qtd_armazem INT NOT NULL CHECK (qtd_armazem >= 0),
	PRIMARY KEY (codigo, empresa_NIF),
	FOREIGN KEY (empresa_NIF) REFERENCES EMPRESA(NIF)
);

CREATE TABLE TIPO_FORNECEDOR (
	designacao VARCHAR(100) NOT NULL,
	cod_interno INT NOT NULL CHECK (cod_interno > 0),
	PRIMARY KEY (cod_interno)
);

CREATE TABLE FORNECEDOR (
	NIF INT NOT NULL CHECK (NIF > 0 AND NIF < 999999),
	tipo_cod_interno INT NOT NULL CHECK (tipo_cod_interno > 0),
	nome VARCHAR(30) NOT NULL,
	FAX VARCHAR(9) NOT NULL,
	endereco VARCHAR(30) NOT NULL,
	cond_pagamento INT NOT NULL CHECK (cond_pagamento > 0 AND cond_pagamento <= 90),
	PRIMARY KEY (NIF),
	FOREIGN KEY (tipo_cod_interno) REFERENCES TIPO_FORNECEDOR(cod_interno),
);

CREATE TABLE ENCOMENDA (
	num INT NOT NULL CHECK (num > 0),
	empresa_NIF INT NOT NULL,
	data_encomenda DATE NOT NULL,
	fornecedor_NIF INT NOT NULL,
	PRIMARY KEY (num, empresa_NIF, fornecedor_NIF),
	FOREIGN KEY (empresa_NIF) REFERENCES EMPRESA(NIF),
	FOREIGN KEY (fornecedor_NIF) REFERENCES FORNECEDOR(NIF)
);

CREATE TABLE TEM (
	qtd INT NOT NULL CHECK (qtd > 0),
	encomenda_num INT,
	prod_codigo INT NOT NULL,
	empresa_NIF INT NOT NULL,
	PRIMARY KEY (encomenda_num, prod_codigo),
	FOREIGN KEY (prod_codigo, empresa_NIF) REFERENCES PRODUTO(codigo, empresa_NIF)
);

CREATE TABLE FORNECE (
	empresa_NIF INT NOT NULL,
	fornecedor_NIF INT NOT NULL,
	PRIMARY KEY (empresa_NIF, fornecedor_NIF),
	FOREIGN KEY (empresa_NIF) REFERENCES EMPRESA(NIF),
	FOREIGN KEY (fornecedor_NIF) REFERENCES FORNECEDOR(NIF)
);

