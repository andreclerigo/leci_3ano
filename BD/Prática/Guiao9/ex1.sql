-- a)
GO
CREATE PROC sp_remove_employee @ssn INT 
AS
	BEGIN
		DELETE FROM Company.[Dependent] WHERE Essn=@ssn;
		DELETE FROM Company.Works_on WHERE Essn=@ssn;
		UPDATE Company.Department SET Mgr_ssn=NULL WHERE Mgr_ssn=@ssn;
		UPDATE Company.Employee set Super_ssn=NULL WHERE Super_ssn=@ssn;
		DELETE FROM Company.Employee WHERE Ssn=@ssn;
	END;
-- Preocupações adicionais: Update do Mgr_ssn no Department e na tabela Employee
EXEC sp_remove_employee 21312332;

-- b)
GO
CREATE PROC sp_dept_managers (@mgr_ssn INT OUTPUT, @worked_yrs INT OUTPUT)
AS
	BEGIN
		SELECT Employee.* FROM Company.Employee INNER JOIN Company.Department ON Company.Employee.Ssn=Company.Department.Mgr_ssn;
		SELECT @mgr_ssn = Department.Mgr_ssn, @worked_yrs = DATEDIFF(year, Mgr_start_date, GETDATE()) FROM Company.Department 
			WHERE Mgr_start_date = (SELECT MIN(Mgr_start_date) from Company.Department);
	END

DECLARE @ssn INT;
DECLARE @yrs INT;
EXEC sp_dept_managers @ssn OUTPUT, @yrs OUTPUT;
PRINT @ssn;
PRINT @yrs;

-- c)
GO
CREATE TRIGGER one_dept ON Company.Department INSTEAD OF INSERT, UPDATE
AS
	BEGIN
		IF (SELECT count(*) FROM inserted) > 0
			BEGIN
				DECLARE @employee_ssn AS INT;
				SELECT @employee_ssn = Mgr_ssn FROM inserted;

				IF (@employee_ssn) IS NULL OR ((SELECT count(*) FROM Employee WHERE Ssn=@employee_ssn) = 0)
					RAISERROR('Employee doesnt existing', 16, 1);
				ELSE
					BEGIN
						IF (SELECT COUNT(Dnumber) FROM Company.Department WHERE Mgr_ssn=@employee_ssn) >=1
							RAISERROR('Employee cant manage more than one department', 16, 1);	
						ELSE
							INSERT INTO Company.Department SELECT * FROM inserted;
					END
			END
	END

SELECT * FROM Company.Department;
SELECT * FROM Company.Employee;
INSERT INTO Company.Department VALUES ('Teste', 5, 21312332, '2013-05-16');
INSERT INTO Company.Department VALUES ('Teste', 5, NULL, '2013-05-16');
INSERT INTO Company.Department VALUES ('Teste', 5, 123456789, '2013-05-16');

-- d)
GO
CREATE TRIGGER salary_get_low ON Company.Employee AFTER INSERT, UPDATE
AS
	BEGIN
		DECLARE @ssn_emp AS INT;
		DECLARE @sal_emp AS INT;
		DECLARE @dno AS INT;
		DECLARE @mgr_sal AS INT;

		SELECT @ssn_emp=inserted.Ssn, @sal_emp=inserted.Salary, @dno=inserted.Dno FROM inserted;
		SELECT @mgr_sal=Company.Employee.Salary FROM Company.Department
			INNER JOIN Company.Employee ON Company.Department.Mgr_Ssn=Company.Employee.Ssn
			WHERE @dno=Company.Department.Dnumber;

		IF @sal_emp > @mgr_sal
		BEGIN
			UPDATE Company.Employee SET Company.Employee.Salary=@mgr_sal-1
			WHERE Company.Employee.Ssn=@ssn_emp
		END
	END

INSERT INTO Company.Employee VALUES ('Ze', 'T', 'Afonsado', 999888777, '2001-03-10', 'Rua Principal 8', 'M', 1500, 21312332, 1);
INSERT INTO Company.Employee VALUES ('Andre', 'M', 'Zuquete', 123456789, '2001-06-17', 'Estrada da Cela 8', 'M', 1200, 21312332, 1);
-- Se o salário for igual ao do manager já não há alteração ¯\_(ツ)_/¯ 
SELECT * FROM Company.Employee;

-- e)
GO
CREATE FUNCTION Company.ft_proj_info (@emp_ssn INT) RETURNS @table
TABLE([name] VARCHAR(45), [location] VARCHAR(15))
AS
	BEGIN
		INSERT @table
			SELECT Company.Project.Pname, Company.Project.Plocation FROM Company.Project
				INNER JOIN Company.Works_on ON Company.Works_on.Pno=Company.Project.Pnumber
				WHERE Works_on.Essn=@emp_ssn
		RETURN;
	END

SELECT * FROM Company.Works_on;
SELECT * FROM Company.Project;
SELECT * FROM Company.ft_proj_info(21312332);
SELECT * FROM Company.ft_proj_info(183623612);
SELECT * FROM Company.ft_proj_info(342343434);

-- f)
GO
CREATE FUNCTION Company.ft_dept_better_paid_emp (@dno INT) RETURNS @table
TABLE ([ssn] INT, [fname] VARCHAR(15), [lname] VARCHAR(15))
AS
    BEGIN 
        INSERT @table
            SELECT Company.Employee.Ssn, Company.Employee.Fname, Company.Employee.Lname
            FROM Company.Employee JOIN (SELECT Dno, AVG(Salary) as avg_sal 
                                        FROM Company.Department, Company.Employee
                                        WHERE Dno=Dnumber
                                        GROUP BY Dno) AS dep_avg_sal
            ON dep_avg_sal.Dno=Company.Employee.Dno AND Salary > avg_sal AND Company.Employee.Dno = @dno;
        RETURN;
    END

-- avg salary by department
SELECT Dno, AVG(Salary) as avg_sal 
	FROM Company.Department, Company.Employee
	WHERE Dno=Dnumber
	GROUP BY Dno;
SELECT * FROM Company.Employee;
SELECT * FROM Company.ft_dept_better_paid_emp(1);
SELECT * FROM Company.ft_dept_better_paid_emp(2);
SELECT * FROM Company.ft_dept_better_paid_emp(3);









