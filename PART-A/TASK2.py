import requests
import mysql.connector

# Replace YOUR_APP_ID with the actual app_id you obtained
app_id = '6579c6905510924627d5d757'

# Connect to MySQL (replace 'localhost', 'root', 'root' with your actual MySQL connection details)
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='db'
)

cursor = db_connection.cursor(dictionary=True)
select_users_query = "SELECT id FROM users"
cursor.execute(select_users_query)
users_list = cursor.fetchall()

# API endpoint for fetching posts
posts_url = 'https://dummyapi.io/data/v1/user/{}/post'

# Store posts data in the MySQL database
cursor = db_connection.cursor()
insert_posts_query = "INSERT INTO posts (id, userId, text) VALUES (%s, %s, %s)"

for user in users_list:
    user_id = user['id']
    user_posts_url = posts_url.format(user_id)

    # Fetch posts data for the user
    response = requests.get(user_posts_url, headers={'app-id': app_id})
    posts_data = response.json()['data']

    # Store posts data in the MySQL database
    for post in posts_data:
        cursor.execute(insert_posts_query, (post.get('id'), post.get('userId'), post.get('text')))

# Commit changes and close the cursor and connection
db_connection.commit()
cursor.close()
db_connection.close()
