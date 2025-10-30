# views/produtos.py
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from models.produtos import Produto

class ProdutosPage(tk.Frame):
    def __init__(self, parent, show_dashboard_callback, show_vendas_callback):
        super().__init__(parent)
        self.parent = parent
        self.show_dashboard_callback = show_dashboard_callback
        self.show_vendas_callback = show_vendas_callback
        self.configure(bg="#2a0a4a")
        
        self.tree = None # Placeholder para a tabela
        self.search_entry = None # Placeholder para a busca
        
        self.create_widgets()
        self.load_products() # Carrega os produtos ao iniciar

    def create_widgets(self):
        # --- Frame Principal ---
        main_frame = tk.Frame(self, bg="#2a0a4a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Cabeçalho ---
        header_frame = tk.Frame(main_frame, bg="#2a0a4a")
        header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(header_frame, text="EIZY - AUTO", font=("Helvetica", 24, "bold"), fg="white", bg="#2a0a4a").pack(side="left")
        tk.Canvas(header_frame, width=30, height=30, bg="white", highlightthickness=0, borderwidth=0).pack(side="right") # Ícone de perfil

        # --- Conteúdo (Menu Lateral e Área Principal) ---
        content_frame = tk.Frame(main_frame, bg="#2a0a4a")
        content_frame.pack(fill="both", expand=True)

        # --- Menu Lateral ---
        side_menu = tk.Frame(content_frame, bg="#2a0a4a", width=150)
        side_menu.pack(side="left", fill="y", padx=(0, 20))
        
        btn_style = {"font": ("Helvetica", 12), "bg": "#1c0730", "fg": "white", "relief": "flat", "width": 15, "pady": 5, "cursor": "hand2"}
        active_btn_style = {"font": ("Helvetica", 12, "bold"), "bg": "white", "fg": "black", "relief": "flat", "width": 15, "pady": 5, "cursor": "hand2"}

        tk.Button(side_menu, text="Home", **btn_style, command=self.show_dashboard_callback).pack(pady=5)
        tk.Button(side_menu, text="PRODUTOS", **active_btn_style).pack(pady=5) # Botão ativo
        tk.Button(side_menu, text="VENDAS", **btn_style, command=self.show_vendas_callback).pack(pady=5)

        # --- Área de Conteúdo Principal ---
        main_content_frame = tk.Frame(content_frame, bg="#2a0a4a")
        main_content_frame.pack(side="left", fill="both", expand=True)

        # --- Botões de Ação (Novo, Editar, Deletar) ---
        action_buttons_frame = tk.Frame(main_content_frame, bg="#2a0a4a")
        action_buttons_frame.pack(fill="x", pady=(0, 10))

        action_btn_style = {"font": ("Helvetica", 10), "bg": "#1c0730", "fg": "white", "relief": "flat", "width": 10, "pady": 5, "cursor": "hand2"}
        
        tk.Button(action_buttons_frame, text="NOVO", **action_btn_style, command=self.open_new_product_modal).pack(side="left", padx=5)
        tk.Button(action_buttons_frame, text="EDITAR", **action_btn_style, command=self.open_edit_product_modal).pack(side="left", padx=5)
        tk.Button(action_buttons_frame, text="DELETAR", **action_btn_style, command=self.delete_product_action).pack(side="left", padx=5)

        # --- Barra de Busca ---
        search_frame = tk.Frame(main_content_frame, bg="#2a0a4a")
        search_frame.pack(fill="x", pady=(0, 10))

        tk.Label(search_frame, text="Procurar:", font=("Helvetica", 12), fg="white", bg="#2a0a4a").pack(side="left", padx=(0, 5))
        
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 12), bg="white", fg="black", relief="flat", width=30)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Bind <Return> (Enter) to the search action
        self.search_entry.bind('<Return>', self.search_product_action)
        
        search_btn_style = {"font": ("Helvetica", 10), "bg": "#5a2e8e", "fg": "white", "relief": "flat", "width": 10, "pady": 2, "cursor": "hand2"}
        tk.Button(search_frame, text="Buscar", **search_btn_style, command=self.search_product_action).pack(side="left", padx=5)
        tk.Button(search_frame, text="Limpar", **search_btn_style, command=self.clear_search).pack(side="left", padx=5)


        # --- Estilo da Tabela ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1c0730",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#1c0730",
                        bordercolor="#5a2e8e",
                        borderwidth=1,
                        relief="solid")
        style.map('Treeview', background=[('selected', '#3e1a66')])
        style.configure("Treeview.Heading",
                        background="#5a2e8e",
                        foreground="white",
                        font=("Helvetica", 10, "bold"),
                        relief="flat")
        style.map("Treeview.Heading",
                    background=[('active', '#3e1a66')])

        # --- Tabela de Produtos ---
        # Colunas alinhadas com db/database.py
        columns = ("id", "nome", "descricao", "preco", "estoque")
        self.tree = ttk.Treeview(main_content_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", anchor="center", width=40)
        
        self.tree.heading("nome", text="Nome")
        self.tree.column("nome", anchor="w", width=150)

        self.tree.heading("descricao", text="Descrição")
        self.tree.column("descricao", anchor="w", width=250)
        
        self.tree.heading("preco", text="Preço")
        self.tree.column("preco", anchor="center", width=80)
        
        self.tree.heading("estoque", text="Estoque")
        self.tree.column("estoque", anchor="center", width=80)

        self.tree.pack(fill="both", expand=True)

    def load_products(self, products_list=None):
        """
        Busca os produtos no banco de dados e os exibe na tabela.
        Se 'products_list' for fornecido, exibe essa lista (resultado de uma busca).
        Caso contrário, busca todos os produtos.
        """
        if not self.tree:
            print("Erro: A tabela (Treeview) não foi inicializada.")
            return
            
        # Limpa a tabela antes de carregar novos dados
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Se uma lista de produtos não foi passada, busca todos
            if products_list is None:
                products_list = Produto.get_all()
            
            for prod in products_list:
                # Formata o preço para o padrão brasileiro
                preco_formatado = f"R$ {prod['preco']:.2f}".replace('.', ',')
                self.tree.insert("", "end", values=(
                    prod['id_produto'], 
                    prod['nome'], 
                    prod['descricao'], 
                    preco_formatado, 
                    prod['estoque']
                ))
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar os produtos: {e}")
    def search_product_action(self, event=None): # Adicionado 'event=None' para o bind do <Return>
        """Filtra os produtos com base no termo de busca."""
        search_term = self.search_entry.get()
        if search_term:
            products_found = Produto.search(search_term)
            if not products_found:
                messagebox.showinfo("Busca", f"Nenhum produto encontrado para '{search_term}'.")
            self.load_products(products_found)
        else:
            # Se a busca estiver vazia, carrega todos
            self.load_products()

    def clear_search(self):
        """Limpa o campo de busca e recarrega todos os produtos."""
        self.search_entry.delete(0, 'end')
        self.load_products()

    def get_selected_product_data(self):
        """Retorna os dados do produto selecionado na tabela."""
        selected_item = self.tree.focus() # Pega o item focado (selecionado)
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione um produto na tabela primeiro.")
            return None
        
        # Retorna o dicionário de valores do item
        return self.tree.item(selected_item)['values']

    def open_edit_product_modal(self):
        """Abre um modal (Toplevel) para editar um produto selecionado."""
        
        selected_data = self.get_selected_product_data()
        if selected_data is None:
            return # Mensagem de erro já foi mostrada

        # Extrai os dados da tupla 'values'
        # (id, nome, descricao, preco_formatado, estoque)
        try:
            prod_id = selected_data[0]
            prod_nome = selected_data[1]
            prod_desc = selected_data[2]
            # Converte 'R$ 23,00' para '23.00'
            prod_preco_str = str(selected_data[3]).replace("R$ ", "").replace(",", ".")
            prod_preco = float(prod_preco_str)
            prod_estoque = int(selected_data[4])
        except (ValueError, TypeError, IndexError) as e:
            messagebox.showerror("Erro de Dados", f"Não foi possível ler os dados do produto selecionado. {e}")
            return

        modal = Toplevel(self)
        modal.title(f"Editar Produto (ID: {prod_id})")
        modal.geometry("400x400")
        modal.configure(bg="#1c0730")
        modal.transient(self) # Mantém o modal sobre a janela principal
        modal.grab_set() # Bloqueia interação com a janela principal

        modal_frame = tk.Frame(modal, bg="#1c0730", padx=20, pady=20)
        modal_frame.pack(fill="both", expand=True)

        labels = ["Nome:", "Descrição:", "Preço (R$):", "Quantidade (Estoque):"]
        entries = {}

        label_style = {"fg": "white", "bg": "#1c0730", "font": ("Helvetica", 12)}
        entry_style = {"font": ("Helvetica", 12), "bg": "white", "fg": "black", "relief": "flat"}

        for i, label_text in enumerate(labels):
            tk.Label(modal_frame, text=label_text, **label_style).pack(anchor="w", pady=(10, 2))
            entry = tk.Entry(modal_frame, **entry_style)
            entry.pack(fill="x", pady=(0, 10))
            # Usa o texto do label (normalizado) como chave
            entries[label_text.split(" ")[0].lower()] = entry 

        # --- Preenche o modal com os dados existentes ---
        entries["nome:"].insert(0, prod_nome)
        entries["descrição:"].insert(0, prod_desc)
        entries["preço"].insert(0, f"{prod_preco:.2f}".replace('.', ',')) # Formata para '23,00'
        entries["quantidade"].insert(0, str(prod_estoque))

        def save_product_changes():
            try:
                nome = entries["nome:"].get()
                desc = entries["descrição:"].get()
                # Converte preço de '10,50' para 10.50
                preco_str = entries["preço"].get().replace(',', '.')
                preco = float(preco_str)
                estoque = int(entries["quantidade"].get())

                if not nome or preco <= 0 or estoque < 0:
                    messagebox.showerror("Erro de Validação", "Nome, Preço (positivo) e Estoque (positivo) são obrigatórios.", parent=modal)
                    return
                
                # Cria um objeto Produto com o ID para chamar o método 'save' (que agora faz UPDATE)
                produto_atualizado = Produto(nome, desc, preco, estoque, id_produto=prod_id)
                produto_atualizado.save()
                
                messagebox.showinfo("Sucesso", f"Produto '{nome}' atualizado com sucesso!", parent=modal)
                modal.destroy()
                self.load_products() # Atualiza a lista de produtos na tela

            except ValueError:
                messagebox.showerror("Erro de Formato", "Preço e Quantidade devem ser números válidos (ex: 10.50 ou 10,50 para preço).", parent=modal)
            except Exception as e:
                messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}", parent=modal)

        save_button = tk.Button(
            modal_frame, text="Salvar Alterações", 
            command=save_product_changes, 
            bg="#5a2e8e", fg="white", 
            font=("Helvetica", 12, "bold"),
            relief="flat", cursor="hand2"
        )
        save_button.pack(pady=20)


    def open_new_product_modal(self):
        """Abre um modal (Toplevel) para adicionar um novo produto."""
        modal = Toplevel(self)
        modal.title("Novo Produto")
        modal.geometry("400x400")
        modal.configure(bg="#1c0730")
        modal.transient(self) # Mantém o modal sobre a janela principal
        modal.grab_set() # Bloqueia interação com a janela principal

        modal_frame = tk.Frame(modal, bg="#1c0730", padx=20, pady=20)
        modal_frame.pack(fill="both", expand=True)

        labels = ["Nome:", "Descrição:", "Preço (R$):", "Quantidade (Estoque):"]
        entries = {}

        label_style = {"fg": "white", "bg": "#1c0730", "font": ("Helvetica", 12)}
        entry_style = {"font": ("Helvetica", 12), "bg": "white", "fg": "black", "relief": "flat"}

        for i, label_text in enumerate(labels):
            tk.Label(modal_frame, text=label_text, **label_style).pack(anchor="w", pady=(10, 2))
            entry = tk.Entry(modal_frame, **entry_style)
            entry.pack(fill="x", pady=(0, 10))
            # Usa o texto do label (normalizado) como chave
            entries[label_text.split(" ")[0].lower()] = entry 

        def save_product():
            try:
                nome = entries["nome:"].get()
                desc = entries["descrição:"].get()
                # Converte preço de '10,50' para 10.50
                preco_str = entries["preço"].get().replace(',', '.')
                preco = float(preco_str)
                estoque = int(entries["quantidade"].get())

                if not nome or preco <= 0 or estoque < 0:
                    messagebox.showerror("Erro de Validação", "Nome, Preço (positivo) e Estoque (positivo) são obrigatórios.", parent=modal)
                    return
                
                novo_produto = Produto(nome, desc, preco, estoque)
                novo_produto.save()
                
                messagebox.showinfo("Sucesso", f"Produto '{nome}' salvo com sucesso!", parent=modal)
                modal.destroy()
                self.load_products() # Atualiza a lista de produtos na tela

            except ValueError:
                messagebox.showerror("Erro de Formato", "Preço e Quantidade devem ser números válidos (ex: 10.50 ou 10,50 para preço).", parent=modal)
            except Exception as e:
                messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}", parent=modal)

        save_button = tk.Button(
            modal_frame, text="Salvar Produto", 
            command=save_product, 
            bg="#5a2e8e", fg="white", 
            font=("Helvetica", 12, "bold"),
            relief="flat", cursor="hand2"
        )
        save_button.pack(pady=20)


    def delete_product_action(self):
        """Deleta o produto selecionado da tabela e do banco de dados."""
        
        selected_data = self.get_selected_product_data()
        if selected_data is None:
            return # Mensagem de erro já foi mostrada

        try:
            prod_id = selected_data[0]
            prod_nome = selected_data[1]
        except (IndexError) as e:
            messagebox.showerror("Erro de Dados", "Não foi possível ler o ID do produto selecionado.")
            return

        # Pede confirmação
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o produto:\n\nID: {prod_id}\nNome: {prod_nome}\n\nEsta ação não pode ser desfeita."):
            try:
                Produto.delete(prod_id)
                messagebox.showinfo("Sucesso", f"Produto '{prod_nome}' deletado com sucesso.")
                self.load_products() # Recarrega a lista
            except Exception as e:
                messagebox.showerror("Erro ao Deletar", f"Não foi possível deletar o produto: {e}")


