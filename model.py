from typing import Protocol

from repository import TarefaRepository


class TarefaModelPort(Protocol):
    def adicionar_pendentes(self, tarefa: str) -> bool:
        ...

    def tarefa_concluida(self, concluir_tarefa: str) -> bool:
        ...

    def dicionario_tarefas(self) -> dict[str, list[str]]:
        ...


class TarefaModel:
    """Mantém as tarefas e aplica as regras de negócio."""

    def __init__(self, repositorio: TarefaRepository) -> None:
        self._repositorio = repositorio
        dados = self._repositorio.carregar()
        self.tarefas_pendentes = dados["Tarefas Pendentes"]
        self.tarefas_concluidas = dados["Tarefas Concluidas"]

    def adicionar_pendentes(self, tarefa: str) -> bool:
        if not tarefa or not tarefa.strip():
            return False

        pendentes = [*self.tarefas_pendentes, tarefa]
        self._salvar(pendentes, self.tarefas_concluidas)
        self.tarefas_pendentes = pendentes
        return True

    def tarefa_concluida(self, concluir_tarefa: str) -> bool:
        if not concluir_tarefa or concluir_tarefa not in self.tarefas_pendentes:
            return False

        pendentes = self.tarefas_pendentes.copy()
        pendentes.remove(concluir_tarefa)
        concluidas = [*self.tarefas_concluidas, concluir_tarefa]
        self._salvar(pendentes, concluidas)
        self.tarefas_pendentes = pendentes
        self.tarefas_concluidas = concluidas
        return True

    def dicionario_tarefas(self) -> dict[str, list[str]]:
        return {
            "Tarefas Pendentes": self.tarefas_pendentes,
            "Tarefas Concluidas": self.tarefas_concluidas,
        }

    def _salvar(self, pendentes: list[str], concluidas: list[str]) -> None:
        self._repositorio.salvar({
            "Tarefas Pendentes": pendentes,
            "Tarefas Concluidas": concluidas,
        })
