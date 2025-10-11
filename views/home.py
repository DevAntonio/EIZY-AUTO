import tkinter as tk
from tkinter import font

try:
    from PIL import Image, ImageTk
except ImportError:
    raise ImportError("A biblioteca 'Pillow' é necessária. Instale com: pip install Pillow")

# A classe HomePage herda de tk.Frame, um container para outros widgets.
class HomePage(tk.Frame):
    def __init__(self, parent, show_login_callback):
        """
        Inicializa a HomePage.
        :param parent: O widget pai (a janela principal da aplicação).
        :param show_login_callback: A função a ser chamada para mostrar a tela de login.
        """
        super().__init__(parent)
        self.parent = parent
        self.show_login_callback = show_login_callback
        # Chama o método para criar os componentes da interface
        self.create_widgets()

    def create_widgets(self):
        # --- Imagem de Fundo ---
        try:
            # Carrega a imagem de fundo.
            image_path = "image_0cfdbc.jpg"
            original_image = Image.open(image_path)
            resized_image = original_image.resize((1024, 576), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(self, image=self.bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            # Se a imagem não for encontrada, exibe uma mensagem de erro
            self.configure(bg="#2a0a4a") # Cor de fundo alternativa
            error_label = tk.Label(
                self,
                text="Erro: 'image_0cfdbc.jpg' não encontrado.",
                fg="white", bg="#2a0a4a", font=("Helvetica", 16)
            )
            error_label.pack(pady=50)

        # --- Botão "Entrar" ---
        button_font = font.Font(family="Helvetica", size=12)
        entrar_button = tk.Button(
            self,
            text="Entrar",
            font=button_font,
            bg="#1c0730",
            fg="white",
            activebackground="#2a0a4a",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            # O comando agora chama o callback para trocar de tela
            command=self.on_enter_click
        )
        entrar_button.place(relx=0.88, rely=0.85, relwidth=0.1, relheight=0.08)

    def on_enter_click(self):
        """Função chamada pelo botão 'Entrar' para trocar para a tela de login."""
        self.show_login_callback()

