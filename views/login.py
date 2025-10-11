import tkinter as tk
from tkinter import font, messagebox
from db.database import check_credentials # Importa a função de verificação

try:
    from PIL import Image, ImageTk
except ImportError:
    raise ImportError("A biblioteca 'Pillow' é necessária. Instale com: pip install Pillow")

class LoginPage(tk.Frame):
    def __init__(self, parent, show_home_callback, show_dashboard_callback):
        super().__init__(parent)
        self.parent = parent
        self.show_home_callback = show_home_callback
        self.show_dashboard_callback = show_dashboard_callback

        self.password_visible = tk.BooleanVar(value=False)
        self.create_widgets()

    def create_widgets(self):
        try:
            image_path = "image_0cf980.jpg"
            original_image = Image.open(image_path)
            resized_image = original_image.resize((1024, 576), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(self, image=self.bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            self.configure(bg="#2a0a4a")

        login_frame = tk.Frame(self, bg="#1c0730", bd=2, relief="solid")
        login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.35, relheight=0.4)

        self.email_entry = tk.Entry(login_frame, font=("Helvetica", 12), relief="flat", bg="white", fg="black")
        self.email_entry.insert(0, "vendedor@gmail.com")
        self.email_entry.place(relx=0.5, rely=0.2, anchor="center", relwidth=0.8, relheight=0.15)

        self.password_entry = tk.Entry(login_frame, font=("Helvetica", 12), relief="flat", bg="white", fg="black", show="*")
        self.password_entry.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8, relheight=0.15)

        show_button = tk.Button(
            login_frame, text="Show", font=("Helvetica", 9, "bold"),
            bg="white", fg="black", activebackground="white", relief="flat",
            cursor="hand2", command=self.toggle_password_visibility
        )
        show_button.place(relx=0.86, rely=0.4, anchor="center", relwidth=0.15, relheight=0.15)

        cancel_button = tk.Button(
            login_frame, text="Cancel", font=("Helvetica", 12), bg="#3e1a66",
            fg="white", activebackground="#2a0a4a", relief="flat", cursor="hand2",
            command=self.show_home_callback
        )
        cancel_button.place(relx=0.3, rely=0.75, anchor="center", relwidth=0.3, relheight=0.18)

        login_button = tk.Button(
            login_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#5a2e8e",
            fg="white", activebackground="#4a1e7e", relief="flat", cursor="hand2",
            command=self.on_login_click
        )
        login_button.place(relx=0.7, rely=0.75, anchor="center", relwidth=0.3, relheight=0.18)

    def toggle_password_visibility(self):
        if self.password_visible.get():
            self.password_entry.config(show="*")
            self.password_visible.set(False)
        else:
            self.password_entry.config(show="")
            self.password_visible.set(True)

    def on_login_click(self):
        """Função chamada pelo botão 'Login' que agora verifica no banco de dados."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if check_credentials(email, password):
            # Se as credenciais estiverem corretas, vai para o dashboard
            self.show_dashboard_callback()
        else:
            # Caso contrário, exibe uma mensagem de erro
            messagebox.showerror("Erro de Login", "E-mail ou senha incorretos.")

