import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Configuração do Canvas para a imagem de fundo ---
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Carrega a imagem de fundo
        # Garanta que o caminho para a imagem esteja correto
        image_path = os.path.join("assets", "bc01.png")
        
        # Mantém uma referência da imagem para evitar que seja coletada pelo garbage collector
        self.bg_image_pil = None
        self.bg_image_tk = None

        # Adiciona um listener para quando o frame for redimensionado
        self.canvas.bind("<Configure>", self.resize_background)

        # --- Estilo para os widgets ---
        style = ttk.Style()
        # Estilo para os textos "EIZY" e "AUTO"
        style.configure("Home.TLabel", 
                        background="#2c1a42", # Cor de fundo aproximada da imagem
                        foreground="white", 
                        font=("Arial", 60, "bold"))
        
        # Estilo para o botão "Entrar"
        style.configure("Home.TButton", 
                        background="#1e122d",
                        foreground="white",
                        font=("Arial", 10, "bold"),
                        borderwidth=1)
        style.map("Home.TButton",
                  background=[('active', '#3a2556')])


        # --- Widgets ---
        # Adiciona os textos "EIZY" e "AUTO"
        self.eizy_label = ttk.Label(self, text="EIZY", style="Home.TLabel")
        self.auto_label = ttk.Label(self, text="AUTO", style="Home.TLabel")
        
        # Botão para ir para a tela de login
        self.login_button = ttk.Button(
            self,
            text="Entrar",
            style="Home.TButton",
            command=lambda: controller.show_frame("LoginScreen")
        )

        # Carrega a imagem de fundo pela primeira vez
        try:
            if os.path.exists(image_path):
                self.bg_image_pil = Image.open(image_path)
            else:
                # Cria uma imagem de fallback caso o arquivo não seja encontrado
                self.bg_image_pil = Image.new('RGB', (600, 400), color = '#2c1a42')
                # Adiciona texto de erro na imagem de fallback
                from PIL import ImageDraw
                draw = ImageDraw.Draw(self.bg_image_pil)
                draw.text((10, 10), "Imagem 'assets/bc01.png' não encontrada", fill="white")

        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")
            self.bg_image_pil = Image.new('RGB', (600, 400), color = '#2c1a42')


    def resize_background(self, event):
        """Redimensiona a imagem de fundo para preencher a janela."""
        if not self.bg_image_pil:
            return

        # Novas dimensões
        new_width = event.width
        new_height = event.height

        # Redimensiona a imagem PIL
        resized_pil = self.bg_image_pil.resize((new_width, new_height), Image.LANCZOS)
        
        # Converte para PhotoImage do Tkinter
        self.bg_image_tk = ImageTk.PhotoImage(resized_pil)
        
        # Atualiza a imagem no canvas
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        
        # Reposiciona os widgets sobre a imagem
        self.reposition_widgets(new_width, new_height)

    def reposition_widgets(self, width, height):
        """Reposiciona os widgets com base no novo tamanho da janela."""
        # Remove widgets antigos para evitar sobreposição
        self.canvas.delete("widgets")

        # Posiciona "EIZY" (aproximadamente 25% da largura)
        self.canvas.create_window(width * 0.25, height / 2, 
                                  anchor="center", window=self.eizy_label, tags="widgets")
        
        # Posiciona "AUTO" (aproximadamente 75% da largura)
        self.canvas.create_window(width * 0.75, height / 2, 
                                  anchor="center", window=self.auto_label, tags="widgets")
        
        # Posiciona o botão "Entrar" no canto inferior direito
        self.canvas.create_window(width - 60, height - 40, 
                                  anchor="center", window=self.login_button, tags="widgets")

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Página 1", font=("Arial", 20))
        label.pack(pady=20, padx=20)
        
        button = ttk.Button(
            self,
            text="Voltar para Início",
            command=lambda: controller.show_frame("HomeScreen")
        )
        button.pack(pady=10)
