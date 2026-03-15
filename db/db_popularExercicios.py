import os
import json
import psycopg2
import re
from dotenv import load_dotenv

load_dotenv()

FOLDER = "./exercicios"

conn = psycopg2.connect(
    host=os.getenv("host"),
    dbname=os.getenv("dbname"),
    user=os.getenv("user"),
    password=os.getenv("password").strip(),
    port=os.getenv("port")
)
cursor = conn.cursor()


def extrair_casos_teste(texto):
    exemplos = re.findall(
        r'Example \d+:\s*\n\nInput:\s*(.*?)\n\nOutput:\s*(.*?)(?:\n|$)',
        texto,
        re.DOTALL
    )
    casos_teste = []
    for entrada, saida in exemplos:
        casos_teste.append({
            "entrada": entrada.strip(),
            "saida": saida.strip()
        })
    return casos_teste


def extrair_dados(texto):
    linhas = texto.strip().split('\n')
    nome = linhas[0].strip() if len(linhas) >= 1 else "Sem Nome"
    nivel_dificuldade = linhas[1].strip() if len(linhas) >= 2 else "Sem dificuldade"
    estrutura_id = linhas[2].strip() if len(linhas) >= 3 else "Sem estrutura"
    estrutura_id = int(estrutura_id) if estrutura_id.isdigit() else None
    

    enunciado_match = re.search(r'(?:\n\n)(.*?)(?:\n\nExample)', texto, re.DOTALL)
    enunciado = enunciado_match.group(1).strip() if enunciado_match else ""

    # Complexidades
    tempo_match = re.search(r'Recommended Time.*?O\([^)]+\)', texto)
    espaco_match = re.search(r'Recommended Space.*?O\([^)]+\)', texto)

    tempo = tempo_match.group(0).split()[-1] if tempo_match else None
    espaco = espaco_match.group(0).split()[-1] if espaco_match else None

    codigo_match = re.search(r'(class .*?:.*)', texto, re.DOTALL)
    solucao = codigo_match.group(1).strip() if codigo_match else None

    hints = re.findall(r'Hint \d+\n\n(.*?)(?=\n\n|$)', texto, re.DOTALL)

    casos_teste = extrair_casos_teste(texto)

    return {
        "nome": nome,
        "nivel_dificuldade": nivel_dificuldade,
        "enunciado": enunciado,
        "estrutura_id": estrutura_id,
        "tempo_ideal": tempo,
        "espaco_ideal": espaco,
        "solucao_ideal": solucao,
        "dicas": hints,
        "casos_teste": casos_teste
    }


def processar_txts():
    dados = []
    for arquivo in os.listdir(FOLDER):
        if arquivo.endswith(".txt"):
            caminho = os.path.join(FOLDER, arquivo)
            with open(caminho, 'r', encoding='utf-8') as file:
                conteudo = file.read()
                #print(conteudo)
                dados.append(extrair_dados(conteudo))
    return dados


def inserir_no_banco(lista_exercicios):
    for ex in lista_exercicios:
        try:
            cursor.execute("""
                INSERT INTO exercicio (enunciado, nivel_dificuldade, solucao_esperada, estrutura_id, tempo_ideal, espaco_ideal)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                ex["enunciado"],
                ex["nivel_dificuldade"],
                ex["solucao_esperada"],
                ex["estrutura_id"],
                ex["tempo_ideal"],
                ex["espaco_ideal"]
            ))
            exercicio_id = cursor.fetchone()[0]
            
            # Inserindo casos de teste
            for ct in ex["casos_teste"]:
                cursor.execute("""
                    INSERT INTO caso_teste (entrada, saida_esperada, exercicio_id)
                    VALUES (%s, %s, %s)
                """, (
                    ct["entrada"],
                    ct["saida"],
                    exercicio_id
                ))

            # Inserindo dicas
            for dica in ex["dicas"]:
                cursor.execute("""
                    INSERT INTO dicas (texto, exercicio_id)
                    VALUES (%s, %s)
                """, (
                    dica.strip(),
                    exercicio_id
                ))

            conn.commit()
            print(f"Exercício '{ex['nome']}' inserido com sucesso!")

        except Exception as e:
            print(f"Erro ao inserir exercício {ex['nome']}: {e}")
            conn.rollback()


if __name__ == "__main__":
    print("Processando arquivos .txt...")
    dados = processar_txts()
    #print(dados)
    print(f"{len(dados)} exercícios encontrados. Inserindo no banco...")
    with open("exercicios_extraidos.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    inserir_no_banco(dados)

    cursor.close()
    conn.close()
    print("Processo finalizado.")
