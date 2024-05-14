import pandas as pd
import functions as fc
from os import system
from database import User, Room, Schedules

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
        query = fc.room_query(sala_nome)
        print(query)
        system("pause")
    elif choice == 3:
        print("Programa Encerrado!")
        exit()
    else:
        print("Comando inválido")
        system("pause")