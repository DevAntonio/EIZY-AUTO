import tkinter as tk
from tkinter import font

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
        self.create_widgets()

    def create_widgets(self):
        # --- Cabeçalho e Perfil (sem alterações) ---
        header_label = tk.Label(self, text="EIZY - AUTO", font=("Helvetica", 20, "bold"), bg="#2a0a4a", fg="white")
        header_label.place(relx=0.05, rely=0.05)
        profile_canvas = tk.Canvas(self, width=40, height=40, bg="#2a0a4a", bd=0, highlightthickness=0)
        profile_canvas.place(relx=0.95, rely=0.07, anchor="center")
        profile_canvas.create_oval(2, 2, 38, 38, fill="white", outline="white")
        welcome_banner = tk.Label(self, text="Bem vindo a sua dashboard de gerenciamento com o EIZY - AUTO", font=("Helvetica", 16), bg="#1c0730", fg="white", padx=20, pady=10)
        welcome_banner.place(relx=0.5, rely=0.2, anchor="center", relwidth=0.9)

        # --- Menu de Navegação Lateral ---
        nav_frame = tk.Frame(self, bg="#2a0a4a")
        nav_frame.place(relx=0.05, rely=0.3, relheight=0.4)

        button_font = ("Helvetica", 11)
        nav_buttons_config = [
            {"text": "Home", "command": lambda: print("Botão Home clicado")},
            {"text": "PRODUTOS", "command": self.show_produtos_callback},
            {"text": "VENDAS", "command": self.show_vendas_callback} # Navega para vendas
        ]
        for config in nav_buttons_config:
            bg_color = "white" if config["text"] == "Home" else "#1c0730"
            fg_color = "black" if config["text"] == "Home" else "white"
            button = tk.Button(
                nav_frame, text=config["text"], font=button_font,
                bg=bg_color, fg=fg_color, relief="flat", width=15, pady=5,
                activebackground="#3e1a66", activeforeground="white",
                cursor="hand2", command=config["command"]
            )
            button.pack(pady=5, fill="x")

        # --- Botões de Ação Principal ---
        action_frame = tk.Frame(self, bg="#2a0a4a")
        action_frame.place(relx=0.5, rely=0.4, anchor="n")

        action_font = ("Helvetica", 14, "bold")
        vendas_button = tk.Button(
            action_frame, text="2 Vendas", font=action_font, bg="#1c0730",
            fg="white", relief="solid", bd=1, width=15, height=3, cursor="hand2",
            command=self.show_vendas_callback # Navega para vendas
        )
        vendas_button.grid(row=0, column=0, padx=20)
        produtos_button = tk.Button(
            action_frame, text="3 Produtos", font=action_font,
            bg="#1c0730", fg="white", relief="solid", bd=1,
            width=15, height=3, cursor="hand2",
            command=self.show_produtos_callback
        )
        produtos_button.grid(row=0, column=1, padx=20)

        # --- Botão Sair ---
        logout_button = tk.Button(
            self, text="Sair", font=("Helvetica", 12, "bold"), bg="#d9534f", fg="white",
            activebackground="#c9302c", activeforeground="white", relief="flat", cursor="hand2",
            command=self.show_home_callback
        )
        logout_button.place(relx=0.05, rely=0.9, relwidth=0.1, relheight=0.07)

