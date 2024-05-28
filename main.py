from customtkinter import *
from tkinter import messagebox
from PIL import Image
from tkinter import StringVar
from tkinter.ttk import OptionMenu
import re
import os

from create_db import * # Banco de dados
from interface import * # Interface
from logs import * # Logs
from config import * # Configs da empresa
from function import * #Funções

current_user_email = None

# Função para realizar o login
def login_sucesso():
    email = email_entry.get()
    password = password_entry.get()
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        show_success_message()
        log_login_attempt(email, "Sucesso")  # Log de login bem-sucedido
    else:
        show_error_message()
        log_login_attempt(email, "Falha")  # Log de login mal-sucedido

def show_success_message():
    global current_user_email
    email = email_entry.get()
    current_user_email = email

    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute('SELECT company, coins FROM users WHERE email = ?', (email,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        company = user_data[0]
        coins = user_data[1]

        clear_frame()
        CTkLabel(master=frame, text="Bem vindo(a) !", text_color="#3d85c6", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        CTkLabel(master=frame, text="Confira abaixo seus dados", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))
        CTkLabel(master=frame, text=f"Seu email: {email}", text_color="#3d85c6", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", padx=(25, 40))
        CTkLabel(master=frame, text=f"Empresa: {company}", text_color="#3d85c6", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", padx=(25, 40))
        CTkLabel(master=frame, text=f"Coins: {coins}", text_color="#3d85c6", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", padx=(25, 40))
        CTkButton(master=frame, text="Transferir", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=show_transfer_screen).pack(anchor="w", padx=(25, 0), pady=(200, 0))
        CTkButton(master=frame, text="Sair", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=return_to_home_page).pack(anchor="w", padx=(25, 0), pady=(10, 0))

def show_transfer_screen():
    clear_frame()
    CTkLabel(master=frame, text="Transferência de Coins", text_color="#3d85c6", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Email do destinatário:", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    recipient_email_entry = CTkEntry(master=frame, width=225)
    recipient_email_entry.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="Valor a ser transferido:", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    amount_entry = CTkEntry(master=frame, width=225)
    amount_entry.pack(anchor="w", padx=(25, 0))

    def execute_transfer():
        global current_user_email
        sender_email = current_user_email
        recipient_email = recipient_email_entry.get()
        amount = amount_entry.get()

        if not amount.isdigit():
            CTkLabel(master=frame, text="Valor inválido. Por favor, insira um número.", text_color="red", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))
            return

        amount = int(amount)

        conn = sqlite3.connect('database.sql')
        cursor = conn.cursor()

        cursor.execute('SELECT coins FROM users WHERE email = ?', (sender_email,))
        sender_data = cursor.fetchone()

        cursor.execute('SELECT coins FROM users WHERE email = ?', (recipient_email,))
        recipient_data = cursor.fetchone()

        if not recipient_data:
            CTkLabel(master=frame, text="Email do destinatário não encontrado.", text_color="red", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))
            conn.close()
            return

        if sender_data and sender_data[0] >= amount:
            new_sender_coins = sender_data[0] - amount
            new_recipient_coins = recipient_data[0] + amount

            cursor.execute('UPDATE users SET coins = ? WHERE email = ?', (new_sender_coins, sender_email))
            cursor.execute('UPDATE users SET coins = ? WHERE email = ?', (new_recipient_coins, recipient_email))
            conn.commit()
            conn.close()

            CTkLabel(master=frame, text="Transferência bem sucedida!", text_color="green", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))
        else:
            CTkLabel(master=frame, text="Saldo insuficiente.", text_color="red", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))
            conn.close()

    CTkButton(master=frame, text="Transferir", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=execute_transfer).pack(anchor="w", padx=(25, 0), pady=(20, 0))
    CTkButton(master=frame, text="Voltar", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=show_success_message).pack(anchor="w", padx=(25, 0), pady=(10, 0))

# Função para mostrar uma mensagem de erro
def show_error_message():
    clear_frame()
    CTkLabel(master=frame, text="Erro: Email ou senha incorretos", text_color="#FF0000", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkButton(master=frame, text="Tentar Novamente", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=show_login_page).pack(anchor="w", padx=(25, 0), pady=(20, 0))

# Função para retornar ao inicio
def return_to_home_page():
    clear_frame()
    show_login_page()




# Função para mostrar a página de login
def show_login_page():
    clear_frame()
    CTkLabel(master=frame, text="Bem vindo(a) !", text_color="#3d85c6", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Faça login com sua conta", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    global email_entry
    global password_entry

    # Email
    CTkLabel(master=frame, text="  Email:", text_color="#3d85c6", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    email_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#3d85c6", border_width=1, text_color="#000000")
    email_entry.pack(anchor="w", padx=(25, 0))

    # Senha
    CTkLabel(master=frame, text="  Senha:", text_color="#3d85c6", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(20, 0), padx=(25, 0))
    password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#3d85c6", border_width=1, text_color="#000000", show="*")
    password_entry.pack(anchor="w", padx=(25, 0))

    # Botão Login
    CTkButton(master=frame, text="Login", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=login_sucesso).pack(anchor="w", padx=(25, 0), pady=(20, 0))

    # Botão Criar Conta
    CTkButton(master=frame, text="Criar Nova Conta", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=show_signup_page).pack(anchor="w", padx=(25, 0), pady=(20, 0))

# Função para salvar as informações de criação de conta no banco de dados
def save_new_account():
    name = signup_name_entry.get()
    email = signup_email_entry.get()
    password = signup_password_entry.get()
    company = selected_company.get()

    if not name or not email or not password or not company:
        messagebox.showwarning("Atenção", "Por favor, verifique se todos os campos foram preenchidos.")
        return

    valid_domains = VALID_EMAILS
    pattern = '|'.join(map(re.escape, valid_domains))
    if not re.search(pattern, email):
        messagebox.showwarning("Atenção", "Por favor, insira um email válido.")
        return

    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, password, company, coins) VALUES (?, ?, ?, ?, ?)', (name, email, password, company, COINS_INIT))
    conn.commit()
    conn.close()
    show_signup_success_message()
    log_event(name, email, company)

# Função para mostrar uma mensagem de sucesso ao criar conta
def show_signup_success_message():
    clear_frame()
    CTkLabel(master=frame, text="Conta criada com sucesso!", text_color="#3d85c6", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkButton(master=frame, text="Fazer Login", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=show_login_page).pack(anchor="w", padx=(25, 0), pady=(20, 0))

# Função para mostrar a página de criação de conta
def show_signup_page():
    clear_frame()
    CTkLabel(master=frame, text="Criar nova nonta", text_color="#3d85c6", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Preencha os campos abaixo", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    global signup_name_entry
    global signup_email_entry
    global signup_password_entry
    global selected_company  # Declarando como global

    # Nome
    CTkLabel(master=frame, text="  Nome:", text_color="#3d85c6", anchor="w", justify="left", font=("Arial Bold", 14)).pack(anchor="w", pady=(20, 0), padx=(25, 0))
    signup_name_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#3d85c6", border_width=1, text_color="#000000")
    signup_name_entry.pack(anchor="w", padx=(25, 0))

    # Email
    CTkLabel(master=frame, text="  Email:", text_color="#3d85c6", anchor="w", justify="left", font=("Arial Bold", 14)).pack(anchor="w", pady=(20, 0), padx=(25, 0))
    signup_email_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#3d85c6", border_width=1, text_color="#000000")
    signup_email_entry.pack(anchor="w", padx=(25, 0))

    # Senha
    CTkLabel(master=frame, text="  Senha:", text_color="#3d85c6", anchor="w", justify="left", font=("Arial Bold", 14)).pack(anchor="w", pady=(20, 0), padx=(25, 0))
    signup_password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#3d85c6", border_width=1, text_color="#000000", show="*")
    signup_password_entry.pack(anchor="w", padx=(25, 0))

    # Opções da Empresa
    CTkLabel(master=frame, text="  Empresa:", text_color="#3d85c6", anchor="w", justify="left", font=("Arial Bold", 14)).pack(anchor="w", pady=(20, 0), padx=(10, 0))
    selected_company = StringVar()
    selected_company.set(COMPANY_OPTIONS[0])  # Define o valor padrão
    OptionMenu(frame, selected_company, *COMPANY_OPTIONS).pack(anchor="w", padx=(25, 0))

    # Botão Criar Conta
    CTkButton(master=frame, text="Criar Conta", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=save_new_account).pack(anchor="w", padx=(25, 0), pady=(3, 0))
    CTkButton(master=frame, text="Voltar", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=show_login_page).pack(anchor="w", padx=(25, 0), pady=(3, 0))

    # Botão Fazer Login
    CTkButton(master=frame, text="Fazer Login", width=225, height=30, fg_color="#3d85c6", text_color="#FFFFFF", hover_color="#3d85c6", command=show_login_page).pack(anchor="w", padx=(25, 0), pady=(20, 0))

# Configuração do banco de dados
setup_database()

# Mostrar a página de login inicialmente
show_login_page()

app.mainloop()
