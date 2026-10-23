import json
import os
import tempfile
from pathlib import Path
from typing import Protocol


class PersistenceError(Exception):
    """Indica falhas ao carregar ou salvar as tarefas persistidas."""


class TarefaRepository(Protocol):
    def carregar(self) -> dict[str, list[str]]:
        ...

    def salvar(self, dados: dict[str, list[str]]) -> None:
        ...


class JsonTarefaRepository:
    """Lê e grava as tarefas em um arquivo JSON."""

    _CHAVES = ("Tarefas Pendentes", "Tarefas Concluidas")

    def __init__(self, arquivo: str | Path | None = None) -> None:
        self.arquivo = Path(arquivo) if arquivo is not None else Path(__file__).parent / "tarefas.json"

    def carregar(self) -> dict[str, list[str]]:
        if not self.arquivo.exists():
            return {chave: [] for chave in self._CHAVES}

        try:
            dados = json.loads(self.arquivo.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise PersistenceError(f"não foi possível carregar '{self.arquivo}': {error}") from error

        if not isinstance(dados, dict):
            raise PersistenceError(f"o conteúdo de '{self.arquivo}' deve ser um objeto JSON.")

        tarefas: dict[str, list[str]] = {}
        for chave in self._CHAVES:
            valores = dados.get(chave, [])
            if not isinstance(valores, list) or not all(isinstance(item, str) for item in valores):
                raise PersistenceError(
                    f"a propriedade '{chave}' em '{self.arquivo}' deve ser uma lista de textos."
                )
            tarefas[chave] = valores
        return tarefas

    def salvar(self, dados: dict[str, list[str]]) -> None:
        if any(
            not isinstance(dados.get(chave), list)
            or not all(isinstance(item, str) for item in dados[chave])
            for chave in self._CHAVES
        ):
            raise PersistenceError("os dados das tarefas devem conter listas de textos.")

        arquivo_temporario: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.arquivo.parent,
                prefix=f".{self.arquivo.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporario:
                arquivo_temporario = Path(temporario.name)
                json.dump(dados, temporario, ensure_ascii=False, indent=4)
                temporario.flush()
                os.fsync(temporario.fileno())

            if arquivo_temporario is None:
                raise OSError("o arquivo temporário não foi criado.")
            os.replace(arquivo_temporario, self.arquivo)
        except (OSError, TypeError, ValueError) as error:
            if arquivo_temporario is not None:
                try:
                    arquivo_temporario.unlink(missing_ok=True)
                except OSError as cleanup_error:
                    raise PersistenceError(
                        f"falha ao salvar '{self.arquivo}' e ao remover o arquivo temporário "
                        f"'{arquivo_temporario}': {cleanup_error}"
                    ) from error
            raise PersistenceError(f"não foi possível salvar '{self.arquivo}': {error}") from error
