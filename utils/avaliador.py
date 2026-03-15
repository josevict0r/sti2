import re
import subprocess
import tempfile
import textwrap
from typing import Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Exercicio, CasoTeste, TentativaAluno, Aluno
# from pontuacao import update_pontuacao, calcular_pontuacao
from .pontuacao import update_pontuacao, calcular_pontuacao


def reformatar_codigo(codigo: str) -> str:
    codigo = re.sub(r'(class\s+\w+\s*:\s*)', r'\1\n    ', codigo)
    codigo = re.sub(r'(def\s+\w+\s*\([^\)]*\)\s*->\s*\w+\s*:)', r'\1\n        ', codigo)

    linhas = codigo.split('\n')
    linhas_formatadas = []
    for linha in linhas:
        if linha.strip().startswith("return") and not linha.startswith(" "):
            linha = "        " + linha
        linhas_formatadas.append(linha)

    return "\n".join(linhas_formatadas)


def detectar_metodo(codigo: str) -> str:
    match = re.search(r"def\s+(\w+)\s*\(", codigo)
    if match:
        return match.group(1)
    raise ValueError("Nenhum método encontrado no código.")


def executar_codigo(codigo_aluno: str, entrada: any) -> str:
    try:
        codigo_aluno = codigo_aluno.encode().decode('unicode_escape')
        metodo = detectar_metodo(codigo_aluno)

        if isinstance(entrada, tuple):
            entrada_para_funcao = ', '.join(repr(arg) for arg in entrada)
        else:
            entrada_para_funcao = repr(entrada)

        codigo_aluno = reformatar_codigo(codigo_aluno)
        codigo_execucao = f"""
from typing import *

{codigo_aluno}

if __name__ == "__main__":
    sol = Solution()
    resultado = sol.{metodo}({entrada_para_funcao})
    print(resultado)
"""

        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as temp_file:
            temp_file.write(textwrap.dedent(codigo_execucao))
            temp_file.flush()

            result = subprocess.run(
                ["python", temp_file.name],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip())

            return result.stdout.strip()

    except subprocess.TimeoutExpired:
        raise RuntimeError("Execução excedeu o tempo limite.")
    except Exception as e:
        raise RuntimeError(f"Erro durante execução: {e}")


def parse_entrada(entrada_str: str):
    try:
        return eval(entrada_str, {"__builtins__": {}})
    except Exception as e:
        raise ValueError(f"Erro ao interpretar a entrada: {e}")


def avaliar_tentativa(db: Session, exercicio_id: int, aluno_id: int, codigo_aluno: str) -> Tuple[bool, int]:
    print(f"Código do aluno recebido:\n{codigo_aluno}")

    exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado.")

    casos_teste = db.query(CasoTeste).filter(CasoTeste.exercicio_id == exercicio_id).all()
    if not casos_teste:
        raise HTTPException(status_code=404, detail="Nenhum caso de teste encontrado para este exercício.")

    try:
        passou_todos = True

        for caso in casos_teste:
            entrada = parse_entrada(caso.entrada)
            saida_obtida = executar_codigo(codigo_aluno, entrada)

            if str(saida_obtida).strip().lower() != str(caso.saida_esperada).strip().lower():
                passou_todos = False
                break

        tentativas_anteriores = db.query(TentativaAluno).filter(
            TentativaAluno.aluno_id == aluno_id,
            TentativaAluno.exercicio_id == exercicio_id
        ).count()

        pontos = 0
        if passou_todos: #and tentativas_anteriores == 0
            aluno = db.query(Aluno).get(aluno_id)
            update_pontuacao(db, aluno=aluno, exercicio=exercicio)
            pontos = calcular_pontuacao(exercicio)

        nova_tentativa = TentativaAluno(
            aluno_id=aluno_id,
            exercicio_id=exercicio_id,
            codigo_enviado=codigo_aluno,
            concluido=passou_todos
        )
        db.add(nova_tentativa)
        db.commit()

        return passou_todos, pontos

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na execução ou avaliação do código: {e}")


def pode_fazer_exercicio(db: Session, aluno_id: int, exercicio: Exercicio) -> bool:
    dependencias = exercicio.dependencias_origem
    if not dependencias:
        return True

    for dep in dependencias:
        tentativa = (
            db.query(TentativaAluno)
            .filter(
                TentativaAluno.aluno_id == aluno_id,
                TentativaAluno.exercicio_id == dep.exercicio_destino_id,
                TentativaAluno.concluido == True,
            )
            .first()
        )
        if not tentativa:
            return False
    return True
