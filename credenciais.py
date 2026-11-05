# Responsável: Gabriel Calado | Função 2 (Dados): CRUD de credenciais e categorias e mascarar senha.
from armazenamento import carregar_credenciais, salvar_credenciais

def adicionar_credencial(servico, usuario, senha, categoria):
    credenciais = carregar_credenciais()

    credencial = {
        "servico": servico,
        "usuario": usuario,
        "senha" : senha,
        "categoria": categoria
    }

    credenciais.append(credencial)
    salvar_credenciais(credenciais)

    return credencial

def listar_credenciais():
    credenciais = carregar_credenciais()

    return credenciais

def buscar_credencial(servico):
    credenciais = carregar_credenciais()

    for credencial in credenciais:
        if credencial["servico"].lower() == servico.lower():
            return credencial 

    return None

def editar_credencial(servico, novo_usuario, nova_senha, nova_categoria):
    credenciais = carregar_credenciais()

    for credencial in credenciais:
        if credencial["servico"].lower() == servico.lower():
            credencial["usuario"] = novo_usuario
            credencial["senha"] = nova_senha
            credencial["categoria"] = nova_categoria

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
    return "*" * len(senha)