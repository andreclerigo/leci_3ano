(SELECT pub_name, stor_name
FROM publishers, stores
GROUP BY pub_name, stor_name)
EXCEPT
(SELECT pub_name, stor_name
FROM (((publishers	JOIN titles ON publishers.pub_id=titles.pub_id)
					JOIN sales  ON titles.title_id=sales.title_id)
					JOIN stores ON sales.stor_id=stores.stor_id)
GROUP BY pub_name, stor_name)