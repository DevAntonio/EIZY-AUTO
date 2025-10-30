# utils.py
import sys
import os

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funcionando em dev e no PyInstaller """
    try:
        # PyInstaller cria uma pasta temp e guarda o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # _MEIPASS não está definido, rodando em modo de desenvolvimento
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)