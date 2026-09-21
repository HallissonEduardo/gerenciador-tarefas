import json
from pathlib import Path



class TarefaModel:

    """
    Essa é a classe do TarefaModel, tem o objetivo e apenas armazenar os dados fornecidos na classe TarefaView;
  e passados pela classe TarefaController.
Agora os dados tambem sao persistidos em um arquivo JSON, entao as tarefas sobrevivem ao fechamento do programa.
    """

    # CAMINHO PADRAO DO BANCO: FICA NA MESMA PASTA DOS MODULOS, INDEPENDENTE DE ONDE O SCRIPT FOR EXECUTADO.
    ARQUIVO_PADRAO = Path(__file__).parent / "tarefas.json"

    def __init__(self, arquivo=None):
        self.arquivo = Path(arquivo) if arquivo else self.ARQUIVO_PADRAO

        self.tarefas_pendentes: list = []   # CRIEI DUAS LISTAS A PRIMEIRA CONTEM AS TAREFAS PENDENTES.
        self.tarefas_concluidas: list = [] # A SEGUNDA CONTEM TODAS AS TAREFAS CONCLUIDAS.

        self.carregar() # AO INICIAR, JA TRAZ O QUE ESTAVA SALVO NO JSON.


    # ---------- PERSISTENCIA ----------

    def carregar(self) -> bool:
        # LE O JSON E PREENCHE AS DUAS LISTAS. SE O ARQUIVO NAO EXISTIR, COMECA VAZIO (PRIMEIRA EXECUCAO).
        if not self.arquivo.exists():
            return False

        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except (json.JSONDecodeError, OSError):
            # ARQUIVO CORROMPIDO OU SEM PERMISSAO DE LEITURA: NAO DERRUBA O PROGRAMA, SO IGNORA O CONTEUDO.
            return False

        # .get() COM LISTA VAZIA EVITA KeyError SE O JSON VIER INCOMPLETO.
        self.tarefas_pendentes = dados.get("Tarefas Pendentes", [])
        self.tarefas_concluidas = dados.get("Tarefas Concluidas", [])
        return True


    def salvar(self) -> bool:
        # GRAVA O DICIONARIO INTEIRO NO JSON. E CHAMADO SEMPRE QUE UMA LISTA MUDA.
        try:
            with open(self.arquivo, "w", encoding="utf-8") as f:
                # ensure_ascii=False MANTEM ACENTOS LEGIVEIS / indent=4 DEIXA O ARQUIVO LEGIVEL PARA HUMANOS.
                json.dump(self.dicionario_tarefas(), f, ensure_ascii=False, indent=4)
        except OSError:
            return False

        return True


    # ---------- REGRAS DE NEGOCIO ----------

    def adicionar_pendentes(self, tarefa) -> bool:
        self.tarefa_limpa = tarefa # RECEBE A TAREFA PENDENTE PASSADA NO PELA CLASSE VIEW E ENTREGUE PELO CONTROLLER

        if not self.tarefa_limpa: # VALIDA SE TAREFA EXISTE
            return False

        self.tarefas_pendentes.append(self.tarefa_limpa) # ADICIONA TAREFA A LISTA TAREFAS_PENDENTES.
        self.salvar() # PERSISTE A MUDANCA NO JSON.
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
        self.salvar() # PERSISTE A MUDANCA NO JSON.
        return True


    def dicionario_tarefas(self) -> dict:
        dados = {
            "Tarefas Pendentes": self.tarefas_pendentes,
            "Tarefas Concluidas": self.tarefas_concluidas
        }

        return dados # RETORNA OS DADOS DAS DUAS LISTAS SALVAS EM UM DICIONARIO.


