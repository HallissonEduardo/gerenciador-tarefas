from model import TarefaModel
from view import TarefaView



class TarefaController:

    """
Classe TarefaController responsavel por processar os dados, e fazer a ligação entre Model e View.
    """

    def __init__(self):
        self.model = TarefaModel()
        self.view = TarefaView()


    def dicionario(self):
        self.listas = self.model.dicionario_tarefas()
        return self.listas


    def iniciar(self):

        while True:

            self.view.interface()
            self.opcao = self.view.pedir_dados("\nDigite o número referente a opção desejada:")


            match self.opcao:

                case "1":

                    self.novo_tarefa = self.view.adicionar_texto_tarefa("\nQual tarefa quer adicionar:")

                    if self.model.adicionar_pendentes(self.novo_tarefa): # AGORA O MODEL CONFIRMA SE GRAVOU
                        self.view.exibir_mensagem("\nTarefa adicionada com sucesso")
                    else:
                        self.view.exibir_mensagem("\nTarefa vazia, nada foi adicionado")

                case "2":

                    dados = self.model.dicionario_tarefas()

                    lista_pendentes = dados["Tarefas Pendentes"]

                    lista_concluidas = dados["Tarefas Concluidas"]

                    self.view.listar_tarefas(lista_pendentes, lista_concluidas)

                case "3":

                    self.concluir_tarefa = self.view.adicionar_texto_tarefa("\nQual tarefa quer marcar como concluida:")

                    # CORRECAO: SO AVISA SUCESSO SE A TAREFA EXISTIA MESMO EM PENDENTES
                    if self.model.tarefa_concluida(self.concluir_tarefa):
                        self.view.exibir_mensagem("\nTarefa concluida com sucesso")
                    else:
                        self.view.exibir_mensagem("\nTarefa não encontrada na lista de pendentes")

                case "4":
                    self.view.exibir_mensagem("\nSaindo do Gerenciador de Tarefas")
                    return False

                case _:
                    self.view.exibir_mensagem("\nValor invalido")