import tkinter as tk
from tkinter import ttk, messagebox
from models.produtos import Produto

class ProdutosPage(tk.Frame):
    def __init__(self, parent, show_dashboard_callback, show_vendas_callback):
        super().__init__(parent)
        self.parent = parent
        self.show_dashboard_callback = show_dashboard_callback
        self.show_vendas_callback = show_vendas_callback
        self.configure(bg="#2a0a4a")
        self.create_widgets()
        self.load_products() # Carrega os produtos ao iniciar

    def create_widgets(self):
        # ... (código do cabeçalho e menu lateral existente) ...
        
        main_content_frame = tk.Frame(self, bg="#2a0a4a")
        main_content_frame.place(relx=0.25, rely=0.3, relwidth=0.7, relheight=0.6)
        
        # ... (código do botão "NOVO" e estilo da tabela existente) ...

        columns = ("id", "nome", "categoria", "preco", "quantidade", "descricao")
        self.tree = ttk.Treeview(main_content_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", anchor="center", width=40)
        # ... (código das outras colunas existente) ...

        self.tree.pack(fill="both", expand=True)

    def load_products(self):
        """Busca os produtos no banco de dados e os exibe na tabela."""
        # Limpa a tabela antes de carregar novos dados
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = Produto.get_all()
        for prod in products:
            # Formata o preço para o padrão brasileiro
            preco_formatado = f"R$ {prod['preco']:.2f}".replace('.', ',')
            # O campo 'categoria' não está no DB, então deixamos em branco por enquanto
            self.tree.insert("", "end", values=(prod['id_produto'], prod['nome'], "", preco_formatado, prod['estoque'], prod['descricao']))

    def open_new_product_modal(self):
        # ... (código do modal existente) ...
        
        def save_product():
            try:
                nome = entries["nome"].get()
                desc = entries["descrição"].get()
                preco = float(entries["preço"].get().replace(',', '.'))
                estoque = int(entries["quantidade"].get())

                if not nome or preco <= 0 or estoque < 0:
                    messagebox.showerror("Erro de Validação", "Nome, preço e estoque são obrigatórios e devem ser válidos.", parent=modal)
                    return
                
                novo_produto = Produto(nome, desc, preco, estoque)
                novo_produto.save()
                
                messagebox.showinfo("Sucesso", f"Produto '{nome}' salvo com sucesso!", parent=modal)
                modal.destroy()
                self.load_products() # Atualiza a lista de produtos na tela

            except ValueError:
                messagebox.showerror("Erro de Formato", "Preço e Quantidade devem ser números válidos.", parent=modal)
            except Exception as e:
                messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}", parent=modal)

        # ... (restante do código do modal) ...

