from flask import Blueprint, render_template, request, session
#from routes.databaseLiteInMemory import get_dataframe, calculate_average_salary
from routes.databaseLite import calculate_average_salary
import sqlite3

pesquisa_route = Blueprint('pesquisa',__name__)


def getPesqRefData():
    conn = sqlite3.connect('professions.db')
    cursor = conn.cursor()

    # If the user is not in the profession_data table, fetch available professions and regions
    cursor.execute('SELECT id, profession_name FROM professions')
    professions = cursor.fetchall()
    
    cursor.execute('SELECT id, region_name FROM regions')
    regions = cursor.fetchall()

    conn.close()

    return regions, professions


def get_name_by_id(data_list, search_id):
    # Iterate over the list of tuples to find the matching ID
    for item in data_list:
        item_id, item_name = item  # Unpack the tuple
        if str(item_id) == str(search_id):
            return item_name  # Return the name if ID matches
    return None  # Return None if ID not found


@pesquisa_route.route('/init', methods=['GET'])
def routeInicioPesquisa():
    # Check if the user is logged in
    if 'user' not in session:
        return render_template('indexL.html')
    
    user_email = session['user']

    regions, professions = getPesqRefData()

    # Render the form to insert a new profession for the logged-in user
    return render_template('calcmedia.html', professions=professions, regions=regions, useremail=user_email)


@pesquisa_route.route('/search', methods=['POST'])
def processar():
    # Check if the user is logged in
    if 'user' not in session:
        return render_template('indexL.html')
    
    user_email = session['user']


    profession_id = request.form['profession_id']
    region_id = request.form['region_id']


    print (f"Opção 1 selecionada: {region_id}, Opção 2 selecionada: {profession_id}")


    #localDF = get_dataframe() # so usar se for o databaseLiteInMemory
    #average_salary = calculate_average_salary(localDF, regiao, profissao)

    average_salary = calculate_average_salary(region_id, profession_id)

    regions, professions = getPesqRefData()

    # Get the names for the specific IDs
    region_name = get_name_by_id(regions, region_id)
    profession_name = get_name_by_id(professions, profession_id)

    if average_salary is not None:
        print(f"The average salary for {profession_name} in {region_name} is: {average_salary:.2f}")
    else:
        print(f"No data available for {profession_name} in {region_name}.")

    return render_template('calcmedia.html', region=region_name, profession=profession_name, average_salary=average_salary, professions=professions, regions=regions, useremail=user_email)
