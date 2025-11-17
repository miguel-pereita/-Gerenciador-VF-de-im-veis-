import tkinter as tk
from tkinter import ttk, messagebox
from dados import DADOS_RESIDENCIAS, DADOS_IMOVEIS_DISPONIVEIS

class TelaInicial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1) 
        topo_frame = tk.Frame(self)
        topo_frame.pack(fill="x", pady=10)

        tk.Label(topo_frame, text="Gerenciador de Aluguéis Residências", font=('Arial', 18, 'bold')).pack(side="left", padx=20)
        tk.Label(topo_frame, textvariable=controller.saldo_var, font=('Arial', 12)).pack(side="right", padx=20)
        
        
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        main_frame.grid_columnconfigure(0, weight=1) 
        main_frame.grid_columnconfigure(1, weight=2) 
        main_frame.grid_rowconfigure(0, weight=1)
        
        lista_frame = tk.LabelFrame(main_frame, text="Residências Cadastradas")
        lista_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        lista_frame.grid_rowconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(0, weight=1)
        
        self.lista_residencias = tk.Listbox(lista_frame, height=10)
        self.lista_residencias.pack(side="left", fill="both", expand=True)
        self.lista_residencias.bind('<<ListboxSelect>>', self.mostrar_detalhes)
        
        scrollbar = tk.Scrollbar(lista_frame, command=self.lista_residencias.yview)
        scrollbar.pack(side="right", fill="y")
        self.lista_residencias.config(yscrollcommand=scrollbar.set)

        self.atualizar_lista_residencias()


        detalhes_frame = tk.LabelFrame(main_frame, text="Detalhes")
        detalhes_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        detalhes_frame.grid_columnconfigure(1, weight=1) 
        

        tk.Label(detalhes_frame, text="[Imagem]", width=20, height=10, bg='lightgray').grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="n")
        self.nome_var = tk.StringVar(value="---")
        self.renda_var = tk.StringVar(value="---")
        self.endereco_var = tk.StringVar(value="---")
        self.situacao_var = tk.StringVar(value="---")
        
        tk.Label(detalhes_frame, text="Nome da Residência:").grid(row=0, column=1, sticky="w", pady=2, padx=5)
        tk.Label(detalhes_frame, textvariable=self.nome_var, font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky="w", pady=2)
        
        tk.Label(detalhes_frame, text="Renda Mensal:").grid(row=1, column=1, sticky="w", pady=2, padx=5)
        tk.Label(detalhes_frame, textvariable=self.renda_var).grid(row=1, column=2, sticky="w", pady=2)
        
        tk.Label(detalhes_frame, text="Endereço:").grid(row=2, column=1, sticky="w", pady=2, padx=5)
        tk.Label(detalhes_frame, textvariable=self.endereco_var, wraplength=200, justify="left").grid(row=2, column=2, sticky="w", pady=2)
        
        tk.Label(detalhes_frame, text="Situação:").grid(row=3, column=1, sticky="w", pady=2, padx=5)
        tk.Label(detalhes_frame, textvariable=self.situacao_var).grid(row=3, column=2, sticky="w", pady=2)

        tk.Button(main_frame, text="adquirir imóvel", command=lambda: controller.show_frame("TelaImoveis")).grid(row=1, column=1, sticky="se", padx=10, pady=10)

    def atualizar_lista_residencias(self):
        """Preenche a Listbox com os dados de residências."""
        self.lista_residencias.delete(0, tk.END)
        for residencia in DADOS_RESIDENCIAS:
            self.lista_residencias.insert(tk.END, residencia["nome"])

    def mostrar_detalhes(self, event):
        """Atualiza os campos de detalhes ao selecionar um item na lista."""
        try:
            indice_selecionado = self.lista_residencias.curselection()[0]
            residencia = DADOS_RESIDENCIAS[indice_selecionado]
            
            self.nome_var.set(residencia["nome"])
            self.renda_var.set(residencia["renda"])
            self.endereco_var.set(residencia["endereco"])
            self.situacao_var.set(residencia["situacao"])
        except IndexError:
            self.nome_var.set("Nenhuma Residência Selecionada")
            self.renda_var.set("---")
            self.endereco_var.set("---")
            self.situacao_var.set("---")


class TelaImoveis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        topo_frame = tk.Frame(self)
        topo_frame.pack(fill="x", pady=10, padx=20)
        
        tk.Button(topo_frame, text="voltar", command=lambda: controller.show_frame("TelaInicial")).pack(side="left")
        tk.Label(topo_frame, textvariable=controller.saldo_var, font=('Arial', 12)).pack(side="right")
        
        
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.treeview = ttk.Treeview(main_frame, columns=('Nome'), show='headings', selectmode='browse')
        self.treeview.heading('Nome', text='Imóveis Disponíveis', anchor='w')
        self.treeview.column('Nome', width=300, anchor='w')
        self.treeview.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        self.atualizar_lista_imoveis()
        
        
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill="x", pady=10, padx=20)
        
        tk.Button(bottom_frame, text="analisar", command=self.analisar_imovel_selecionado).pack(side="right")
        
    def atualizar_lista_imoveis(self):
        """Preenche o Treeview com os dados de imóveis disponíveis."""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
            
        for imovel in DADOS_IMOVEIS_DISPONIVEIS:
            self.treeview.insert('', tk.END, values=(f"[Imagem] {imovel['nome']}"), tags=(imovel["nome"]))
    
    def analisar_imovel_selecionado(self):
        """Simula a abertura da tela de detalhes."""
        selecao = self.treeview.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um imóvel para analisar.")
            return

        item = self.treeview.item(selecao[0], 'values')
        nome_imovel = item[0].replace("[Imagem] ", "")
        
        messagebox.showinfo("Análise", f"Abrindo tela de detalhes para: {nome_imovel}")