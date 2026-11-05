from armazenamento import carregar_credenciais, salvar_credenciais
from tempo import agora_texto


def adicionar_credencial(servico, usuario, senha, categoria, observacoes=""):
    credenciais = carregar_credenciais()

    credencial = {
        "servico": servico,
        "usuario": usuario,
        "senha": senha,
        "categoria": categoria,
        "observacoes": observacoes,
        "data_alteracao": agora_texto()
    }

    credenciais.append(credencial)
    salvar_credenciais(credenciais)

    return credencial


def listar_credenciais():
    return carregar_credenciais()


def buscar_credencial(servico):
    credenciais = carregar_credenciais()

    for credencial in credenciais:
        if credencial["servico"].lower() == servico.lower():
            return credencial

    return None


def editar_credencial(
    servico,
    novo_usuario,
    nova_senha,
    nova_categoria,
    novas_observacoes=""
):
    credenciais = carregar_credenciais()

    for credencial in credenciais:
        if credencial["servico"].lower() == servico.lower():
            credencial["usuario"] = novo_usuario
            credencial["senha"] = nova_senha
            credencial["categoria"] = nova_categoria
            credencial["observacoes"] = novas_observacoes
            credencial["data_alteracao"] = agora_texto()

            salvar_credenciais(credenciais)
            return credencial

    return None


def excluir_credencial(servico):
    credenciais = carregar_credenciais()

    for credencial in credenciais:
        if credencial["servico"].lower() == servico.lower():
            credenciais.remove(credencial)
            salvar_credenciais(credenciais)
            return True

    return False


def mascarar_senha(senha):
    return senha[:2] + "*" * max(0, len(senha) - 2)