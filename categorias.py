
# Responsável: Gabriel Calado | Função 2 (Dados)
# CRUD de categorias e definição da força mínima de senha.
from armazenamento import carregar_categorias, salvar_categorias

def cadastrar_categoria(nome, forca_minima):
    categorias = carregar_categorias()

    for categoria in categorias:
        if categoria["nome"].lower() == nome.lower():
            return None

    if forca_minima < 0 or forca_minima > 4:
        return None

    categoria = {
        "nome": nome,
        "forca_minima": str(forca_minima)
    }

    categorias.append(categoria)

    salvar_categorias(categorias)

    return categoria

def listar_categorias():
    categorias = carregar_categorias()

    return categorias

def buscar_categoria(nome):
    categorias = carregar_categorias()

    for categoria in categorias:
        if categoria["nome"].lower() == nome.lower():
            return categoria

    return None

def editar_categoria(nome, novo_nome, nova_forca_minima):
    categorias = carregar_categorias()

    if nova_forca_minima < 0 or nova_forca_minima > 4:
        return None

    for categoria in categorias:
        if categoria["nome"].lower() == nome.lower():

            for outra_categoria in categorias:
                if (
                    outra_categoria["nome"].lower() == novo_nome.lower()
                    and outra_categoria != categoria
                ):
                    return None

            categoria["nome"] = novo_nome
            categoria["forca_minima"] = str(nova_forca_minima)

            salvar_categorias(categorias)

            return categoria

    return None
