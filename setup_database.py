import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",  # or your MySQL username
    password=""   # your MySQL password (leave empty if none)
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS secure_app")
cursor.execute("USE secure_app")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password TEXT NOT NULL
    )
""")
cursor.execute("CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'SimplePass123'")
cursor.execute("GRANT ALL PRIVILEGES ON secure_app.* TO 'app_user'@'localhost'")
cursor.execute("FLUSH PRIVILEGES")
db.commit()
print("Database setup complete!")