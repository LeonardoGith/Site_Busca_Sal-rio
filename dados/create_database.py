import sqlite3
import random
import hashlib

from dados import databasehelper

# Options for profession names and regions
professions = ["Analista de Sistemas", "Analista de Dados", "Programador VBA", "Programador Python"]
regions = ["São Paulo", "Rio de Janeiro", "Minas Gerais"]

# Function to hash passwords
def hash_password(password):
    # Use SHA-256 to hash the password
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a SQLite database and populate it
def create_and_populate_database(db_name=databasehelper.database_name()):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create profession_data table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS profession_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        profession_name TEXT NOT NULL,
                        profession_region TEXT NOT NULL,
                        salary INTEGER NOT NULL)''')
    
    # Create users table without plaintext_password
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        useremail TEXT PRIMARY KEY,
                        username TEXT NOT NULL,
                        userpassword TEXT NOT NULL)''')

    # Insert random profession data
    for _ in range(100):
        profession = random.choice(professions)
        region = random.choice(regions)
        salary = random.randint(1000, 10000)
        cursor.execute('''INSERT INTO profession_data (profession_name, profession_region, salary)
                          VALUES (?, ?, ?)''', (profession, region, salary))
    
    # Insert random user data
    for i in range(1, 101):  # Generate users user1 to user100
        username = f"user{i}"
        password = f"password{random.randint(1, 100)}"  # Generate a simple password
        hashed_password = hash_password(password)  # Hash the password
        useremail = f"user{i}@example.com"  # Generate email
        cursor.execute('''INSERT INTO users (useremail, username, userpassword)
                          VALUES (?, ?, ?)''', (useremail, username, hashed_password))
        print(f"Email: {useremail}, Username: {username}, Plaintext Password: {password}")  # Print the email, username, and plaintext password
    
    # Commit and close the connection
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created and populated with random profession and user data.")

# Function to verify login
def verify_login(useremail, password, db_name=databasehelper.database_name()):
    # Hash the provided password
    hashed_password = hash_password(password)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Fetch user record based on useremail
    cursor.execute('SELECT userpassword FROM users WHERE useremail = ?', (useremail,))
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # Check if user exists and verify password
    if result is None:
        print("Email not found.")
        return False
    elif result[0] == hashed_password:
        print("Login successful!")
        return True
    else:
        print("Incorrect password.")
        return False

create_and_populate_database()
