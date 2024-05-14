import pandas as pd
from os import system
from database import User, Room, Schedules
from werkzeug.security import check_password_hash


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


def room_query(room_name:str):
    user_df = pd.DataFrame(list(User.find()))
    user_df['user_id'] = user_df['_id']
    user_df = user_df.drop(['_id','role','register','account'], axis=1)

    room_df = pd.DataFrame(list(Room.find()))
    room_df['room_id'] = room_df['_id']
    room_df = room_df.drop(['_id','floor', 'description'], axis=1)


    schedules_df = pd.DataFrame(list(Schedules.find()))
    query = schedules_df.merge( room_df, on='room_id')
    query = query.merge(user_df, on='user_id', how='left')

    query["date"] = pd.to_datetime(query["date"]).dt.strftime('%d-%m-%Y')
    query['start_time'] = pd.to_datetime(query["start_time"]).dt.strftime('%H:%M')
    query['end_time'] = pd.to_datetime(query["end_time"]).dt.strftime('%H:%M')
    return query


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
    print("            [2] RESERVAR SALA            ")
    print("            [3]     SAIR                 ")
    print("                                         ")
    print("-----------------------------------------")
    choice = int(input("> "))

    if choice == 1:
        sala_nome = input("Digite o nome da sala: ")
        query = room_query(sala_nome)
        print(query)
        system("pause")
