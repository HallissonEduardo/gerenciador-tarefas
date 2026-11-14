import tkinter as tk
from tkinter import messagebox
from controller import TarefaController
from model import TarefaModel
from repository import JsonTarefaRepository, PersistenceError
from view import TarefaTkinterView



def main() -> int:

    try:
        model = TarefaModel(JsonTarefaRepository())

    except PersistenceError as error:
        mensagem = f"Erro de persistência ao iniciar o gerenciador: {error}"
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro de persistência", mensagem, parent=root)
        root.destroy()
        return 1

    root = tk.Tk()
    controller = TarefaController(model)
    view = TarefaTkinterView(controller, root)
    view.iniciar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
