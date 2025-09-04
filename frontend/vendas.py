import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
# from backend.vendas import Venda
# from backend.produtos import Produto

# --- Classes de Mock para testes ---
class Venda:
    _vendas = [
        {'id': 1, 'data_venda': '21/01/2025', 'produto': 'ARROZ', 'quantidade': 2, 'total': 22.00},
        {'id': 2, 'data_venda': '21/01/2025', 'produto': 'ARROZ', 'quantidade': 2, 'total': 22.00},
    ]
    @classmethod
    def buscar_todas(cls):
        return cls._vendas
# --- Fim das classes de Mock ---

class VendasScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Configuração do Canvas ---
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
        self.carregar_vendas()

        # Carrega a imagem de fundo
        try:
            if os.path.exists(image_path):
                self.bg_image_pil = Image.open(image_path)
            else:
                self.bg_image_pil = Image.new('RGB', (800, 600), color="#2c1a42")
        except Exception as e:
            print(f"Erro ao carregar a imagem de vendas: {e}")
            self.bg_image_pil = Image.new('RGB', (800, 600), color="#2c1a42")

    def setup_styles(self):
        style = ttk.Style(self)
        BG_COLOR = "#2c1a42"
        FG_COLOR = "white"
        
        style.configure("Vendas.TFrame", background=BG_COLOR)
        style.configure("Header.TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Arial", 16, "bold"))
        style.configure("Nav.TButton", background="#3c2a52", foreground=FG_COLOR, font=("Arial", 10, "bold"), width=15)
        style.map("Nav.TButton", background=[('active', '#5a417a'), ('disabled', '#3c2a52')])
        style.configure("Action.TButton", background="#1e122d", foreground=FG_COLOR, font=("Arial", 10))
        style.map("Action.TButton", background=[('active', '#3a2556')])

        # Estilo da Treeview
        style.configure("Treeview", background="#1e122d", fieldbackground="#1e122d", foreground=FG_COLOR, borderwidth=0)
        style.configure("Treeview.Heading", background="#1e122d", foreground=FG_COLOR, font=("Arial", 10, "bold"), borderwidth=0)
        style.map("Treeview.Heading", background=[('active', '#3a2556')])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    def criar_layout_principal(self):
        self.main_frame = ttk.Frame(self, style="Vendas.TFrame")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # --- Cabeçalho ---
        header_frame = ttk.Frame(self.main_frame, style="Vendas.TFrame", padding=10)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(header_frame, text="EIZY - AUTO", style="Header.TLabel").pack(side="left")
        tk.Label(header_frame, text="●", fg="white", bg="#2c1a42", font=("Arial", 24)).pack(side="right")

        # --- Painel de Navegação Lateral ---
        nav_panel = ttk.Frame(self.main_frame, style="Vendas.TFrame", padding=(10, 0))
        nav_panel.grid(row=1, column=0, sticky="ns", padx=10, pady=(0, 10))
        
        ttk.Button(nav_panel, text="Home", style="Nav.TButton", command=lambda: self.controller.show_frame("DashboardScreen")).pack(pady=5, fill="x")
        ttk.Button(nav_panel, text="PRODUTOS", style="Nav.TButton", command=lambda: self.controller.show_frame("ProdutosScreen")).pack(pady=5, fill="x")
        vendas_btn = ttk.Button(nav_panel, text="VENDAS", style="Nav.TButton")
        vendas_btn.state(['disabled'])
        vendas_btn.pack(pady=5, fill="x")

        # --- Área de Conteúdo Principal ---
        content_area = ttk.Frame(self.main_frame, style="Vendas.TFrame")
        content_area.grid(row=1, column=1, sticky="nsew", padx=20, pady=(0, 20))
        content_area.grid_rowconfigure(1, weight=1)
        content_area.grid_columnconfigure(0, weight=1)

        # Botões de Ação (Excel, PDF, Novo)
        action_frame = ttk.Frame(content_area, style="Vendas.TFrame")
        action_frame.grid(row=0, column=0, sticky="e", pady=(10, 5))
        ttk.Button(action_frame, text="EXCEL", style="Action.TButton").pack(side="left", padx=5)
        ttk.Button(action_frame, text="PDF", style="Action.TButton").pack(side="left", padx=5)
        ttk.Button(action_frame, text="NOVO", style="Action.TButton", command=self.abrir_modal).pack(side="left", padx=5)

        # Tabela de Vendas
        columns = ("DIA", "PRODUTO", "QUANTIDADE", "TOTAL")
        self.tree = ttk.Treeview(content_area, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        
        self.tree.grid(row=1, column=0, sticky="nsew")

    def carregar_vendas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            vendas = Venda.buscar_todas()
            for v in vendas:
                self.tree.insert("", "end", values=(
                    v['data_venda'],
                    v['produto'],
                    v['quantidade'],
                    f"{v['total']:.2f} R$"
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar vendas: {str(e)}")

    def abrir_modal(self):
        # Sua lógica de modal de nova venda pode ser chamada aqui
        messagebox.showinfo("Info", "Abrir modal de nova venda.")

    def resize_background(self, event):
        if not self.bg_image_pil: return
        new_width, new_height = event.width, event.height
        resized_pil = self.bg_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(resized_pil)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        self.canvas.create_window(0, 0, anchor="nw", window=self.main_frame, width=new_width, height=new_height)

