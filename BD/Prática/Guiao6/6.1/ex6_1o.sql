SELECT title, ytd_sales, ytd_sales*price AS facturacao, 
	ytd_sales*price*royalty/100 AS auths_revenue, 
	price*ytd_sales-price*ytd_sales*royalty/100 AS publisher_revenue
FROM titles