"""Configuración del proyecto. Los valores se leen de variables de entorno
y, si no existen, se usan los valores de desarrollo de abajo."""
import os

# Datos de conexión a MySQL (cámbialos por los tuyos)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', '3306'))
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'winnie')
DB_NAME = os.environ.get('DB_NAME', 'Impulso_mexa')

# Clave para firmar la sesión. En un proyecto real debe ser larga y secreta.
SECRET_KEY = os.environ.get('SECRET_KEY', 'Winnie@1718PigletP@choclo')
