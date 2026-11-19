import os

pasta_dados = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dados"
)

arquivo_credenciais = os.path.join(
    pasta_dados,
    "credenciais.csv"
)

arquivo_categorias = os.path.join(
    pasta_dados,
    "categorias.csv"
)

campos_credenciais = [
    "servico",
    "usuario",
    "senha",
    "categoria",
    "observacoes",
    "data_alteracao"
]

campos_categorias = ["nome", "forca_minima"]


def limpar_campo(texto):
    """Remove do texto os caracteres que quebrariam o formato do CSV."""
    # Se sobrar um ";" dentro de um campo, a linha ganha uma coluna a mais
    # e é descartada na próxima leitura, ou seja, o registro some.
    texto = str(texto)
    texto = texto.replace(";", ",")
    texto = texto.replace("\n", " ").replace("\r", " ")
    return texto.strip()


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

        # linha com mais ou menos colunas que o cabeçalho está corrompida
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
                valor = limpar_campo(credencial.get(campo, ""))
                valores.append(valor)

            arquivo.write(";".join(valores) + "\n")


def carregar_categorias():
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

    with open(arquivo_categorias, "w", encoding="utf-8") as arquivo:
        arquivo.write(";".join(campos_categorias) + "\n")

        for categoria in categorias:
            valores = []

            for campo in campos_categorias:
                valor = limpar_campo(categoria.get(campo, ""))
                valores.append(valor)

            arquivo.write(";".join(valores) + "\n")
