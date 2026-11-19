from collections import defaultdict
 
from credenciais import listar_credenciais
from forca_senha import obter_nivel_senha, senhas_comuns, niveis
from tempo import dias_desde
 
 
def encontrar_senhas_repetidas(credenciais, chave_senha, chave_nome):
    # {senha: [serviços que usam essa senha]}
    grupos = defaultdict(list)
    for c in credenciais:
        grupos[c[chave_senha]].append(c[chave_nome])
    return [nomes for nomes in grupos.values() if len(nomes) > 1]
 
 
def encontrar_senhas_comuns(credenciais, chave_senha, chave_nome, lista_comuns):
    return [c[chave_nome] for c in credenciais
            if c[chave_senha].lower() in lista_comuns]
 
 
def encontrar_senhas_fracas(credenciais, chave_senha, chave_nome,
                            funcao_forca, niveis_fracos):
    return [c[chave_nome] for c in credenciais
            if funcao_forca(c[chave_senha]) in niveis_fracos]
 
 
def calcular_tempo_sem_alterar(credenciais, chave_nome, chave_data, funcao_dias):
    def dias(c):
        try:
            return funcao_dias(c[chave_data])
        except ValueError:
            return None
 
    resultado = [(c[chave_nome], dias(c)) for c in credenciais]
    # mais antigas primeiro; sem data (None) no fim
    resultado.sort(key=lambda item: (item[1] is None, -(item[1] or 0)))
    return resultado
 
 
def _texto_dias(dias):
    if dias is None:
        return "data indisponível"
    return f"{dias} dia" + ("" if dias == 1 else "s")
 
 
def gerar_relatorio(total_credenciais, repetidas, comuns, fracas, tempos):
    total_repetidas = sum(len(g) for g in repetidas)
 
    linhas = [
        "=== RELATÓRIO DE SEGURANÇA ===",
        "",
        "--- RESUMO ---",
        f"Total de credenciais: {total_credenciais}",
        f"Senhas fracas: {len(fracas)}",
        f"Credenciais com senha repetida: {total_repetidas} "
        f"(em {len(repetidas)} grupo(s))",
        f"Senhas na lista de senhas comuns: {len(comuns)}",
    ]
 
    if tempos and tempos[0][1] is not None:
        nome, dias = tempos[0]
        linhas.append(f"Maior tempo sem alteração: {nome} ({_texto_dias(dias)})")
 
    linhas += ["", "--- DETALHES ---",
               f"[Senhas repetidas] {len(repetidas)} grupo(s)"]
    linhas += ([f"  Grupo {n}: {', '.join(g)}"
                for n, g in enumerate(repetidas, start=1)]
               or ["  Nenhuma senha repetida."])
 
    linhas += ["", f"[Senhas comuns] {len(comuns)} credencial(is)",
               f"  {', '.join(comuns)}" if comuns
               else "  Nenhuma senha comum encontrada."]
 
    linhas += ["", f"[Senhas fracas] {len(fracas)} credencial(is)",
               f"  {', '.join(fracas)}" if fracas
               else "  Nenhuma senha fraca encontrada."]
 
    linhas += ["", "[Tempo desde a última alteração]"]
    linhas += ([f"  {nome}: {_texto_dias(dias)}" for nome, dias in tempos]
               or ["  Nenhuma credencial cadastrada."])
 
    linhas += ["", "Recomendação: troque as senhas listadas acima."
               if repetidas or comuns or fracas
               else "Tudo certo! Nenhum problema encontrado."]
 
    return "\n".join(linhas)
 
 
def relatorio_de_seguranca():
    credenciais = listar_credenciais()
    chave_senha, chave_nome, chave_data = "senha", "servico", "data_alteracao"
 
    repetidas = encontrar_senhas_repetidas(credenciais, chave_senha, chave_nome)
    comuns = encontrar_senhas_comuns(credenciais, chave_senha, chave_nome,
                                     senhas_comuns)
    fracas = encontrar_senhas_fracas(credenciais, chave_senha, chave_nome,
                                     obter_nivel_senha, [0, 1])
    tempos = calcular_tempo_sem_alterar(credenciais, chave_nome, chave_data,
                                        dias_desde)
 
    return gerar_relatorio(len(credenciais), repetidas, comuns, fracas, tempos)


def montar_dados_ia(credenciais):
    # Senha, usuário e observações não vão para a IA: a senha é o dado sensível e as
    # observações são texto livre, onde caberia uma injeção de prompt.
    repetidas = encontrar_senhas_repetidas(credenciais, "senha", "servico")
    comuns = encontrar_senhas_comuns(credenciais, "senha", "servico", senhas_comuns)

    linhas = ["servico;categoria;forca_da_senha;senha_comum;mesma_senha_que;dias_sem_alterar"]

    for c in credenciais:
        mesma_senha = []
        for grupo in repetidas:
            if c["servico"] in grupo:
                mesma_senha = [nome for nome in grupo if nome != c["servico"]]

        dias = dias_desde(c["data_alteracao"])
        forca = niveis[obter_nivel_senha(c["senha"])].replace("Senha ", "").strip("!")

        linhas.append(";".join([
            c["servico"],
            c["categoria"],
            forca,
            "sim" if c["servico"] in comuns else "não",
            ", ".join(mesma_senha) or "-",
            "?" if dias is None else str(dias)
        ]))

    return "\n".join(linhas)
 