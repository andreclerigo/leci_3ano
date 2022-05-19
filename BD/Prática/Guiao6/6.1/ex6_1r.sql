SELECT stor_name FROM storesINNER JOIN sales ON stores.stor_id=sales.stor_idINNER JOIN titles ON sales.title_id=titles.title_id
GROUP BY stores.stor_name
HAVING SUM(sales.qty)>(SELECT SUM(sales.qty)/COUNT(stor_id) FROM sales);