import os
import psycopg2
from dotenv import load_dotenv

def drop_all_tables():

    load_dotenv()

    USER = os.getenv("user")
    PASSWORD = os.getenv("password").strip()
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    try:
        conn = psycopg2.connect(
            host=HOST,
            dbname=DBNAME,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        cursor = conn.cursor()

        # Desativa restrições de chave estrangeira temporariamente
        cursor.execute("SET session_replication_role = 'replica';")

        # Lista todas as tabelas do schema public
        cursor.execute("""
            SELECT tablename FROM pg_tables WHERE schemaname='public';
        """)
        tabelas = cursor.fetchall()

        for tabela in tabelas:
            nome_tabela = tabela[0]
            print(f"Excluindo tabela: {nome_tabela}")
            cursor.execute(f"DROP TABLE IF EXISTS {nome_tabela} CASCADE;")

        # Restaura as restrições de FK
        cursor.execute("SET session_replication_role = 'origin';")

        conn.commit()
        print("Todas as tabelas foram excluídas com sucesso!")

    except Exception as e:
        print(f"Erro ao apagar tabelas: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

# Executa
drop_all_tables()
