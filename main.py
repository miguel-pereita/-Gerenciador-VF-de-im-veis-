import tkinter as tk
from telas import TelaInicial, TelaImoveis

class GerenciadorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Aluguéis Residências")
        self.geometry("800x600")
        self.saldo_var = tk.StringVar(value="R$: 100.000.000,00")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (TelaInicial, TelaImoveis):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TelaInicial")

    def show_frame(self, page_name):
        '''Mostra um frame específico na frente (faz a navegação)'''
        frame = self.frames[page_name]
        frame.tkraise()
        

        if page_name == "TelaInicial":
            if hasattr(frame, 'atualizar_lista_residencias'):
                frame.atualizar_lista_residencias()
        elif page_name == "TelaImoveis":
            if hasattr(frame, 'atualizar_lista_imoveis'):
                frame.atualizar_lista_imoveis()


if __name__ == "__main__":
    app = GerenciadorApp()
    app.mainloop()