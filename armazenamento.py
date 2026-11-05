
# Responsável: Gabriel Calado | Função 2 (Dados): ler e gravar os arquivos .csv de credenciais e categorias (sem o módulo csv).

import os

pasta_dados = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")
arquivo_credenciais = os.path.join(pasta_dados, "credenciais.csv")


def carregar_credenciais():
    if not os.path.exists(arquivo_credenciais):
        return []

    credenciais = []

    with open(arquivo_credenciais, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    if not linhas:
        return []

    cabecalho = linhas[0].strip().split(";")

    for linha in linhas[1:]:
        valores = linha.strip().split(";")

        if len(valores) != len(cabecalho):
            continue

        credencial = {}

        for i in range(len(cabecalho)):
            credencial[cabecalho[i]] = valores[i]

        credenciais.append(credencial)

    return credenciais


def salvar_credenciais(credenciais):
    os.makedirs(pasta_dados, exist_ok=True)

    if not credenciais:
        with open(arquivo_credenciais, "w", encoding="utf-8") as arquivo:
            arquivo.write("")
        return

    cabecalho = list(credenciais[0].keys())

    with open(arquivo_credenciais, "w", encoding="utf-8") as arquivo:
        arquivo.write(";".join(cabecalho) + "\n")

        for credencial in credenciais:
            valores = []

            for campo in cabecalho:
                valor = str(credencial.get(campo, ""))
                valores.append(valor)

            arquivo.write(";".join(valores) + "\n")
