from sqlalchemy.orm import Session
from models import TentativaAluno, Exercicio, EstruturaDeDado


def calcular_progresso_estrutura(db: Session, aluno_id: int, estrutura_id: int):
    total = db.query(Exercicio).filter(Exercicio.estrutura_id == estrutura_id).count()
    concluidos = (
        db.query(TentativaAluno)
        .filter(
            TentativaAluno.aluno_id == aluno_id,
            TentativaAluno.exercicio.has(estrutura_id=estrutura_id),
            TentativaAluno.concluido == True,
        )
        .count()
    )
    pendentes = total - concluidos

    return {
        "estrutura_id": estrutura_id,
        "total_exercicios": total,
        "concluidos": concluidos,
        "pendentes": pendentes,
        "concluido": pendentes == 0,
    }


def listar_progresso_aluno(db: Session, aluno_id: int):
    estruturas = db.query(EstruturaDeDado).all()
    progresso = []
    for estrutura in estruturas:
        progresso.append(
            calcular_progresso_estrutura(db, aluno_id, estrutura.id)
        )
    return progresso
