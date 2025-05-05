import os

# Directorio base donde se ubica este archivo de configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Definición del directorio que contendrá la base de datos (sube un nivel y busca la carpeta 'db')
DB_DIR = os.path.join(BASE_DIR, "..", "db")

# NOTA: SQLite creará el archivo 'database.db' si no existe, pero no creará la carpeta 'db'.
# En futuras implementaciones podrías incluir la siguiente línea para asegurarte de que exista:
# if not os.path.exists(DB_DIR):
#     os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, "database.db")

# Otras configuraciones de la aplicación
SECRET_KEY = "tu_clave_secreta_aqui"
DEBUG = True
APP_PORT = 5000

# Configuración específica para STL Tools
DEFAULT_SCALE_FACTOR = 1.0