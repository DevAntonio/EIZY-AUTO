import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, filedialog
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import openpyxl
from models.vendas import Venda
from models.produtos import Produto

class VendasPage(tk.Frame):
    def __init__(self, parent, show_dashboard_callback, show_produtos_callback):
        super().__init__(parent, bg="#2a0a4a")
        self.parent = parent
        self.show_dashboard_callback = show_dashboard_callback
        self.show_produtos_callback = show_produtos_callback
        self.create_widgets()

    def create_widgets(self):
        # --- Frame Principal ---
        main_frame = tk.Frame(self, bg="#2a0a4a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Cabeçalho ---
        header_frame = tk.Frame(main_frame, bg="#2a0a4a")
        header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(header_frame, text="EIZY - AUTO", font=("Helvetica", 24, "bold"), fg="white", bg="#2a0a4a").pack(side="left")
        tk.Canvas(header_frame, width=30, height=30, bg="white", highlightthickness=0, borderwidth=0).pack(side="right")

        # --- Conteúdo (Menu Lateral e Área Principal) ---
        content_frame = tk.Frame(main_frame, bg="#2a0a4a")
        content_frame.pack(fill="both", expand=True)

        # --- Menu Lateral ---
        side_menu = tk.Frame(content_frame, bg="#2a0a4a", width=150)
        side_menu.pack(side="left", fill="y", padx=(0, 20))
        
        btn_style = {"font": ("Helvetica", 12), "bg": "#1c0730", "fg": "white", "relief": "flat", "width": 15, "pady": 5}
        active_btn_style = {"font": ("Helvetica", 12, "bold"), "bg": "white", "fg": "black", "relief": "flat", "width": 15, "pady": 5}

        tk.Button(side_menu, text="Home", **btn_style, command=self.show_dashboard_callback).pack(pady=5)
        tk.Button(side_menu, text="PRODUTOS", **btn_style, command=self.show_produtos_callback).pack(pady=5)
        tk.Button(side_menu, text="VENDAS", **active_btn_style).pack(pady=5)

        # --- Área de Conteúdo Principal ---
        main_content_frame = tk.Frame(content_frame, bg="#2a0a4a")
        main_content_frame.pack(side="left", fill="both", expand=True)

        # --- Botões de Ação (Excel, PDF, Novo) ---
        action_buttons_frame = tk.Frame(main_content_frame, bg="#2a0a4a")
        action_buttons_frame.pack(fill="x", pady=(0, 10), anchor="ne")

        action_btn_style = {"font": ("Helvetica", 12), "bg": "#1c0730", "fg": "white", "relief": "flat", "width": 10, "pady": 5}

        tk.Button(action_buttons_frame, text="EXCEL", **action_btn_style, command=self.generate_excel).pack(side="left", padx=5)
        tk.Button(action_buttons_frame, text="PDF", **action_btn_style, command=self.generate_pdf).pack(side="left", padx=5)
        tk.Button(action_buttons_frame, text="NOVO", **action_btn_style, command=self.open_new_sale_modal).pack(side="left", padx=5)

        # --- Tabela de Vendas ---
        columns = ("dia", "produto", "quantidade", "total")
        self.tree = ttk.Treeview(main_content_frame, columns=columns, show="headings", height=15)

        self.tree.heading("dia", text="DIA")
        self.tree.heading("produto", text="PRODUTO")
        self.tree.heading("quantidade", text="QUANTIDADE")
        self.tree.heading("total", text="TOTAL")

        self.tree.column("dia", anchor="center", width=120)
        self.tree.column("produto", anchor="center", width=200)
        self.tree.column("quantidade", anchor="center", width=100)
        self.tree.column("total", anchor="center", width=120)

        self.tree.pack(fill="both", expand=True)
        self.load_sales()

    def load_sales(self):
        """Carrega e exibe as vendas do banco de dados na tabela."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        sales_data = Venda.get_all()
        for sale in sales_data:
            formatted_total = f"{sale['subtotal']:.2f} R$"
            self.tree.insert("", "end", values=(sale['data_venda'], sale['nome'], sale['quantidade'], formatted_total))

    def open_new_sale_modal(self):
        """Abre um modal para adicionar uma nova venda."""
        modal = Toplevel(self)
        modal.title("Nova Venda")
        modal.geometry("400x300")
        modal.configure(bg="#1c0730")
        modal.transient(self)
        modal.grab_set()

        tk.Label(modal, text="Produto:", fg="white", bg="#1c0730", font=("Helvetica", 12)).pack(pady=(10,0))
        
        # Dropdown para produtos
        product_list = Produto.get_list()
        product_map = {f"{p['nome']} (R$ {p['preco']:.2f})": p for p in product_list}
        product_names = list(product_map.keys())
        
        selected_product_str = tk.StringVar()
        product_dropdown = ttk.Combobox(modal, textvariable=selected_product_str, values=product_names, state="readonly")
        product_dropdown.pack(pady=5, padx=20, fill="x")

        tk.Label(modal, text="Quantidade:", fg="white", bg="#1c0730", font=("Helvetica", 12)).pack(pady=(10,0))
        quantidade_entry = tk.Entry(modal, font=("Helvetica", 12))
        quantidade_entry.pack(pady=5, padx=20, fill="x")

        def save_sale():
            selected_product_name = selected_product_str.get()
            if not selected_product_name:
                messagebox.showerror("Erro", "Por favor, selecione um produto.", parent=modal)
                return
            
            try:
                quantidade = int(quantidade_entry.get())
                if quantidade <= 0: raise ValueError
            except (ValueError, TypeError):
                messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.", parent=modal)
                return

            selected_product_data = product_map[selected_product_name]
            
            # Lógica para criar e salvar a venda
            cliente_nome = "Cliente Padrão" # Pode ser um campo no futuro
            subtotal = quantidade * selected_product_data['preco']
            
            items = [{
                'id_produto': selected_product_data['id_produto'],
                'quantidade': quantidade,
                'preco_unitario': selected_product_data['preco'],
                'subtotal': subtotal
            }]

            Venda.create(cliente_nome, subtotal, items)
            
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!", parent=modal)
            self.load_sales() # Recarrega a lista de vendas na tela principal
            modal.destroy()

        save_button = tk.Button(modal, text="Salvar Venda", command=save_sale, bg="#5a2e8e", fg="white", font=("Helvetica", 12, "bold"))
        save_button.pack(pady=20)

    def generate_pdf(self):
        """Gera um PDF com os dados da tabela de vendas."""
        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Documents", "*.pdf")])
        if not filepath:
            return

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("Relatório de Vendas", styles['Title']))
        
        data = [self.tree.heading(c)["text"] for c in self.tree["columns"]]
        table_data = [data]
        for row_id in self.tree.get_children():
            table_data.append(self.tree.item(row_id)["values"])

        table = Table(table_data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5a2e8e")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmokey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#2a0a4a")),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.white)
        ])
        table.setStyle(style)
        
        elements.append(table)
        doc.build(elements)
        messagebox.showinfo("Sucesso", f"Relatório PDF salvo em:\n{filepath}")

    def generate_excel(self):
        """Gera uma planilha Excel com os dados da tabela de vendas."""
        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not filepath:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Relatório de Vendas"

        headers = [self.tree.heading(c)["text"] for c in self.tree["columns"]]
        sheet.append(headers)

        for row_id in self.tree.get_children():
            sheet.append(self.tree.item(row_id)["values"])

        workbook.save(filepath)
        messagebox.showinfo("Sucesso", f"Relatório Excel salvo em:\n{filepath}")

