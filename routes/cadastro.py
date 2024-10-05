from flask import Blueprint, render_template

home_route = Blueprint('cadastro',__name__)

@home_route.route('/cadastro')
def home():
    return render_template('indexL.html')

