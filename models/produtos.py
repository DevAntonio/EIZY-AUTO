from db.database import add_product, get_all_products

class Produto:
    def __init__(self, nome, descricao, preco, estoque, id_produto=None):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque

    def save(self):
        """Salva um novo produto no banco de dados."""
        if self.id_produto is None:
            add_product(self.nome, self.descricao, self.preco, self.estoque)
        else:
            # A lógica de atualização (UPDATE) pode ser adicionada aqui
            print("Função de atualização de produto não implementada.")

    @staticmethod
    def get_all():
        """Retorna uma lista de todos os produtos do banco de dados."""
        return get_all_products()
