import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from dados import DADOS_RESIDENCIAS, DADOS_IMOVEIS_DISPONIVEIS


def carregar_imagem_proporcional(path, largura_max, altura_max):
    try:
        imagem = Image.open(path)
        largura_original, altura_original = imagem.size
        proporcao = min(largura_max / largura_original, altura_max / altura_original)
        nova_largura = int(largura_original * proporcao)
        nova_altura = int(altura_original * proporcao)
        imagem = imagem.resize((nova_largura, nova_altura), Image.LANCZOS)
        return ImageTk.PhotoImage(imagem)
    except:
        return None


# TELA INICIAL

class TelaInicial(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Gerenciador de Aluguéis Residências",
                 font=("Arial", 20, "bold")).pack(pady=10)

        tk.Label(self, textvariable=controller.saldo_var,
                 font=("Arial", 14)).pack(pady=5)

        self.lista = tk.Listbox(self, height=10)
        self.lista.pack(fill="both", expand=True, padx=20, pady=10)
        self.lista.bind("<<ListboxSelect>>", self.mostrar_detalhes)

        self.nome = tk.StringVar()
        self.renda = tk.StringVar()
        self.endereco = tk.StringVar()
        self.situacao = tk.StringVar()

        frame_det = tk.Frame(self)
        frame_det.pack(pady=10)

        tk.Label(frame_det, text="Nome:").grid(row=0, column=0)
        tk.Label(frame_det, textvariable=self.nome).grid(row=0, column=1)

        tk.Label(frame_det, text="Renda:").grid(row=1, column=0)
        tk.Label(frame_det, textvariable=self.renda).grid(row=1, column=1)

        tk.Label(frame_det, text="Endereço:").grid(row=2, column=0)
        tk.Label(frame_det, textvariable=self.endereco).grid(row=2, column=1)

        tk.Label(frame_det, text="Situação:").grid(row=3, column=0)
        tk.Label(frame_det, textvariable=self.situacao).grid(row=3, column=1)

        tk.Button(self, text="Comprar Imóvel",
                  command=lambda: controller.show_frame("TelaImoveis")).pack(pady=5)

        tk.Button(self, text="Cadastrar Imóvel",
                  command=lambda: controller.show_frame("TelaCadastro")).pack()

    def atualizar(self):
        self.lista.delete(0, tk.END)
        for r in DADOS_RESIDENCIAS:
            self.lista.insert(tk.END, r["nome"])

    def mostrar_detalhes(self, event):
        try:
            index = self.lista.curselection()[0]
            r = DADOS_RESIDENCIAS[index]
            self.nome.set(r["nome"])
            self.renda.set(r["renda"])
            self.endereco.set(r["endereco"])
            self.situacao.set(r["situacao"])
        except:
            pass


# TELA LISTA DE IMÓVEIS

