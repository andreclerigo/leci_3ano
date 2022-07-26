/* ======================== DEVIA FUNCIONAR ======================== */
/* Criar atleta */
INSERT INTO Atleta VALUES ('joao', '2001-06-14', 'ténis', 'apto')
INSERT INTO Atleta VALUES ('andre', '2001-06-14', 'Ténis', DEFAULT)
INSERT INTO Atleta VALUES ('pedro', '2001-01-05', 'basquetebol', DEFAULT)
INSERT INTO Atleta VALUES ('claudio', '2001-05-06', 'natacão', 'inapto')
SELECT * FROM Atleta;

/* Criar Estabelecimentos Piscina, Ginasio e Pista */
INSERT INTO Estabelecimento VALUES ('07:00', '18:00', '2022-08-20', 5);
INSERT INTO Estabelecimento VALUES ('08:00', '20:00', '2022-08-22', 15);
INSERT INTO Estabelecimento VALUES ('09:00', '21:00', '2022-08-24', 8);
INSERT INTO Estabelecimento VALUES ('07:00', '18:00', '2022-08-20', 5);
INSERT INTO Estabelecimento VALUES ('09:00', '22:00', '2022-08-22', 15);
INSERT INTO Estabelecimento VALUES ('10:00', '22:00', '2022-08-24', 10);

INSERT INTO Piscina VALUES (1, 22);
INSERT INTO Ginasio VALUES (2, 30);
INSERT INTO Pista VALUES (3, 'sintética');
INSERT INTO Piscina VALUES (4, 29);
INSERT INTO Ginasio VALUES (5, 22);
INSERT INTO Pista VALUES (6, 'esteira');

SELECT * FROM Estabelecimento;
SELECT * FROM Piscina;
SELECT * FROM Ginasio;
SELECT * FROM Pista;

/* Criar Empregado -> Treinador, Secretariado, Emp_Saude */
--Empregados Treinadores
INSERT INTO Empregado VALUES ('Pedro', 800, 237092891);
INSERT INTO Empregado VALUES ('André', 1600, 237092892);
INSERT INTO Empregado VALUES ('Cláudio', 705, 237092893);
INSERT INTO Empregado VALUES ('João', 1200, 237092894);
INSERT INTO Empregado VALUES ('Maria', 1350, 237092895);
INSERT INTO Empregado VALUES ('José', 1500, 237092896);
INSERT INTO Empregado VALUES ('José Carlos', 800, 237092897);
INSERT INTO Empregado VALUES ('José Maria', 870, 237092898);
INSERT INTO Empregado VALUES ('Joana', 900, 237092899);
INSERT INTO Empregado VALUES ('Hugo', 1000, 237092900);
INSERT INTO Empregado VALUES ('Cláudio', 1200, 237092901);
INSERT INTO Empregado VALUES ('José Manuel', 1300, 237092902);
INSERT INTO Empregado VALUES ('Manuel', 1200, 237092903);
INSERT INTO Empregado VALUES ('Carlos Manuel', 980, 237092904);
INSERT INTO Empregado VALUES ('João Pedro', 1300, 237092905);
INSERT INTO Empregado VALUES ('Pedro Manuel', 790, 237092906);
INSERT INTO Empregado VALUES ('Pedro António', 2000, 237092907);
INSERT INTO Empregado VALUES ('Rebeca', 1740, 237092908);
INSERT INTO Empregado VALUES ('Rui', 1800, 237092909);
INSERT INTO Empregado VALUES ('Sara', 800, 237092910);

--Empregados Secretariados
INSERT INTO Empregado VALUES ('Sara Sofia', 720, 237092911);
INSERT INTO Empregado VALUES ('Sofia', 740, 237092912);
INSERT INTO Empregado VALUES ('Ana', 790, 237092913);
INSERT INTO Empregado VALUES ('Inês', 800, 237092914);
INSERT INTO Empregado VALUES ('Rita', 810, 237092915);
INSERT INTO Empregado VALUES ('Carla', 730, 237092916);
INSERT INTO Empregado VALUES ('José', 860, 237092917);
INSERT INTO Empregado VALUES ('José Manuel', 870, 237092918);
INSERT INTO Empregado VALUES ('João António', 1080, 237092919);
INSERT INTO Empregado VALUES ('Bruno', 890, 237092920);

--Empregados Emp_Saude
INSERT INTO Empregado VALUES ('Olga', 1800, 237092921);
INSERT INTO Empregado VALUES ('Maria', 1200, 237092922);
INSERT INTO Empregado VALUES ('José', 1300, 237092923);
INSERT INTO Empregado VALUES ('Carlos Alberto', 1000, 237092924);
INSERT INTO Empregado VALUES ('Tiago', 2100, 237092925);

