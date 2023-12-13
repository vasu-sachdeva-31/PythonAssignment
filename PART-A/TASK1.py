import requests
import mysql.connector

app_id = '6579c6905510924627d5d757'

users_url = 'https://dummyapi.io/data/v1/user'
headers = {'app-id': app_id}
response = requests.get(users_url, headers=headers)
users_data = response.json()['data']

db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='db'
)

cursor = db_connection.cursor()
insert_users_query = "INSERT INTO users (id, firstName, lastName, email) VALUES (%s, %s, %s, %s)"

for user in users_data:
    cursor.execute(insert_users_query, (user.get('id'), user.get('firstName'), user.get('lastName'), user.get('email')))
    
db_connection.commit()
cursor.close()
db_connection.close()
