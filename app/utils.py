from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

# Configuramos el hasher de forma explícita
# Esto reemplaza al antiguo pwd_context de passlib
password_hash = PasswordHash((BcryptHasher(),))

def hash(password: str):
    """
    Recibe la contraseña en texto plano y devuelve el hash.
    """
    return password_hash.hash(password)

def verify(plain_password: str, hashed_password: str):
    """
    Verifica si la contraseña coincide con el hash almacenado.
    """
    return password_hash.verify(plain_password, hashed_password)