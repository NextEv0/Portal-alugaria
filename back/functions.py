import pandas as pd
import numpy as np
from os import system
from pprint import pprint
from database import User, Room, Schedules
from werkzeug.security import check_password_hash
from email_sender import send_email


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


def reserve_room(user_id, room_name, date, start_time, end_time):
    response = {'success': False, 'message': None}
    
    # Obter dados da sala
    room_df = room_query(room_name)
    
    if room_df.empty:
        response['message'] = "Sala não encontrada"
        return response
    
    # Convertendo strings para datetime para comparação
    date = pd.to_datetime(date, format='%d-%m-%Y')
    start_time = pd.to_datetime(start_time, format='%H:%M').time()
    end_time = pd.to_datetime(end_time, format='%H:%M').time()
    
    # Filtrando para a data específica
    room_df['date'] = pd.to_datetime(room_df['date'], format='%d-%m-%Y')
    room_df = room_df[room_df['date'] == date]
    
    if room_df.empty:
        response['message'] = "Nenhuma reserva encontrada para a data fornecida"
        return response

    # Verificando se o intervalo está disponível
    availability = room_df[
        (pd.to_datetime(room_df['start_time'], format='%H:%M').dt.time >= start_time) & 
        (pd.to_datetime(room_df['end_time'], format='%H:%M').dt.time <= end_time) &
        (room_df['reserved'] == False)
    ]
    
    if availability.empty:
        response['message'] = "Horário já reservado ou indisponível"
        return response
    
    # Atualizando as reservas
    room_df.loc[
        (pd.to_datetime(room_df['start_time'], format='%H:%M').dt.time >= start_time) & 
        (pd.to_datetime(room_df['end_time'], format='%H:%M').dt.time <= end_time) &
        (room_df['reserved'] == False),
        ['reserved', 'user_id', 'description']
    ] = [True, user_id, 'Reserva Pessoal']
    
    for index, row in room_df.iterrows():
        Schedules.update_one({'_id': row['_id']}, {'$set': {'reserved': row['reserved'], 'user_id': row['user_id'], 'description': row['description']}})
    
    response['success'] = True
    response['message'] = "Sala reservada com sucesso"

    # Enviando e-mail de confirmação
    user = User.find_one({'_id': user_id})
    email = user['account']['email']
    subject = "Confirmação de Reserva de Sala"
    message = f"Olá {user['name']},\n\nSua reserva para a sala {room_name} foi confirmada para o dia {date.strftime('%d-%m-%Y')} das {start_time.strftime('%H:%M')} às {end_time.strftime('%H:%M')}.\n\nAtenciosamente,\nEquipe de Reservas"

    send_email(email, subject, message)

    return response


def cancel_reserve(user_id, room_name, date):
    response = {'success': False, 'message': None}
    room_df = room_query(room_name)
    
    if room_df.empty:
        response['message'] = "Sala não encontrada"
        return response
    
    date = pd.to_datetime(date, format='%d-%m-%Y')

    room_df['date'] = pd.to_datetime(room_df['date'], format='%d-%m-%Y')
    room_df = room_df[room_df['date'] == date]
    
    if room_df.empty:
        response['message'] = "Nenhuma reserva encontrada para a data fornecida"
        return response

    availability = room_df[(room_df['reserved'] == True)]
    
    if availability.empty:
        response['message'] = "Você não possui reservas este dia"
        return response

    room_df.loc[
        (room_df['user_id'] == user_id) &
        (room_df['reserved'] == True),
        ['reserved', 'user_id', 'description']
    ] = [False, np.nan, 'Livre']

    for index, row in room_df.iterrows():
        Schedules.update_one({'_id': row['_id']}, {'$set': {'reserved': row['reserved'], 'user_id': row['user_id'], 'description': row['description']}})

    response['success'] = True
    response['message'] = "Reserva cancelada com sucesso"

    # Enviando e-mail de confirmação
    user = User.find_one({'_id': user_id})
    email = user['account']['email']
    subject = "Confirmação de cancelamento de Reserva de Sala"
    message = f"Olá {user['name']},\n\nSua reserva para a sala {room_name} foi cancelada para o dia {date.strftime('%d-%m-%Y')}.\n\nAtenciosamente,\nEquipe de Reservas"
    send_email(email, subject, message)
    
    return response


def update_reserve(user_id, room_name, current_date, new_date):
    response = {'success': False, 'message': None}

    # Obter dados da sala
    room_df = room_query(room_name)

    if room_df.empty:
        response['message'] = "Sala não encontrada"
        return response

    # Convertendo strings para datetime para comparação
    current_date = pd.to_datetime(current_date, format='%d-%m-%Y')
    new_date = pd.to_datetime(new_date, format='%d-%m-%Y')

    # Filtrando para a data específica
    room_df['date'] = pd.to_datetime(room_df['date'], format='%d-%m-%Y')
    user_reservations = room_df[(room_df['date'] == current_date) & (room_df['user_id'] == user_id) & (room_df['reserved'] == True)]

    if user_reservations.empty:
        response['message'] = "Nenhuma reserva encontrada para a data fornecida ou usuário não tem reservas"
        return response

    # Verificando se o novo dia está disponível nos mesmos horários
    conflict = False
    for index, row in user_reservations.iterrows():
        start_time = row['start_time']
        end_time = row['end_time']
        availability = room_df[(room_df['date'] == new_date) & (room_df['reserved'] == True) & 
                               ((room_df['start_time'] < end_time) & (room_df['end_time'] > start_time))]

        if not availability.empty:
            conflict = True
            break

    if conflict:
        response['message'] = "Novo dia entra em conflito com outra reserva"
        return response

    # Atualizando o dia da reserva
    for index, row in user_reservations.iterrows():
        Schedules.update_one(
            {'_id': row['_id']},
            {'$set': {'date': new_date}}
        )

    response['success'] = True
    response['message'] = "Data da reserva atualizada com sucesso"

    # Enviando e-mail de confirmação
    user = User.find_one({'_id': user_id})
    email = user['account']['email']
    subject = "Confirmação de Atualização de Reserva de Sala"
    message = f"Olá {user['name']},\n\nSua reserva para a sala {room_name} foi atualizada para o dia {new_date.strftime('%d-%m-%Y')}.\n\nAtenciosamente,\nEquipe de Reservas"

    send_email(email, subject, message)

    return response


if __name__ == "__main__":
    system("cls")
    current_user = User.find_one({'register': '22300028'})

    response = reserve_room(current_user['_id'], room_name="Sala 08", date="13-05-2024", start_time="16:30", end_time="18:10")

    resultado = room_query("Sala 08").drop(['room_id', 'user_id'], axis=1)

    print(response['message'])
    print(resultado.head(15))
    
