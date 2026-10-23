 # Gerenciador de Tarefas — Python 

Aplicação de linha de comando em Python, sem dependências externas, para cadastrar,
listar e concluir tarefas. Os dados são persistidos em `tarefas.json`, localizado
na mesma pasta do projeto.

```bash
python main.py
```

Requisito: Python 3.10 ou superior, por causa do `match/case`.

## Arquitetura

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada; inicia o Controller e exibe falhas de carregamento. |
| `controller.py` | Coordena as ações do usuário entre Model e View. |
| `model.py` | Mantém o estado das tarefas e aplica as regras de negócio. |
| `repository.py` | Define o contrato do repositório e implementa a persistência JSON. |
| `view.py` | Apresenta o menu, recebe entrada e exibe resultados no terminal. |
| `tarefas.json` | Armazenamento persistente das tarefas. |

O fluxo continua no padrão MVC: a View não acessa o Model nem o repositório; o
Controller coordena a interação. O Model depende da abstração `TarefaRepository`,
em vez de implementar operações de arquivo, e `JsonTarefaRepository` fornece a
implementação usada por padrão.

## SOLID aplicado

- **Responsabilidade única (SRP):** regras das tarefas ficam no Model; leitura e
  gravação JSON ficam no repositório; interação com o terminal fica na View.
- **Aberto/fechado (OCP):** é possível adicionar outro repositório compatível com
  `TarefaRepository` sem alterar as regras do Model.
- **Substituição de Liskov (LSP):** qualquer implementação que cumpra o contrato
  `carregar()`/`salvar()` pode substituir o repositório JSON.
- **Segregação de interfaces (ISP):** o contrato do repositório contém apenas as
  operações necessárias para carregar e salvar tarefas.
- **Inversão de dependência (DIP):** o Model recebe o repositório por injeção; o
  Controller também permite receber Model e View, facilitando testes e substituições.

## Operações

- **Adicionar:** rejeita texto vazio ou composto apenas por espaços.
- **Listar:** exibe tarefas pendentes e concluídas.
- **Concluir:** move uma ocorrência da tarefa de pendentes para concluídas; uma
  tarefa que não exista na lista pendente não altera o estado.
- **Sair:** encerra o loop do menu.

As alterações são gravadas antes de atualizar o estado em memória. Se a gravação
falhar, a operação não é confirmada e as listas mantêm os valores anteriores.
Falhas de leitura, JSON malformado, conteúdo incompatível e falhas de gravação são
reportados como erros de persistência; o programa não os ignora silenciosamente.
Na primeira execução, se `tarefas.json` ainda não existir, o repositório começa
com listas vazias e cria o arquivo na primeira alteração bem-sucedida.

## Injeção de dependências

O Model pode receber um repositório alternativo:

```python
model = TarefaModel(repositorio=meu_repositorio)
controller = TarefaController(model=model, view=minha_view)
```

O ponto de entrada (`main.py`) monta os componentes concretos: Model com
`JsonTarefaRepository`, Controller e View do terminal. O Controller recebe os
contratos `TarefaModelPort` e `TarefaViewPort`; assim, testes podem injetar dublês
sem depender das implementações reais.
