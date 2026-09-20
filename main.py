
from controller import TarefaController




if __name__ == '__main__':

    app = TarefaController()
    app.iniciar()




    """lista_tarefas = TarefaModel()
    lista_tarefas.adicionar_pendentes("A")
    print(lista_tarefas.tarefas_pendentes)
    lista_tarefas.adicionar_pendentes("B")
    lista_tarefas.adicionar_pendentes("C")
    lista_tarefas.tarefa_concluida("C")
    print(lista_tarefas.tarefas_pendentes)
    print(lista_tarefas.tarefas_concluidas)
    print(lista_tarefas.listar_tarefas())"""



    '''model = TarefaModel()
    view = TarefaView(model)
    model.adicionar_pendentes("A")
    model.adicionar_pendentes("B")

    view.interface()
    view.listar_tarefas(model)'''



    """model = TarefaModel()

    # 2. Injetamos o Modelo na View
    view = TarefaView(model)

    controller = TarefaController(view, model)

    # 3. Adicionamos dados no modelo
    model.adicionar_pendentes("Estudar Injeção de Dependências")
    model.adicionar_pendentes("Fazer o projeto principal")

    # Marcamos a primeira como concluída para testar a lógica
    model.tarefa_concluida("Estudar Injeção de Dependências")

    # 4. Usamos a View para exibir os dados do Modelo
    view.interface()
    view.listar_tarefas()"""