# Gerenciador de Tarefas — Python + MVC

Aplicação de linha de comando (CLI) escrita em Python puro, sem dependências externas.
O objetivo é praticar o padrão **MVC**, separando
dados, interface e fluxo de controle em camadas independentes.

```bash
python main.py
```

Requisitos: Python 3.10 ou superior (por causa do `match/case`).

---

## Arquitetura

| Arquivo | Camada | Responsabilidade |
|---|---|---|
| `model.py` | Model | Guarda e manipula as tarefas. Não imprime nada. |
| `view.py` | View | Só `print()` e `input()`. Não decide nada. |
| `controller.py` | Controller | Traduz a escolha do usuário em chamadas ao Model e à View. |
| `main.py` | Entrada | Instancia o Controller e inicia o loop. |

Fluxo de uma operação (adicionar tarefa):

```
main → Controller.iniciar()
         ↓ pede o texto
       View.adicionar_texto_tarefa()  →  usuário digita
         ↓ repassa a string
       Model.adicionar_pendentes()    →  grava na lista
         ↓ confirma
       View.exibir_mensagem()         →  usuário lê
```

O ponto central: **a View nunca fala com o Model**. Toda troca passa pelo Controller.

---

## Model (`model.py`)

`TarefaModel` mantém duas listas em memória:

- `tarefas_pendentes` — tarefas ainda em aberto
- `tarefas_concluidas` — tarefas já finalizadas

| Método | O que faz |
|---|---|
| `adicionar_pendentes(tarefa)` | Rejeita string vazia e adiciona à lista de pendentes. |
| `tarefa_concluida(tarefa)` | Remove de pendentes e move para concluídas. |
| `dicionario_tarefas()` | Devolve as duas listas em um `dict`, pronto para leitura. |

Por que um dicionário no retorno? Porque a camada que consome não precisa conhecer
os atributos internos do objeto — ela recebe um pacote de dados já organizado.

---

## View (`view.py`)

`TarefaView` é a única camada que enxerga o terminal.

| Método | O que faz |
|---|---|
| `interface()` | Desenha o menu (1 a 4). |
| `pedir_dados(msg)` | Lê a opção escolhida, já com `.strip()`. |
| `adicionar_texto_tarefa(msg)` | Lê o texto da tarefa, já com `.strip()`. |
| `exibir_mensagem(msg)` | Mostra retorno ao usuário. |
| `listar_tarefas(pendentes, concluidas)` | Recebe as listas prontas e imprime cada uma. |

`listar_tarefas` recebe as listas como **parâmetro** — não vai buscá-las no Model.
É isso que mantém a View substituível: trocar o terminal por Tkinter ou por uma API web
exige reescrever só este arquivo.

---

## Controller (`controller.py`)

`TarefaController` instancia Model e View no construtor e roda um `while True` com
`match/case` sobre a opção digitada:

| Opção | Ação |
|---|---|
| 1 | Pede o texto → grava no Model → confirma na View |
| 2 | Busca o dicionário no Model → entrega as listas para a View imprimir |
| 3 | Pede o nome da tarefa → Model move de pendentes para concluídas |
| 4 | Encerra o loop |
| outro | Avisa que a opção é inválida |

O `match/case` substitui uma cadeia de `if/elif` e deixa o roteamento das opções
mais legível.

---

## Decisões de projeto

**Separação de responsabilidades.** A lógica de negócio vive no Model, isolada da
interface. Se amanhã este CLI virar uma tela gráfica, o Model continua intacto.

**Limpeza preventiva na entrada.** O `.strip()` aplicado no momento da leitura evita
que espaços em branco entrem como tarefa válida.

**Model sem estado externo.** Os dados existem só enquanto o programa roda. É uma
escolha consciente para manter o foco no padrão arquitetural, não em persistência.

---

## Futuras atualizacoes

Pontos já mapeados para evoluir o projeto:

1. **Injeção de dependências** — receber Model e View como parâmetros do Controller
   (`TarefaController(model, view)`) em vez de instanciá-los internamente. Facilita
   testes automatizados, permitindo passar dublês no lugar das classes reais.
2. **Persistência** — salvar as listas em JSON ou SQLite para os dados sobreviverem
   ao fechamento do programa.
3. **Seleção por índice** — concluir tarefas pelo número da lista em vez de digitar
   o texto exato.
4. **Testes** — cobrir o Model com `unittest` ou `pytest`, já que ele não depende de
   entrada e saída.
