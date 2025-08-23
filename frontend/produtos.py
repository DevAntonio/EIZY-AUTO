import tkinter as tk
from tkinter import ttk, messagebox
from backend.produtos import Produto

class ProdutosScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.produto_editando = None
        self.criar_interface()
        self.carregar_produtos()

    def criar_interface(self):
        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(header, text="Gerenciamento de Produtos", font=("Arial", 16)).pack(side="left")
        
        btn_novo = ttk.Button(
            header,
            text="Novo Produto",
            command=self.abrir_modal_produto
        )
        btn_novo.pack(side="right")

        # Tabela de produtos
        columns = ("ID", "Nome", "Preço", "Estoque", "Descrição")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        
        # Configuração das colunas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botões de ação
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        btn_editar = ttk.Button(
            btn_frame,
            text="Editar",
            command=self.editar_produto
        )
        btn_editar.pack(side="left", padx=5)
        
        btn_excluir = ttk.Button(
            btn_frame,
            text="Excluir",
            command=self.excluir_produto
        )
        btn_excluir.pack(side="left", padx=5)

    def carregar_produtos(self):
        # Limpa a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carrega os produtos do banco
        try:
            produtos = Produto.buscar_todos()
            for produto in produtos:
                self.tree.insert("", "end", values=(
                    produto['id'],
                    produto['nome'],
                    f"R$ {produto['preco']:.2f}",
                    produto['estoque'],
                    produto['descricao'] or '-'
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")

    def abrir_modal_produto(self, produto=None):
        self.produto_editando = produto
        modal = tk.Toplevel(self)
        modal.title("Novo Produto" if not produto else "Editar Produto")
        modal.geometry("400x300")
        
        # Centraliza o modal
        modal.update_idletasks()
        width = modal.winfo_width()
        height = modal.winfo_height()
        x = (modal.winfo_screenwidth() // 2) - (width // 2)
        y = (modal.winfo_screenheight() // 2) - (height // 2)
        modal.geometry(f'400x300+{x}+{y}')
        
        # Campos do formulário
        frame = ttk.Frame(modal, padding=20)
        frame.pack(fill="both", expand=True)
        
        # Nome
        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        nome_var = tk.StringVar(value=produto['nome'] if produto else '')
        ttk.Entry(frame, textvariable=nome_var, width=40).grid(row=0, column=1, sticky="ew", pady=5)
        
        # Preço
        ttk.Label(frame, text="Preço:").grid(row=1, column=0, sticky="w", pady=5)
        preco_var = tk.StringVar(value=f"{produto['preco']:.2f}" if produto else '0.00')
        ttk.Entry(frame, textvariable=preco_var, width=20).grid(row=1, column=1, sticky="w", pady=5)
        
        # Estoque
        ttk.Label(frame, text="Estoque:").grid(row=2, column=0, sticky="w", pady=5)
        estoque_var = tk.IntVar(value=produto['estoque'] if produto else 0)
        ttk.Spinbox(frame, from_=0, to=9999, textvariable=estoque_var, width=10).grid(row=2, column=1, sticky="w", pady=5)
        
        # Descrição
        ttk.Label(frame, text="Descrição:").grid(row=3, column=0, sticky="nw", pady=5)
        descricao_var = tk.StringVar(value=produto['descricao'] if produto else '')
        ttk.Entry(frame, textvariable=descricao_var, width=40).grid(row=3, column=1, sticky="ew", pady=5)
        
        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            btn_frame,
            text="Cancelar",
            command=modal.destroy
        ).pack(side="right", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Salvar",
            command=lambda: self.salvar_produto(
                modal,
                nome_var.get(),
                preco_var.get(),
                estoque_var.get(),
                descricao_var.get()
            )
        ).pack(side="right")

    def salvar_produto(self, modal, nome, preco, estoque, descricao):
        try:
            preco_float = float(preco.replace(",", "."))
            estoque_int = int(estoque)
            
            if self.produto_editando:
                # Atualizar produto existente
                Produto.atualizar(
                    self.produto_editando['id'],
                    nome=nome,
                    preco=preco_float,
                    estoque=estoque_int,
                    descricao=descricao
                )
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            else:
                # Criar novo produto
                Produto.criar(nome, preco_float, estoque_int, descricao)
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            
            modal.destroy()
            self.carregar_produtos()
            self.produto_editando = None
            
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números válidos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {str(e)}")

    def editar_produto(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para editar")
            return
            
        produto_id = self.tree.item(selecionado[0])['values'][0]
        produto = Produto.buscar_por_id(produto_id)
        
        if produto:
            self.abrir_modal_produto(produto)

    def excluir_produto(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir")
            return
            
        produto_id = self.tree.item(selecionado[0])['values'][0]
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este produto?"):
            try:
                if Produto.deletar(produto_id):
                    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                    self.carregar_produtos()
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir o produto")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao excluir produto: {str(e)}")