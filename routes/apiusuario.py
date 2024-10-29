from flask import Blueprint, jsonify, request
import hashlib
import sqlite3

apiusuario_route = Blueprint('apiusuario',__name__)

"""""
Rota de usuarios

    -/api/usuarios / Listar os usuarios
    -/api/usuarios /new        (POST)    - inserir o cliente no servidor
    -/api/usuarios /<email>        (GET)    - Obter os dados de um cliente
    -/api/usuarios /<email>/update (PUT)    - Atualizar os dados do cliente
    -/api/usuarios /<email>/delete (DELETE) - deleta o registro do usuário

"""""

# Function to hash passwords
def hash_password(password):
    # Use SHA-256 to hash the password
    return hashlib.sha256(password.encode()).hexdigest()

# Função para conectar ao banco de dados e obter todos os usuários
def get_all_usuarios(db_name="professions.db"):
    conn = sqlite3.connect(db_name)  # Conecte ao seu banco de dados
    cursor = conn.cursor()
    
    cursor.execute("SELECT useremail, username FROM users")
    usuarios = cursor.fetchall()
    
    conn.close()
    return usuarios

def get_usuario(user_email, db_name="professions.db"):

    print("vou obter dados de " + user_email)
    conn = sqlite3.connect(db_name)  # Conecte ao seu banco de dados
    cursor = conn.cursor()
    
    cursor.execute("SELECT useremail, username FROM users where useremail = ?", (user_email,))

    usuarios = cursor.fetchall()
    
    conn.close()
    return usuarios


def add_user_to_db(useremail, username, userpassword, db_name="professions.db"):
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

@apiusuario_route.route('/', methods=['GET'])
def api_usuarios_lista_usuarios():
    usuarios = get_all_usuarios()
    # Converter lista de usuários para dicionário para formatação em JSON
    usuarios_json = [
        {
            "useremail": usuario[0],
            "username": usuario[1]
        } for usuario in usuarios
    ]
    
    return jsonify(usuarios_json)



@apiusuario_route.route('/new', methods=['POST'])
def api_usuarios_inserir_usuario():
   try:
      # Dados do usuário a serem adicionados
      new_usuario = request.get_json()
      username = new_usuario.get('useremail')
      useremail = new_usuario.get('username')
      userpassword = new_usuario.get('password')

      add_user_to_db(useremail, username, userpassword, db_name="professions.db")

      return jsonify({"message": "Usuário adicionado com sucesso!"}), 201
   except Exception as e:
      return jsonify({"error": str(e)}), 400


@apiusuario_route.route('/<string:user_email>', methods=['GET'])
def api_usuarios_detalhe_usuario(user_email):
    usuarios = get_usuario(user_email)
    # Converter lista de usuários para dicionário para formatação em JSON
    usuarios_json = [
        {
            "useremail": usuario[0],
            "username": usuario[1]
        } for usuario in usuarios
    ]
    
    return jsonify(usuarios_json)


@apiusuario_route.route('/<string:user_email>/delete', methods=['DELETE','POST','GET'])
def api_usuarios_deletar_usuario(user_email):
  try:
        # Conectando ao banco de dados
        conn = sqlite3.connect('professions.db')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM users WHERE useremail = ?", (user_email,))
        conn.commit()

        # Verifica se a exclusão foi bem-sucedida
        if cursor.rowcount == 0:
            return jsonify({"message": "Usuário não encontrado."}), 404

        conn.close()
        return jsonify({"message": "Usuário excluído com sucesso!"})
  except Exception as e:
        return jsonify({"error": str(e)}), 400


