import tkinter as tk
from tkinter import ttk
from frontend.home import HomeScreen, PageOne
from frontend.login import LoginScreen
from frontend.dashboard import DashboardScreen
from frontend.vendas import VendasScreen
from frontend.produtos import ProdutosScreen
from db.db import init_db

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EIZY AUTO - Sistema de Gestão")
        self.geometry("1200x800")
        
        # Inicializa o banco de dados
        init_db()
        
        # Container para as telas
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # Adicionando as telas
        for F in (HomeScreen, PageOne, LoginScreen, DashboardScreen, VendasScreen, ProdutosScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("DashboardScreen")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()