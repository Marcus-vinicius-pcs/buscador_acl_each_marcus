import argparse
import json
import re
from pathlib import Path

from acl_anthology import Anthology


ANO_INICIAL = 2021
ANO_FINAL = 2026


def corresponde_a_string(texto):
    """Aplica os quatro blocos da string de busca ao título e ao resumo."""
    # Cada variável abaixo representa um bloco ligado por AND na string original.
    # Dentro de cada expressão regular, o caractere | representa OR.
    sentimento = (
        re.search(r"\bsentiment\b", texto, re.IGNORECASE)
        and re.search(r"\b(analysis|classification)\b", texto, re.IGNORECASE)
    ) or re.search(r"\bopinion\s+mining\b", texto, re.IGNORECASE)

    mercado = re.search(
        r"\b(stock\s+market\w*|financial\s+market\w*|stock\s+price\w*|stock\s+return\w*)",
        texto,
        re.IGNORECASE,
    )
    previsao = re.search(r"\b(predict\w*|forecast\w*)", texto, re.IGNORECASE)
    microblog = re.search(
        r"\b(x|twitter|tweet\w*|microblog\w*)\b", texto, re.IGNORECASE
    )

    return bool(sentimento and mercado and previsao and microblog)


def main():
    parser = argparse.ArgumentParser(
        description="Busca artigos da revisão em título e resumo no ACL Anthology."
    )
    parser.add_argument("--anthology-dir", default="acl-anthology")
    parser.add_argument("--output", default="results/acl.json")
    args = parser.parse_args()

    pasta_dados = Path(args.anthology_dir) / "data"
    if not pasta_dados.is_dir():
        parser.error(f"Pasta do ACL Anthology não encontrada: {pasta_dados}")

    anthology = Anthology(datadir=str(pasta_dados))
    resultados = []

    for artigo in anthology.papers():
        titulo = artigo.title.as_text() if artigo.title else ""
        resumo = artigo.abstract.as_text() if artigo.abstract else ""
        ano = int(artigo.year)
        idioma = artigo.language

        if not ANO_INICIAL <= ano <= ANO_FINAL:
            continue

        # A ACL nem sempre informa o idioma; nesses casos o artigo fica para triagem manual.
        if idioma and not idioma.lower().startswith(("en", "eng", "pt", "por")):
            continue

        if not corresponde_a_string(f"{titulo}\n{resumo}"):
            continue

        eventos = artigo.get_events()
        resultados.append(
            {
                "source": "ACL Anthology",
                "year": ano,
                "language": idioma,
                "title": titulo,
                "authors": [
                    f"{autor.first} {autor.last}".strip()
                    for autor in artigo.authors
                    if autor.first or autor.last
                ],
                "venue": str(eventos[0].title) if eventos else "",
                "doi": artigo.doi or "",
                "url": artigo.web_url,
                "abstract": resumo,
            }
        )

    arquivo_saida = Path(args.output)
    arquivo_saida.parent.mkdir(parents=True, exist_ok=True)
    arquivo_saida.write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"{len(resultados)} registros gravados em {arquivo_saida}")


if __name__ == "__main__":
    main()
