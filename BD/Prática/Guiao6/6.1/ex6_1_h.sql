SELECT pub_name, SUM(ytd_sales) AS total_sales 
FROM ((sales INNER JOIN titles ON sales.title_id=titles.title_id) INNER JOIN publishers ON publishers.pub_id=titles.pub_id)
GROUP BY pub_name;