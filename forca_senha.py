# Responsável: João Henrique | Função 3 (Força de Senha): classificar a senha, explicar o porquê e checar a lista de senhas comuns.
import os
import string

niveis = ["Senha muito fraca!!", "Senha Fraca!!", "Senha Média!!", "Senha Forte!!", "Senha muito forte!!"]

# Abaixo de 8 caracteres a senha é muito fraca não importa o que tenha nela.
# Com 14 ou mais ela pode chegar a Forte ou Muito forte; antes disso fica no máximo Média.
tamanho_minimo = 8
tamanho_forte = 14

def carregar_lista(caminho):
    try:
        with open(caminho, "r", encoding="utf8") as arquivo:
            # set em vez de lista porque são 10 mil senhas e o "in" num set é instantâneo
            return {linha.strip().lower() for linha in arquivo}
    except FileNotFoundError:
        return set()

def verificador_maiusculas(senha):
    return any(letra.isupper() for letra in senha)

def verificador_minusculas(senha):
    return any(letra.islower() for letra in senha)

def verificador_tamanho(senha):
    return len(senha) >= tamanho_forte


def verificador_numeros(senha):
    return any(caractere.isdigit() for caractere in senha)


def verificador_pontuacao(senha):
    return any(caractere in string.punctuation for caractere in senha)

# O caminho sai da pasta deste arquivo. Com só "senhas_comuns.txt", a lista
# vinha vazia sempre que o programa era rodado de outra pasta.
senhas_comuns = carregar_lista(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "senhas_comuns.txt")
)

def marca(ok):
    return "✅" if ok else "❌"

def avaliar_senha(senha):
    if senha.lower() in senhas_comuns:

        criterios = {
            "Senha comum": False
        }

        explicacao = ("Essa senha está presente na lista de senhas comuns e pode ser facilmente descoberta.")

        return 0, criterios, explicacao

    criterios = {
        f"Tamanho mínimo de {tamanho_forte} caracteres": verificador_tamanho(senha),
        "Letras maiúsculas": verificador_maiusculas(senha),
        "Letras minúsculas": verificador_minusculas(senha),
        "Caracteres especiais": verificador_pontuacao(senha),
        "Números": verificador_numeros(senha),
    }

    pontos = sum(criterios.values())
    explicacao = []

    for nome, resultado in criterios.items():

        if resultado:
            explicacao.append(f"{nome}: atendido.")

        else:
            explicacao.append(f"{nome}: não atendido.")

    if len(senha) < tamanho_minimo:
        explicacao.append(
            f"Como tem menos de {tamanho_minimo} caracteres, "
            "a senha é muito fraca mesmo atendendo os outros critérios."
        )

    elif not verificador_tamanho(senha):
        explicacao.append(
            f"Como tem menos de {tamanho_forte} caracteres, "
            "a senha não passa de Média."
        )

    explicacao = " ".join(explicacao)

    return pontos, criterios, explicacao

def classificar_senha(senha):
    return niveis[obter_nivel_senha(senha)]

def main():

    senha = input("Escreva a sua senha: ")
    pontos, criterios, explicacao = avaliar_senha(senha)
    nivel = classificar_senha(senha)

    print(f"\nClassificação: {nivel}")
    print(f"\nCritérios: ")

    for nome, ok in criterios.items():
        print(f"{nome} - {marca(ok)}")

    print(f"\nExplicação: {explicacao}")


def obter_nivel_senha(senha):
    pontos, criterios, explicacao = avaliar_senha(senha)

    # Senhas comuns sempre são consideradas muito fracas.
    if "Senha comum" in criterios:
        return 0

    if len(senha) < tamanho_minimo:
        return 0

    # São 5 critérios para 5 níveis (0 a 4): com todos atendidos é 4,
    # e cada critério que falta desce um nível.
    nivel = max(pontos - 1, 0)

    if not verificador_tamanho(senha):
        nivel = min(nivel, 2)

    return nivel


def senha_atende_categoria(senha, forca_minima):
    nivel_senha = obter_nivel_senha(senha)

    return nivel_senha >= int(forca_minima)

if __name__ == "__main__":
    main()
