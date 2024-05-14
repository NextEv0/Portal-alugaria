import pandas as pd
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


def room_query(room_name=None):
    # Carregando dados de usuário e transformando em dataframes
    user_df = pd.DataFrame(list(User.find()))
    user_df = user_df.rename(columns={'_id': 'user_id', 'name': 'user_name'})
    user_df = user_df.drop(['role', 'register', 'account'], axis=1)

    # Verificando se a sala foi fornecida
    if room_name:
        room = Room.find_one({'name': room_name})
        #Verificando se a sala existe
        if room:
            room_df = pd.DataFrame([room])
        #Se não existir, retorne um dataframe vazio
        else:
            return pd.DataFrame([])
    #Se a sala não foi fornecida, retorne todas as salas
    else:
        room_df = pd.DataFrame(list(Room.find()))

    #Adquirindo dados da sala de usuário
    room_df = room_df.rename(columns={'_id': 'room_id', 'name': 'room_name'})
    room_df = room_df.drop(['floor', 'description'], axis=1)

    schedules_df = pd.DataFrame(list(Schedules.find()))

    #Unindo os dados dos 3 dataframes em um só
    query = schedules_df.merge(room_df, on='room_id')
    query = query.merge(user_df, on='user_id', how='left')

    #Formatando data e horário
    query["date"] = pd.to_datetime(query["date"]).dt.strftime('%d-%m-%Y')
    query['start_time'] = pd.to_datetime(query["start_time"]).dt.strftime('%H:%M')
    query['end_time'] = pd.to_datetime(query["end_time"]).dt.strftime('%H:%M')

    return query