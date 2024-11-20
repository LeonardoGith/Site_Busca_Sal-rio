from flask import Blueprint, render_template, request, session
import hashlib
import sqlite3

from dados import databasehelper

home_route = Blueprint('home',__name__)

# Function to hash passwords
def hash_password(password):
    # Use SHA-256 to hash the password
    return hashlib.sha256(password.encode()).hexdigest()


# Function to verify login
def verify_login(useremail, password, db_name=databasehelper.database_name()):
    # Hash the provided password
    hashed_password = hash_password(password)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Fetch user record based on username
    cursor.execute('SELECT userpassword FROM users WHERE useremail = ?', (useremail,))
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # Check if user exists and verify password
    if result is None:
        print("useremail not found.")
        return False
    elif result[0] == hashed_password:
        print("Login successful!")
        return True
    else:
        print("Incorrect password.")
        return False
    

@home_route.route('/check', methods=['POST'])
def home_tamplate():
    email = request.form['email']
    password = request.form['Senha']

    if verify_login(email, password, db_name=databasehelper.database_name()):
        session['user'] = email
        return render_template('indexTH.html')
    else:
        return render_template('indexL.html', message="Senha ou Usuário inválidos")


@home_route.route('/return', methods=['GET', 'POST'])
def home_return():
    return render_template('indexTH.html')


