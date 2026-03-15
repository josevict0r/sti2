import os
import google.genai as genai
from google.genai import types
import re
from sqlalchemy.orm import Session
from db.db_config import get_db
from models import Exercicio, CasoTeste
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key do Google não encontrada. Verifique seu arquivo .env")

client= genai.Client(api_key=api_key)

def gerar_codigo(exercicio_id: int):
    db: Session = next(get_db())

    try:
        exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
        if not exercicio:
            raise ValueError(f"Exercício com id {exercicio_id} não encontrado.")

        casos = db.query(CasoTeste).filter(CasoTeste.exercicio_id == exercicio_id).all()
        casos_texto = "\n".join([f"Input: {c.entrada}\nExpected Output: {c.saida_esperada}" for c in casos])

        prompt = f"""
Você é um solucionador de problemas especialista em Python.
Escreva uma função em Python que resolva o seguinte problema:

{exercicio.enunciado}

A função deve se chamar 'solucao'.

A função deve passar nos seguintes casos de teste. Inclua a função e chamadas print() para os testes.

{casos_texto}

Escreva apenas o código Python dentro de um bloco de código markdown. Não adicione nenhuma explicação fora do bloco de código.
"""


        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=types.Part.from_text(text=prompt))
        
        

        full_text_response_content = ""
        codigo_gerado = None
        output_execucao = None # Still likely None as CodeExecutionTool is commented out

        # Iterate through all parts to reconstruct the full text and find code blocks
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'text'): # Check if the part has a 'text' attribute
                full_text_response_content += part.text
            # You can also keep your original logic if you expect executable_code parts
            if hasattr(part, 'executable_code') and part.executable_code:
                 # This might capture it if the model specifically formats it this way
                 # However, regex from full_text_response_content is more reliable for markdown
                 pass # We'll rely on regex for code extraction below

        # Use regex to extract code from the accumulated text content
        match = re.search(r"```python\n(.*?)```", full_text_response_content, re.DOTALL)

        if match:
            codigo_gerado = match.group(1).strip()

        if not codigo_gerado:
            raise ValueError(
                "Não foi possível gerar o código. "
                "Nenhum bloco de código Python em Markdown foi encontrado na resposta do LLM."
            )

        return {
            "codigo": codigo_gerado,
            "resultado_execucao": output_execucao
        }

    finally:
        db.close()