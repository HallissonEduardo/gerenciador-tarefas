from typing import Protocol
from model import TarefaModelPort
from repository import PersistenceError



class TarefaControllerPort(Protocol):
    def adicionar_tarefa(self, tarefa: str) -> bool:
        ...

    def concluir_tarefa(self, tarefa: str) -> bool:
        ...

    def obter_tarefas(self) -> dict[str, list[str]]:
        ...


class TarefaControllerError(Exception):

    """
        Indica que uma operação de tarefa não pôde ser concluída.
    """


class TarefaController:

    def __init__(self, model: TarefaModelPort) -> None:
        self.model = model


    def adicionar_tarefa(self, tarefa: str) -> bool:
        try:
            return self.model.adicionar_pendentes(tarefa)

        except PersistenceError as error:
            raise TarefaControllerError(str(error)) from error


    def concluir_tarefa(self, tarefa: str) -> bool:
        try:
            return self.model.tarefa_concluida(tarefa)

        except PersistenceError as error:
            raise TarefaControllerError(str(error)) from error


    def obter_tarefas(self) -> dict[str, list[str]]:
        return self.model.dicionario_tarefas()
