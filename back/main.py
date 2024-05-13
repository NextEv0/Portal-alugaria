from login import login
from pesquisa import pesquisar_sala, verificar_disponibilidade

def main():
    if login(email_usuario, senha_usuario):
        print("Autenticação bem-sucedida!")
        
        sala_info = pesquisar_sala(numero_sala)
        if sala_info:
            print("Informações da sala:", sala_info)
        else:
            print("Sala não encontrada.")

        # Verificar a disponibilidade da sala
        disponibilidade = verificar_disponibilidade(numero_sala)
        if disponibilidade:
            print("A sala está disponível.")
        else:
            print("A sala não está disponível.")
    else:
        print("Falha na autenticação.")

if __name__ == '__main__':
    main()
