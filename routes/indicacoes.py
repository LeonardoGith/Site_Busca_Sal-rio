from flask import Flask, render_template

indicacoes_route = Flask(__name__)

@indicacoes_route.route('/init')
def funcao():
    return render_template('indicacoes.html')