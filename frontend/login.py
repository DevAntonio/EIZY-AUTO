import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Configuração do Canvas para a imagem de fundo ---
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Carrega a imagem de fundo
        image_path = os.path.join("assets", "bc02.png")
        
        # Mantém referências da imagem
        self.bg_image_pil = None
        self.bg_image_tk = None

        # Listener para redimensionamento
        self.canvas.bind("<Configure>", self.resize_background)

        # --- Estilos ---
        style = ttk.Style(self)
        BG_COLOR = "#3c2a52"  # Cor de fundo do frame de login
        FONT_COLOR = "white"

        style.configure("Login.TFrame", background=BG_COLOR)
        style.configure("Login.TLabel", background=BG_COLOR, foreground=FONT_COLOR, font=("Arial", 10))
        style.configure("Login.TButton", background="#5a417a", foreground=FONT_COLOR, font=("Arial", 10, "bold"))
        style.map("Login.TButton", background=[('active', '#7b59a6')])
        style.configure("Login.TEntry", fieldbackground="white", foreground="black")

        # --- Frame de Login Central ---
        self.login_frame = ttk.Frame(self, style="Login.TFrame", padding=(20, 20, 20, 20))

        # --- Widgets dentro do Frame ---
        # Usuário
        user_label = ttk.Label(self.login_frame, text="Nome de Usuário:", style="Login.TLabel")
        user_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.user_entry = ttk.Entry(self.login_frame, style="Login.TEntry", width=30)
        self.user_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Senha
        pass_label = ttk.Label(self.login_frame, text="Senha:", style="Login.TLabel")
        pass_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.pass_entry = ttk.Entry(self.login_frame, show="*", style="Login.TEntry")
        self.pass_entry.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        
        # Botão de mostrar senha
        self.show_pass_button = ttk.Button(self.login_frame, text="Show", style="Login.TButton", command=self.toggle_password)
        self.show_pass_button.grid(row=3, column=1, sticky="e", padx=(5,0))
        self.login_frame.grid_columnconfigure(0, weight=1)

        # Botões de ação
        cancel_button = ttk.Button(self.login_frame, text="Cancel", style="Login.TButton", command=lambda: controller.show_frame("HomeScreen"))
        cancel_button.grid(row=4, column=0, sticky="ew", padx=(0, 5))
        
        login_button = ttk.Button(self.login_frame, text="Login", style="Login.TButton", command=lambda: controller.show_frame("DashboardScreen"))
        login_button.grid(row=4, column=1, sticky="ew", padx=(5, 0))

        # Carrega a imagem de fundo
        try:
            if os.path.exists(image_path):
                self.bg_image_pil = Image.open(image_path)
            else:
                self.bg_image_pil = Image.new('RGB', (600, 400), color='#2c1a42')
                from PIL import ImageDraw
                draw = ImageDraw.Draw(self.bg_image_pil)
                draw.text((10, 10), "Imagem 'assets/bc02.png' não encontrada", fill="white")
        except Exception as e:
            print(f"Erro ao carregar a imagem de login: {e}")
            self.bg_image_pil = Image.new('RGB', (600, 400), color='#2c1a42')

    def toggle_password(self):
        """Alterna a visibilidade da senha no campo de entrada."""
        if self.pass_entry.cget('show') == '*':
            self.pass_entry.config(show='')
            self.show_pass_button.config(text='Hide')
        else:
            self.pass_entry.config(show='*')
            self.show_pass_button.config(text='Show')


    def resize_background(self, event):
        """Redimensiona a imagem de fundo e centraliza o frame de login."""
        if not self.bg_image_pil:
            return

        new_width, new_height = event.width, event.height
        
        resized_pil = self.bg_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(resized_pil)
        
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        
        # Centraliza o frame de login
        self.canvas.create_window(new_width / 2, new_height / 2, 
                                  anchor="center", window=self.login_frame)

        