import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Crear la tabla de usuarios con más información
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    birth_date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos creada correctamente.")
