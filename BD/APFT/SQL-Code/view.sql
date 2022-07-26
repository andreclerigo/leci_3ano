-- melhores avaliacoes por modalidade
CREATE VIEW melhores_avaliacoes_por_modalidade AS
SELECT modalidade, Atleta.nome, MAX(avaliacao) AS melhor_avaliacao
    FROM Atleta 
    INNER JOIN Reserva ON Atleta.n_inscricao = Reserva.n_insc_atleta
    INNER JOIN Sessao_treino ON Reserva.num_reserva = Sessao_treino.num_reserva
    GROUP BY modalidade, nome;