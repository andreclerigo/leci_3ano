-- Queries

--a
SELECT Pname, Ssn, Fname, Lname FROM Company.Project
INNER JOIN Company.Works_on ON Pno=Pnumber
INNER JOIN Company.Employee ON Essn=Ssn;

--b
SELECT Fname, Lname FROM Company.Employee
WHERE Super_ssn=(SELECT Ssn FROM Company.Employee WHERE Fname='Carlos' AND Minit='D' AND Lname='Gomes')

--c
SELECT Pname, total_worked FROM Company.Project
INNER JOIN (
			SELECT Pno, SUM(Hours) AS total_worked FROM Company.Works_on
			GROUP BY Pno
			) AS Worked_Table
ON Pnumber=Pno

--d
SELECT Fname, Lname FROM Company.Project
INNER JOIN Company.Works_on ON Pnumber=Pno
INNER JOIN (
			SELECT Fname, Lname, Ssn FROM Company.Employee
			WHERE Dno=3
			) AS dep3_empls
ON Essn=Ssn
WHERE Hours>20

--e
SELECT Fname, Minit, Lname FROM Company.Employee
LEFT JOIN Company.Works_on ON Essn=Ssn
WHERE Pno IS NULL

--f
SELECT Dname, AVG(Salary) AS Avg_Salary FROM Company.Department
INNER JOIN (SELECT * FROM Company.Employee WHERE Sex='F') AS F_DEP ON Dnumber=Dno
GROUP BY Dname

--g
SELECT Fname, Minit, Lname FROM Company.Employee
INNER JOIN (
			SELECT Essn, COUNT(Essn) AS count_dep FROM Company.Dependent
			GROUP BY Essn
			HAVING COUNT(Essn)>1
			) AS TWOORMORE
ON Ssn=Essn

--h
SELECT Fname, Minit, Lname FROM Company.Department
INNER JOIN (
			SELECT E.Fname, E.Minit, E.Lname, E.Ssn FROM Company.Employee AS E
			LEFT JOIN Company.Dependent ON Ssn=Essn
			WHERE Essn IS NULL
			) AS NODEP_EMP
ON Mgr_ssn=Ssn

--i
SELECT Fname, Minit, Lname, e_Address FROM Company.Employee
INNER JOIN (
			SELECT * FROM Company.Project
			INNER JOIN Company.Dept_locations ON Dnum=Dnumber
			WHERE Dlocation!='Aveiro' AND Plocation='Aveiro'
			) AS PROJECT_LST
ON Dno=Dnum