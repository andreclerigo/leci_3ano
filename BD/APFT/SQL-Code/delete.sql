DROP SCHEMA AltoRendimento;

DROP TABLE Consulta;
DROP TABLE Sessao_Treino;
DROP TABLE Reserva;
DROP TABLE Secretariado;
DROP TABLE Treinador;
DROP TABLE Emp_Saude;
DROP TABLE Empregado;
DROP TABLE Pista;
DROP TABLE Ginasio; 
DROP TABLE Piscina;
DROP TABLE Estabelecimento;
DROP TABLE Atleta;

DROP PROCEDURE sp_add_treinador;
DROP PROCEDURE sp_add_emp_saude;
DROP PROCEDURE sp_add_secretariado;
DROP PROCEDURE sp_add_piscina;
DROP PROCEDURE sp_add_pista;
DROP PROCEDURE sp_add_ginasio;

DROP TRIGGER del_treinador;
DROP TRIGGER del_secretariado;
DROP TRIGGER del_emp_saude;
DROP TRIGGER del_piscina;
DROP TRIGGER del_pista;
DROP TRIGGER del_ginasio;
DROP TRIGGER atualiza_saude;
DROP TRIGGER check_reserva;

DROP FUNCTION Reserva_disponivel;

DROP VIEW melhores_avaliacoes_por_modalidade;

DROP INDEX index_data_reserva ON Reserva;