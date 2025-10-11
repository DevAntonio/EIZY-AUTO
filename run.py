import tkinter as tk
import sys
import os
from db.database import init_db

# --- Adiciona a raiz do projeto ao Python Path ---
# Isso garante que os módulos em diretórios irmãos (como views e models)
# possam ser importados corretamente em qualquer parte do sistema.
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# ---------------------------------------------

from views.home import HomePage
from views.login import LoginPage
from views.dashboard import DashboardPage
from views.produtos import ProdutosPage
from views.vendas import VendasPage
from db.database import init_db

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        init_db()
        self.title("Eizy Auto")
        self.geometry("1024x576")
        self.resizable(False, False)

        self.home_page = HomePage(self, self.show_login)
        self.login_page = LoginPage(self, self.show_home, self.show_dashboard)
        self.dashboard_page = DashboardPage(self, self.show_home, self.show_produtos, self.show_vendas)
        self.produtos_page = ProdutosPage(self, self.show_dashboard, self.show_vendas)
        self.vendas_page = VendasPage(self, self.show_dashboard, self.show_produtos)

        self._current_frame = None
        self.show_home()

    def show_home(self):
        if self._current_frame: self._current_frame.pack_forget()
        self._current_frame = self.home_page
        self._current_frame.pack(fill="both", expand=True)

    def show_login(self):
        if self._current_frame: self._current_frame.pack_forget()
        self._current_frame = self.login_page
        self._current_frame.pack(fill="both", expand=True)

    def show_dashboard(self):
        if self._current_frame: self._current_frame.pack_forget()
        self._current_frame = self.dashboard_page
        self._current_frame.pack(fill="both", expand=True)

    def show_produtos(self):
        if self._current_frame: self._current_frame.pack_forget()
        self._current_frame = self.produtos_page
        self._current_frame.pack(fill="both", expand=True)

    def show_vendas(self):
        if self._current_frame: self._current_frame.pack_forget()
        self._current_frame = self.vendas_page
        self._current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

