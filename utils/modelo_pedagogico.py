import os
import google.genai as genai
from google.genai import types
from sqlalchemy.orm import Session
from db.db_config import get_db
from models import Dicas, Exercicio, CasoTeste
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print(f"APIKEY ---------------------->{api_key}")

# Configurar a API key do Google GenAI
if not api_key:
    raise ValueError("API key do Google não encontrada. Verifique seu arquivo .env")
client = genai.Client(api_key=api_key)

# --- Função anterior (gerar_codigo) pode ser mantida aqui se desejar ---

def fornecer_feedback_aluno(exercicio_id: int, resposta_aluno: str) -> str:
    """
    Analisa a resposta de um aluno para um exercício, compara com a solução
    esperada e os casos de teste, e gera um feedback construtivo sem
    fornecer a resposta correta.

    Args:
        exercicio_id: O ID do exercício no banco de dados.
        resposta_aluno: O código Python enviado pelo aluno.

    Returns:
        Uma string contendo o feedback gerado pela IA.
    """
    db: Session = next(get_db())

    try:
        # 1. Buscar todos os dados necessários do banco
        exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
        if not exercicio:
            raise ValueError(f"Exercício com id {exercicio_id} não encontrado.")

        casos = db.query(CasoTeste).filter(CasoTeste.exercicio_id == exercicio_id).all()
        casos_texto = "\n".join([f"Input: {c.entrada} -> Saída Esperada: {c.saida_esperada}" for c in casos])
        dicas = db.query(Dicas).filter(Dicas.exercicio_id == exercicio_id).first()
        dicas_texto = dicas.conteudo if dicas else "Nenhuma dica disponível para este exercício."

        # 2. PROMPT ENGINEERING: A parte mais importante!
        # Damos ao modelo uma persona (tutor), o contexto completo (problema, solução, testes)
        # e regras muito estritas sobre como ele deve se comportar.
        prompt = f"""
            Você é um tutor de programação amigável e experiente. Seu objetivo é analisar a solução de um aluno para um problema de programação e fornecer dicas construtivas e feedback.

            **REGRA MAIS IMPORTANTE: NUNCA, SOB NENHUMA CIRCUNSTÂNCIA, FORNEÇA A SOLUÇÃO CORRETA OU TRECHOS DE CÓDIGO DA SOLUÇÃO CORRETA. O objetivo é guiar, não resolver.**

            Aqui estão as informações do exercício:

            ---
            **PROBLEMA (ENUNCIADO):**
            {exercicio.enunciado}
            ---
            **CASOS DE TESTE:**
            {casos_texto}
            ---
            **DICAS**
            {dicas_texto}
            **SOLUÇÃO IDEAL (PARA SUA REFERÊNCIA INTERNA - NÃO MOSTRE AO ALUNO):**
            ```python
            {exercicio.solucao_esperada}
                
            {resposta_aluno}

            SUA TAREFA:

            Analise a "RESPOSTA DO ALUNO" com base no "ENUNCIADO", "CASOS DE TESTE" e na "SOLUÇÃO IDEAL". Forneça um feedback em português que ajude o aluno a melhorar. Siga estas diretrizes:

                Se o código estiver correto: Elogie o aluno! Você pode sugerir uma pequena melhoria de estilo ou uma forma alternativa de pensar no problema, se for relevante. Ex: "Parabéns, sua solução está correta e passa em todos os testes! Uma outra forma de pensar nisso seria usando [conceito alternativo], mas sua abordagem está ótima."

                Se o código tiver um erro de lógica (quase certo): Não aponte o erro diretamente. Em vez disso, faça uma pergunta que o guie. Ex: "Você está no caminho certo usando um loop! Mas observe o que acontece com o seu código no caso de teste com a entrada [input que falha]. Será que sua condição de parada está correta para todos os casos?"

                Se a abordagem geral estiver errada: Traga o aluno de volta ao enunciado. Ex: "Sua abordagem é interessante, mas parece que você não está lidando com a parte do enunciado que pede para [requisito específico do problema]. Que tal reler o problema e pensar em qual estrutura de dados seria ideal para armazenar [tipo de dado]?"

                Se houver um erro de sintaxe: Aponte o tipo de erro de forma genérica. Ex: "Parece haver um pequeno erro de sintaxe perto da linha X. Lembre-se de como as estruturas de repetição (loops) são definidas em Python."

            Fale diretamente com o aluno de forma encorajadora. O foco é no aprendizado. De dicas que ajudem a entender o que pode estar errado, mas sem dar a resposta. Dicas técnicas são bem-vindas, mas evite jargões complexos. Use uma linguagem simples e acessível.
            """
        
        # 3. Chamar o modelo Gemini
        '''
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=types.Part.from_text(text=prompt))
        '''
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        
        return response.text
    
    finally:
        db.close() # Garante que a conexão com o banco seja sempre fechada