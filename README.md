 Criei esse repositorio com o intuito de praticar o relacionamento entre objetos, separei em três modulos, contendo model, view e controller e o modulo main que e o bootloader, os modulos contem as classes TarefaModel, TarefaView e TarefaController (com  esses nomes ficou mais facil de fixar) a classe TarefaView nao se comunica diretamente com aTarefaModel.    

TarefaModel não sabe da existencia de TarefaView, elas interagem atraves da  classe Tarefacontroller, que é responsavel pela relacao entre as demais.


TarefaModel é responsavel pelo armazenamento de dados.  

Tarefaview respoosavel pela interacao com o usuario, mostra as informacoes aramazenadas em TarefaModel e passadas pelo Tarefacontroller. 

TarefaController responsavel pela relacao das classes de model e view.

Vou evoluindo o projeto para praticar o desenvolvimento de projetos em poo python na branch develop. tenho planos de adicionar tkinter no view e add persistencia com json no model.


