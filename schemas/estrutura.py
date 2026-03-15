from typing import Optional
from pydantic import BaseModel


class EstruturaDeDadoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None


class EstruturaDeDadoCreate(EstruturaDeDadoBase):
    pass


class EstruturaDeDado(EstruturaDeDadoBase):
    id: int

    class Config:
        from_attributes = True
