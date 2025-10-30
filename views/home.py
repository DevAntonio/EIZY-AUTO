# views/home.py
import tkinter as tk
from tkinter import font
from utils import resource_path
try:
    from PIL import Image, ImageTk
except ImportError:
    # Lança um erro mais claro se o Pillow não estiver instalado
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
        
        # --- Variáveis para guardar referências ---
        self.original_image = None # Guarda a imagem original (para redimensionar)
        self.bg_image_tk = None # Guarda a imagem no formato do Tkinter
        self.canvas = None
        
        # Referências para os itens do canvas que precisam ser movidos
        self.canvas_bg_item = None
        self.canvas_text_eizy = None
        self.canvas_text_auto = None
        self.entrar_button = None
        self.canvas_button_window = None
        
        # Chama o método para criar os componentes da interface
        self.create_widgets()

    def create_widgets(self):
        # --- Canvas para Imagem e Texto ---
        # Usamos um Canvas para poder desenhar o texto SOBRE a imagem
        # Removemos o tamanho fixo para que ele possa expandir
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            # Carrega a imagem de fundo.
            # Assumindo que 'assets/bc01.jpg' é a imagem do foguete com fundo roxo,
            # mas SEM o texto "EIZY AUTO".
            image_path = resource_path("assets/bc01.jpg") 
            self.original_image = Image.open(image_path) # Salva a imagem original
            
        except FileNotFoundError:
            # Se a imagem não for encontrada, exibe uma mensagem de erro
            print(f"Erro: Imagem '{image_path}' não encontrada. Verifique o caminho.")
            self.configure(bg="#2a0a4a") # Cor de fundo alternativa (roxo escuro)
            self.canvas.configure(bg="#2a0a4a") # Define o fundo do canvas também
            error_label = tk.Label(
                self,
                text=f"Erro: Imagem '{image_path}' não encontrada.",
                fg="white", bg="#2a0a4a", font=("Helvetica", 16)
            )
            # Adiciona o texto de erro ao Canvas
            self.canvas.create_window(512, 100, window=error_label)
            self.original_image = None # Define como None para evitar erros no resize
            
        except Exception as e:
            # Captura outros erros do Pillow (ex: formato inválido)
            print(f"Erro ao carregar imagem: {e}")
            self.configure(bg="#2a0a4a")
            self.canvas.configure(bg="#2a0a4a")
            error_label = tk.Label(
                self,
                text="Erro ao carregar imagem de fundo.",
                fg="white", bg="#2a0a4a", font=("Helvetica", 16)
            )
            self.canvas.create_window(512, 100, window=error_label)
            self.original_image = None # Define como None

        # --- Cria os Itens do Canvas (sem posição ou com posição inicial) ---
        
        # Cria o item da imagem de fundo (vazio por enquanto)
        self.canvas_bg_item = self.canvas.create_image(0, 0, anchor="nw")

        # Define a fonte para o título (o tamanho será ajustado no on_resize)
        self.title_font = font.Font(family="Helvetica", size=48, weight="bold")
        
        # Cria o texto "EIZY"
        self.canvas_text_eizy = self.canvas.create_text(
            1024 * 0.25, 576 * 0.4,
            text="EIZY",
            font=self.title_font,
            fill="white"
        )

        # Cria o texto "AUTO"
        self.canvas_text_auto = self.canvas.create_text(
            1024 * 0.75, 576 * 0.4,
            text="AUTO",
            font=self.title_font,
            fill="white"
        )

        # --- Botão "Entrar" (Estilo do Protótipo) ---
        button_font = font.Font(family="Helvetica", size=10)
        self.entrar_button = tk.Button(
            self, # O botão deve ser filho do 'self' (o Frame) para o create_window
            text="Entrar",
            font=button_font,
            bg="#1c0730",
            fg="white",
            activebackground="#2a0a4a",
            activeforeground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground="white",
            highlightcolor="white",
            cursor="hand2",
            command=self.on_enter_click
        )
        
        # Adiciona o botão ao Canvas usando create_window
        self.canvas_button_window = self.canvas.create_window(
            1024 * 0.93, 576 * 0.89,
            anchor="center",
            window=self.entrar_button,
            width=1024 * 0.1,
            height=576 * 0.08
        )
        
        # --- Bind do Evento <Configure> ---
        # Chama self.on_resize sempre que o tamanho do Canvas mudar
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Chamado quando a janela é redimensionada."""
        w = event.width
        h = event.height
        
        # Proteção contra tamanhos nulos (acontece brevemente na inicialização)
        if w < 2 or h < 2:
            return

        # 1. Redimensiona a Imagem de Fundo
        if self.original_image:
            # Redimensiona a imagem original para o novo tamanho da janela
            resized_image = self.original_image.resize((w, h), Image.Resampling.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(resized_image)
            
            # Atualiza a imagem no item do canvas
            self.canvas.itemconfig(self.canvas_bg_item, image=self.bg_image_tk)

        # 2. Redimensiona a Fonte (opcional, mas melhora a aparência)
        # Ajusta o tamanho da fonte proporcionalmente à altura
        new_font_size = max(10, int(h / 12)) # Ex: 576 / 12 = 48
        self.title_font.configure(size=new_font_size)
        
        # Atualiza a fonte nos itens de texto
        self.canvas.itemconfig(self.canvas_text_eizy, font=self.title_font)
        self.canvas.itemconfig(self.canvas_text_auto, font=self.title_font)

        # 3. Reposiciona os Textos
        self.canvas.coords(self.canvas_text_eizy, w * 0.25, h * 0.4)
        self.canvas.coords(self.canvas_text_auto, w * 0.75, h * 0.4)

        # 4. Reposiciona e Redimensiona o Botão
        self.canvas.coords(self.canvas_button_window, w * 0.93, h * 0.89)
        self.canvas.itemconfigure(self.canvas_button_window, width=(w * 0.1), height=(h * 0.08))


    def on_enter_click(self):
        """Função chamada pelo botão 'Entrar' para trocar para a tela de login."""
        self.show_login_callback()

