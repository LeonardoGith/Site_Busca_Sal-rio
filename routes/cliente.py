from flask import Blueprint, render_template

cliente_route = Blueprint('cliente', __name__)


"""""
Rota de Clientes

    -/clientes / Listar os clientes
    -/clientes /           (POST)    - inserir o cliente no servidor
    -/clientes /new         (GET)    - renderizar o formulario para criar um cliente
    -/clientes /<id>        (GET)    - Obter os dados de um cliente
    -/clientes /<id>/edit   (GET)    - rederizar um formulario para editar um cliente
    -/clientes /<id>/update (PUT)    - Atualizar os dados do cliente
    -/clientes /<id>/delete (DELETE) - deleta o registro do usuário

"""""

@cliente_route.route('/')
def lista_clientes():
    """""
    Listar os clientes
    """""
    return render_template('litsa_clientes.html')





@cliente_route.route('/', methods=['POST'])
def inserir_cliente(cliente_id):
    """""
    Inserir os dados do cliente no banco de dados
    """""
    pass





@cliente_route.route('/new')
def form_cliente():
    """""
    Formulário para cadastrar um cliente
    """""
    return render_template('form_clientes.html')





@cliente_route.route('/<int:client_id>')
def detalhe_cliente(client_id):
    """""
    Exibir detalhes do cliente
    """""
    return render_template('detalhe_cliente.html')





@cliente_route.route('/<int:client_id>/edit')
def form_edit_cliente(client_id):
    """""
    Formulario para editar um cliente
    """""
    return render_template('form_edit_cliente.html')




@cliente_route.route('/<int:client_id>/eupdate', methods=['PUT'])
def atualizar_cliente(client_id):
    """""
    Atualizar informações do Cliente
    """""
    pass



@cliente_route.route('/<int:client_id>/delete', methods=['PUT'])
def deletar_cliente(client_id):
    """""
    Deletar informações do Cliente
    """""
    pass


