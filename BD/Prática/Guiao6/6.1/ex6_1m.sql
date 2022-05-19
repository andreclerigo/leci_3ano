SELECT type FROM titles
GROUP BY type
HAVING MAX(advance) > 1.5*AVG(advance);
