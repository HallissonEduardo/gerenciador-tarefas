from model import TarefaModelPort
from repository import PersistenceError
from view import TarefaViewPort


class TarefaController:
    def __init__(
        self,
        model: TarefaModelPort,
        view: TarefaViewPort,
    ) -> None:
        self.model = model
        self.view = view

    def iniciar(self) -> None:
        while True:
            self.view.interface()
            opcao = self.view.pedir_dados("\nDigite o número referente a opção desejada:")

            match opcao:
                case "1":
                    tarefa = self.view.adicionar_texto_tarefa("\nQual tarefa quer adicionar:")
                    try:
                        adicionada = self.model.adicionar_pendentes(tarefa)
                    except PersistenceError as error:
                        self.view.exibir_mensagem(f"\nErro de persistência: {error}")
                    else:
                        if adicionada:
                            self.view.exibir_mensagem("\nTarefa adicionada com sucesso")
                        else:
                            self.view.exibir_mensagem("\nTarefa vazia, nada foi adicionado")
                case "2":
                    dados = self.model.dicionario_tarefas()
                    self.view.listar_tarefas(
                        dados["Tarefas Pendentes"],
                        dados["Tarefas Concluidas"],
                    )
                case "3":
                    tarefa = self.view.adicionar_texto_tarefa(
                        "\nQual tarefa quer marcar como concluida:"
                    )
                    try:
                        concluida = self.model.tarefa_concluida(tarefa)
                    except PersistenceError as error:
                        self.view.exibir_mensagem(f"\nErro de persistência: {error}")
                    else:
                        if concluida:
                            self.view.exibir_mensagem("\nTarefa concluida com sucesso")
                        else:
                            self.view.exibir_mensagem(
                                "\nTarefa não encontrada na lista de pendentes"
                            )
                case "4":
                    self.view.exibir_mensagem("\nSaindo do Gerenciador de Tarefas")
                    return
                case _:
                    self.view.exibir_mensagem("\nValor invalido")