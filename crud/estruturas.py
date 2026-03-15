from sqlalchemy.orm import Session
from models import EstruturaDeDado
from schemas import EstruturaCreate


def create_estrutura(db: Session, estrutura: EstruturaCreate):
    db_estrutura = EstruturaDeDado(**estrutura.dict())
    db.add(db_estrutura)
    db.commit()
    db.refresh(db_estrutura)
    return db_estrutura


def get_estruturas(db: Session):
    return db.query(EstruturaDeDado).all()


def get_estrutura(db: Session, estrutura_id: int):
    return db.query(EstruturaDeDado).filter(EstruturaDeDado.id == estrutura_id).first()


def delete_estrutura(db: Session, estrutura_id: int):
    estrutura = get_estrutura(db, estrutura_id)
    if estrutura:
        db.delete(estrutura)
        db.commit()
    return estrutura
