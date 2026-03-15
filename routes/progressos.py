from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db_config import get_db
from utils.progresso import listar_progresso_aluno
from utils.avaliador import avaliar_tentativa
from models import TentativaAluno

router = APIRouter(prefix="/progresso", tags=["Progresso"])


@router.get("/{aluno_id}")
def get_progresso(aluno_id: int, db: Session = Depends(get_db)):
    return listar_progresso_aluno(db, aluno_id)
