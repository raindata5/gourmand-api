from passlib.context import CryptContext
from passlib.hash import argon2
from passlib.exc import UnknownHashError
import secrets
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

interface_argon2 = lambda the_salt: argon2.using(salt_size=16, rounds=2, salt=the_salt)

def get_password_hash(password):
    # TODO: encode in UTF8 bytes
    salt = secrets.token_bytes(16)
    return  interface_argon2(the_salt=salt).hash(password)

def verification(plain_password, hashed_password):
    salt = secrets.token_bytes(16)
    for algo in [interface_argon2(the_salt=salt), pwd_context]:
        try:
            if algo.verify(plain_password,hashed_password):
                return True
        except (UnknownHashError, ValueError) as ex:
            print(f'{ex}:Reverting to bcrypto algo')
            break
    return False