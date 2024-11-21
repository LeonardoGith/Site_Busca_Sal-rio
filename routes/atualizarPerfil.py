from flask import Blueprint, render_template, request, session
import hashlib
import sqlite3

from dados import databasehelper

atualizarPerfil_route = Blueprint('atualizarPerfil',__name__)


@atualizarPerfil_route.route('/init')
def atualizarPerfil_init():
    # Check if the user is logged in
    if 'user' not in session:
        return render_template('indexTH.html')

    user_email = session['user']

    conn = sqlite3.connect(databasehelper.database_name())
    cursor = conn.cursor()

    # Check if the user is already in the profession_data table, join with professions and regions to get names
    cursor.execute('''
        SELECT pd.salary, p.profession_name, r.region_name, pd.profession_id, pd.region_id
        FROM profession_data pd
        JOIN professions p ON pd.profession_id = p.id
        JOIN regions r ON pd.region_id = r.id
        WHERE pd.email = ?
    ''', (user_email,))
    user_data = cursor.fetchone()

    if user_data:
        user_salary = user_data[0]
        user_profession_id = user_data[3]
        user_region_id = user_data[4]

        # If the user is not in the profession_data table, fetch available professions and regions
        cursor.execute('SELECT id, profession_name FROM professions')
        professions = cursor.fetchall()
        
        cursor.execute('SELECT id, region_name FROM regions')
        regions = cursor.fetchall()

        conn.close()

        # Render the form to insert a new profession for the logged-in user
        return render_template('mudançaInformacoes.html', professions=professions, regions=regions, useremail=user_email, user_profession_id=user_profession_id, user_region_id=user_region_id, user_salary=user_salary)
    else:
        return render_template('indexTH.html')   

@atualizarPerfil_route.route('/update_user', methods=['POST'])
def atualizarPerfil_updateuser():
    # Check if the user is logged in
    if 'user' not in session:
        return render_template('indexTH.html')
    
    user_email = session['user']

    conn = sqlite3.connect(databasehelper.database_name())
    cursor = conn.cursor()

    # Get data from the form submission
    profession_id = request.form.get('profession_id')
    region_id = request.form.get('region_id')
    salary = request.form.get('salary')

    # Check if the user already exists in the profession_data table
    cursor.execute('SELECT id FROM profession_data WHERE email = ?', (user_email,))
    user_data_exists = cursor.fetchone()

    if user_data_exists:
        # Update existing record
        cursor.execute('''
            UPDATE profession_data
            SET profession_id = ?, region_id = ?, salary = ?
            WHERE email = ?
        ''', (profession_id, region_id, salary, user_email))
    else:
        # Insert new record
        cursor.execute('''
            INSERT INTO profession_data (email, profession_id, region_id, salary)
            VALUES (?, ?, ?, ?)
        ''', (user_email, profession_id, region_id, salary))

    conn.commit()
    conn.close()

    # Render the form to insert a new profession for the logged-in user
    return render_template('indexTH.html')