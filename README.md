# Buscador ACL — Mestrado

Busca em título e resumo no ACL Anthology usando a string canônica da revisão:

```text
(("sentiment" AND ("analysis" OR "classification")) OR "opinion mining")
AND ("stock market*" OR "financial market*" OR "stock price*" OR "stock return*")
AND (predict* OR forecast*)
AND ("X" OR Twitter OR tweet* OR microblog*)
```

Filtros aplicados:

- publicação entre 2021 e 2026, inclusive;
- inglês ou português;
- registros sem metadado de idioma são mantidos para verificação manual;
- busca somente em título e resumo.

O programa está concentrado em um único arquivo, `buscar_acl.py`. Ele adapta a estratégia de recuperação de Wesley Pompeu Carvalho, mas refaz o comparador para preservar a estrutura booleana e as expressões compostas da string acima.

## Como funciona

1. Carrega os metadados da cópia local do ACL Anthology.
2. Verifica período e idioma.
3. Aplica os quatro blocos da string ao título e ao resumo.
4. Grava os registros encontrados em JSON.

Na expressão regular, `|` significa "ou", `\s+` separa as palavras de uma expressão e `\w*` representa o curinga `*` da string.

## Preparação

Requer Python 3.12 ou superior e uma cópia local do ACL Anthology:

```powershell
git clone https://github.com/acl-org/acl-anthology.git
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Execução

```powershell
.venv\Scripts\python.exe buscar_acl.py
```

Por padrão, o programa lê `acl-anthology/data` e grava `results/acl.json`. Caminhos alternativos podem ser informados:

```powershell
.venv\Scripts\python.exe buscar_acl.py --anthology-dir C:\caminho\acl-anthology --output C:\caminho\acl.json
```

## Testes

```powershell
.venv\Scripts\python.exe -m unittest -v
```

Código original usado como referência: https://github.com/wes-carvalho/emotion_ibov_usp_each/blob/5f316dc280b690191544b8125ee8554789782997/systematic%20review/retireve_acl_papers.py
