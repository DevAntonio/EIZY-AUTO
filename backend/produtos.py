from db.db import get_db_connection

class Produto:
    @staticmethod
    def criar(nome, preco, estoque, descricao=''):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO produtos (nome, descricao, preco, estoque) VALUES (?, ?, ?, ?)',
            (nome, descricao, preco, estoque)
        )
        produto_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return produto_id

    @staticmethod
    def buscar_todos():
        conn = get_db_connection()
        produtos = conn.execute('SELECT * FROM produtos').fetchall()
        conn.close()
        return [dict(produto) for produto in produtos]

    @staticmethod
    def buscar_por_id(produto_id):
        conn = get_db_connection()
        produto = conn.execute(
            'SELECT * FROM produtos WHERE id = ?', (produto_id,)
        ).fetchone()
        conn.close()
        return dict(produto) if produto else None

    @staticmethod
    def atualizar(produto_id, **campos):
        if not campos:
            return False
            
        set_clause = ', '.join(f"{k} = ?" for k in campos.keys())
        valores = list(campos.values())
        valores.append(produto_id)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            f'UPDATE produtos SET {set_clause} WHERE id = ?',
            valores
        )
        alterados = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return alterados

    @staticmethod
    def deletar(produto_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        removidos = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return removidos

    @staticmethod
    def atualizar_estoque(produto_id, quantidade):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE produtos SET estoque = estoque + ? WHERE id = ?',
            (quantidade, produto_id)
        )
        alterados = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return alterados