from database import User, Room, Reserve
from werkzeug.security import check_password_hash

def login(email:str, password:str):
    user = User.find_one({'account.email': email})
    
    if not user:
        raise Exception("Usuário não encontrado")
    if not check_password_hash(user['account']['password'], password):
        raise Exception("Senha incorreta")
    print("Acesso concedido")



if __name__ == "__main__":
    login("carlos22300028@aluno.cesupa.br", "22300028")
