from app.models.domain import certificate
from app.models.schemas import users


def get_solana_user_schema():
    return users.SolanaUser


def get_certificate_storage_model():
    return certificate.CertificateStorage
