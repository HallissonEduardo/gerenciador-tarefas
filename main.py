
from controller import TarefaController
from model import TarefaModel
from repository import JsonTarefaRepository, PersistenceError
from view import TarefaView


if __name__ == '__main__':
    try:
        model = TarefaModel(JsonTarefaRepository())
        view = TarefaView()
        TarefaController(model, view).iniciar()
    except PersistenceError as error:
        print(f"Erro de persistência ao iniciar o gerenciador: {error}")