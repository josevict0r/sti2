from pydantic import BaseModel


class ProgressoEstrutura(BaseModel):
    estrutura_id: int
    estrutura_nome: str
    total_exercicios: int
    concluidos: int
    pendentes: int
    concluido: bool
