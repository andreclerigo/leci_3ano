-- udf return table (record set) com estabelecimentos e treinadores nao reservados  com os parametros de entrada data_reserva, hora_inicio, duracao
CREATE FUNCTION Reserva_disponivel(@data_reserva DATE, @hora_inicio TIME, @hora_fim TIME, @n_insc_atleta INT)
RETURNS @disponivel TABLE (estabelecimento INT, n_func_treinador INT, nome_treinador NVARCHAR(50))
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM Reserva r WHERE r.n_insc_atleta = @n_insc_atleta 
		AND r.data_reserva = @data_reserva
        AND (@hora_inicio = r.hora_inicio OR @hora_fim = r.hora_fim
            OR @hora_inicio < r.hora_inicio AND @hora_fim > r.hora_fim 
            OR @hora_inicio BETWEEN r.hora_inicio AND r.hora_fim AND @hora_inicio NOT IN (r.hora_inicio, r.hora_fim)
            OR @hora_fim BETWEEN r.hora_inicio AND r.hora_fim AND @hora_fim NOT IN (r.hora_inicio, r.hora_fim)))
    BEGIN
        INSERT @disponivel
        SELECT e.id, t.n_func, (SELECT nome FROM Empregado WHERE n_func = t.n_func)
        FROM Estabelecimento e
        CROSS JOIN Treinador t
        --estabelecimento nao esta reservado
        WHERE e.id NOT IN (SELECT e.id FROM Estabelecimento e 
                            INNER JOIN Reserva r ON r.id_estabelecimento = e.id
                            WHERE r.data_reserva = @data_reserva AND r.id_estabelecimento = e.id
                                                                AND (@hora_inicio = r.hora_inicio OR @hora_fim = r.hora_fim
                                                                    OR @hora_inicio < r.hora_inicio AND @hora_fim > r.hora_fim 
                                                                    OR @hora_inicio BETWEEN r.hora_inicio AND r.hora_fim AND @hora_inicio NOT IN (r.hora_inicio, r.hora_fim)
                                                                    OR @hora_fim BETWEEN r.hora_inicio AND r.hora_fim AND @hora_fim NOT IN (r.hora_inicio, r.hora_fim)))

        --treinador nao esta reservado
        AND t.n_func NOT IN (SELECT t.n_func FROM Treinador t 
                                INNER JOIN Reserva r ON r.n_func_treinador = t.n_func
                                WHERE r.data_reserva = @data_reserva AND r.hora_inicio = @hora_inicio 
                                                                    AND (@hora_inicio = r.hora_inicio 
                                                                        OR @hora_fim = r.hora_fim
                                                                        OR @hora_inicio < r.hora_inicio AND @hora_fim > r.hora_fim 
                                                                        OR @hora_inicio BETWEEN r.hora_inicio AND r.hora_fim 
                                                                            AND @hora_inicio NOT IN (r.hora_inicio, r.hora_fim)
                                                                        OR @hora_fim BETWEEN r.hora_inicio AND r.hora_fim 
                                                                            AND @hora_fim NOT IN (r.hora_inicio, r.hora_fim)))
                                                                        
        --estabelecimento nao esta em manutencao
        AND e.id NOT IN (SELECT e.id FROM Estabelecimento e 
                            WHERE @data_reserva = e.data_manutencao)
        --hora_inicio nao pode ser antes da abertura do estabelecimento e nao pode ser depois da fechamento do estabelecimento
        AND e.id IN (SELECT e.id FROM Estabelecimento e WHERE @hora_inicio >= e.hora_aberto AND @hora_fim <= e.hora_fechado)
        
    END
    RETURN
END;
GO

DROP FUNCTION Reserva_disponivel
--verificar que o atleta nao tem reserva à mesma hora

