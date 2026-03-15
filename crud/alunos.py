from sqlalchemy.orm import Session
from models import Aluno
from schemas.aluno import AlunoCreate


def create_aluno(db: Session, aluno: AlunoCreate):
    db_aluno = Aluno(**aluno.dict())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno


def get_alunos(db: Session):
    return db.query(Aluno).all()


def get_aluno(db: Session, aluno_id: int):
    return db.query(Aluno).filter(Aluno.id == aluno_id).first()


def delete_aluno(db: Session, aluno_id: int):
    aluno = get_aluno(db, aluno_id)
    if aluno:
        db.delete(aluno)
        db.commit()
    return aluno

def update_aluno(db: Session, aluno_id: int, aluno_data: AlunoCreate):
    aluno = get_aluno(db, aluno_id)
    if not aluno:
        return None
    for key, value in aluno_data.dict().items():
        setattr(aluno, key, value)
    db.commit()
    db.refresh(aluno)
    return aluno
