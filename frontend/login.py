import tkinter as tk
from tkinter import ttk

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Tela de Login", font=("Arial", 20))
        label.pack(pady=20, padx=20)
        
        # Frame para o campo de usuário
        user_frame = ttk.Frame(self)
        user_label = ttk.Label(user_frame, text="Usuário:")
        user_label.pack(side="left", padx=5, pady=5)
        self.user_entry = ttk.Entry(user_frame)
        self.user_entry.pack(side="left")
        user_frame.pack()

        # Frame para o campo de senha
        pass_frame = ttk.Frame(self)
        pass_label = ttk.Label(pass_frame, text="Senha:  ")
        pass_label.pack(side="left", padx=5, pady=5)
        self.pass_entry = ttk.Entry(pass_frame, show="*")
        self.pass_entry.pack(side="left")
        pass_frame.pack()

        # Botão de Login atualizado para ir para o Dashboard
        login_button = ttk.Button(
            self,
            text="Login",
            command=lambda: controller.show_frame("DashboardScreen")
        )
        login_button.pack(pady=20)
        
        # Botão para voltar para a tela inicial
        button_back = ttk.Button(
            self,
            text="Voltar para Início",
            command=lambda: controller.show_frame("HomeScreen")
        )
        button_back.pack(pady=10)
