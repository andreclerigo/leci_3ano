/* ======================= NAO DEVIA FUNCIONAR ======================= */
/* Criar atleta com modalidade inv�lida */
INSERT INTO Atleta VALUES ('andre', '2001-06-14', 'tenis')


/* Criar Estabelecimentos com lota��o inv�lida */
INSERT INTO Estabelecimento VALUES ('07:00', '18:00', '2022-08-20', 0);
/* Criar Estabelecimentos com abertura depois do fecho */
INSERT INTO Estabelecimento VALUES ('08:00', '07:00', '2022-08-22', 50);
/* Criar Estabelecimentos com abertura inv�lida */
INSERT INTO Estabelecimento VALUES ('06:00', '21:00', '2022-08-24', 100);

INSERT INTO Estabelecimento VALUES ('07:00', '18:00', '2022-08-20', 10);
INSERT INTO Estabelecimento VALUES ('09:00', '19:00', '2022-08-22', 100);
/* Criar Piscina com temperatura inv�lida */
INSERT INTO Piscina VALUES (4, 19);
/* Criar Pista com modalidade inv�lida */
INSERT INTO Pista VALUES (5, 1, 'cimento');


/* Criar Empregado com NIF inv�lido */
INSERT INTO Empregado VALUES ('Pedro', 800, 501618970);
/* Criar Empregado com Salario inv�lido */
INSERT INTO Empregado VALUES ('Andre', 700, 237092892);
/* Criar Secretariado com id de estabelecimento inv�lido */
INSERT INTO Secretariado VALUES (2, 1);
/* Criar Emp_Saude com fisioterapia inv�lida */
INSERT INTO Empregado VALUES ('Claudio', 705, 237092893);
INSERT INTO Emp_Saude VALUES (1, 'medico');