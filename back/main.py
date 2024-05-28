import functions as fc
from os import system

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
        
        response = fc.login(email, password)

        if not response['authenticated']:
            print("Usuário ou senha incorretos")
            input("Pressione qualquer tecla para continuar...")
        else:
            print(response['message'])
            input("Pressione qualquer tecla para continuar...")
            break

    elif choice == 2:
        print("Programa Encerrado!")
        exit()
    else:
        print("Comando inválido")
        input("Pressione qualquer tecla para continuar...")

current_user = response['user']

while True:
    system("cls")
    print("-------------------------------------------")
    print("                                           ")
    print("            [1]  PESQUISAR SALA            ")
    print("            [2]  RESERVAR SALA             ")
    print("            [3] VISUALIZAR RESERVAS        ")
    print("            [4]     SAIR                   ")
    print("                                           ")
    print("-------------------------------------------")
    choice = int(input("> "))

    if choice == 1:
        sala_nome = input("Digite o nome da sala: ")
        query = fc.room_query(sala_nome)
        if query.empty:
            print("A sala pesquisada não existe")
        else:
            horario = input("Digite o dia para visualizar(dd-mm-yyyy): ")
        
        query = query.loc[query['date'] == horario]

        if query.empty:
            print("O horário não está disponível ou não se encontra cadastrado")
        else:
            query = query.drop(['_id', 'room_id', 'user_id', 'reserved'], axis=1)
            colunas = {'date': 'Data', 'start_time': 'Inicio', 'end_time': 'Fim', 'description': 'Descrição', 'room_name': 'Sala', 'user_name': 'Usuário'}
            query = query.rename(columns=colunas)
            print(query)
        input("Pressione qualquer tecla para continuar...")
    
    elif choice == 2:
        sala_nome = input("Digite o nome da sala para reserva: ")
        query = fc.room_query(sala_nome)
        
        if query.empty:
            print("A sala pesquisada não existe")
            input("Pressione qualquer tecla para continuar...")
        else:
            date = input("Digite o dia para visualizar(dd-mm-yyyy): ")
        
        query = query.loc[query['date'] == date]

        if query.empty:
            print("O horário não está disponível ou não se encontra cadastrado")
            input("Pressione qualquer tecla para continuar...")
        
        else:
            query = query.drop(['_id', 'room_id', 'user_id', 'reserved'], axis=1)
            colunas = {'date': 'Data', 'start_time': 'Inicio', 'end_time': 'Fim', 'description': 'Descrição', 'room_name': 'Sala', 'user_name': 'Usuário'}
            query = query.rename(columns=colunas)
            system("cls")
            print(query)
            start_time = input("Digite a hora de início (HH:MM): ")
            end_time = input("Digite a hora de fim (HH:MM): ")
            response = fc.reserve_room(current_user['_id'], sala_nome, date, start_time, end_time)
            print(response['message'])
            input("Pressione qualquer tecla para continuar...")

    elif choice == 3:
        query = fc.room_query()
        query = query.loc[query['user_id'] == current_user['_id']]

        if query.empty:
            print("Não há reservas feitas por você")
        else:
            query = query.drop(['_id', 'room_id', 'user_id', 'reserved'], axis=1)
            colunas = {'date': 'Data', 'start_time': 'Inicio', 'end_time': 'Fim', 'description': 'Descrição', 'room_name': 'Sala', 'user_name': 'Usuário'}
            query = query.rename(columns=colunas)
            print(query)
        input("Pressione qualquer tecla para continuar...")

    elif choice == 4:
        print("Programa Encerrado!")
        exit()
    
    else:
        print("Comando inválido")
        input("Pressione qualquer tecla para continuar...")
