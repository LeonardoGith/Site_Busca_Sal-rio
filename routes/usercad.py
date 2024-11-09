from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import sqlite3

from dados import databasehelper

usercad_route = Blueprint('usercad',__name__)

@usercad_route.route('/start')
def login_template():
    return render_template('newuser.html')

# Function to hash passwords
def hash_password(password):
    # Use SHA-256 to hash the password
    return hashlib.sha256(password.encode()).hexdigest()

def add_user_to_db(useremail, username, userpassword, db_name=databasehelper.database_name()):
    # Hash the password
    hashed_password = hash_password(userpassword)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''INSERT INTO users (useremail, username, userpassword)
                          VALUES (?, ?, ?)''', (useremail, username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # This will occur if the email already exists
    finally:
        conn.close()

@usercad_route.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        useremail = request.form['useremail']
        username = request.form['username']
        userpassword = request.form['userpassword']
        
        if add_user_to_db(useremail, username, userpassword):
            return render_template('indexL.html', message="Usuário cadastrado com sucesso.")
        else:
            return render_template('newuser.html', message="Email existente, tente novamente")
    
    return render_template('newuser.html')
