from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_password(passwd: str, hash_pass: str) -> bool:
    """
    Função para verificar se a senha está correta, comparando
    a senha em texto puro, informada pelo usuário, é o hash da senha
    no banco de dados
    """
    return CRIPTO.verify(passwd, hash_pass)


def generate_hast_pass(passwd: str) -> str:
    return CRIPTO.hash(passwd)
