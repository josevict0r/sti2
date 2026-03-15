import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password").strip()
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Conexão com Supabase (PostgreSQL)
conn = psycopg2.connect(
    host=HOST,
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    port=PORT
)

cursor = conn.cursor()

try:
    # Inserindo Categorias
    cursor.execute("""
        INSERT INTO estrutura_dado (nome, descricao) VALUES
        ('Array', 'Coleção linear de elementos armazenados em posições de memória contíguas, acessíveis por índice. Pode ser estático (tamanho fixo) ou dinâmico (tamanho variável).'),
        ('Linked List', 'Estrutura sequencial de elementos (nós) onde cada nó contém um dado e uma referência (ponteiro) para o próximo nó. Permite inserção e remoção eficiente.'),
        ('Queue', 'Estrutura de dados linear que segue o princípio FIFO (First-In, First-Out). Elementos são adicionados na "traseira" (enqueue) e removidos da "frente" (dequeue).'),
        ('Stack', 'Estrutura de dados linear que segue o princípio LIFO (Last-In, First-Out). Elementos são adicionados (push) e removidos (pop) do mesmo lado, o "topo".'),
        ('Graph', 'Conjunto de vértices (nós) e arestas que os conectam. Usado para modelar relações, como redes sociais ou mapas. Pode ser direcionado/não direcionado, ponderado/não ponderado.'),
        ('Binary Tree', 'Estrutura de dados hierárquica composta por nós, onde cada nó pai pode ter no máximo dois filhos: um filho esquerdo e um filho direito.'),
        ('Hash Table', 'Estrutura de dados que mapeia chaves para valores. Utiliza uma função de hash para calcular um índice em um array de "slots" ou "baldes", permitindo acesso muito rápido.');
    """)

    # Inserindo Operações
    cursor.execute("""
        INSERT INTO operacao (tipo, complexidade_esperada) VALUES
        ('Acesso por Índice em Array', 'O(1)'),
        ('Inserção no Final de Array Dinâmico', 'O(1) Amortizado'),
        ('Remoção no Final de Array Dinâmico', 'O(1) Amortizado'),
        ('Inserção no Início de Lista Encadeada', 'O(1)'),
        ('Busca Sequencial em Lista Encadeada', 'O(n)'),
        ('Remoção de Elemento em Lista Encadeada', 'O(n)'),
        ('Push (adicionar) em Pilha', 'O(1)'),
        ('Pop (remover) de Pilha', 'O(1)'),
        ('Peek (ver topo) de Pilha', 'O(1)'),
        ('Enqueue (adicionar) em Fila', 'O(1)'),
        ('Dequeue (remover) de Fila', 'O(1)'),
        ('Peek (ver frente) de Fila', 'O(1)'),
        ('Busca em Largura (BFS) em Grafo', 'O(V + E)'),
        ('Busca em Profundidade (DFS) em Grafo', 'O(V + E)'),
        ('Adicionar Aresta em Grafo (Lista de Adjacência)', 'O(1)'),
        ('Inserção em Árvore Binária de Busca (ABB)', 'O(log n) Médio, O(n) Pior Caso'),
        ('Busca em Árvore Binária de Busca (ABB)', 'O(log n) Médio, O(n) Pior Caso'),
        ('Remoção em Árvore Binária de Busca (ABB)', 'O(log n) Médio, O(n) Pior Caso'),
        ('Busca de Chave em Hash Table (Média)', 'O(1)'),
        ('Inserção de Chave-Valor em Hash Table (Média)', 'O(1)'),
        ('Trversal Inorder em Árvore Binária', 'O(n)');
    """)

    # Inserindo Complexidades
    cursor.execute("""
        INSERT INTO complexidade (tipo, valor_esperado) VALUES
        ('Tempo', 'O(1)'),
        ('Tempo', 'O(log n)'),
        ('Tempo', 'O(n)'),
        ('Tempo', 'O(n log n)'),
        ('Tempo', 'O(n^2)'),
        ('Tempo', 'O(2^n)'), 
        ('Tempo', 'O(n!)'),  
        ('Tempo', 'O(V + E)'),
        ('Espaço', 'O(1)'),
        ('Espaço', 'O(log n)'),
        ('Espaço', 'O(n)'),
        ('Espaço', 'O(V + E)'); 
    """)

    # Inserindo Feedbacks
    cursor.execute("""
        INSERT INTO feedback (texto, tipo_erro, sugestao_melhoria) VALUES
        ('Erro de sintaxe: verifique a indentação e a correspondência de parênteses/chaves.', 'Sintaxe', 'Revise a formatação do código e use um linter.'),
        ('Erro de lógica: a saída não corresponde ao esperado. O algoritmo não está processando os dados corretamente para todos os casos.', 'Lógica', 'Revise a lógica do algoritmo, faça testes de mesa e use um depurador.'),
        ('Problema de performance: a solução atual tem complexidade temporal ou espacial maior que a ideal para grandes entradas.', 'Performance', 'Considere algoritmos mais eficientes ou o uso de estruturas de dados otimizadas.'),
        ('Erro de tempo de execução: o programa travou, retornou uma exceção não tratada ou excedeu o limite de tempo/memória.', 'Execução', 'Verifique por loops infinitos, recursão excessiva, uso ineficiente de memória ou acesso a recursos inexistentes.'),
        ('Falta de tratamento de casos de borda: o código falha para entradas mínimas (e.g., lista vazia, único elemento) ou máximas.', 'Lógica', 'Adicione verificações e lógica específica para gerenciar casos extremos de entrada.'),
        ('Uso incorreto da API/biblioteca: a função foi chamada com parâmetros errados ou de forma inadequada.', 'Uso de API', 'Consulte a documentação da biblioteca para garantir o uso correto de funções e classes.'),
        ('Vazamento de memória: em linguagens com gerenciamento manual de memória, recursos não foram liberados.', 'Memória', 'Implemente a desalocação de memória ou use ferramentas de perfil para detectar vazamentos.');
    """)
    # Inserindo Erros Comuns
    cursor.execute("""
        INSERT INTO erro_comum (descricao, tipo) VALUES
        ('Loop infinito por condição de parada mal definida ou variável de controle não atualizada corretamente.', 'Lógica'),
        ('Tentativa de acessar um índice fora dos limites de um array, resultando em "IndexError" ou "ArrayIndexOutOfBoundsException".', 'Lógica'),
        ('Falta de tratamento para estruturas de dados vazias (e.g., pop em pilha vazia, dequeue em fila vazia), causando erros de tempo de execução.', 'Lógica'),
        ('Uso incorreto ou desalinhado de ponteiros/referências em listas encadeadas, resultando em nós perdidos ou loops na lista.', 'Lógica'),
        ('Condição de base ausente ou incorreta em funções recursivas, levando a "RecursionError" ou estouro de pilha.', 'Lógica'),
        ('Colisões em Hash Tables não tratadas adequadamente, degradando o desempenho da busca e inserção para O(n).', 'Performance'),
        ('Confundir as operações FIFO (Fila) e LIFO (Pilha), aplicando a lógica errada para a estrutura.', 'Lógica'),
        ('Não fechar recursos (arquivos, conexões de banco de dados) após o uso, causando vazamento de recursos.', 'Execução'),
        ('Modificar uma coleção enquanto a itera (concorremente), levando a resultados inesperados ou erros.', 'Lógica');
    """)

    # Inserindo Dependências entre Estruturas de Dados
    cursor.execute("""
        INSERT INTO dependencia_estrutura (estrutura_origem_id, estrutura_destino_id) VALUES
        (1, 2),  -- Array → Linked List
        (2, 3),  -- Linked List → Queue
        (3, 4),  -- Queue → Stack
        (4, 5),  -- Stack → Graph
        (5, 6),  -- Graph → Binary Tree
        (6, 7);  -- Binary Tree → Hash Table
    """)

    conn.commit()
    print("Carga base inicial + dependências inserida com sucesso!")

except Exception as e:
    print(f"Erro ao executar a carga base: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
