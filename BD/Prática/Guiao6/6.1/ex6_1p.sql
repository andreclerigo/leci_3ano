SELECT title, au_fname, au_lname, 
	ytd_sales*price*royalty/100 as auths_revenue,
	price*ytd_sales-price*ytd_sales*royalty/100 AS publisher_revenue
FROM titles
INNER JOIN titleauthor ON titleauthor.title_id=titles.title_id
INNER JOIN authors ON authors.au_id=titleauthor.au_id
GROUP BY title, price, au_fname, au_lname, ytd_sales, royalty
