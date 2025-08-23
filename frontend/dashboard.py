import tkinter as tk
from tkinter import ttk

class DashboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Menu de Navegação ---
        nav_frame = ttk.Frame(self)
        nav_frame.pack(side="top", fill="x", pady=5)

        home_button = ttk.Button(
            nav_frame,
            text="Home",
            # O comando está desabilitado pois já estamos nesta tela
        )
        home_button.pack(side="left", padx=5)
        home_button.state(['disabled'])

        vendas_button = ttk.Button(
            nav_frame,
            text="Vendas",
            command=lambda: controller.show_frame("VendasScreen")
        )
        vendas_button.pack(side="left", padx=5)

        produtos_button = ttk.Button(
            nav_frame,
            text="Produtos",
            command=lambda: controller.show_frame("ProdutosScreen")
        )
        produtos_button.pack(side="left", padx=5)

        # --- Conteúdo da Página ---
        label = ttk.Label(self, text="Bem-vindo ao Dashboard!", font=("Arial", 20))
        label.pack(pady=20, padx=20)
        
        # Botão de Logout para voltar à tela inicial
        logout_button = ttk.Button(
            self,
            text="Logout",
            command=lambda: controller.show_frame("HomeScreen")
        )
        logout_button.pack(pady=10)
