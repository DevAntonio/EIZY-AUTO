# views/vendas.py
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, filedialog
from datetime import date
from models.vendas import Venda
from models.produtos import Produto # Importa o modelo Produto para pegar a lista

# Importações para PDF e Excel
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False
    print("Aviso: 'reportlab' não encontrado. Geração de PDF desabilitada. Instale com: pip install reportlab")

try:
    import openpyxl
    OPENPYXL_OK = True
except ImportError:
    OPENPYXL_OK = False
    print("Aviso: 'openpyxl' não encontrado. Geração de Excel desabilitada. Instale com: pip install openpyxl")


class VendasPage(tk.Frame):
    def __init__(self, parent, show_dashboard_callback, show_produtos_callback):
        super().__init__(parent, bg="#2a0a4a")
        self.parent = parent
        self.show_dashboard_callback = show_dashboard_callback
        self.show_produtos_callback = show_produtos_callback
        
        self.tree = None # Placeholder para a tabela
        
        self.create_widgets()

    def create_widgets(self):
        # --- Frame Principal ---
        main_frame = tk.Frame(self, bg="#2a0a4a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Cabeçalho ---
        header_frame = tk.Frame(main_frame, bg="#2a0a4a")
        header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(header_frame, text="EIZY - AUTO", font=("Helvetica", 24, "bold"), fg="white", bg="#2a0a4a").pack(side="left")
        tk.Canvas(header_frame, width=30, height=30, bg="white", highlightthickness=0, borderwidth=0).pack(side="right") # Ícone de perfil

        # --- Conteúdo (Menu Lateral e Área Principal) ---
        content_frame = tk.Frame(main_frame, bg="#2a0a4a")
        content_frame.pack(fill="both", expand=True)

        # --- Menu Lateral ---
        side_menu = tk.Frame(content_frame, bg="#2a0a4a", width=150)
        side_menu.pack(side="left", fill="y", padx=(0, 20))
        
        btn_style = {"font": ("Helvetica", 12), "bg": "#1c0730", "fg": "white", "relief": "flat", "width": 15, "pady": 5, "cursor": "hand2"}
        active_btn_style = {"font": ("Helvetica", 12, "bold"), "bg": "white", "fg": "black", "relief": "flat", "width": 15, "pady": 5, "cursor": "hand2"}

        tk.Button(side_menu, text="Home", **btn_style, command=self.show_dashboard_callback).pack(pady=5)
        tk.Button(side_menu, text="PRODUTOS", **btn_style, command=self.show_produtos_callback).pack(pady=5)
        tk.Button(side_menu, text="VENDAS", **active_btn_style).pack(pady=5) # Botão ativo

        # --- Área de Conteúdo Principal ---
        main_content_frame = tk.Frame(content_frame, bg="#2a0a4a")
        main_content_frame.pack(side="left", fill="both", expand=True)

        # --- Botões de Ação (Excel, PDF, Novo) ---
        action_buttons_frame = tk.Frame(main_content_frame, bg="#2a0a4a")
        action_buttons_frame.pack(fill="x", pady=(0, 10), anchor="ne")

        action_btn_style = {"font": ("Helvetica", 12), "bg": "#1c0730", "fg": "white", "relief": "flat", "width": 10, "pady": 5, "cursor": "hand2"}

        tk.Button(action_buttons_frame, text="EXCEL", **action_btn_style, command=self.generate_excel).pack(side="left", padx=5)
        tk.Button(action_buttons_frame, text="PDF", **action_btn_style, command=self.generate_pdf).pack(side="left", padx=5)
        tk.Button(action_buttons_frame, text="NOVO", **action_btn_style, command=self.open_new_sale_modal).pack(side="left", padx=5)

        # --- Estilo da Tabela ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1c0730",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#1c0730",
                        bordercolor="#5a2e8e",
                        borderwidth=1,
                        relief="solid")
        style.map('Treeview', background=[('selected', '#3e1a66')])
        style.configure("Treeview.Heading",
                        background="#5a2e8e",
                        foreground="white",
                        font=("Helvetica", 10, "bold"),
                        relief="flat")
        style.map("Treeview.Heading",
                    background=[('active', '#3e1a66')])
                    
        # --- Tabela de Vendas ---
        columns = ("dia", "produto", "quantidade", "total")
        self.tree = ttk.Treeview(main_content_frame, columns=columns, show="headings", height=15)

        self.tree.heading("dia", text="DIA")
        self.tree.column("dia", anchor="center", width=120)
        
        self.tree.heading("produto", text="PRODUTO")
        self.tree.column("produto", anchor="w", width=200) # Alinhado à esquerda (w)
        
        self.tree.heading("quantidade", text="QUANTIDADE")
        self.tree.column("quantidade", anchor="center", width=100)
        
        self.tree.heading("total", text="TOTAL")
        self.tree.column("total", anchor="e", width=120) # Alinhado à direita (e)

        self.tree.pack(fill="both", expand=True)
        self.load_sales()

    def load_sales(self):
        """Carrega e exibe as vendas do banco de dados na tabela."""
        if not self.tree:
            return
            
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        try:
            sales_data = Venda.get_all()
            for sale in sales_data:
                # Formata o total para R$ 0,00
                formatted_total = f"R$ {sale['subtotal']:.2f}".replace(".", ",")
                self.tree.insert("", "end", values=(sale['data_venda'], sale['nome'], sale['quantidade'], formatted_total))
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar as vendas: {e}")

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
        try:
            product_list = Produto.get_list()
            # Mapeia o nome de exibição para os dados do produto
            self.product_map = {f"{p['nome']} (Estoque: {p['estoque']})": p for p in product_list if p['estoque'] > 0}
            product_names = list(self.product_map.keys())
            
            if not product_names:
                messagebox.showerror("Sem Estoque", "Não há produtos com estoque disponíveis para venda.", parent=modal)
                modal.destroy()
                return

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os produtos: {e}", parent=modal)
            modal.destroy()
            return
            
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
                messagebox.showerror("Erro", "Por favor, insira uma quantidade válida (número inteiro maior que 0).", parent=modal)
                return

            selected_product_data = self.product_map[selected_product_name]
            
            # Validação de estoque
            if quantidade > selected_product_data['estoque']:
                messagebox.showerror("Estoque Insuficiente", f"Estoque disponível para '{selected_product_data['nome']}': {selected_product_data['estoque']}.", parent=modal)
                return
                
            # Lógica para criar e salvar a venda
            cliente_nome = "Cliente Padrão" # Pode ser um campo no futuro
            subtotal = quantidade * selected_product_data['preco']
            
            items = [{
                'id_produto': selected_product_data['id_produto'],
                'quantidade': quantidade,
                'preco_unitario': selected_product_data['preco'],
                'subtotal': subtotal
            }]

            # Venda.create() agora retorna True/False
            success = Venda.create(cliente_nome, subtotal, items)
            
            if success:
                messagebox.showinfo("Sucesso", "Venda registrada com sucesso!", parent=modal)
                self.load_sales() # Recarrega a lista de vendas na tela principal
                modal.destroy()
            else:
                # O erro de estoque (ou outro erro de DB) será tratado pelo database.py
                messagebox.showerror("Erro no Banco", "Não foi possível registrar a venda. Verifique o console ou o estoque.", parent=modal)


        save_button = tk.Button(modal, text="Salvar Venda", command=save_sale, bg="#5a2e8e", fg="white", font=("Helvetica", 12, "bold"))
        save_button.pack(pady=20)

    def generate_pdf(self):
        """Gera um PDF com os dados da tabela de vendas."""
        if not REPORTLAB_OK:
            messagebox.showerror("Erro de Biblioteca", "A biblioteca 'reportlab' é necessária para gerar PDFs.")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Documents", "*.pdf")])
        if not filepath:
            return

        try:
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            elements.append(Paragraph("Relatório de Vendas", styles['Title']))
            
            # Cabeçalhos da tabela
            data = [self.tree.heading(c)["text"] for c in self.tree["columns"]]
            table_data = [data]
            
            # Dados das linhas
            for row_id in self.tree.get_children():
                table_data.append(self.tree.item(row_id)["values"])

            table = Table(table_data)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5a2e8e")), # Cor do Cabeçalho
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f0f0f0")), # Cor das linhas
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#5a2e8e")) # Cor da grade
            ])
            table.setStyle(style)
            
            elements.append(table)
            doc.build(elements)
            messagebox.showinfo("Sucesso", f"Relatório PDF salvo em:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro ao Gerar PDF", f"Ocorreu um erro: {e}")

    def generate_excel(self):
        """Gera uma planilha Excel com os dados da tabela de vendas."""
        if not OPENPYXL_OK:
            messagebox.showerror("Erro de Biblioteca", "A biblioteca 'openpyxl' é necessária para gerar arquivos Excel.")
            return
            
        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not filepath:
            return

        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Relatório de Vendas"

            # Adiciona os cabeçalhos
            headers = [self.tree.heading(c)["text"] for c in self.tree["columns"]]
            sheet.append(headers)

            # Adiciona os dados
            for row_id in self.tree.get_children():
                sheet.append(self.tree.item(row_id)["values"])

            workbook.save(filepath)
            messagebox.showinfo("Sucesso", f"Relatório Excel salvo em:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro ao Gerar Excel", f"Ocorreu um erro: {e}")
