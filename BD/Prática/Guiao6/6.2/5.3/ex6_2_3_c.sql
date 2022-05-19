-- Queries

--a
SELECT nome, paciente.numUtente FROM Prescricao.prescricao 
FULL OUTER JOIN Prescricao.paciente ON prescricao.numUtente=paciente.numUtente
WHERE numPresc IS NULL

--b
SELECT especialidade, COUNT(numPresc) AS total_presc FROM Prescricao.prescricao
INNER JOIN Prescricao.medico ON numMedico=numSNS
GROUP BY especialidade

--c
SELECT nome, COUNT(numPresc) AS total_presc FROM Prescricao.prescricao
INNER JOIN Prescricao.farmacia ON farmacia=nome
GROUP BY nome

--d
SELECT farmaco.nome  FROM Prescricao.farmaco
INNER JOIN Prescricao.farmaceutica ON numRegFarm=numReg
WHERE numRegFarm=906
EXCEPT
(SELECT nomeFarmaco FROM Prescricao.presc_farmaco
WHERE numRegFarm=906)

--e
SELECT farmacia, nome, qtd_farmacos FROM Prescricao.farmaceutica
INNER JOIN (
			SELECT farmacia, numRegFarm, COUNT(numRegFarm) AS qtd_farmacos FROM
				(SELECT farmacia, numRegFarm FROM Prescricao.presc_farmaco
				INNER JOIN Prescricao.prescricao ON presc_farmaco.numPresc=prescricao.numPresc
				WHERE farmacia IS NOT NULL) AS FARM_SELLED
			GROUP BY farmacia, numRegFarm
			) AS AUX_TABLE
ON numRegFarm=numReg

--f
SELECT nome FROM Prescricao.paciente
INNER JOIN (
			SELECT numUtente, COUNT(numMedico) AS medicos_dif FROM 
				( SELECT numUtente, numMedico FROM Prescricao.prescricao ) AS AUX
			GROUP BY numUtente
			HAVING COUNT(numMedico)>1
			) AS UTENTE_2MED
ON paciente.numUtente=UTENTE_2MED.numUtente