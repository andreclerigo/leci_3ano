SELECT au_fname AS first_name, au_lname AS last_name, phone AS telephone FROM authors
WHERE au_lname!='Ringer' AND state='CA'
ORDER BY first_name, last_name;