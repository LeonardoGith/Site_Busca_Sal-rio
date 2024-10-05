import hashlib
import pytest
import sqlite3
from flask import session, request, render_template
from flask.testing import FlaskClient
from unittest.mock import patch
from flask import Blueprint
from main import create_app  # Assuming you have an app factory in `app.py`
from routes.home import hash_password, verify_login, home_route

@pytest.fixture
def client():
    # Create a test client using Flask's built-in test client mechanism
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testkey'

    # Dynamically register a new Blueprint with a unique name
    test_home_route = Blueprint('home_test', __name__)  # Unique name

    @test_home_route.route('/check', methods=['POST'])
    def home_template():
        # Reuse the verify_login function
        email = request.form['email']
        password = request.form['Senha']

        if verify_login(email, password, db_name="professions.db"):
            session['user'] = email
            return render_template('indexTH.html')
        else:
            return render_template('indexL.html', message="Senha ou Usuário inválidos")
    
    # Register the dynamically created Blueprint
    app.register_blueprint(test_home_route)

    with app.test_client() as client:
        yield client

def test_hash_password():
    password = "mysecretpassword"
    hashed = hash_password(password)
    assert hashed == hashlib.sha256(password.encode()).hexdigest()

@patch('sqlite3.connect')
def test_verify_login_success(mock_connect):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = ('688787d8ff144c502c7f5cffaafe2cc588d86079f9de88304c26b0cb99ce91c6',)
    assert verify_login("leonardoemaill1@gmail.com", "asd") == True

@patch('sqlite3.connect')
def test_verify_login_failure(mock_connect):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = None  # No user found
    
    assert verify_login("wronguser@example.com", "password", db_name="test.db") == False

@patch('sqlite3.connect')
def test_verify_login_wrong_password(mock_connect):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = ('incorrecthashedpassword',)
    
    assert verify_login("testuser@example.com", "wrongpassword", db_name="test.db") == False

def test_home_template_success(client):
    with patch('routes.home.verify_login') as mock_verify_login:
        mock_verify_login.return_value = True

        response = client.post('/check', data={'email': 'leonardoemaill1@gmail.com', 'Senha': 'asd'})
        assert response.status_code == 200
        #assert b'indexTH.html' in response.data
        assert 'user' in session
        assert session['user'] == 'leonardoemaill1@gmail.com'

