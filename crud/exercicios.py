from sqlalchemy.orm import Session
from models import CasoTeste, Dicas, Exercicio, DependenciaExercicio
from models import DependenciaEstrutura
from schemas.exercicio import ExercicioCreate


def get_exercicio(db: Session, exercicio_id: int):
    return db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()


def get_dependencias_exercicio(db: Session, exercicio_id: int):
    return db.query(DependenciaExercicio).filter(
        DependenciaExercicio.exercicio_destino_id == exercicio_id
    ).all()


def get_dependencias_estrutura(db: Session, exercicio_id: int):
    exercicio = get_exercicio(db, exercicio_id)
    if exercicio is None:
        return []

    dependencias = db.query(DependenciaEstrutura).filter(
        DependenciaEstrutura.estrutura_origem_id == exercicio.estrutura_id
    ).all()

    return dependencias


def create_exercicio(db: Session, exercicio: ExercicioCreate):
    novo_exercicio = Exercicio(
        enunciado=exercicio.enunciado,
        nivel_dificuldade=exercicio.nivel_dificuldade,
        solucao_esperada=exercicio.solucao_esperada,
        estrutura_id=exercicio.estrutura_id,
        tempo_ideal=exercicio.tempo_ideal,
        espaco_ideal=exercicio.espaco_ideal
    )
    db.add(novo_exercicio)
    db.commit()
    db.refresh(novo_exercicio)

    # Inserindo dicas
    for dica in exercicio.dicas:
        dica_obj = Dicas(
            conteudo=dica,
            exercicio_id=novo_exercicio.id
        )
        db.add(dica_obj)

    # Inserindo casos de teste
    for caso in exercicio.casos_teste:
        caso_obj = CasoTeste(
            entrada=caso.entrada,
            saida_esperada=caso.saida_esperada,
            exercicio_id=novo_exercicio.id
        )
        db.add(caso_obj)

    db.commit()
    return novo_exercicio

#get all exercicios
def get_exercicios(db: Session):
    return db.query(Exercicio).all()