import tkinter as tk
from tkinter import messagebox, ttk
from controller import TarefaControllerError, TarefaControllerPort


class TarefaTkinterView:

    def __init__(self, controller: TarefaControllerPort, root: tk.Tk) -> None:
        self.controller = controller
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("720x480")
        self.root.minsize(560, 360)
        self._criar_widgets()
        self._atualizar_listas()


    def iniciar(self) -> None:
        self.root.mainloop()


    def _criar_widgets(self) -> None:
        conteudo = ttk.Frame(self.root, padding=16)
        conteudo.pack(fill=tk.BOTH, expand=True)
        conteudo.columnconfigure(0, weight=1)
        conteudo.rowconfigure(2, weight=1)

        ttk.Label(
            conteudo,
            text="Gerenciador de Tarefas",
            font=("TkDefaultFont", 16, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))

        entrada_frame = ttk.Frame(conteudo)
        entrada_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        entrada_frame.columnconfigure(0, weight=1)

        self.entrada_tarefa = ttk.Entry(entrada_frame)
        self.entrada_tarefa.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.entrada_tarefa.bind("<Return>", self._adicionar_tarefa)

        ttk.Button(
            entrada_frame,text="Adicionar",command=self._adicionar_tarefa).grid(row=0, column=1)

        listas_frame = ttk.Frame(conteudo)
        listas_frame.grid(row=2, column=0, sticky="nsew")

        for coluna in (0, 1):
            listas_frame.columnconfigure(coluna, weight=1, uniform="listas")
        listas_frame.rowconfigure(0, weight=1)

        self.lista_pendentes = self._criar_lista(listas_frame, "Tarefas Pendentes", 0)
        self.lista_concluidas = self._criar_lista(listas_frame, "Tarefas Concluidas", 1)

        ttk.Button(conteudo,text="Concluir tarefa selecionada",command=self._concluir_tarefa,).grid(row=3, column=0, sticky="w", pady=(12, 0))

        self.mensagem_status = tk.StringVar()
        ttk.Label(conteudo,textvariable=self.mensagem_status,anchor="w").grid(row=4, column=0, sticky="ew", pady=(8, 0))


    @staticmethod
    def _criar_lista(parent: ttk.Frame,titulo: str,coluna: int) -> tk.Listbox:

        frame = ttk.LabelFrame(parent, text=titulo, padding=8)
        frame.grid(
            row=0,column=coluna,sticky="nsew",padx=(0, 6) if coluna == 0 else (6, 0))

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        lista = tk.Listbox(frame, height=10, exportselection=False)
        lista.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=lista.yview)
        barra.grid(row=0, column=1, sticky="ns")
        lista.configure(yscrollcommand=barra.set)
        return lista


    def _atualizar_listas(self) -> None:
        tarefas = self.controller.obter_tarefas()
        self._preencher_lista(
            self.lista_pendentes,tarefas["Tarefas Pendentes"])

        self._preencher_lista(
            self.lista_concluidas,tarefas["Tarefas Concluidas"])


    @staticmethod
    def _preencher_lista(lista: tk.Listbox, tarefas: list[str]) -> None:
        lista.delete(0, tk.END)

        for tarefa in tarefas:
            lista.insert(tk.END, tarefa)

    def _adicionar_tarefa(self, _evento: tk.Event | None = None) -> None:
        tarefa = self.entrada_tarefa.get().strip()

        if not tarefa:
            messagebox.showwarning("Tarefa vazia","Digite uma tarefa antes de adicionar.",parent=self.root)
            self.entrada_tarefa.focus_set()
            return

        try:
            adicionada = self.controller.adicionar_tarefa(tarefa)

        except TarefaControllerError as error:
            messagebox.showerror(
                "Erro de persistência",
                f"Não foi possível salvar a tarefa: {error}",parent=self.root)
            return


        if adicionada:
            self.entrada_tarefa.delete(0, tk.END)
            self._atualizar_listas()
            self.mensagem_status.set("Tarefa adicionada com sucesso.")




    def _concluir_tarefa(self) -> None:
        selecao = self.lista_pendentes.curselection()
        if not selecao:
            messagebox.showinfo(
                "Selecione uma tarefa","Selecione uma tarefa pendente para concluir.",parent=self.root)
            return

        tarefa = self.lista_pendentes.get(selecao[0])

        try:
            concluida = self.controller.concluir_tarefa(tarefa)

        except TarefaControllerError as error:
            messagebox.showerror(
                "Erro de persistência",
                f"Não foi possível concluir a tarefa: {error}",parent=self.root)
            return

        if concluida:
            self._atualizar_listas()
            self.mensagem_status.set("Tarefa concluida com sucesso.")

        else:
            self.mensagem_status.set(
                "A tarefa não foi encontrada na lista de pendentes."
            )
