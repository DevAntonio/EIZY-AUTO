from db.database import add_sale, get_all_sales

class Venda:
    def __init__(self, cliente_nome, valor_total, items, id_venda=None):
        self.id_venda = id_venda
        self.cliente_nome = cliente_nome
        self.valor_total = valor_total
        # `items` é uma lista de dicionários, cada um representando um item da venda
        self.items = items

    def save(self):
        """Salva uma nova venda no banco de dados."""
        if self.id_venda is None:
            add_sale(self.cliente_nome, self.valor_total, self.items)
        else:
            # A lógica de atualização (UPDATE) pode ser adicionada aqui
            print("Função de atualização de venda não implementada.")

    @staticmethod
    def get_all():
        """Retorna uma lista de todos os itens de venda do banco de dados."""
        return get_all_sales()
