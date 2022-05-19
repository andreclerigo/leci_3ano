SELECT title FROM titles
EXCEPT
SELECT DISTINCT title FROM titlesINNER JOIN sales ON sales.title_id=titles.title_id
INNER JOIN stores ON stores.stor_id=sales.stor_id
WHERE stor_name='Bookbeat'