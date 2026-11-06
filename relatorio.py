from credenciais import listar_credenciais
from forca_senha import obter_nivel_senha, senhas_comuns
from tempo import dias_desde



def encontrar_senhas_repetidas(credenciais, chave_senha, chave_nome):
   

    grupos = []

    for credencial in credenciais:
        senha = credencial[chave_senha]
        nome = credencial[chave_nome]

        if senha not in grupos:
            grupos[senha] = []
        grupos.append(grupo) 


    repetidas = []
    for nomes in grupos.values():
        if len(nomes) > 1:
            repetidas.append(nomes)

    return repetidas


def encontrar_senhas_comuns(credenciais, chave_senha, chave_nome, lista_comuns):
    encontradas = []

    for credencial in credenciais:
        if credencial[chave_senha].lower() in lista_comuns:
            encontradas.append(credencial[chave_nome])

    return encontradas


def encontrar_senhas_fracas(credenciais, chave_senha, chave_nome,
                            funcao_forca, niveis_fracos):
    fracas = []

    for credencial in credenciais:
        if funcao_forca(credencial[chave_senha]) in niveis_fracos:
            fracas.append(credencial[chave_nome])

    return fracas


def calcular_tempo_sem_alterar(credenciais, chave_nome, chave_data, funcao_dias):
    
    resultado = []

    for credencial in credenciais:
        try:
            dias = funcao_dias(credencial[chave_data])
        except ValueError:
            dias = None

        resultado.append((credencial[chave_nome], dias))


    resultado.sort(key=lambda item: (item[1] is None, -(item[1] or 0)))

    return resultado


def _texto_dias(dias):

    if dias is None:
        return "data indisponível"
    if dias == 1:
        return "1 dia"
    return f"{dias} dias"


def gerar_relatorio(total_credenciais, repetidas, comuns, fracas, tempos):
    

    total_repetidas = sum(len(grupo) for grupo in repetidas)

    linhas = []
    linhas.append("=== RELATÓRIO DE SEGURANÇA ===")
    linhas.append("")
    linhas.append("--- RESUMO ---")
    linhas.append(f"Total de credenciais: {total_credenciais}")
    linhas.append(f"Senhas fracas: {len(fracas)}")
    linhas.append(f"Credenciais com senha repetida: {total_repetidas} "
                  f"(em {len(repetidas)} grupo(s))")
    linhas.append(f"Senhas na lista de senhas comuns: {len(comuns)}")

    
    if tempos and tempos[0][1] is not None:
        nome_antigo, dias_antigo = tempos[0]
        linhas.append(f"Maior tempo sem alteração: {nome_antigo} "
                      f"({_texto_dias(dias_antigo)})")
    linhas.append("")
    linhas.append("--- DETALHES ---")

    linhas.append(f"[Senhas repetidas] {len(repetidas)} grupo(s)")
    if repetidas:
        for numero, grupo in enumerate(repetidas, start=1):
            linhas.append(f"  Grupo {numero}: {', '.join(grupo)}")
    else:
        linhas.append("  Nenhuma senha repetida.")
    linhas.append("")

    linhas.append(f"[Senhas comuns] {len(comuns)} credencial(is)")
    if comuns:
        linhas.append(f"  {', '.join(comuns)}")
    else:
        linhas.append("  Nenhuma senha comum encontrada.")
    linhas.append("")

    linhas.append(f"[Senhas fracas] {len(fracas)} credencial(is)")
    if fracas:
        linhas.append(f"  {', '.join(fracas)}")
    else:
        linhas.append("  Nenhuma senha fraca encontrada.")
    linhas.append("")

    linhas.append("[Tempo desde a última alteração]")
    if tempos:
        for nome, dias in tempos:
            linhas.append(f"  {nome}: {_texto_dias(dias)}")
    else:
        linhas.append("  Nenhuma credencial cadastrada.")
    linhas.append("")

    if repetidas or comuns or fracas:
        linhas.append("Recomendação: troque as senhas listadas acima.")
    else:
        linhas.append("Tudo certo! Nenhum problema encontrado.")

    return "\n".join(linhas)


def relatorio_de_seguranca():

    credenciais = listar_credenciais()
    chave_senha = "senha"
    chave_nome = "servico"
    chave_data = "data_alteracao"
    funcao_forca = obter_nivel_senha    
    niveis_fracos = [0, 1]              
    funcao_dias = dias_desde             

    repetidas = encontrar_senhas_repetidas(credenciais, chave_senha, chave_nome)
    comuns = encontrar_senhas_comuns(credenciais, chave_senha, chave_nome,
                                     senhas_comuns)
    fracas = encontrar_senhas_fracas(credenciais, chave_senha, chave_nome,
                                     funcao_forca, niveis_fracos)
    tempos = calcular_tempo_sem_alterar(credenciais, chave_nome, chave_data,
                                        funcao_dias)

    return gerar_relatorio(len(credenciais), repetidas, comuns, fracas, tempos)