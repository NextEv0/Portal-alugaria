import pandas as pd

# Substitua 'caminho_para_o_arquivo.xlsx' pelo caminho real do seu arquivo Excel
caminho_arquivo_excel = 'SalasAlugaria.xlsx'

# Carregar o arquivo Excel em um DataFrame pandas
tabela_excel = pd.read_excel(caminho_arquivo_excel)

if __name__ == "__main__":
    # Exibir a tabela
    print(tabela_excel)