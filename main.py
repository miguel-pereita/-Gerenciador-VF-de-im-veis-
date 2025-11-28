import tkinter as tk
from telas import TelaInicial, TelaImoveis, TelaDetalhes, TelaCadastro

class GerenciadorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Aluguéis Residências")
        self.geometry("900x650")

        self.saldo = 1000000  
        self.saldo_var = tk.StringVar()
        self.atualizar_saldo()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (TelaInicial, TelaImoveis, TelaDetalhes, TelaCadastro):
            page_name = F.__name__
            frame = F(parent=container, controller=self)

            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TelaInicial")

    def atualizar_saldo(self):
        self.saldo_var.set(f"Saldo: R$ {self.saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    def diminuir_saldo(self, valor):
        self.saldo -= valor
        self.atualizar_saldo()

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


        if hasattr(frame, "atualizar"):
            frame.atualizar()


if __name__ == "__main__":
    app = GerenciadorApp()
    app.mainloop()
