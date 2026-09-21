


class TarefaView:


    def interface(self) -> None:
        print("\n--Gerenciador De Tarefas---")
        print("1-Adicionar Tarefa")
        print("2-Listar Tarefas")
        print("3-Concluir Tarefas")
        print("4-Sair")


    def pedir_dados(self, mensagem) -> str:
        return input(mensagem).strip() # CORRECAO: A ANOTACAO ERA -> None, MAS O METODO SEMPRE RETORNOU str


    def exibir_mensagem(self, msg) -> None:
        # CORRECAO: ANTES USAVA input(), O QUE OBRIGAVA O USUARIO A APERTAR ENTER A CADA CONFIRMACAO.
        # EXIBIR MENSAGEM SO PRECISA IMPRIMIR.
        print(msg)


    def adicionar_texto_tarefa(self, mensagem) -> str:
        return input(mensagem).strip()


    def listar_tarefas(self, pendentes, concluidas) -> None:
    # LISTA TODAS AS TAREFAS ARMAZENADAS NO MODEL E PROCESSAS E ENTREGUES PELO CONTROLLER.

        print("\nTarefas Pendentes:")

        if not pendentes: # VALIDA SE EXISTE TAREFAS PENDENTES
            print("Não tem tarefas pendentes")

        else:
            for pendente in pendentes: # LAÇO DE REPETIÇÃO "FOR" PERCORRE A LISTA DE PENDENTES E RETORNA A LISTA
                print(pendente)

        print("\nTarefas Concluidas:")

        if not concluidas:
            print("Não tem tarefas concluidas")

        else:
            for concluida in concluidas:
                print(concluida)

