from pathlib import Path
from decouple import config  # Asegúrate de tener instalada la librería python-decouple

# Obtener el directorio base donde se ubica este archivo de configuración
BASE_DIR = Path(__file__).resolve().parent

# Definición del directorio que contendrá la base de datos (sube un nivel y busca la carpeta 'db')
DB_DIR = BASE_DIR.parent / "db"
DB_DIR.mkdir(exist_ok=True)  # Crea la carpeta 'db' si no existe

# Ruta completa hacia la base de datos SQLite
DB_PATH = DB_DIR / "database.db"

# Otras configuraciones de la aplicación
SECRET_KEY = config('SECRET_KEY', default="tu_clave_secreta_aqui")
DEBUG = config('DEBUG', default=True, cast=bool)
APP_PORT = config('APP_PORT', default=5000, cast=int)

# Configuración específica para STL Tools
DEFAULT_SCALE_FACTOR = config('DEFAULT_SCALE_FACTOR', default=1.0, cast=float)