from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db.db_config import get_db
from models import TentativaAluno, Exercicio, Aluno
from utils.avaliador import avaliar_tentativa
from utils.pontuacao import update_pontuacao, calcular_pontuacao

router = APIRouter(prefix="/tentativas", tags=["Tentativas"])


@router.post("/avaliar")
def avaliar_tentativa_manual(
    aluno_id: int = Body(...),
    exercicio_id: int = Body(...),
    codigo: str = Body(...),
    db: Session = Depends(get_db)
):
    """
    Avalia o código do aluno e atualiza a pontuação se for a primeira tentativa correta.
    """
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
    if exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    passou, pontos = avaliar_tentativa(db, exercicio_id, aluno_id, codigo)

    return {
        "aluno_id": aluno_id,
        "exercicio_id": exercicio_id,
        "passou_testes": passou,
        "pontos_ganhos": pontos,
        "pontuacao_total": aluno.pontuacao_total or 0
    }


@router.get("/{aluno_id}")
def listar_tentativas(aluno_id: int, db: Session = Depends(get_db)):
    tentativas = db.query(TentativaAluno).filter(TentativaAluno.aluno_id == aluno_id).all()
    return tentativas



# POST /tentativas/avaliar
# {
#   "aluno_id": 1,
#   "exercicio_id": 5,
#   "codigo": "class Solution:\n    def soma(self, a, b):\n        return a + b"
# }
