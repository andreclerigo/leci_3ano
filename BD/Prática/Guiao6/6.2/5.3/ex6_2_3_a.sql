CREATE SCHEMA Prescricao;
GO
--CREATE DATABASE Prescricao;

CREATE TABLE Prescricao.Medico(
    numSNS              INT         PRIMARY KEY,
    nome                VARCHAR(45) NOT NULL,
    especialidade       VARCHAR(45),                      
);

CREATE TABLE Prescricao.Paciente(
    numUtente           INT         PRIMARY KEY,
    nome                VARCHAR(45) NOT NULL,
    dataNasc            DATE        NOT NULL,
    endereco            TEXT,
);

CREATE TABLE Prescricao.Farmacia(
    nome                VARCHAR(45) PRIMARY KEY,
    telefone            INT         UNIQUE,
    endereco            TEXT,                      
);

CREATE TABLE Prescricao.Farmaceutica(
    numReg              INT         PRIMARY KEY,
    nome                VARCHAR(45),
    endereco            TEXT,                      
);

CREATE TABLE Prescricao.Farmaco(
    numRegFarm          INT,
    nome                VARCHAR(45),
    formula             TEXT,                      
    PRIMARY KEY (numRegFarm, nome),
	FOREIGN KEY (numRegFarm)REFERENCES Prescricao.Farmaceutica(numReg) ON DELETE NO ACTION ON UPDATE CASCADE,
);

CREATE TABLE Prescricao.Prescricao(
    numPresc            INT         PRIMARY KEY,
    numUtente           INT         NOT NULL REFERENCES Prescricao.Paciente(numUtente) ON DELETE NO ACTION ON UPDATE CASCADE,
    numMedico           INT         NOT NULL REFERENCES Prescricao.Medico(numSNS) ON DELETE NO ACTION ON UPDATE CASCADE,
    farmacia            VARCHAR(45) REFERENCES Prescricao.Farmacia(nome) ON DELETE NO ACTION ON UPDATE CASCADE,
    dataProc            DATE,
);

CREATE TABLE Prescricao.Presc_farmaco(
    numPresc            INT	REFERENCES Prescricao.Prescricao(numPresc) ON DELETE NO ACTION ON UPDATE CASCADE,
    numRegFarm          INT,
    nomeFarmaco         VARCHAR(45),
    FOREIGN KEY (numRegFarm, nomeFarmaco) REFERENCES Prescricao.Farmaco(numRegFarm, nome) ON DELETE NO ACTION ON UPDATE CASCADE,
    PRIMARY KEY (numPresc, numRegFarm, nomeFarmaco),
);