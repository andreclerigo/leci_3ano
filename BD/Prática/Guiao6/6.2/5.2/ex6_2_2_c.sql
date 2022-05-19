-- Queries 

--a
SELECT nome FROM GESTSTOCK.encomenda
FULL OUTER JOIN GESTSTOCK.fornecedor ON fornecedor=nif
WHERE fornecedor IS NULL

--b
SELECT nome, AVG(I.unidades) AS media FROM GESTSTOCK.item AS I
INNER JOIN GESTSTOCK.produto ON codProd=codigo
GROUP BY codProd, nome

--c
SELECT AVG(num_prod) AS media FROM 
	(SELECT COUNT(codProd) AS num_prod FROM GESTSTOCK.item
	GROUP BY numEnc) AS P
	
--d
SELECT F.nome, P.nome, qnt_total FROM GESTSTOCK.fornecedor AS F
INNER JOIN (
			SELECT codProd, fornecedor, SUM(unidades) AS qnt_total FROM GESTSTOCK.item
			INNER JOIN GESTSTOCK.encomenda ON numEnc=numero
			GROUP BY codProd, fornecedor
			) AS AUX_TABLE
ON fornecedor=nif
INNER JOIN GESTSTOCK.produto AS P ON codProd=codigo