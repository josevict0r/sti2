def calcular_pontuacao(exercicio):
    """
    Retorna a pontuação com base no nível de dificuldade.
    Suporta nomes em português e inglês.
    """
    nivel = exercicio.nivel_dificuldade.strip().lower()

    map_niveis = {
        "facil": 10,
        "easy": 10,
        "medio": 20,
        "médio": 20,
        "medium": 20,
        "dificil": 30,
        "difícil": 30,
        "hard": 30
    }

    return map_niveis.get(nivel, 10)


def update_pontuacao(db, aluno, exercicio):
    """
    Atualiza a pontuação do aluno ao concluir um exercício.
    """
    pontos = calcular_pontuacao(exercicio)

    if aluno.pontuacao_total is None:
        aluno.pontuacao_total = 0

    aluno.pontuacao_total += pontos
    db.flush()
    db.commit()