--Treinadores
INSERT INTO Treinador VALUES (1, 'natacão');
INSERT INTO Treinador VALUES (2, 'judo');
INSERT INTO Treinador VALUES (3, 'ténis');
INSERT INTO Treinador VALUES (4, 'rugby');
INSERT INTO Treinador VALUES (5, 'basquetebol');
INSERT INTO Treinador VALUES (6, 'voleibol');
INSERT INTO Treinador VALUES (7, 'atletismo');
INSERT INTO Treinador VALUES (8, 'natacão');
INSERT INTO Treinador VALUES (9, 'judo');
INSERT INTO Treinador VALUES (10, 'ténis');
INSERT INTO Treinador VALUES (11, 'judo');
INSERT INTO Treinador VALUES (12, 'basquetebol');
INSERT INTO Treinador VALUES (13, 'voleibol');
INSERT INTO Treinador VALUES (14, 'atletismo');
INSERT INTO Treinador VALUES (15, 'rugby');
INSERT INTO Treinador VALUES (16, 'badminton');
INSERT INTO Treinador VALUES (17, 'badminton');
INSERT INTO Treinador VALUES (18, 'atletismo');
INSERT INTO Treinador VALUES (19, 'basquetebol');
INSERT INTO Treinador VALUES (20, 'atletismo');

--Secretariados
INSERT INTO Secretariado VALUES (21, 1);
INSERT INTO Secretariado VALUES (22, 2);
INSERT INTO Secretariado VALUES (23, 3);
INSERT INTO Secretariado VALUES (24, 4);
INSERT INTO Secretariado VALUES (25, 5);
INSERT INTO Secretariado VALUES (26, 5);
INSERT INTO Secretariado VALUES (27, 6);
INSERT INTO Secretariado VALUES (28, 6);

--Emp_Saude
INSERT INTO Emp_Saude VALUES (29, 'oftalmologia');
INSERT INTO Emp_Saude VALUES (30, 'medicina geral');
INSERT INTO Emp_Saude VALUES (31, 'fisioterapia');
INSERT INTO Emp_Saude VALUES (32, 'nutricão');
INSERT INTO Emp_Saude VALUES (33, 'cardiologia');


SELECT * FROM Atleta;
SELECT * FROM Reserva
SELECT * FROM Consulta
SELECT * FROM Estabelecimento;
SELECT * FROM Piscina;
SELECT * FROM Ginasio;
SELECT * FROM Pista;
SELECT * FROM Empregado;
SELECT * FROM Treinador;
SELECT * FROM Secretariado;
SELECT * FROM Emp_Saude;

/* Registar Consulta */
SELECT * FROM Atleta;
INSERT INTO Consulta VALUES (31, 1, '2022-06-21', 'apto') 
INSERT INTO Consulta VALUES (29, 3, '2022-06-01', 'apto')
INSERT INTO Consulta VALUES (31, 2, '2022-05-02', 'apto')
INSERT INTO Consulta VALUES (31, 4, '2022-06-02', 'apto')
SELECT * FROM Consulta;
SELECT * FROM Atleta;


/* Reservar um estabelecimento */
INSERT INTO Reserva VALUES (1, 2, '2022-08-23', '8:30', '00:30', 1);
INSERT INTO Reserva VALUES (1, 2, '2022-07-12', '10:00', '00:30', 1);
INSERT INTO Reserva VALUES (2, 2, '2022-07-20', '12:00', '00:30', 1);
INSERT INTO Reserva VALUES (2, 2, '2022-07-02', '13:00', '00:30', 1);
INSERT INTO Reserva VALUES (1, 3, '2022-08-20', '14:00', '01:30', 2);
INSERT INTO Reserva VALUES (14, 4, '2022-08-01', '15:00', '01:00', 5);
INSERT INTO Reserva VALUES (10, 4, '2022-09-03', '14:00', '02:00', 2);
INSERT INTO Reserva VALUES (8, 3, '2022-10-29', '09:00', '01:00', 1);


/* Sessao_Treino */
INSERT INTO Sessao_Treino VALUES (2, 18)
INSERT INTO Sessao_Treino VALUES (3, 15)
INSERT INTO Sessao_Treino VALUES (4, 19)
INSERT INTO Sessao_Treino VALUES (5, 13)
INSERT INTO Sessao_Treino VALUES (6, 10)
INSERT INTO Sessao_Treino VALUES (7, 12)

SELECT * FROM Sessao_Treino;

/* Procedures */
SELECT * FROM Empregado;
SELECT * FROM Treinador;
EXECUTE sp_add_treinador @nome='andre', @salario=705, @nif=237792891, @modalidade='Ténis';
SELECT * FROM Empregado;
SELECT * FROM Treinador;

SELECT * FROM Estabelecimento;
SELECT * FROM Piscina;
EXECUTE sp_add_piscina @hora_aberto='09:00', @hora_fechado='20:00', @data_manutencao='2022-06-22', @lotacao=50, @temp_agua=27
SELECT * FROM Estabelecimento;
SELECT * FROM Piscina;
