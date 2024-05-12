import pandas as pd

def pesquisar_sala(numero_sala, dados_salas):
    if numero_sala in dados_salas.index:
        return dados_salas.loc[numero_sala]
    else:
        return None


def encontrar_salas_similares(numero_sala, dados_salas):
    salas_similares = []
    for index, sala in dados_salas.iterrows():
        if str(numero_sala) in str(index):
            salas_similares.append((index, sala))
    return salas_similares


if __name__ == "__main__":
    # Carregar o arquivo Excel em um DataFrame pandas
    try:
        arquivo_excel = pd.read_excel('SalasAlugaria.xlsx', index_col=0)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        exit()

    # Solicitação do número da sala ao usuário
    numero_sala_pesquisada = input("Digite o número da sala que deseja pesquisar: ")

    # Pesquisar a sala
    informacoes_sala = pesquisar_sala(numero_sala_pesquisada, arquivo_excel)
    if informacoes_sala is not None:
        print("Informações sobre a sala", numero_sala_pesquisada)
        print(informacoes_sala)
    else:
        print("Sala não encontrada.")

    # Encontrar salas similares
    salas_similares = encontrar_salas_similares(numero_sala_pesquisada, arquivo_excel)
    if salas_similares:
        print("\nSalas similares à sala", numero_sala_pesquisada)
        for sala in salas_similares:
            print("Dia da Semana:", sala[0])
            print(sala[1])
            print()
    else:
        print("Não foram encontradas salas similares.")    