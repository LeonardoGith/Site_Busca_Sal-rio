from flask import Blueprint, render_template, request, session
import hashlib
import sqlite3

from dados import databasehelper

logout_route = Blueprint('logout',__name__)


@logout_route.route('/init')
def logout_init():
    session['user'] = ""
    return render_template('indexL.html', message="Usuário desconectado")
