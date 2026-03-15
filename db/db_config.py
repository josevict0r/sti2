from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Date, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base

import os

def get_connection():
    load_dotenv()

    USER = os.getenv("user")
    PASSWORD = os.getenv("password").strip()
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    return USER, PASSWORD, HOST, PORT, DBNAME

USER, PASSWORD, HOST, PORT, DBNAME = get_connection()

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


engine = create_engine(DATABASE_URL)


try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

# Criando a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Dependência para obter uma sessão DB em cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

