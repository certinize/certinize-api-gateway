import bcrypt
from passlib.context import CryptContext

passw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_salt() -> str:
    return bcrypt.gensalt().decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return passw_context.verify(plain_password, hashed_password)  # type: ignore


def get_password_hash(password: str) -> str:
    return passw_context.hash(password)  # type: ignore
