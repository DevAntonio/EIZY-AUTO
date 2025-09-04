import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class DashboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Configuração do Canvas para a imagem de fundo ---
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        image_path = os.path.join("assets", "bc03.png")
        self.bg_image_pil = None
        self.bg_image_tk = None
        self.canvas.bind("<Configure>", self.resize_background)

        # --- Estilos ---
        style = ttk.Style(self)
        BG_COLOR = "#2c1a42"
        FG_COLOR = "white"
        
        style.configure("Dashboard.TFrame", background=BG_COLOR)
        
        # Estilo do cabeçalho
        style.configure("Header.TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Arial", 16, "bold"))
        
        # Estilo da mensagem de boas-vindas
        style.configure("Welcome.TFrame", background="#1e122d")
        style.configure("Welcome.TLabel", background="#1e122d", foreground=FG_COLOR, font=("Arial", 12, "bold"))

        # Estilo dos botões de navegação lateral
        style.configure("Nav.TButton", background="#3c2a52", foreground=FG_COLOR, font=("Arial", 10, "bold"), width=15)
        style.map("Nav.TButton", background=[('active', '#5a417a'), ('disabled', '#3c2a52')])

        # Estilo dos botões de conteúdo principal
        style.configure("Content.TButton", background="#1e122d", foreground=FG_COLOR, font=("Arial", 12, "bold"), padding=(20, 10))
        style.map("Content.TButton", background=[('active', '#3a2556')])
        
        # Estilo do botão Sair
        style.configure("Exit.TButton", background="#e63946", foreground=FG_COLOR, font=("Arial", 10, "bold"))
        style.map("Exit.TButton", background=[('active', '#c22b37')])


        # --- Frame Principal que conterá todo o layout ---
        self.main_frame = ttk.Frame(self, style="Dashboard.TFrame")
        
        # Configuração do Grid no main_frame
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # --- Cabeçalho ---
        header_frame = ttk.Frame(self.main_frame, style="Dashboard.TFrame", padding=10)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_label = ttk.Label(header_frame, text="EIZY - AUTO", style="Header.TLabel")
        header_label.pack(side="left")
        # Placeholder para o círculo branco
        # Criar um círculo real no canvas seria mais complexo, então usamos um label por simplicidade
        profile_circle = tk.Label(header_frame, text="●", fg="white", bg=BG_COLOR, font=("Arial", 24))
        profile_circle.pack(side="right")


        # --- Mensagem de Boas-Vindas ---
        welcome_frame = ttk.Frame(self.main_frame, style="Welcome.TFrame", padding=10)
        welcome_frame.grid(row=1, column=1, sticky="ew", padx=20, pady=10)
        welcome_label = ttk.Label(welcome_frame, text="Bem vindo a sua dashboard de gerenciamento com o EIZY - AUTO", style="Welcome.TLabel")
        welcome_label.pack()

        # --- Painel de Navegação Lateral ---
        nav_panel = ttk.Frame(self.main_frame, style="Dashboard.TFrame", padding=(10, 0))
        nav_panel.grid(row=2, column=0, sticky="ns", padx=10)
        
        home_button = ttk.Button(nav_panel, text="Home", style="Nav.TButton")
        home_button.state(['disabled']) # Desabilitado pois já está na home
        home_button.pack(pady=5, fill="x")

        produtos_button_nav = ttk.Button(nav_panel, text="PRODUTOS", style="Nav.TButton", command=lambda: controller.show_frame("ProdutosScreen"))
        produtos_button_nav.pack(pady=5, fill="x")

        vendas_button_nav = ttk.Button(nav_panel, text="VENDAS", style="Nav.TButton", command=lambda: controller.show_frame("VendasScreen"))
        vendas_button_nav.pack(pady=5, fill="x")

        # --- Área de Conteúdo Principal ---
        content_area = ttk.Frame(self.main_frame, style="Dashboard.TFrame")
        content_area.grid(row=2, column=1, sticky="nsew", padx=20)
        content_area.grid_columnconfigure(0, weight=1)
        content_area.grid_columnconfigure(1, weight=1)

        vendas_button_content = ttk.Button(content_area, text="2 Vendas", style="Content.TButton", command=lambda: controller.show_frame("VendasScreen"))
        vendas_button_content.grid(row=0, column=0, padx=10, pady=20)

        produtos_button_content = ttk.Button(content_area, text="3 Produtos", style="Content.TButton", command=lambda: controller.show_frame("ProdutosScreen"))
        produtos_button_content.grid(row=0, column=1, padx=10, pady=20)

        # --- Botão Sair ---
        exit_button = ttk.Button(self.main_frame, text="Sair", style="Exit.TButton", command=lambda: controller.show_frame("HomeScreen"))
        exit_button.grid(row=3, column=0, sticky="sw", padx=20, pady=20)

        # Carrega a imagem de fundo
        try:
            if os.path.exists(image_path):
                self.bg_image_pil = Image.open(image_path)
            else:
                self.bg_image_pil = Image.new('RGB', (800, 600), color=BG_COLOR)
        except Exception as e:
            print(f"Erro ao carregar a imagem do dashboard: {e}")
            self.bg_image_pil = Image.new('RGB', (800, 600), color=BG_COLOR)


    def resize_background(self, event):
        """Redimensiona a imagem de fundo e o frame principal."""
        if not self.bg_image_pil:
            return

        new_width, new_height = event.width, event.height
        
        resized_pil = self.bg_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(resized_pil)
        
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        
        # Posiciona o frame principal sobre o canvas
        self.canvas.create_window(0, 0, anchor="nw", window=self.main_frame, width=new_width, height=new_height)

