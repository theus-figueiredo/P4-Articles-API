from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def password_hash_generate(password: str) -> str:
    return CRIPTO.hash(password)


def validate_password(password: str, hash_password: str) -> bool:
    return CRIPTO.verify(password, hash_password)
