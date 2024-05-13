from database import Room

def pesquisar_sala(numero_sala):
    sala = Room.find_one({'numero': numero_sala})
    if sala:
        return sala
    else:
        return "Sala não encontrada."

def verificar_disponibilidade(numero_sala):
    """Verifica se a sala está disponível."""
    sala = Room.find_one({'numero': numero_sala})
    if sala:
        return sala['disponibilidade'] == 'Sim'
    else:
        return "Sala não encontrada."
