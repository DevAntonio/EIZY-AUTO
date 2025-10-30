# views/dashboard.py
import tkinter as tk
from tkinter import font
# Importa as funções de contagem do banco de dados
from db.database import get_total_products_count, get_total_sales_count

class DashboardPage(tk.Frame):
    def __init__(self, parent, show_home_callback, show_produtos_callback, show_vendas_callback):
        """
        Inicializa a DashboardPage.
        :param parent: O widget pai (a janela principal).
        :param show_home_callback: A função para "deslogar" e voltar para a tela inicial.
        :param show_produtos_callback: A função para navegar para a tela de produtos.
        :param show_vendas_callback: A função para navegar para a tela de vendas.
        """
        super().__init__(parent)
        self.parent = parent
        self.show_home_callback = show_home_callback
        self.show_produtos_callback = show_produtos_callback
        self.show_vendas_callback = show_vendas_callback
        self.configure(bg="#2a0a4a") # Cor de fundo principal
        
        # Placeholders para os botões que precisam ser atualizados
        self.vendas_button = None
        self.produtos_button = None
        
        self.create_widgets()
        self.update_counts() # Atualiza as contagens na inicialização

    def create_widgets(self):
        # --- Cabeçalho e Perfil ---
        header_label = tk.Label(self, text="EIZY - AUTO", font=("Helvetica", 20, "bold"), bg="#2a0a4a", fg="white")
        header_label.place(relx=0.05, rely=0.05)
        
        profile_canvas = tk.Canvas(self, width=40, height=40, bg="#2a0a4a", bd=0, highlightthickness=0)
        profile_canvas.place(relx=0.95, rely=0.07, anchor="center")
        profile_canvas.create_oval(2, 2, 38, 38, fill="white", outline="white")
        # TODO: Adicionar ícone de pessoa ou imagem do usuário
        
        welcome_banner = tk.Label(self, text="Bem vindo a sua dashboard de gerenciamento com o EIZY - AUTO", font=("Helvetica", 16), bg="#1c0730", fg="white", padx=20, pady=10)
        welcome_banner.place(relx=0.5, rely=0.2, anchor="center", relwidth=0.9)

        # --- Menu de Navegação Lateral ---
        nav_frame = tk.Frame(self, bg="#2a0a4a")
        nav_frame.place(relx=0.05, rely=0.3, relheight=0.4, relwidth=0.15) # Ajustado relwidth

        button_font = ("Helvetica", 11)
        btn_style = {"font": button_font, "bg": "#1c0730", "fg": "white", "relief": "flat", "pady": 5,
                     "activebackground": "#3e1a66", "activeforeground": "white", "cursor": "hand2"}
        
        active_btn_style = {"font": button_font, "bg": "white", "fg": "black", "relief": "flat", "pady": 5, 
                            "cursor": "hand2"}

        # Botão Home (Ativo)
        tk.Button(
            nav_frame, text="Home", **active_btn_style,
            command=lambda: print("Já está na Home")
        ).pack(pady=5, fill="x")
        
        # Botão Produtos
        tk.Button(
            nav_frame, text="PRODUTOS", **btn_style,
            command=self.show_produtos_callback
        ).pack(pady=5, fill="x")
        
        # Botão Vendas
        tk.Button(
            nav_frame, text="VENDAS", **btn_style,
            command=self.show_vendas_callback
        ).pack(pady=5, fill="x")


        # --- Botões de Ação Principal (Mockup) ---
        # Idealmente, esses números (2 Vendas, 3 Produtos) viriam do banco de dados
        action_frame = tk.Frame(self, bg="#2a0a4a")
        action_frame.place(relx=0.55, rely=0.4, anchor="n") # Ajustado relx

        action_font = ("Helvetica", 14, "bold")
        action_btn_style = {"font": action_font, "bg": "#1c0730", "fg": "white", 
                            "relief": "solid", "bd": 1, "width": 15, "height": 3, "cursor": "hand2"}
        
        # Armazena os botões como atributos da classe
        self.vendas_button = tk.Button(
            action_frame, text="Vendas", **action_btn_style,
            command=self.show_vendas_callback # Navega para vendas
        )
        self.vendas_button.grid(row=0, column=0, padx=20)
        
        self.produtos_button = tk.Button(
            action_frame, text="Produtos", **action_btn_style,
            command=self.show_produtos_callback
        )
        self.produtos_button.grid(row=0, column=1, padx=20)

        # --- Botão Sair ---
        logout_button = tk.Button(
            self, text="Sair", font=("Helvetica", 12, "bold"), bg="#d9534f", fg="white",
            activebackground="#c9302c", activeforeground="white", relief="flat", cursor="hand2",
            command=self.show_home_callback
        )
        logout_button.place(relx=0.05, rely=0.9, relwidth=0.15, relheight=0.07) # Ajustado relwidth

    def update_counts(self):
        """Busca os totais do DB e atualiza o texto dos botões."""
        try:
            total_produtos = get_total_products_count()
            total_vendas = get_total_sales_count()
            
            # Atualiza o texto dos botões se eles já foram criados
            if self.produtos_button:
                self.produtos_button.config(text=f"{total_produtos} Produtos")
            
            if self.vendas_button:
                self.vendas_button.config(text=f"{total_vendas} Vendas")
                
        except Exception as e:
            print(f"Erro ao atualizar contagens do dashboard: {e}")
            if self.produtos_button:
                self.produtos_button.config(text="Produtos (Erro)")
            if self.vendas_button:
                self.vendas_button.config(text="Vendas (Erro)")

