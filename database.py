from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


DB_HOST = "localhost"
DB_PORT = 3306
DB_USERNAME = "root"
DB_PASSWORD = "Bibha23#@"
DB_NAME = "fastapi_learning"

DATABASE_URL = URL.create(
    "mysql+pymysql",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()