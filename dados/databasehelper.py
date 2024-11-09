import hashlib
import os

def hash_password(password):
    # Use SHA-256 to hash the password
    return hashlib.sha256(password.encode()).hexdigest()

def database_name():

    # Check if the environment variable exists
    if os.getenv('BUSCADB') is not None:
        print("BUSCADB exists")
        name = str(os.getenv('BUSCADB')) + '/professions.db'
    else:
        name = 'professions.db'

    print("db name :" + name)
    
    return name


#os.environ['BUSCADB'] = '/home/LeonardoSv/buscasalario'
print(database_name())