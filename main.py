from unittest.mock import Base
from fastapi import FastAPI
from routes import alunos, exercicios, progressos, tentativas
from db.db_config import engine, Base

# Criação das tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="STI de Estruturas de Dados", version="1.0")

# Registrar rotas
app.include_router(alunos.router)
app.include_router(exercicios.router)
app.include_router(progressos.router)
app.include_router(tentativas.router)


@app.get("/")
def read_root():
    return {"message": "STI rodando! Bora codar estrutura de dados"}
