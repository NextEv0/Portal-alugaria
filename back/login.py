from database import User
from werkzeug.security import check_password_hash

def login(email: str, password: str) -> bool:

    if "@cesupa.br" not in email:
        raise ValueError("O e-mail fornecido não pertence ao domínio do CESUPA.")

    user = User.find_one({'account.email': email})
    
    if not user:
        raise ValueError("Usuário não encontrado")
    
    if not check_password_hash(user['account']['password'], password):
        raise ValueError("Senha incorreta")
    
    print("Acesso concedido")
    return True

