import pandas as pd
import functions as fc
from os import system
from time import sleep

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
            print(response['message'])
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
        query = fc.room_query(sala_nome)
        print(query)
        input("Pressione qualquer tecla para continuar...")
    elif choice == 2:
        sala_nome = input("Digite o nome da sala para reserva: ")
        date = input("Digite a data (dd-mm-yyyy): ")
        start_time = input("Digite a hora de início (HH:MM): ")
        end_time = input("Digite a hora de fim (HH:MM): ")
        response = fc.reserve_room(current_user['_id'], sala_nome, date, start_time, end_time)
        print(response['message'])
        input("Pressione qualquer tecla para continuar...")
    elif choice == 3:
        print("Programa Encerrado!")
        exit()
    else:
        print("Comando inválido")
        input("Pressione qualquer tecla para continuar...")
