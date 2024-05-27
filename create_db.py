import sqlite3

# Função para conectar-se ao banco de dados e criar a tabela de usuários
def setup_database():
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            company TEXT,
            coins INTEGER DEFAULT 1000  -- Definindo o valor padrão como 1000
        )
    ''')
    conn.commit()
    conn.close()