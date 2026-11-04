# Responsável: João Henrique | Função 3 (Força de Senha): classificar a senha, explicar o porquê e checar a lista de senhas comuns.
# Detalhes em ARQUITETURA.md.
import os
import string

categorias = ["Senha muito fraca!!", "Senha Fraca!!", "Senha Média!!", "Senha Forte!!", "Senha muito forte!!"]


def verificador_maiusculas(senha):
    return any(letra.isupper() for letra in senha)


def verificador_tamanho(senha):
    return len(senha) >= 14


def verificador_numeros(senha):
    return any(caractere.isdigit() for caractere in senha)


def verificador_pontuacao(senha):
    return any(caractere in string.punctuation for caractere in senha)


def carregar_lista(caminho):
    try:
        with open(caminho, "r", encoding="utf8") as arquivo:
            return {linha.strip().lower() for linha in arquivo}
    except FileNotFoundError:
        print(f"Aviso: arquivo '{caminho}' não encontrado. Pulando a checagem de senhas comuns.")
        return set()


def marca(ok):
    return "✅" if ok else "❌"


def main():
    os.system("cls" if os.name == "nt" else "clear")

    senha = input("Escreva a sua senha: ")
    senhas_comuns = carregar_lista("senhas_comuns.txt")

    if senha.lower() in senhas_comuns:
        print("Senha fraca (está presente no arquivo de senhas comuns)")
        return

    criterios = {
        "Tamanho": verificador_tamanho(senha),
        "Letras maiúsculas": verificador_maiusculas(senha),
        "Caracteres especiais": verificador_pontuacao(senha),
        "Números": verificador_numeros(senha),
    }

    pontos = sum(criterios.values())  # True conta como 1
    print(categorias[pontos])

    for nome, ok in criterios.items():
        print(f"{nome} - {marca(ok)}")


if __name__ == "__main__":
    main()