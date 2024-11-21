from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from routes.home import home_route
from routes.cliente import cliente_route
from routes.login import login_route
from routes.logout import logout_route
from routes.pesquisa import pesquisa_route
from routes.usercad import usercad_route
from routes.professioncad import professioncad_route
from routes.indicacoes import indicacoes_route
from routes.apiusuario import apiusuario_route
from routes.webhook import webhook_route
from routes.atualizarPerfil import atualizarPerfil_route


# inicialização (Sempre no início)dhdh
app = Flask(__name__)

app.secret_key = 'mack_enzie_key'


app.register_blueprint(login_route)
app.register_blueprint(logout_route, url_prefix='/logout')
app.register_blueprint(home_route, url_prefix='/home')
app.register_blueprint(cliente_route, url_prefix='/clientes')
app.register_blueprint(pesquisa_route, url_prefix='/pesquisa')
app.register_blueprint(usercad_route, url_prefix='/user')
app.register_blueprint(professioncad_route, url_prefix='/professioncad')
app.register_blueprint(indicacoes_route, url_prefix='/indicacoes')
app.register_blueprint(apiusuario_route, url_prefix='/api/usuarios')
app.register_blueprint(webhook_route, url_prefix='/git_pull')
app.register_blueprint(atualizarPerfil_route, url_prefix='/AtualizarPerf')


SWAGGER_URL = '/api/docs'  # Swagger UI URL
API_URL = '/static/swagger.yaml'  # Path to your swagger.yaml file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI endpoint
    API_URL,  # Swagger file endpoint
    config={'app_name': "Busca Salario"}  # Swagger UI config
)

app.register_blueprint(swaggerui_blueprint)


def create_app():
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
