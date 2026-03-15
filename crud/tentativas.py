from sqlalchemy.orm import Session
from models import TentativaAluno
from schemas import TentativaCreate


def create_tentativa(db: Session, tentativa: TentativaCreate):
    db_tentativa = TentativaAluno(**tentativa.dict())
    db.add(db_tentativa)
    db.commit()
    db.refresh(db_tentativa)
    return db_tentativa


def get_tentativas(db: Session):
    return db.query(TentativaAluno).all()


def get_tentativa(db: Session, tentativa_id: int):
    return db.query(TentativaAluno).filter(TentativaAluno.id == tentativa_id).first()


def delete_tentativa(db: Session, tentativa_id: int):
    tentativa = get_tentativa(db, tentativa_id)
    if tentativa:
        db.delete(tentativa)
        db.commit()
    return tentativa
