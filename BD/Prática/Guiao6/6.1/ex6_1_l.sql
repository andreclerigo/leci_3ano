SELECT titles.pub_id, type, COUNT(ytd_sales) AS sales_amount, AVG(price) AS average_price
FROM publishers JOIN titles ON titles.pub_id=publishers.pub_id
GROUP BY titles.pub_id, type