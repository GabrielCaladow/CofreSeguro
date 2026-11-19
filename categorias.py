# Responsável: Gabriel Calado | Função 2 (Dados)
from armazenamento import carregar_categorias, salvar_categorias

# Força mínima de 0 (muito fraca) a 4 (muito forte). Banco e trabalho exigem mais.
categorias_padrao = [
    ("Banco", 3),
    ("Rede social", 2),
    ("Estudo", 2),
    ("Trabalho", 3),
    ("Outros", 1)
]


def criar_categorias_padrao():
    if carregar_categorias():
        return

    categorias = []

    for nome, forca_minima in categorias_padrao:
        categorias.append({
            "nome": nome,
            "forca_minima": str(forca_minima)
        })

    salvar_categorias(categorias)

def cadastrar_categoria(nome, forca_minima):
    categorias = carregar_categorias()

    nome = nome.strip()

    if not nome:
        return None

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
