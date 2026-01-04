from app.app_settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from app import database_models

# 1. CARGA DE CONFIGURACIÓN
# Obtenemos las variables de entorno (User, Pass, DSN) validadas por Pydantic
settings = get_settings()

username = settings.ORACLE_DB_USERNAME
password = settings.ORACLE_DB_PASSWORD
dsn = settings.ORACLE_DB_DSN

# 2. CREACIÓN DEL MOTOR (ENGINE)
# Usamos el driver 'oracle+oracledb'. 
# Mejora 2.0: Añadimos 'pool_size' y 'max_overflow' para gestionar mejor las 
# conexiones simultáneas hacia Oracle Autonomous DB.
engine = create_engine(
    f"oracle+oracledb://{username}:{password}@{dsn}",
    pool_pre_ping=True,      # Verifica si la conexión sigue viva antes de usarla
    pool_size=3,             # Conexiones base mantenidas: 3 conexiones base
    max_overflow=5,         # Conexiones adicionales en caso de alta demanda: 5 extras (total 8)
    pool_recycle=1800        # Cierra conexiones inactivas cada 30 min para liberar recursos
    )

# 3. CONFIGURACIÓN DE SESIONES
# Creamos una fábrica de sesiones. 'autoflush=False' evita cambios accidentales
# antes de que nosotros decidamos hacer el commit.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. CREACIÓN DE TABLAS (forma manual, se reemplaza con Alambic)
# Esta línea busca todos los modelos definidos en 'database_models' y crea
# las tablas en Oracle si aún no existen
#database_models.Base.metadata.create_all(bind=engine)

# 5. GENERADOR DE SESIONES (Dependency Injection)
# Esta función será utilizada por FastAPI con 'Depends' para dar a cada 
# petición su propia conexión limpia a la base de datos.
def get_db():
    # Creamos una nueva sesión usando nuestra fábrica configurada
    db = SessionLocal()
    try:
        # 'yield' permite que FastAPI use la sesión y luego regrese aquí
        yield db
    finally:
        # Se cierra la conexión SIEMPRE, incluso si hubo un error en el endpoint,
        # para no agotar el pool de conexiones de Oracle Cloud.
        db.close()