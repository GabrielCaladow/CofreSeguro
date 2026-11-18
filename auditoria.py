# Responsável: João Felipe | Função 4 (Auditoria): gravar e consultar o log de auditoria.
# O log é um arquivo CSV (separado por ";") em que cada linha é uma operação:
#     data_hora;operacao;servico
# O arquivo só recebe novas linhas no final (modo "append"): o programa nunca
# edita nem apaga registros antigos. Por isso o log mostra o que foi FEITO,
# e não apenas o estado atual das credenciais.
# A senha NUNCA é gravada no log, apenas o nome do serviço afetado.

import os

from armazenamento import pasta_dados
from tempo import agora_texto

arquivo_log = os.path.join(pasta_dados, "auditoria.csv")

campos_log = ["data_hora", "operacao", "servico"]

OP_ADICIONAR = "ADICIONAR_CREDENCIAL"
OP_EDITAR = "EDITAR_CREDENCIAL"
OP_EXCLUIR = "EXCLUIR_CREDENCIAL"
OP_REVELAR = "REVELAR_SENHA"
OP_CADASTRAR_CATEGORIA = "CADASTRAR_CATEGORIA"
OP_EDITAR_CATEGORIA = "EDITAR_CATEGORIA"
OP_GERAR_RELATORIO = "GERAR_RELATORIO"
OP_GERAR_SENHA = "GERAR_SENHA"


def limpar_campo(texto):
    """Remove do texto os caracteres que quebrariam o formato do CSV."""
    texto = str(texto)
    texto = texto.replace(";", ",")
    texto = texto.replace("\n", " ").replace("\r", " ")
    return texto.strip()


def registrar_operacao(operacao, servico="-"):
    """Grava uma linha no log: data/hora, operação e serviço afetado.
    Retorna True se gravou e False se não foi possível gravar."""
    try:
        os.makedirs(pasta_dados, exist_ok=True)

        # Cria o cabeçalho apenas se o arquivo ainda não existe ou está vazio
        precisa_cabecalho = (
            not os.path.exists(arquivo_log)
            or os.path.getsize(arquivo_log) == 0
        )

        with open(arquivo_log, "a", encoding="utf-8") as arquivo:
            if precisa_cabecalho:
                arquivo.write(";".join(campos_log) + "\n")

            linha = [
                agora_texto(),
                limpar_campo(operacao),
                limpar_campo(servico) or "-"
            ]
            arquivo.write(";".join(linha) + "\n")

        return True

    except OSError:
        print("\nAVISO: não foi possível gravar no log de auditoria.")
        return False


def carregar_log():
    """Lê o arquivo de log e devolve uma lista de dicionários
    (do mais antigo para o mais recente)."""
    if not os.path.exists(arquivo_log):
        return []

    try:
        with open(arquivo_log, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except OSError:
        print("\nAVISO: não foi possível ler o log de auditoria.")
        return []

    registros = []

    # linhas[0] é o cabeçalho
    for linha in linhas[1:]:
        valores = linha.strip().split(";")

        if len(valores) != len(campos_log):
            continue  # ignora linhas corrompidas

        registro = {}

        for i in range(len(campos_log)):
            registro[campos_log[i]] = valores[i]

        registros.append(registro)

    return registros


def consultar_log(filtro_operacao="", filtro_servico=""):
    """Devolve os registros do log. Os filtros são opcionais e não
    diferenciam maiúsculas de minúsculas (busca por trecho do texto)."""
    filtro_operacao = filtro_operacao.strip().lower()
    filtro_servico = filtro_servico.strip().lower()

    resultado = []

    for registro in carregar_log():
        if filtro_operacao and filtro_operacao not in registro["operacao"].lower():
            continue

        if filtro_servico and filtro_servico not in registro["servico"].lower():
            continue

        resultado.append(registro)

    return resultado


def formatar_log(registros):
    """Monta o texto do log em formato de tabela, pronto para imprimir."""
    linhas = []
    linhas.append("=== LOG DE AUDITORIA ===")
    linhas.append("")

    if not registros:
        linhas.append("Nenhum registro encontrado.")
        return "\n".join(linhas)

    largura_operacao = max(len(r["operacao"]) for r in registros)
    largura_operacao = max(largura_operacao, len("OPERAÇÃO"))

    linhas.append(
        f"{'DATA/HORA':<19}  {'OPERAÇÃO':<{largura_operacao}}  SERVIÇO"
    )
    linhas.append("-" * (19 + 2 + largura_operacao + 2 + 20))

    for registro in registros:
        linhas.append(
            f"{registro['data_hora']:<19}  "
            f"{registro['operacao']:<{largura_operacao}}  "
            f"{registro['servico']}"
        )

    linhas.append("")
    linhas.append(f"Total de registros: {len(registros)}")

    return "\n".join(linhas)