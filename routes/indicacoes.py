from flask import Flask, render_template, g, Blueprint, session, request
import sqlite3

from dados import databasehelper

# Configurações e inicialização
DATABASE = db_name=databasehelper.database_name()
indicacoes_route = Blueprint('indicacoes', __name__)

# Função para obter conexão com o banco de dados
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Função para executar consultas SQL
def query_db(query, args=(), one=False):
    """Função auxiliar para consultar o banco de dados."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Fechar a conexão com o banco de dados ao final da requisição
@indicacoes_route.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Função para conectar ao banco de dados e obter o usuário com base no índice
def get_usuario_by_index(index, user_email):

    user_rank = query_db('SELECT Rank FROM profession_data WHERE email = ?', [user_email], one=True)

    print("user_rank " + str(user_rank))
    if user_rank:
            user_rank = user_rank[0]
            
            # Consultar usuários com rank maior (menor número indica rank mais alto)
            higher_rank_users = query_db('''
                SELECT p.email, i.courses, i.videos, i.books, i.motivational_text, p.rank
                FROM profession_data p
                JOIN indications i ON p.email = i.email
                WHERE p.Rank >= ? LIMIT 1 OFFSET ?
            ''', [user_rank, index])

            print("higher_rank_users " + str(higher_rank_users))    
    else:
        higher_rank_users = None
    return higher_rank_users, user_rank


# Rota para exibir as recomendações
@indicacoes_route.route('/init')
def usuarios():
    user_email = session['user']

    print("logged email " + user_email)

    page = request.args.get('page', 0, type=int)  # Obter o número da página (0 por padrão)
    higher_rank_users, user_rank = get_usuario_by_index(page, user_email)
    
    # Verifique se o usuário existe
    if higher_rank_users is None:
        return render_template('indicacoes.html', indicacoes=None, has_next=False)
    
    has_next = True if higher_rank_users != None else False
    
    print("higher_rank_users " + str(higher_rank_users))

    return render_template('indicacoes.html', indicacoes=higher_rank_users, has_next=has_next, page=page, user_email=user_email, user_rank=user_rank)


def mostrar_indicacoes():
    # Obter o rank do usuário atual

    user_email = session['user']

    print("logged email " + user_email)
    user_rank = query_db('SELECT Rank FROM profession_data WHERE email = ?', [user_email], one=True)

    print("user_rank " + str(user_rank))

    if user_rank:
        user_rank = user_rank[0]
        
        # Consultar usuários com rank maior (menor número indica rank mais alto)
        higher_rank_users = query_db('''
            SELECT p.email, i.courses, i.videos, i.books, i.motivational_text
            FROM profession_data p
            JOIN indications i ON p.email = i.email
            WHERE p.Rank < ?
        ''', [user_rank])

        print("higher_rank_users " + str(higher_rank_users))

        return render_template('indicacoes.html', indicacoes=higher_rank_users)
    else:
        return "Usuário não encontrado."


