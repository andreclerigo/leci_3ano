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

-- Insert dataset info
INSERT INTO COMPANY.DEPARTMENT(Dname,Dnumber,Mgr_ssn,Mgr_start_date)VALUES('Investigacao',1,21312332,'2010-08-02')
INSERT INTO COMPANY.DEPARTMENT(Dname,Dnumber,Mgr_ssn,Mgr_start_date)VALUES('Comercial',2,321233765,'2013-05-16')
INSERT INTO COMPANY.DEPARTMENT(Dname,Dnumber,Mgr_ssn,Mgr_start_date)VALUES('Logistica',3,41124234,'2013-05-16')
INSERT INTO COMPANY.DEPARTMENT(Dname,Dnumber,Mgr_ssn,Mgr_start_date)VALUES('Recursos Humanos',4,12652121,'2014-04-02')
INSERT INTO COMPANY.DEPARTMENT(Dname,Dnumber,Mgr_ssn,Mgr_start_date)VALUES('Desporto',5,NULL,NULL)
INSERT INTO COMPANY.EMPLOYEE(Fname,Minit,Lname,Ssn,Bdate,e_Address,Sex,Salary,Super_ssn,Dno)VALUES('Paula','A','Sousa',183623612,'2001-08-11','Rua da FRENTE','F',1450.00,NULL,3)
INSERT INTO COMPANY.EMPLOYEE(Fname,Minit,Lname,Ssn,Bdate,e_Address,Sex,Salary,Super_ssn,Dno)VALUES('Carlos','D','Gomes',21312332,'2000-01-01','Rua XPTO','M',1200.00,NULL,1)
INSERT INTO COMPANY.EMPLOYEE(Fname,Minit,Lname,Ssn,Bdate,e_Address,Sex,Salary,Super_ssn,Dno)VALUES('Juliana','A','Amaral',321233765,'1980-08-11','Rua BZZZZ','F',1350.00,NULL,3)
INSERT INTO COMPANY.EMPLOYEE(Fname,Minit,Lname,Ssn,Bdate,e_Address,Sex,Salary,Super_ssn,Dno)VALUES('Maria','I','Pereira',342343434,'2001-05-01','Rua JANOTA','F',1250.00,21312332,2)
INSERT INTO COMPANY.EMPLOYEE(Fname,Minit,Lname,Ssn,Bdate,e_Address,Sex,Salary,Super_ssn,Dno)VALUES('Joao','G','Costa',41124234,'2001-01-01','Rua YGZ','M',1300.00,21312332,2)
INSERT INTO COMPANY.EMPLOYEE(Fname,Minit,Lname,Ssn,Bdate,e_Address,Sex,Salary,Super_ssn,Dno)VALUES('Ana','L','Silva',12652121,'1990-03-03','Rua ZIG ZAG','F',1400.00,21312332,2)
INSERT INTO COMPANY.DEPT_LOCATIONS(Dnumber, Dlocation)VALUES(2, 'Aveiro')
INSERT INTO COMPANY.DEPT_LOCATIONS(Dnumber, Dlocation)VALUES(3, 'Coimbra')
INSERT INTO COMPANY.[DEPENDENT](Essn,Dependent_name,Sex,Bdate,Relationship)VALUES(21312332,'Joana Costa','F','2008-04-01','Filho')
INSERT INTO COMPANY.[DEPENDENT](Essn,Dependent_name,Sex,Bdate,Relationship)VALUES(21312332,'Maria Costa','F','1990-10-05','Neto')
INSERT INTO COMPANY.[DEPENDENT](Essn,Dependent_name,Sex,Bdate,Relationship)VALUES(21312332,'Rui Costa','M','2000-08-04','Neto')
INSERT INTO COMPANY.[DEPENDENT](Essn,Dependent_name,Sex,Bdate,Relationship)VALUES(321233765,'Filho Lindo','M','2001-02-22','Filho')
INSERT INTO COMPANY.[DEPENDENT](Essn,Dependent_name,Sex,Bdate,Relationship)VALUES(342343434,'Rosa Lima','F','2006-03-11','Filho')
INSERT INTO COMPANY.[DEPENDENT](Essn,Dependent_name,Sex,Bdate,Relationship)VALUES(41124234,'Ana Sousa','F','2007-04-13','Neto')
INSERT INTO COMPANY.[DEPENDENT](Essn,Dependent_name,Sex,Bdate,Relationship)VALUES(41124234,'Gaspar Pinto','M','2006-02-08','Sobrinho')
INSERT INTO COMPANY.PROJECT(Pname,Pnumber,Plocation,Dnum)VALUES('Aveiro Digital',1,'Aveiro',3)
INSERT INTO COMPANY.PROJECT(Pname,Pnumber,Plocation,Dnum)VALUES('BD Open Day',2,'Espinho',2)
INSERT INTO COMPANY.PROJECT(Pname,Pnumber,Plocation,Dnum)VALUES('Dicoogle',3,'Aveiro',3)
INSERT INTO COMPANY.PROJECT(Pname,Pnumber,Plocation,Dnum)VALUES('GOPACS',4,'Aveiro',3)
INSERT INTO COMPANY.WORKS_ON(Essn,Pno,[Hours])VALUES(183623612,1,20.0)
INSERT INTO COMPANY.WORKS_ON(Essn,Pno,[Hours])VALUES(183623612,3,10.0)
INSERT INTO COMPANY.WORKS_ON(Essn,Pno,[Hours])VALUES(21312332 ,1,20.0)
INSERT INTO COMPANY.WORKS_ON(Essn,Pno,[Hours])VALUES(321233765,1,25.0)
INSERT INTO COMPANY.WORKS_ON(Essn,Pno,[Hours])VALUES(342343434,1,20.0)
INSERT INTO COMPANY.WORKS_ON(Essn,Pno,[Hours])VALUES(342343434,4,25.0)
INSERT INTO COMPANY.WORKS_ON(Essn,Pno,[Hours])VALUES(41124234,2,20.0)
INSERT INTO COMPANY.WORKS_ON(Essn,Pno,[Hours])VALUES(41124234,3,30.0)

--a)