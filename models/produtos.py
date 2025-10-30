# models/produtos.py
from db.database import (
    add_product, 
    get_all_products, 
    get_product_list,
    update_product,
    delete_product,
    search_products
)

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
            # Chama a função de atualização
            update_product(self.id_produto, self.nome, self.descricao, self.preco, self.estoque)


    @staticmethod
    def get_all():
        """Retorna uma lista de todos os produtos do banco de dados."""
        return get_all_products()

    @staticmethod
    def get_list():
        """Retorna uma lista simplificada de produtos para vendas."""
        return get_product_list()

    @staticmethod
    def delete(id_produto):
        """Deleta um produto do banco de dados."""
        delete_product(id_produto)

    @staticmethod
    def search(search_term):
        """Busca produtos por nome ou descrição."""
        return search_products(search_term)

