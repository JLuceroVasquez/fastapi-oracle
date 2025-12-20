from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. DEFINICIÓN DE LA CLASE DE CONFIGURACIÓN
# Heredar de BaseSettings permite que Pydantic lea automáticamente
# variables de entorno o archivos .env y las valide.
class Settings(BaseSettings):

    # Definimos las variables que nuestra aplicación necesita.
    # Al ponerles el tipo (: str), Pydantic validará que existan
    # y que sean cadenas de texto. Si falta alguna en el .env, 
    # la app lanzará un error claro al intentar arrancar.
    ORACLE_DB_USERNAME : str 
    ORACLE_DB_PASSWORD: str
    ORACLE_DB_DSN: str

    # 2. CONFIGURACIÓN DEL ORIGEN DE DATOS
    # Indicamos que debe buscar estas variables en un archivo llamado ".env"
    model_config = SettingsConfigDict(env_file=".env")

# 3. OPTIMIZACIÓN CON CACHÉ (lru_cache)
# Leer un archivo .env del disco en cada petición sería lento.
# @lru_cache hace que la primera vez que llamemos a get_settings(), 
# el resultado se guarde en memoria (caché).
@lru_cache
def get_settings():
    return Settings()