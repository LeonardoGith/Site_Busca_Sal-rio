import hashlib
import os

def hash_password(password):
    # Use SHA-256 to hash the password
    return hashlib.sha256(password.encode()).hexdigest()

def database_name():
    name = str(os.path.join(os.getcwd(), 'professions.db'))
    return name

print(database_name())