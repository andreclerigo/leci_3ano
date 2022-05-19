-- create database
CREATE SCHEMA Company;
GO
CREATE DATABASE Company;

CREATE TABLE Company.Department(
	Dname			VARCHAR(45)		NOT NULL,
	Dnumber			INT				CHECK(Dnumber> 0),
	Mgr_Ssn			CHAR(9),
	Mgr_start_date	DATE,

	PRIMARY KEY (Dnumber)
);

CREATE TABLE Company.Employee (
	Fname		VARCHAR(15)		NOT NULL,
	Minit		CHAR(1),
	Lname		VARCHAR(15)		NOT NULL,
	Ssn			CHAR(9),
	Bdate		DATE,
	e_Address	VARCHAR(45),	
	Sex			CHAR(1)			NOT NULL	CHECK(Sex='F' OR Sex='M'),
	Salary		DECIMAL(6,2)	NOT NULL	CHECK(Salary >= 0),
	Super_ssn	CHAR(9),
	Dno			INT				NOT NULL
	
	PRIMARY KEY (Ssn),			
	FOREIGN KEY (Dno) REFERENCES Company.Department (Dnumber)
);

ALTER TABLE Company.Employee ADD CONSTRAINT employeeSuper FOREIGN KEY (Super_ssn) REFERENCES Company.Employee (Ssn);

CREATE TABLE Company.Dept_locations(
	Dnumber		INT,
	Dlocation	VARCHAR(30)

	PRIMARY KEY (Dnumber,Dlocation),
	FOREIGN KEY (Dnumber) REFERENCES Company.Department(Dnumber)
);

CREATE TABLE Company.Project(
	Pname		VARCHAR(45)		NOT NULL,
	Pnumber		INT				CHECK(Pnumber> 0),
	Plocation	VARCHAR(15)		NOT NULL,
	Dnum		INT				NOT NULL,

	PRIMARY KEY (Pnumber),
	FOREIGN KEY (Dnum) REFERENCES Company.Department (Dnumber)
);

CREATE TABLE Company.Works_on(
	Essn	CHAR(9),
	Pno		INT,
	[Hours]	DECIMAL(4,2)	NOT NULL,

	PRIMARY KEY (Essn,Pno),
	FOREIGN KEY (Pno) REFERENCES Company.Project (Pnumber),
	FOREIGN KEY (Essn) REFERENCES Company.Employee (Ssn)
);

CREATE TABLE Company.[Dependent](
	Essn			CHAR(9),
	Dependent_name	VARCHAR(45),
	Sex				CHAR(1)		NOT NULL,
	Bdate			DATE,
	Relationship	VARCHAR(15)	NOT NULL,

	PRIMARY KEY (Essn,Dependent_name),
	FOREIGN KEY (Essn) REFERENCES Company.Employee (Ssn)
);