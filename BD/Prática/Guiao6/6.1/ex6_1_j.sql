SELECT title
FROM ((titles JOIN sales ON titles.title_id=sales.title_id) JOIN stores ON sales.stor_id=stores.stor_id)
WHERE stor_name LIKE 'Bookbeat';