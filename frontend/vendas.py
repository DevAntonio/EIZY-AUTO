import tkinter as tk
from tkinter import ttk, messagebox
from backend.vendas import Venda
from backend.produtos import Produto

class VendasScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.criar_interface()
        self.carregar_vendas()

    def criar_interface(self):
        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(header, text="Vendas", font=("Arial", 16)).pack(side="left")
        
        ttk.Button(
            header,
            text="Nova Venda",
            command=self.abrir_modal
        ).pack(side="right")

        # Tabela
        columns = ("ID", "Data", "Cliente", "Valor Total", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def carregar_vendas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            vendas = Venda.buscar_todas()
            for v in vendas:
                self.tree.insert("", "end", values=(
                    v['id'],
                    v['data_venda'],
                    v['cliente_nome'],
                    f"R$ {v['valor_total']:.2f}",
                    v['status']
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar vendas: {str(e)}")

    def abrir_modal(self):
        self.modal = tk.Toplevel(self)
        self.modal.title("Nova Venda")
        self.modal.geometry("600x500")
        
        # Cliente
        ttk.Label(self.modal, text="Cliente:").pack(padx=10, pady=5)
        self.cliente_nome = ttk.Entry(self.modal, width=40)
        self.cliente_nome.pack(padx=10, pady=5)
        
        # Itens
        ttk.Label(self.modal, text="Itens da Venda").pack(pady=10)
        self.itens_frame = ttk.Frame(self.modal)
        self.itens_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Botão para adicionar itens
        ttk.Button(
            self.modal,
            text="Adicionar Item",
            command=self.adicionar_item
        ).pack(pady=10)
        
        # Total
        self.total_var = tk.StringVar(value="Total: R$ 0,00")
        ttk.Label(self.modal, textvariable=self.total_var, font=("Arial", 12, "bold")).pack(pady=10)
        
        # Botões
        btn_frame = ttk.Frame(self.modal)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="Finalizar Venda",
            command=self.finalizar_venda
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Cancelar",
            command=self.modal.destroy
        ).pack(side="left", padx=5)
        
        self.itens = []

    def adicionar_item(self):
        # Implementar a lógica para adicionar itens
        pass

    def finalizar_venda(self):
        cliente = self.cliente_nome.get().strip()
        if not cliente:
            messagebox.showwarning("Aviso", "Informe o nome do cliente")
            return
            
        if not self.itens:
            messagebox.showwarning("Aviso", "Adicione pelo menos um item")
            return
            
        try:
            venda_id = Venda.criar(cliente, self.itens)
            if venda_id:
                messagebox.showinfo("Sucesso", f"Venda #{venda_id} registrada com sucesso!")
                self.modal.destroy()
                self.carregar_vendas()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar venda: {str(e)}")