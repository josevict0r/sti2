from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db_config import get_db
from models import Exercicio
from schemas import exercicio
from crud import  exercicios
from utils.avaliador import pode_fazer_exercicio

router = APIRouter(prefix="/exercicios", tags=["Exercícios"])

from typing import List

@router.post("/", response_model=exercicio.Exercicio)
def create(exercicio: exercicio.ExercicioCreate, db: Session = Depends(get_db)):
    try:
        return exercicios.create_exercicio(db=db, exercicio=exercicio)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/", response_model= List[exercicio.Exercicio])
def read(db: Session = Depends(get_db)):
    all_exercicios = exercicios.get_exercicios(db)
    print("Dados retornados por get_exercicios:", all_exercicios) 
    return all_exercicios 



@router.get("/{id}", response_model=exercicio.Exercicio)
def read_one(id: int, db: Session = Depends(get_db)):
    db_item = exercicios.get_exercicio(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return db_item


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    db_item = exercicios.delete_exercicio(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return {"ok": True}

@router.get("/disponiveis/{aluno_id}")
def listar_exercicios_disponiveis(aluno_id: int, db: Session = Depends(get_db)):
    exercicios = db.query(Exercicio).all()
    liberados = []

    for ex in exercicios:
        if pode_fazer_exercicio(db, aluno_id, ex):
            liberados.append({
                "id": ex.id,
                "enunciado": ex.enunciado,
                "estrutura": ex.estrutura.nome,
                "nivel": ex.nivel_dificuldade,
            })

    return liberados

