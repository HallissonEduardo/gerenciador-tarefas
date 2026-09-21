
class TarefaModel:

    """
Essa é a classe do TarefaModel, tem o objetivo e apenas armazenar os dados fornecidos na classe TarefaView;
e passados pela classe TarefaController.
    """

    def __init__(self):
        self.tarefas_pendentes: list = []   # CRIEI DUAS LISTAS A PRIMEIRA CONTEM AS TAREFAS PENDENTES.
        self.tarefas_concluidas: list = [] # A SEGUNDA CONTEM TODAS AS TAREFAS CONCLUIDAS.


    def adicionar_pendentes(self, tarefa) -> bool:
        self.tarefa_limpa = tarefa # RECEBE A TAREFA PENDENTE PASSADA NO PELA CLASSE VIEW E ENTREGUE PELO CONTROLLER

        if not self.tarefa_limpa: # VALIDA SE TAREFA EXISTE
            return False

        self.tarefas_pendentes.append(self.tarefa_limpa) # ADICIONA TAREFA A LISTA TAREFAS_PENDENTES.
        return True


    def tarefa_concluida(self, concluir_tarefa) -> bool:
        self.concluir_tarefa = concluir_tarefa # RECEBE A TAREFA QUE FICARA COMO CONCLUIDA

        if not self.concluir_tarefa: # VALIDA SE TAREFA EXISTE
            return False

        # CORRECAO: SO MOVE PARA CONCLUIDAS SE A TAREFA REALMENTE EXISTIR EM PENDENTES.
        # ANTES O APPEND ESTAVA FORA DO IF, ENTAO QUALQUER TEXTO INVENTADO VIRAVA "CONCLUIDO".
        if self.concluir_tarefa not in self.tarefas_pendentes:
            return False

        self.tarefas_pendentes.remove(self.concluir_tarefa) # REMOVE DA LISTA DE PENDENTES
        self.tarefas_concluidas.append(self.concluir_tarefa) # E EM SEGUIDA ADICIONA NA LISTA DE CONCLUIDAS
        return True


    def dicionario_tarefas(self) -> dict:
        dados = {
            "Tarefas Pendentes": self.tarefas_pendentes,
            "Tarefas Concluidas": self.tarefas_concluidas
        }

        return dados # RETORNA OS DADOS DAS DUAS LISTAS SALVAS EM UM DICIONARIO.


