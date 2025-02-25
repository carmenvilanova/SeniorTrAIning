import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Crear la tabla de usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único y autoincremental
    username TEXT NOT NULL,               -- Nombre de usuario (puede repetirse)
    password TEXT NOT NULL                 -- Contraseña del usuario
)
''')

# Insertar un usuario de prueba (si no existe)
cursor.execute('''
INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
''', ('prueba', '12345'))

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos creada y usuario de prueba insertado.")