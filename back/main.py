from os import system 
from database import User, Room, Schedules
from werkzeug.security import check_password_hash
from pesquisa import pesquisar_sala, verificar_disponibilidade

def login(email: str, password: str):
    response = {'authenticated': False, 'message': None,'user': None}
    
    if ".cesupa.br" not in email:
        response['message'] = "E-mail não pertence ao domínio cesupa"
        return response

    user = User.find_one({'account.email': email})
    
    if not user:
        response['message'] = "Usuário não encontrado"
        return  response
    
    if not check_password_hash(user['account']['password'], password):
        response['message'] = "Senha incorreta"
        return response
    response['user'] = user
    response['message'] = "Acesso concedido"
    response['authenticated'] = True
    return response


while True:
    system("cls")
    print("-----------------------------------------")
    print("                                         ")
    print("               [1] LOGIN                 ")
    print("               [2] SAIR                  ")
    print("                                         ")
    print("-----------------------------------------")
    choice = int(input("> "))

    if choice == 1:
        email = input("Por favor, insira o seu email: ")
        password = input("Por favor, insira a sua senha: ")
        
        response = login(email, password)

        if not response['authenticated']:
            print(response['message'])
            system("pause")
        
        else:
            print(response['message'])
            system("pause")
            break

    elif choice == 2:
        print("Programa Encerrado!")
        exit()
    else:
        print("Comando inválido")
        system("pause")
current_user = response['user']
while True:
    system("cls")
    print("-----------------------------------------")
    print("                                         ")
    print("            [1] PESQUISAR SALA           ")
    print("            [2]     SAIR                 ")
    print("                                         ")
    print("-----------------------------------------")
    choice = int(input("> "))