class TelaImoveis(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Button(self, text="Voltar",
                  command=lambda: controller.show_frame("TelaInicial")).pack(anchor="w", pady=5, padx=5)

        tk.Label(self, textvariable=controller.saldo_var,
                 font=("Arial", 12)).pack(anchor="e", padx=10)

        self.tree = ttk.Treeview(self, columns=("nome", "preco"), show="headings")
        self.tree.heading("nome", text="Imóvel")
        self.tree.heading("preco", text="Preço")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(self, text="Analisar",
                  command=self.abrir_detalhes).pack(pady=10)

    def atualizar(self):
        self.tree.delete(*self.tree.get_children())
        for im in DADOS_IMOVEIS_DISPONIVEIS:
            self.tree.insert("", tk.END,
                             values=(im["nome"], f"R$ {im['preco']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")))

    def abrir_detalhes(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um imóvel.")
            return

        nome = self.tree.item(sel[0])["values"][0]
        self.controller.frames["TelaDetalhes"].carregar(nome)
        self.controller.show_frame("TelaDetalhes")


# TELA DE DETALHES

class TelaDetalhes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.imagem_label = tk.Label(self, bg="lightgray")
        self.imagem_label.pack(pady=10)

        self.nome = tk.StringVar()
        self.renda = tk.StringVar()
        self.endereco = tk.StringVar()
        self.situacao = tk.StringVar()
        self.preco = tk.StringVar()

        frame = tk.Frame(self)
        frame.pack(pady=10)

        campos = [
            ("Nome", self.nome),
            ("Renda", self.renda),
            ("Endereço", self.endereco),
            ("Situação", self.situacao),
            ("Preço", self.preco),
        ]

        for i, (t, var) in enumerate(campos):
            tk.Label(frame, text=t + ":").grid(row=i, column=0, sticky="e")
            tk.Label(frame, textvariable=var).grid(row=i, column=1, sticky="w")

        tk.Label(self, textvariable=controller.saldo_var,
                 font=("Arial", 12)).pack(pady=10)

        tk.Button(self, text="Voltar",
                  command=lambda: controller.show_frame("TelaImoveis")).pack()

        tk.Button(self, text="Comprar",
                  command=self.comprar).pack(pady=10)

        self.imovel_atual = None

    def carregar(self, nome):
        for im in DADOS_IMOVEIS_DISPONIVEIS:
            if im["nome"] == nome:
                self.imovel_atual = im
                break

        if not self.imovel_atual:
            return

        im = self.imovel_atual

        self.nome.set(im["nome"])
        self.renda.set(im["renda"])
        self.endereco.set(im["endereco"])
        self.situacao.set(im["situacao"])
        self.preco.set(
            f"R$ {im['preco']:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        if im["imagem"]:
            img = carregar_imagem_proporcional(im["imagem"], 700, 500)
            self.imagem_label.config(image=img, text="")
            self.imagem_label.image = img
        else:
            self.imagem_label.config(text="[Sem Imagem]", image="", bg="lightgray")

    def comprar(self):
        im = self.imovel_atual
        if not im:
            return

        if im["situacao"].lower() != "disponivel":
            messagebox.showerror("Erro", "Este imóvel não está disponível para compra.")
            return

        if self.controller.saldo < im["preco"]:
            messagebox.showerror("Erro", "Saldo insuficiente!")
            return

        self.controller.diminuir_saldo(im["preco"])
        DADOS_RESIDENCIAS.append(im)
        DADOS_IMOVEIS_DISPONIVEIS.remove(im)

        messagebox.showinfo("Sucesso", "Imóvel comprado com sucesso!")
        self.controller.show_frame("TelaInicial")


# TELA DE CADASTRO

class TelaCadastro(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Button(self, text="Voltar",
                  command=lambda: controller.show_frame("TelaInicial")
                 ).pack(anchor="w", padx=10, pady=10)

        tk.Label(self, text="Cadastro de Novo Imóvel",
                 font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = tk.Frame(self)
        form_frame.pack()

        vcmd_num = (self.register(lambda v: v.replace(".", "").replace(",", "").isdigit() or v == ""), "%P")

        self.nome = tk.Entry(form_frame, width=40)
        self.renda = tk.Entry(form_frame, width=40, validate="key", validatecommand=vcmd_num)
        self.endereco = tk.Entry(form_frame, width=40)

        self.situacao = ttk.Combobox(
            form_frame,
            width=37,
            state="readonly",
            values=["alugado", "disponivel", "manutenção", "comprado"]
        )
        self.situacao.current(1)

        self.preco = tk.Entry(form_frame, width=40, validate="key", validatecommand=vcmd_num)
        self.imagem = None

        campos = [
            ("Nome", self.nome),
            ("Renda Mensal", self.renda),
            ("Endereço", self.endereco),
            ("Situação", self.situacao),
            ("Preço", self.preco),
        ]

        for i, (label, widget) in enumerate(campos):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            widget.grid(row=i, column=1, padx=5, pady=5)

        tk.Button(self, text="Carregar Imagem",
                  command=self.selecionar_imagem).pack(pady=5)

        tk.Button(self, text="Salvar Imóvel",
                  command=self.salvar).pack(pady=10)

    def selecionar_imagem(self):
        path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg"), ("Todos", "*.*")]
        )
        if path:
            self.imagem = path
            messagebox.showinfo("Sucesso", "Imagem carregada com sucesso!")

    def salvar(self):
        try:
            preco = float(self.preco.get().replace(",", "."))
            renda = float(self.renda.get().replace(",", "."))
        except:
            messagebox.showerror("Erro", "Use apenas números em Renda Mensal e Preço.")
            return

        situacao = self.situacao.get().lower()
        if situacao not in ["alugado", "disponivel", "manutenção", "comprado"]:
            messagebox.showerror("Erro", "Situação inválida.")
            return

        novo = {
            "nome": self.nome.get(),
            "renda": renda,
            "endereco": self.endereco.get(),
            "situacao": situacao,
            "preco": preco,
            "imagem": self.imagem
        }

        DADOS_IMOVEIS_DISPONIVEIS.append(novo)

        messagebox.showinfo("Sucesso", "Imóvel cadastrado!")
        self.controller.show_frame("TelaImoveis")
