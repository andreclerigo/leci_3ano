CREATE TABLE Conferencia(
	id INT NOT NULL,

	PRIMARY KEY (id)
);

CREATE TABLE Instituicao(
	nome varchar(30) NOT NULL,
	endereco varchar(40) NOT NULL,

	PRIMARY KEY (nome)
);

CREATE TABLE Artigo(
	no_registo INT NOT NULL,
	titulo varchar(40) NOT NULL,

	PRIMARY KEY (no_registo)
);

CREATE TABLE Apresenta(
	id_conf INT NOT NULL,
	no_registo_artigo INT NOT NULL,

	PRIMARY KEY (id_conf, no_registo_artigo),
	FOREIGN KEY (id_conf) REFERENCES Conferencia(id),
	FOREIGN KEY (no_registo_artigo) REFERENCES Artigo(no_registo),
);

CREATE TABLE Autor(
	email varchar(40) NOT NULL,
	nome varchar(40) NOT NULL,
	inst_nome varchar(30) NOT NULL,

	PRIMARY KEY (email),
	FOREIGN KEY (inst_nome) REFERENCES Instituicao(nome)
);

CREATE TABLE Tem(
	autor_email varchar(40) NOT NULL,
	no_registo_artigo INT NOT NULL,

	PRIMARY KEY (autor_email, no_registo_artigo),
	FOREIGN KEY (autor_email) REFERENCES Autor(email),
	FOREIGN KEY (no_registo_artigo) REFERENCES Artigo(no_registo)
);

CREATE TABLE Participante(
	email varchar(40) NOT NULL,
	data_inscr DATE NOT NULL,
	morada varchar(40) NOT NULL,
	nome varchar(40) NOT NULL,
	id_conf INT NOT NULL,

	PRIMARY KEY (email),
	FOREIGN KEY (id_conf) REFERENCES Conferencia(id)
);

CREATE TABLE Nao_Estudante(
	email varchar(40) NOT NULL,
	data_inscr DATE NOT NULL,
	morada varchar(40) NOT NULL,
	nome varchar(50) NOT NULL,
	ref_trans INT NOT NULL,

	PRIMARY KEY (email),
	FOREIGN KEY (email) REFERENCES Participante(email)
);

CREATE TABLE Estudante(
	email varchar(40) NOT NULL,
	data_inscr DATE NOT NULL,
	morada varchar(40) NOT NULL,
	nome varchar(50) NOT NULL,
	inst_nome varchar(30) NOT NULL,
	
	PRIMARY KEY (email),
	FOREIGN KEY (email) REFERENCES Participante(email),
	FOREIGN KEY (inst_nome) REFERENCES Instituicao(nome)
);