CREATE TABLE MEDICO (
	num_sns INT NOT NULL CHECK (num_sns > 0),
	nome VARCHAR(50) NOT NULL,
	especialidade VARCHAR(50) NOT NULL,
	PRIMARY KEY (num_sns)
);

CREATE TABLE PACIENTE (
	num_utente INT NOT NULL CHECK (num_utente > 0 AND num_utente < 999999999),
	data_nasc DATE NOT NULL,
	nome VARCHAR(50) NOT NULL,
	endereco VARCHAR(50) NOT NULL,
	PRIMARY KEY (num_utente)
);

CREATE TABLE FARMACIA (
	telefone VARCHAR(9) NOT NULL,
	endereço VARCHAR(50) NOT NULL,
	nome VARCHAR(50) NOT NULL,
	NIF INT NOT NULL CHECK (NIF > 0 AND NIF < 999999),
	PRIMARY KEY (NIF)
);

CREATE TABLE FARMACEUTICA (
	num_registo INT NOT NULL CHECK (num_registo > 0),
	telefone VARCHAR(9) NOT NULL,
	endereço VARCHAR(50) NOT NULL,
	nome VARCHAR(50) NOT NULL,
	PRIMARY KEY (num_registo)
);

CREATE TABLE PRESCRICAO (
	num_unico INT NOT NULL CHECK (num_unico > 0),
	data_presc DATE NOT NULL,
	medico_num_sns INT NOT NULL,
	paciente_num_utente INT NOT NULL,
	farmacia_NIF INT NOT NULL,
	PRIMARY KEY (num_unico),
	FOREIGN KEY (farmacia_NIF) REFERENCES FARMACIA(NIF),
	FOREIGN KEY (medico_num_sns) REFERENCES MEDICO(num_sns),
	FOREIGN KEY (paciente_num_utente) REFERENCES PACIENTE(num_utente)
);

CREATE TABLE FARMACO (
	farma_num_reg INT NOT NULL,
	formula VARCHAR(100) NOT NULL,
	nome VARCHAR(50) NOT NULL,
	PRIMARY KEY (farma_num_reg, nome),
	FOREIGN KEY (farma_num_reg) REFERENCES FARMACEUTICA (num_registo),
);

CREATE TABLE TEM (
	presc_num_unico INT NOT NULL,
	farmaco_nome VARCHAR(50) NOT NULL,
	farm_num_reg INT NOT NULL,
	PRIMARY KEY (presc_num_unico, farmaco_nome),
	FOREIGN KEY (farm_num_reg, farmaco_nome) REFERENCES FARMACO(farma_num_reg, nome),
	FOREIGN KEY (presc_num_unico) REFERENCES PRESCRICAO(num_unico),
);
