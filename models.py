from db.db_config import Base, get_db
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from dotenv import load_dotenv
import os

get_db()


class EstruturaDeDado(Base):
    __tablename__ = 'estrutura_dado'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(Text)
    exercicios = relationship("Exercicio", back_populates="estrutura")

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.db_config import Base


class Exercicio(Base):
    __tablename__ = 'exercicio'

    id = Column(Integer, primary_key=True)
    enunciado = Column(Text, nullable=False)
    nivel_dificuldade = Column(String)
    solucao_esperada = Column(Text)
    pontuacao_minima = Column(Integer, default=0) #new

    estrutura_id = Column(Integer, ForeignKey('estrutura_dado.id'))
    estrutura = relationship("EstruturaDeDado", back_populates="exercicios")

    tempo_ideal = Column(String, nullable=True)
    espaco_ideal = Column(String, nullable=True)

    # Dependências entre exercícios
    dependencias_origem = relationship(
        "DependenciaExercicio",
        back_populates="exercicio_origem",
        foreign_keys="DependenciaExercicio.exercicio_origem_id"
    )

    dependencias_destino = relationship(
        "DependenciaExercicio",
        back_populates="exercicio_destino",
        foreign_keys="DependenciaExercicio.exercicio_destino_id"
    )

    # Tentativas e Casos de Teste
    tentativas = relationship("TentativaAluno", back_populates="exercicio")
    casos_teste = relationship("CasoTeste", back_populates="exercicio")

    # Dicas
    dicas = relationship("Dicas", back_populates="exercicio")


class DependenciaExercicio(Base):
    __tablename__ = 'dependencia_exercicio'

    id = Column(Integer, primary_key=True)
    exercicio_origem_id = Column(Integer, ForeignKey('exercicio.id'))
    exercicio_destino_id = Column(Integer, ForeignKey('exercicio.id'))

    exercicio_origem = relationship(
        "Exercicio",
        back_populates="dependencias_origem",
        foreign_keys=[exercicio_origem_id]
    )

    exercicio_destino = relationship(
        "Exercicio",
        back_populates="dependencias_destino",
        foreign_keys=[exercicio_destino_id]
    )


class DependenciaEstrutura(Base):
    __tablename__ = 'dependencia_estrutura'

    id = Column(Integer, primary_key=True)
    estrutura_origem_id = Column(Integer, ForeignKey('estrutura_dado.id'))
    estrutura_destino_id = Column(Integer, ForeignKey('estrutura_dado.id'))

    estrutura_origem = relationship(
        "EstruturaDeDado",
        foreign_keys=[estrutura_origem_id]
    )

    estrutura_destino = relationship(
        "EstruturaDeDado",
        foreign_keys=[estrutura_destino_id]
    )



class CasoTeste(Base):
    __tablename__ = 'caso_teste'
    id = Column(Integer, primary_key=True)
    entrada = Column(Text, nullable=False)
    saida_esperada = Column(Text, nullable=False)
    exercicio_id = Column(Integer, ForeignKey('exercicio.id'))
    exercicio = relationship("Exercicio", back_populates="casos_teste")

class Aluno(Base):
    __tablename__ = 'aluno'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    nivel_conhecimento = Column(Integer, nullable=False, default=1)
    historico = relationship("HistoricoDesempenho", back_populates="aluno")
    tentativas = relationship("TentativaAluno", back_populates="aluno")
    pontuacao_total = Column(Integer, default=0)  #new 

class HistoricoDesempenho(Base):
    __tablename__ = 'historico_desempenho'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    aluno_id = Column(Integer, ForeignKey('aluno.id'))
    aluno = relationship("Aluno", back_populates="historico")

class TentativaAluno(Base):
    __tablename__ = 'tentativa_aluno'
    id = Column(Integer, primary_key=True)
    codigo_enviado = Column(Text)
    resultado = Column(String)
    tempo_gasto = Column(Integer)
    aluno_id = Column(Integer, ForeignKey('aluno.id'))
    exercicio_id = Column(Integer, ForeignKey('exercicio.id'))
    aluno = relationship("Aluno", back_populates="tentativas")
    exercicio = relationship("Exercicio", back_populates="tentativas")
    codigos = relationship("CodigoSubmetido", back_populates="tentativa")
    concluido = Column(Boolean, default=False)


class CodigoSubmetido(Base):
    __tablename__ = 'codigo_submetido'
    id = Column(Integer, primary_key=True)
    conteudo = Column(Text, nullable=False)
    tentativa_id = Column(Integer, ForeignKey('tentativa_aluno.id'))
    tentativa = relationship("TentativaAluno", back_populates="codigos")

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    texto = Column(Text)
    tipo_erro = Column(String)
    sugestao_melhoria = Column(Text)

class ErroComum(Base):
    __tablename__ = 'erro_comum'
    id = Column(Integer, primary_key=True)
    descricao = Column(Text)
    tipo = Column(String)

class Operacao(Base):
    __tablename__ = 'operacao'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    complexidade_esperada = Column(String)

class Complexidade(Base):
    __tablename__ = 'complexidade'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)  
    valor_esperado = Column(String)

class Dicas(Base):
    __tablename__ = 'dicas'
    id = Column(Integer, primary_key=True)
    conteudo = Column(Text, nullable=False)
    exercicio_id = Column(Integer, ForeignKey('exercicio.id'))
    exercicio = relationship("Exercicio", back_populates="dicas")

