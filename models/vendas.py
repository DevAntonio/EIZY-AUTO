# models/vendas.py
from db.database import add_sale, get_all_sales

class Venda:
    def __init__(self, cliente_nome, valor_total, items, id_venda=None):
        self.id_venda = id_venda
        self.cliente_nome = cliente_nome
        self.valor_total = valor_total
        self.items = items # Lista de dicionários de itens

    @staticmethod
    def create(cliente_nome, valor_total, items):
        """
        Registra uma nova venda no banco de dados.
        Retorna True se sucesso, False se falhar (ex: estoque).
        """
        return add_sale(cliente_nome, valor_total, items)

    @staticmethod
    def get_all():
        """Retorna um resumo de todos os itens de venda."""
        return get_all_sales()

