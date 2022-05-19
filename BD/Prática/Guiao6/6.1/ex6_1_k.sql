SELECT au_fname, au_lname
FROM ((authors JOIN titleauthor ON authors.au_id=titleauthor.au_id) 
JOIN titles ON titles.title_id=titleauthor.title_id)
GROUP BY au_fname, au_lname
HAVING COUNT(DISTINCT type) > 1;