import sqlite3
import random
import hashlib
import databasehelper

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

# Listas de cursos, vídeos, livros, canais, e mensagens motivacionais
cursos_sugestoes = [
    "Python para Iniciantes", "Data Science com Python", "Desenvolvimento Web Full Stack",
    "Curso Completo de Machine Learning", "DevOps na Prática"
]

videos_sugestoes = [
    "Introdução ao Flask", "Construindo APIs REST com Python", "Como criar projetos em Django",
    "Python para análise de dados", "Testes automatizados com PyTest"
]

livros_sugestoes = [
    "Aprendendo Python com Cherles Barbosa", "Desenvolvimento Web com Python", 
    "Data Science na Prática com Fábio Santos", "Arquitetura de Sistemas com Pedro Silva"
]

canais_sugestoes = [
    "Código Fácil", "Tech Simplificada", "Programação com João", "Academia de Dados", "Aprendendo na Prática"
]

mensagens_motivacionais = [
    "A chave do sucesso na minha carreira foi nunca parar de aprender e buscar novas soluções. Não importa o quão avançado eu estivesse, sempre havia algo novo para aprender. Busque entender o que você faz e nunca pare de questionar e explorar.",
    "Ao longo da minha carreira, percebi que o diferencial não estava nas ferramentas, mas em como eu aplicava o meu conhecimento e otimizava processos. Continue se desafiando e explore novas formas de resolver problemas, isso fará você crescer na profissão."
]





# Function to hash passwords
def hash_password(password):
    # Use SHA-256 to hash the password
    return hashlib.sha256(password.encode()).hexdigest()





# Function to create a SQLite database and populate it
def create_and_populate_database(db_name=databasehelper.database_name()):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Criando tabela de indicações
    cursor.execute('''CREATE TABLE IF NOT EXISTS indications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        courses TEXT,
                        videos TEXT,
                        books TEXT,
                        motivational_text TEXT,
                        FOREIGN KEY (email) REFERENCES users(useremail))''')

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
                        rank INTEGER,
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
    for _ in range(150):  # Adjust the range for how many users you want to create
        useremail = f"user{_}@example.com"
        username = f"User{_}"
        #password = f"password{random.randint(1, 100)}"  # Generate a simple password
        password = f"password{_}"  # Generate a simple password
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
        

    def get_random_suggestions(suggestions, max_suggestions=2):
        num_suggestions = random.randint(0, max_suggestions)
        return ", ".join(random.sample(suggestions, num_suggestions)) if num_suggestions > 0 else None

    # Inserir indicações para cada usuário
    cursor.execute('SELECT useremail FROM users')
    users = cursor.fetchall()
    
    for user in users:
        email = user[0]
        
        # Gerar sugestões aleatórias para cada categoria
        courses = get_random_suggestions(cursos_sugestoes)
        videos = get_random_suggestions(videos_sugestoes)
        books = get_random_suggestions(livros_sugestoes)
        
        # Selecionar uma mensagem motivacional aleatória
        motivational_text = random.choice(mensagens_motivacionais)
        
        # Inserir indicações na tabela
        cursor.execute('''INSERT INTO indications (email, courses, videos, books, motivational_text)
                          VALUES (?, ?, ?, ?, ?)''', (email, courses, videos, books, motivational_text))
    
    

# Calculate average salary and assign ranks
    cursor.execute('''SELECT profession_id, region_id, AVG(salary) 
                      FROM profession_data 
                      GROUP BY profession_id, region_id''')
    
    average_salaries = cursor.fetchall()

    for profession_id, region_id, avg_salary in average_salaries:
        cursor.execute('''SELECT id, salary FROM profession_data 
                          WHERE profession_id = ? AND region_id = ?''', 
                       (profession_id, region_id))
        
        for id, salary in cursor.fetchall():
            if salary > avg_salary:
                rank = '1000'
            elif salary == avg_salary:
                rank = '100'
            else:
                rank = '10'

            # Update the profession_data table with the rank
            cursor.execute('''UPDATE profession_data 
                              SET rank = ? 
                              WHERE id = ?''', (rank, id))


    # Commit and close the connection
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created and populated with random data.")

create_and_populate_database()

