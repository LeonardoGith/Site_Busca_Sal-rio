import sqlite3
import random
import hashlib

# Options for profession names and regions
professions = [
    "Analista de Sistemas", "Analista de Dados", "Programador VBA", "Programador Python",
    "Desenvolvedor Web", "Engenheiro de Software", "Administrador de Redes", "Arquiteto de Soluções",
    "Especialista em Segurança da Informação", "Analista de Suporte Técnico", "Cientista de Dados",
    "Especialista em DevOps", "Engenheiro de Machine Learning", "Especialista em Nuvem",
    "Engenheiro de Redes", "Administrador de Banco de Dados"
]

regions = [
    "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
    "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
    "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí",
    "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia",
    "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
]
# Function to hash passwords
def hash_password(password):
    # Use SHA-256 to hash the password
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a SQLite database and populate it
def create_and_populate_database(db_name="professions.db"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        useremail TEXT PRIMARY KEY,
                        username TEXT NOT NULL,
                        userpassword TEXT NOT NULL)''')

    # Create professions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS professions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        profession_name TEXT UNIQUE NOT NULL)''')

    # Create regions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS regions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        region_name TEXT UNIQUE NOT NULL)''')

    # Create profession_data table
    cursor.execute('''CREATE TABLE IF NOT EXISTS profession_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        profession_id INTEGER NOT NULL,
                        region_id INTEGER NOT NULL,
                        salary INTEGER NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        FOREIGN KEY (profession_id) REFERENCES professions(id),
                        FOREIGN KEY (region_id) REFERENCES regions(id))''')

    # Insert distinct professions
    for profession in professions:
        cursor.execute('''INSERT OR IGNORE INTO professions (profession_name) VALUES (?)''', (profession,))
    
    # Insert distinct regions
    for region in regions:
        cursor.execute('''INSERT OR IGNORE INTO regions (region_name) VALUES (?)''', (region,))
    
    # Insert random user data
    emails = []
    for _ in range(30):  # Adjust the range for how many users you want to create
        useremail = f"user{_}@example.com"
        username = f"User{_}"
        password = f"password{random.randint(1, 100)}"  # Generate a simple password
        hashed_password = hash_password(password)  # Hash the password
        cursor.execute('''INSERT INTO users (useremail, username, userpassword)
                          VALUES (?, ?, ?)''', (useremail, username, hashed_password))
        emails.append(useremail)  # Collect emails for later use
        print(f"Email: {useremail}, Username: {username}, Plaintext Password: {password}")  # Print the email, username, and plaintext password

    # Insert random profession data with unique emails
    for email in emails:
        # Select a random profession and region
        cursor.execute('''SELECT id FROM professions ORDER BY RANDOM() LIMIT 1''')
        profession_id = cursor.fetchone()[0]

        cursor.execute('''SELECT id FROM regions ORDER BY RANDOM() LIMIT 1''')
        region_id = cursor.fetchone()[0]

        salary = random.randint(1000, 10000)
        cursor.execute('''INSERT INTO profession_data (profession_id, region_id, salary, email)
                          VALUES (?, ?, ?, ?)''', (profession_id, region_id, salary, email))
    
    # Commit and close the connection
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created and populated with random data.")

create_and_populate_database()

