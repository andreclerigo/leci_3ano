/* ===================== CRIACAO DE ENTIDADES IS-A ===================== */
-- Quando um treinador é adicionado, ele é adicionado à tabela de empregados
GO
CREATE PROC sp_add_treinador    @nome VARCHAR(50),
                                @salario FLOAT,
                                @nif INTEGER,
                                @modalidade VARCHAR(15)
AS
    BEGIN
        INSERT INTO Empregado(nome, salario, nif) VALUES (@nome, @salario, @nif);
        INSERT INTO Treinador(n_func, modalidade) VALUES (SCOPE_IDENTITY(), @modalidade);
    END

-- Quando um empregado de saúde é adicionado, ele é adicionado à tabela de empregados
GO
CREATE PROC sp_add_emp_saude    @nome VARCHAR(50),
                                @salario FLOAT,
                                @nif INTEGER,
                                @especialidade VARCHAR(15)
AS
    BEGIN
        INSERT INTO Empregado(nome, salario, nif) VALUES (@nome, @salario, @nif)
        INSERT INTO Emp_Saude(n_func, especialidade) VALUES (SCOPE_IDENTITY(), @especialidade)
    END

-- Quando um secretariado é adicionado, ele é adicionado à tabela de empregados
GO
CREATE PROC sp_add_secretariado @nome VARCHAR(50),
                                @salario FLOAT,
                                @nif INTEGER,
                                @id_estabelecimento INTEGER
AS
    BEGIN
        INSERT INTO Empregado(nome, salario, nif) VALUES (@nome, @salario, @nif)
        INSERT INTO Secretariado(n_func, id_estabelecimento) VALUES (SCOPE_IDENTITY(), @id_estabelecimento)
    END

-- Quando uma piscina é adicionada, ela é adicionada à tabela de estabelecimentos
GO
CREATE PROC sp_add_piscina      @hora_aberto TIME,
                                @hora_fechado TIME,
                                @data_manutencao DATE,
                                @lotacao INTEGER,
                                @temp_agua FLOAT
AS
    BEGIN
        INSERT INTO Estabelecimento(hora_aberto, hora_fechado, data_manutencao, lotacao) VALUES (@hora_aberto, @hora_fechado, @data_manutencao, @lotacao);
        INSERT INTO Piscina(id, temp_agua) VALUES (SCOPE_IDENTITY(), @temp_agua);
    END

-- Quando uma pista é adicionada, ela é adicionada à tabela de estabelecimentos
GO
CREATE PROC sp_add_pista        @hora_aberto TIME,
                                @hora_fechado TIME,
                                @data_manutencao DATE,
                                @lotacao INTEGER,
                                @tipo_solo VARCHAR(15)
AS
    BEGIN
        INSERT INTO Estabelecimento(hora_aberto, hora_fechado, data_manutencao, lotacao) VALUES (@hora_aberto, @hora_fechado, @data_manutencao, @lotacao);
        INSERT INTO Pista(id, tipo_solo) VALUES (SCOPE_IDENTITY(), @tipo_solo);
    END

-- Quando um ginásio é adicionado, ela é adicionado à tabela de estabelecimentos
GO
CREATE PROC sp_add_ginasio      @hora_aberto TIME,
                                @hora_fechado TIME,
                                @data_manutencao DATE,
                                @lotacao INTEGER,
                                @qtd_aparelhos INTEGER
AS
    BEGIN
        INSERT INTO Estabelecimento(hora_aberto, hora_fechado, data_manutencao, lotacao) VALUES (@hora_aberto, @hora_fechado, @data_manutencao, @lotacao);
        INSERT INTO Ginasio(id, qtd_aparelhos) VALUES (SCOPE_IDENTITY(), @qtd_aparelhos);
    END
