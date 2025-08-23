from datetime import datetime
from db.db import get_db_connection

class Venda:
    @staticmethod
    def criar(cliente_nome, cliente_documento=None, itens=None):
        if not itens:
            return None

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Calcula o total da venda
            total = sum(item['quantidade'] * item['preco_unitario'] for item in itens)

            # Cria a venda
            cursor.execute(
                'INSERT INTO vendas (cliente_nome, cliente_documento, valor_total) VALUES (?, ?, ?)',
                (cliente_nome, cliente_documento, total)
            )
            venda_id = cursor.lastrowid

            # Adiciona os itens da venda
            for item in itens:
                cursor.execute('''
                    INSERT INTO itens_venda 
                    (venda_id, produto_id, quantidade, preco_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    venda_id,
                    item['produto_id'],
                    item['quantidade'],
                    item['preco_unitario'],
                    item['quantidade'] * item['preco_unitario']
                ))

                # Atualiza o estoque
                cursor.execute(
                    'UPDATE produtos SET estoque = estoque - ? WHERE id = ?',
                    (item['quantidade'], item['produto_id'])
                )

            conn.commit()
            return venda_id

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def buscar_todas():
        conn = get_db_connection()
        vendas = conn.execute('''
            SELECT v.*, 
                   GROUP_CONCAT(p.nome || ' (' || iv.quantidade || 'x R$' || iv.preco_unitario || ')') as itens
            FROM vendas v
            LEFT JOIN itens_venda iv ON v.id = iv.venda_id
            LEFT JOIN produtos p ON iv.produto_id = p.id
            GROUP BY v.id
            ORDER BY v.data_venda DESC
        ''').fetchall()
        conn.close()
        return [dict(venda) for venda in vendas]

    @staticmethod
    def buscar_por_id(venda_id):
        conn = get_db_connection()
        venda = conn.execute('SELECT * FROM vendas WHERE id = ?', (venda_id,)).fetchone()
        if venda:
            itens = conn.execute('''
                SELECT iv.*, p.nome as produto_nome 
                FROM itens_venda iv
                JOIN produtos p ON iv.produto_id = p.id
                WHERE iv.venda_id = ?
            ''', (venda_id,)).fetchall()
            venda = dict(venda)
            venda['itens'] = [dict(item) for item in itens]
        conn.close()
        return venda

    @staticmethod
    def atualizar_status(venda_id, status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE vendas SET status = ? WHERE id = ?',
            (status, venda_id)
        )
        alterados = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return alterados