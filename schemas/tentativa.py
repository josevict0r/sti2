from typing import Optional

from pydantic import BaseModel


class TentativaBase(BaseModel):
    codigo_submetido: str
    resultado: Optional[str]
    tempo_gasto: Optional[int]
    aluno_id: int
    exercicio_id: int
    concluido : bool
    # Campos para a solução gerada pela LLM
    resolucao_llm: str
    resultado_execucao_llm: Optional[str] # Opcional, pois pode não haver resultado de execução da LLM
    pontuacao_minima: Optional[int] = 0

    class Config:
        from_attributes = True

class TentativaCreate(TentativaBase):
    pass


class Tentativa(TentativaBase):
    id: int
    class Config:
        from_attributes = True