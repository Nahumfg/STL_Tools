import os

# Configuración de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "database.db")

# Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_aqui"

# Configuración de la aplicación
DEBUG = True
APP_PORT = 5000

# Parámetros específicos de STL Tools
DEFAULT_SCALE_FACTOR = 1.0  # Valor por defecto para reescalar archivos STL