from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import sqlite3

professioncad_route = Blueprint('professioncad',__name__)

@professioncad_route.route('/init')
def professioncad_init():
    # Check if the user is logged in
    if 'user' not in session:
        return render_template('indexL.html')
    
    user_email = session['user']

    conn = sqlite3.connect('professions.db')
    cursor = conn.cursor()

    # Check if the user is already in the profession_data table, join with professions and regions to get names
    cursor.execute('''
        SELECT pd.salary, p.profession_name, r.region_name
        FROM profession_data pd
        JOIN professions p ON pd.profession_id = p.id
        JOIN regions r ON pd.region_id = r.id
        WHERE pd.email = ?
    ''', (user_email,))
    user_data = cursor.fetchone()

    if user_data:
        # If the user exists in the table, render a new page showing their profession data
        conn.close()
        return render_template('user_profession_data.html', user_data=user_data)
    
    # If the user is not in the profession_data table, fetch available professions and regions
    cursor.execute('SELECT id, profession_name FROM professions')
    professions = cursor.fetchall()
    
    cursor.execute('SELECT id, region_name FROM regions')
    regions = cursor.fetchall()

    conn.close()

    # Render the form to insert a new profession for the logged-in user
    return render_template('professioncad.html', professions=professions, regions=regions, useremail=user_email)


@professioncad_route.route('/add_profession', methods=['POST'])
def add_profession():
    profession_id = request.form['profession_id']
    region_id = request.form['region_id']
    salary = request.form['salary']
    useremail = request.form['email']  # E-mail do usuário logado

    conn = sqlite3.connect('professions.db')
    cursor = conn.cursor()

    # Inserir dados na tabela profession_data
    cursor.execute('''INSERT INTO profession_data (profession_id, region_id, salary, email)
                      VALUES (?, ?, ?, ?)''', (profession_id, region_id, salary, useremail))
    
    conn.commit()
    conn.close()
    
    return render_template('indexH.html')
