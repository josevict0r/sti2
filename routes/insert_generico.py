from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from db import get_connection

router = APIRouter()

@router.post("/insert/{tabela}/")
def insert_generico(tabela: str, payload: Dict[str, Any]):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Monta os campos e placeholders
        colunas = ', '.join(payload.keys())
        valores = tuple(payload.values())
        placeholders = ', '.join(['%s'] * len(payload))

        # Query dinâmica
        query = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"

        cursor.execute(query, valores)
        conn.commit()

        return {"status": f"Insert realizado com sucesso na tabela {tabela}."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
