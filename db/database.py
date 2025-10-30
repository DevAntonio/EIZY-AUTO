# db/database.py
import sqlite3
import hashlib
import os
from datetime import date

# Define o caminho do banco de dados na raiz do projeto
DATABASE_FILE = "eizy_auto.db"

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inicializa o banco de dados, criando as tabelas e inserindo o
    vendedor padrão, se ainda não existirem.
    """
    if not os.path.exists(DATABASE_FILE):
        print("Criando banco de dados...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # --- Criação das Tabelas ---
    # Tabela de Vendedores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendedor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )""")

    # Tabela de Produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produto (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL,
        data_criacao DATE NOT NULL
    )""")

    # Tabela de Vendas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venda (
        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_nome TEXT,
        valor_total REAL NOT NULL,
        status BOOLEAN NOT NULL,
        data_venda DATE NOT NULL
    )""")

    # Tabela de Itens da Venda (tabela de junção)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venda_item (
        id_venda_item INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venda INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        vendedor_email TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (id_venda) REFERENCES venda (id_venda),
        FOREIGN KEY (id_produto) REFERENCES produto (id_produto)
    )""")


    # --- Inserir vendedor padrão ---
    cursor.execute("SELECT email FROM vendedor WHERE email = ?", ('vendedor@gmail.com',))
    if cursor.fetchone() is None:
        email = 'vendedor@gmail.com'
        senha_hash = hashlib.sha256('vendedor24865'.encode()).hexdigest()
        cursor.execute("INSERT INTO vendedor (email, senha) VALUES (?, ?)", (email, senha_hash))
        print(f"Vendedor padrão '{email}' inserido com sucesso.")

    conn.commit()
    conn.close()

def check_credentials(email, password):
    """Verifica se o e-mail e a senha correspondem a um vendedor no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM vendedor WHERE email = ? AND senha = ?", (email, password_hash))
    vendedor = cursor.fetchone()
    conn.close()
    return vendedor is not None

# --- Funções de Produto ---
def add_product(nome, descricao, preco, estoque):
    """Adiciona um novo produto ao banco de dados."""
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO produto (nome, descricao, preco, estoque, data_criacao) VALUES (?, ?, ?, ?, ?)",
            (nome, descricao, preco, estoque, date.today())
        )
        conn.commit()
    finally:
        conn.close()

def get_all_products():
    """Retorna todos os produtos do banco de dados."""
    conn = get_db_connection()
    products = conn.execute("SELECT id_produto, nome, descricao, preco, estoque FROM produto ORDER BY nome").fetchall()
    conn.close()
    return products

def get_product_list():
    """Retorna uma lista de produtos (id, nome, preco) para dropdowns."""
    conn = get_db_connection()
    # Garante que produtos sem estoque não apareçam na lista de vendas
    products = conn.execute("SELECT id_produto, nome, preco, estoque FROM produto WHERE estoque > 0 ORDER BY nome").fetchall()
    conn.close()
    return products

def update_product(id_produto, nome, descricao, preco, estoque):
    """Atualiza um produto existente no banco de dados."""
    conn = get_db_connection()
    try:
        conn.execute(
            """UPDATE produto 
               SET nome = ?, descricao = ?, preco = ?, estoque = ?
               WHERE id_produto = ?""",
            (nome, descricao, preco, estoque, id_produto)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar produto: {e}")
    finally:
        conn.close()

def delete_product(id_produto):
    """Deleta um produto do banco de dados."""
    conn = get_db_connection()
    try:
        # Futuramente, verificar se o produto está em alguma venda antes de deletar
        conn.execute("DELETE FROM produto WHERE id_produto = ?", (id_produto,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao deletar produto: {e}")
    finally:
        conn.close()

def search_products(search_term):
    """Busca produtos por nome ou descrição."""
    conn = get_db_connection()
    query = f"%{search_term}%"
    products = conn.execute(
        "SELECT id_produto, nome, descricao, preco, estoque FROM produto WHERE nome LIKE ? OR descricao LIKE ? ORDER BY nome", 
        (query, query)
    ).fetchall()
    conn.close()
    return products


# --- Funções de Venda ---
def add_sale(cliente_nome, valor_total, items):
    """Adiciona uma nova venda e seus itens ao banco de dados."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Verifica o estoque antes de iniciar a transação
        for item in items:
            cursor.execute("SELECT estoque FROM produto WHERE id_produto = ?", (item['id_produto'],))
            result = cursor.fetchone()
            if result is None or result['estoque'] < item['quantidade']:
                # Se o produto não existe ou não tem estoque, cancela
                raise sqlite3.Error(f"Estoque insuficiente para o produto ID {item['id_produto']}.")

        # Insere a venda
        cursor.execute(
            "INSERT INTO venda (cliente_nome, valor_total, status, data_venda) VALUES (?, ?, ?, ?)",
            (cliente_nome, valor_total, True, date.today())
        )
        id_venda = cursor.lastrowid

        # Insere os itens da venda e atualiza o estoque
        for item in items:
            cursor.execute(
                """INSERT INTO venda_item (id_venda, id_produto, vendedor_email, quantidade, preco_unitario, subtotal)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (id_venda, item['id_produto'], 'vendedor@gmail.com', item['quantidade'], item['preco_unitario'], item['subtotal'])
            )
            # Atualiza o estoque do produto
            cursor.execute("UPDATE produto SET estoque = estoque - ? WHERE id_produto = ?", (item['quantidade'], item['id_produto']))

        conn.commit()
        return True # Indica sucesso
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Erro ao adicionar venda: {e}")
        return False # Indica falha
    finally:
        conn.close()

def get_all_sales():
    """Retorna um resumo de todos os itens de venda para exibição."""
    conn = get_db_connection()
    query = """
    SELECT
        v.data_venda,
        p.nome,
        vi.quantidade,
        vi.subtotal
    FROM venda v
    JOIN venda_item vi ON v.id_venda = vi.id_venda
    JOIN produto p ON vi.id_produto = p.id_produto
    ORDER BY v.data_venda DESC, v.id_venda DESC
    """
    sales = conn.execute(query).fetchall()
    conn.close()
    return sales

# --- Funções de Contagem (Dashboard) ---

def get_total_products_count():
    """Retorna o número total de produtos cadastrados."""
    conn = get_db_connection()
    try:
        count = conn.execute("SELECT COUNT(*) FROM produto").fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"Erro ao contar produtos: {e}")
        return 0
    finally:
        conn.close()

def get_total_sales_count():
    """Retorna o número total de vendas (itens de venda) registradas."""
    conn = get_db_connection()
    try:
        # Isso conta o total de itens vendidos, não o número de vendas únicas
        count = conn.execute("SELECT COUNT(*) FROM venda_item").fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"Erro ao contar vendas: {e}")
        return 0
    finally:
        conn.close()

