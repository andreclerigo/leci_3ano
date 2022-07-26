-- Quando um treinador é apagado, eliminar da tabela Empregado o respetivo
GO
CREATE TRIGGER del_treinador ON Treinador
AFTER DELETE
AS
	DELETE Empregado WHERE Empregado.n_func = (SELECT n_func FROM deleted)

-- Quando um secretariado é apagado, eliminar da tabela Empregado o respetivo
GO
CREATE TRIGGER del_secretariado ON Secretariado
AFTER DELETE
AS
    DELETE Empregado WHERE Empregado.n_func = (SELECT n_func FROM deleted)

-- Quando um empregado de saúde é apagado, eliminar da tabela Empregado o respetivo
GO
CREATE TRIGGER del_emp_saude ON Emp_Saude
AFTER DELETE
AS
    DELETE Empregado WHERE Empregado.n_func = (SELECT n_func FROM deleted)


-- Quando uma piscina é apagado, eliminar da tabela Estabelecimento o respetivo
GO
CREATE TRIGGER del_piscina ON Piscina
AFTER DELETE
AS
	DELETE Estabelecimento WHERE Estabelecimento.id = (SELECT id FROM deleted)


-- Quando uma pista é apagado, eliminar da tabela Estabelecimento o respetivo
GO
CREATE TRIGGER del_pista ON Pista
AFTER DELETE
AS
    DELETE Estabelecimento WHERE Estabelecimento.id = (SELECT id FROM deleted)

-- Quando uma ginásio é apagado, eliminar da tabela Estabelecimento o respetivo
GO
CREATE TRIGGER del_ginasio ON Ginasio
AFTER DELETE
AS
    DELETE Estabelecimento WHERE Estabelecimento.id = (SELECT id FROM deleted)

-- atualizar estado_saude do atleta
GO 
CREATE TRIGGER atualiza_saude ON Consulta
AFTER INSERT
AS
BEGIN
    UPDATE Atleta 
    SET Atleta.estado_saude = (SELECT Consulta.estado_saude  FROM Consulta 
									WHERE id_consulta = (SELECT id_consulta FROM inserted)) 
		WHERE n_inscricao = (SELECT n_insc_atleta FROM inserted);
END

-- Verificar se a reserva é válida
/*
On Update, Insert Reserva

Verificar o estado_saude para ver se é apto
    Verificar consultas com id do atleta, ordenar por data e ver se a ultima nao foi há mais de 6 meses
*/
GO
CREATE TRIGGER check_reserva ON Reserva
INSTEAD OF INSERT, UPDATE
AS
	SET NOCOUNT ON;
    DECLARE @hora_inicio TIME = (SELECT hora_inicio FROM inserted);
    DECLARE @hora_fim TIME = (SELECT hora_fim FROM inserted);
    DECLARE @duracao TIME = (SELECT duracao FROM inserted);
    DECLARE @id_estabelecimento INT = (SELECT id_estabelecimento FROM inserted);
    DECLARE @data_reserva DATE = (SELECT data_reserva FROM inserted);
    DECLARE @hora_fechado TIME = (SELECT CAST(hora_fechado AS TIME) FROM Estabelecimento WHERE id=@id_estabelecimento);
    DECLARE @hora_aberto TIME = (SELECT CAST(hora_aberto AS TIME) FROM Estabelecimento WHERE id=@id_estabelecimento);
    DECLARE @data_ult_consulta DATE = (SELECT TOP 1 CAST(data_consulta AS DATE) FROM Consulta 
			WHERE n_insc_atleta = (SELECT n_insc_atleta FROM inserted) ORDER BY data_consulta DESC);
    DECLARE @lotacao INT = (SELECT lotacao FROM Estabelecimento WHERE id=@id_estabelecimento);
    DECLARE @num_reserva INT = (SELECT num_reserva FROM inserted);
    DECLARE @n_insc_atleta INT = (SELECT n_insc_atleta FROM inserted);
    DECLARE @n_func_treinador INT = (SELECT n_func_treinador FROM inserted);
    BEGIN TRY
			IF (@hora_inicio < @hora_aberto)
			BEGIN
				RAISERROR ('A hora de inicio não pode ser antes da hora de abertura do estabelecimento', 1 , 1);
				ROLLBACK TRAN;
			END
			IF (DATEADD(SECOND, DATEDIFF(SECOND, 0, @hora_inicio), @duracao) > @hora_fechado)
			BEGIN
				RAISERROR ('A hora de fim do treino não pode ser antes da hora de fecho do estabelecimento!', 1 , 1);
				ROLLBACK TRAN;
			END
			IF @data_reserva = (SELECT CAST(data_manutencao AS DATE) FROM Estabelecimento WHERE id=@id_estabelecimento)
			BEGIN
				RAISERROR ('A data da reserva nao pode ser a mesma que a data de manutenção do estabelecimento!', 1 , 1);
				ROLLBACK TRAN;
			END
			-- Verificar se a data da ultima consulta foi há mais de 6 meses
			IF (@data_ult_consulta IS NULL)
			BEGIN
				RAISERROR ('Não existem consultas anteriores a essa!', 1 , 1);
				ROLLBACK TRAN;
			END
			IF (DATEDIFF(MONTH, @data_ult_consulta, @data_reserva) > 5)
			BEGIN
				RAISERROR ('A data da última consulta foi há mais de 6 meses, por favor, marque uma consulta!', 1 , 1);
				ROLLBACK TRAN;
			END 
			--verifica se o atleta está apto
			IF (SELECT estado_saude FROM Atleta WHERE n_inscricao = @n_insc_atleta) != 'apto'
			BEGIN
				RAISERROR ('O atleta não está apto para treinar!', 1 , 1);
				ROLLBACK TRAN;
			END

			-- verifica que o atleta nao tem já uma reserva à mesma hora
			IF EXISTS (SELECT * FROM Reserva r WHERE n_insc_atleta = @n_insc_atleta AND data_reserva = @data_reserva
																				AND (@hora_inicio = r.hora_inicio OR @hora_fim = r.hora_fim
																				OR @hora_inicio < r.hora_inicio AND @hora_fim > r.hora_fim 
																				OR @hora_inicio BETWEEN r.hora_inicio AND r.hora_fim 
																					AND @hora_inicio NOT IN (r.hora_inicio, r.hora_fim)
																				OR @hora_fim BETWEEN r.hora_inicio AND r.hora_fim 
																					AND @hora_fim NOT IN (r.hora_inicio, r.hora_fim)))
			BEGIN
                RAISERROR ('O atleta já tem uma reserva à mesma hora!', 1 , 1);
                THROW 1, 'O atleta tem uma reserva à mesma hora!', 1;
			END
			-- inserir a reserva
			INSERT INTO Reserva(n_func_treinador, n_insc_atleta, data_reserva, hora_inicio, duracao, id_estabelecimento) 
						VALUES (@n_func_treinador, @n_insc_atleta, @data_reserva, @hora_inicio, @duracao, @id_estabelecimento);
		END TRY

		BEGIN CATCH
			PRINT ('');
		END CATCH
 