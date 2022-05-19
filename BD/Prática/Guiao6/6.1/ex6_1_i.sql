SELECT pub_name, title, ytd_sales
FROM (publishers JOIN titles ON publishers.pub_id=titles.pub_id);