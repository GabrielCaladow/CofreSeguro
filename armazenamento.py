import os

pasta_dados = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dados"
)

arquivo_credenciais = os.path.join(
    pasta_dados,
    "credenciais.csv"
)

campos_credenciais = [
    "servico",
    "usuario",
    "senha",
    "categoria",
    "observacoes",
    "data_alteracao"
]


def carregar_credenciais():
    if not os.path.exists(arquivo_credenciais):
        return []

    with open(arquivo_credenciais, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    if not linhas:
        return []

    cabecalho = linhas[0].strip().split(";")
    credenciais = []

    for linha in linhas[1:]:
        valores = linha.strip().split(";")

        if len(valores) != len(cabecalho):
            continue

        credencial = {}

        for i in range(len(cabecalho)):
            credencial[cabecalho[i]] = valores[i]

        # Garante os campos novos em registros antigos
        for campo in campos_credenciais:
            if campo not in credencial:
                credencial[campo] = ""

        credenciais.append(credencial)

    return credenciais


def salvar_credenciais(credenciais):
    os.makedirs(pasta_dados, exist_ok=True)

    with open(arquivo_credenciais, "w", encoding="utf-8") as arquivo:
        arquivo.write(";".join(campos_credenciais) + "\n")

        for credencial in credenciais:
            valores = []

            for campo in campos_credenciais:
                valor = str(credencial.get(campo, ""))
                valores.append(valor)

            arquivo.write(";".join(valores) + "\n")


def carregar_categorias():
    arquivo_categorias = os.path.join(
        pasta_dados,
        "categorias.csv"
    )

    if not os.path.exists(arquivo_categorias):
        return []

    with open(arquivo_categorias, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    if not linhas:
        return []

    cabecalho = linhas[0].strip().split(";")
    categorias = []

    for linha in linhas[1:]:
        valores = linha.strip().split(";")

        if len(valores) != len(cabecalho):
            continue

        categoria = {}

        for i in range(len(cabecalho)):
            categoria[cabecalho[i]] = valores[i]

        categorias.append(categoria)

    return categorias


def salvar_categorias(categorias):
    os.makedirs(pasta_dados, exist_ok=True)

    arquivo_categorias = os.path.join(
        pasta_dados,
        "categorias.csv"
    )

    campos = ["nome", "forca_minima"]

    with open(arquivo_categorias, "w", encoding="utf-8") as arquivo:
        arquivo.write(";".join(campos) + "\n")

        for categoria in categorias:
            valores = []

            for campo in campos:
                valor = str(categoria.get(campo, ""))
                valores.append(valor)

            arquivo.write(";".join(valores) + "\n")