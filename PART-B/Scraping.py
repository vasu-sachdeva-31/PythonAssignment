from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "db2"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

create_db_query = "CREATE DATABASE IF NOT EXISTS db2"
cursor.execute(create_db_query)

conn.database = "db2"

create_table_query = """
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price VARCHAR(10) NOT NULL
)
"""
cursor.execute(create_table_query)

base_url = 'http://books.toscrape.com/catalogue/page-{}.html'

for page_number in range(1, 51):
    myurl = base_url.format(page_number)

    uClient = uReq(myurl)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    bookshelf = page_soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

    insert_query = "INSERT INTO books (title, price) VALUES (%s, %s)"

    for books in bookshelf:
        book_title = books.h3.a["title"]
        book_price = books.findAll("p", {"class": "price_color"})[0].text.strip()

        cursor.execute(insert_query, (book_title, book_price))
        conn.commit()

cursor.close()
conn.close()
