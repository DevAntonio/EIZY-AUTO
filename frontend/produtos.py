import tkinter as tk
from tkinter import ttk, messagebox
import os  # <-- Adicionado para corrigir o NameError
from PIL import Image, ImageTk # <-- Adicionado para evitar futuros erros
# Certifique-se de que o backend está acessível
# from backend.produtos import Produto 

# --- Classe de Mock para testes sem o backend ---
# Remova ou comente esta classe quando for integrar com seu backend real
class Produto:
    _produtos = [
        {'id': 1, 'nome': 'PRODUTO1', 'categoria': 'ALIMENTO', 'preco': 29.90, 'estoque': 23, 'descricao': 'PRODUT...'},
        {'id': 2, 'nome': 'PRODUTO2', 'categoria': 'ALIMENTO', 'preco': 29.90, 'estoque': 23, 'descricao': 'PRODUT...'},
        {'id': 3, 'nome': 'PRODUTO3', 'categoria': 'ALIMENTO', 'preco': 29.90, 'estoque': 23, 'descricao': 'PRODUT...'},
    ]
    _next_id = 4

    @classmethod
    def buscar_todos(cls):
        return cls._produtos

    @classmethod
    def buscar_por_id(cls, prod_id):
        for p in cls._produtos:
            if p['id'] == prod_id:
                return p
        return None

    @classmethod
    def criar(cls, nome, preco, estoque, descricao, categoria):
        novo = {'id': cls._next_id, 'nome': nome, 'categoria': categoria, 'preco': preco, 'estoque': estoque, 'descricao': descricao}
        cls._produtos.append(novo)
        cls._next_id += 1
        return novo

    @classmethod
    def atualizar(cls, prod_id, **kwargs):
        for p in cls._produtos:
            if p['id'] == prod_id:
                p.update(kwargs)
                return True
        return False

    @classmethod
    def deletar(cls, prod_id):
        for i, p in enumerate(cls._produtos):
            if p['id'] == prod_id:
                del cls._produtos[i]
                return True
        return False
# --- Fim da classe de Mock ---


class ProdutosScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.produto_editando = None
        
        # --- Configuração do Canvas para a imagem de fundo ---
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        image_path = os.path.join("assets", "bc03.png")
        self.bg_image_pil = None
        self.bg_image_tk = None
        self.canvas.bind("<Configure>", self.resize_background)

        # --- Estilos ---
        self.setup_styles()

        # --- Layout Principal ---
        self.criar_layout_principal()
        
        # --- Carregar dados ---
        self.carregar_produtos()

        # Carrega a imagem de fundo
        try:
            if os.path.exists(image_path):
                self.bg_image_pil = Image.open(image_path)
            else:
                self.bg_image_pil = Image.new('RGB', (800, 600), color="#2c1a42")
        except Exception as e:
            print(f"Erro ao carregar a imagem de produtos: {e}")
            self.bg_image_pil = Image.new('RGB', (800, 600), color="#2c1a42")

    def setup_styles(self):
        style = ttk.Style(self)
        BG_COLOR = "#2c1a42"
        FG_COLOR = "white"
        
        style.configure("Produtos.TFrame", background=BG_COLOR)
        style.configure("Header.TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Arial", 16, "bold"))
        style.configure("Nav.TButton", background="#3c2a52", foreground=FG_COLOR, font=("Arial", 10, "bold"), width=15)
        style.map("Nav.TButton", background=[('active', '#5a417a'), ('disabled', '#3c2a52')])
        style.configure("Novo.TButton", background="#1e122d", foreground=FG_COLOR, font=("Arial", 10))
        style.map("Novo.TButton", background=[('active', '#3a2556')])

        # Estilo da Treeview
        style.configure("Treeview", background="#1e122d", fieldbackground="#1e122d", foreground=FG_COLOR, borderwidth=0)
        style.configure("Treeview.Heading", background="#1e122d", foreground=FG_COLOR, font=("Arial", 10, "bold"), borderwidth=0)
        style.map("Treeview.Heading", background=[('active', '#3a2556')])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Remove bordas

    def criar_layout_principal(self):
        self.main_frame = ttk.Frame(self, style="Produtos.TFrame")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # --- Cabeçalho ---
        header_frame = ttk.Frame(self.main_frame, style="Produtos.TFrame", padding=10)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(header_frame, text="EIZY - AUTO", style="Header.TLabel").pack(side="left")
        tk.Label(header_frame, text="●", fg="white", bg="#2c1a42", font=("Arial", 24)).pack(side="right")

        # --- Painel de Navegação Lateral ---
        nav_panel = ttk.Frame(self.main_frame, style="Produtos.TFrame", padding=(10, 0))
        nav_panel.grid(row=1, column=0, sticky="ns", padx=10, pady=(0, 10))
        
        ttk.Button(nav_panel, text="Home", style="Nav.TButton", command=lambda: self.controller.show_frame("DashboardScreen")).pack(pady=5, fill="x")
        produtos_btn = ttk.Button(nav_panel, text="PRODUTOS", style="Nav.TButton")
        produtos_btn.state(['disabled'])
        produtos_btn.pack(pady=5, fill="x")
        ttk.Button(nav_panel, text="VENDAS", style="Nav.TButton", command=lambda: self.controller.show_frame("VendasScreen")).pack(pady=5, fill="x")

        # --- Área de Conteúdo Principal ---
        content_area = ttk.Frame(self.main_frame, style="Produtos.TFrame")
        content_area.grid(row=1, column=1, sticky="nsew", padx=20, pady=(0, 20))
        content_area.grid_rowconfigure(1, weight=1)
        content_area.grid_columnconfigure(0, weight=1)

        # Botão Novo
        btn_novo = ttk.Button(content_area, text="NOVO", style="Novo.TButton", command=self.abrir_modal_produto)
        btn_novo.grid(row=0, column=0, sticky="e", pady=(10, 5))

        # Tabela de produtos
        columns = ("IMAGEM", "NOME", "CATEGORIA", "PREÇO", "QUANTIDADE", "DESCRIÇÃO")
        self.tree = ttk.Treeview(content_area, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.column("NOME", width=120)
        self.tree.column("DESCRIÇÃO", width=150)
        
        self.tree.grid(row=1, column=0, sticky="nsew")

    def carregar_produtos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            produtos = Produto.buscar_todos()
            for produto in produtos:
                self.tree.insert("", "end", values=(
                    "🖼️",  # Placeholder para imagem
                    produto['nome'],
                    produto['categoria'],
                    f"R$ {produto['preco']:.2f}",
                    produto['estoque'],
                    produto['descricao']
                ), tags=(produto['id'],))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")

    def abrir_modal_produto(self, produto=None):
        # Implementação do modal (semelhante ao seu código original)
        pass # Adicione sua lógica de modal aqui

    def salvar_produto(self, modal, nome, preco, estoque, descricao, categoria):
        # Implementação do salvar (semelhante ao seu código original)
        pass # Adicione sua lógica de salvar aqui

    def resize_background(self, event):
        if not self.bg_image_pil: return
        new_width, new_height = event.width, event.height
        resized_pil = self.bg_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(resized_pil)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        self.canvas.create_window(0, 0, anchor="nw", window=self.main_frame, width=new_width, height=new_height)
