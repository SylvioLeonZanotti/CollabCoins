import datetime
import json
import os

LOG_FILE_NEW_USER = 'logs_users.json'
LOG_FILE_LOGIN = 'login_users.json'


def log_event(name, email, company):
    data = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        "Evento": "Novo usuario inserido ao banco de dados",
        "Horario": data,
        "Nome": name,
        "Email": email,
        "Empresa": company
    }
    
    if os.path.exists(LOG_FILE_NEW_USER):
        with open(LOG_FILE_NEW_USER, 'r+') as log_file:
            logs = json.load(log_file)
            logs.append(log_entry)
            log_file.seek(0)
            json.dump(logs, log_file, indent=4)
    else:
        with open(LOG_FILE_NEW_USER, 'w') as log_file:
            json.dump([log_entry], log_file, indent=4)


def log_login_attempt(email, successo):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_data = {
        "Horario": timestamp,
        "email": email,
        "login": successo
    }
    if os.path.exists(LOG_FILE_LOGIN):
        if os.path.getsize(LOG_FILE_LOGIN) > 0:
            with open(LOG_FILE_LOGIN, 'r') as log_file:
                logs = json.load(log_file)
        else:
            logs = []
    else:
        logs = []
        
    logs.append(log_data)

    with open(LOG_FILE_LOGIN, 'w') as log_file:
        json.dump(logs, log_file, indent=4)
