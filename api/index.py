from flask import Flask
from routes.home import home_route
from routes.cliente import cliente_route
from routes.login import login_route
from routes.pesquisa import pesquisa_route
from routes.usercad import usercad_route
from routes.professioncad import professioncad_route

app = Flask(__name__)

app.secret_key = 'mack_enzie_key'

@app.route('/year')
def home():
    return 'Hello, World!'


app.register_blueprint(login_route)
app.register_blueprint(home_route, url_prefix='/home')
app.register_blueprint(cliente_route, url_prefix='/clientes')
app.register_blueprint(pesquisa_route, url_prefix='/pesquisa')
app.register_blueprint(usercad_route, url_prefix='/user')
app.register_blueprint(professioncad_route, url_prefix='/professioncad')
