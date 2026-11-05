# Responsável: João Henrique | Função 3 (Força de Senha): classificar a senha, explicar o porquê e checar a lista de senhas comuns.
import string

niveis = ["Senha muito fraca!!", "Senha Fraca!!", "Senha Média!!", "Senha Forte!!", "Senha muito forte!!"]

def carregar_lista(caminho):
    try:
        with open(caminho, "r", encoding="utf8") as arquivo:
            return {linha.strip().lower() for linha in arquivo}
    except FileNotFoundError:
        return set()

def verificador_maiusculas(senha):
    return any(letra.isupper() for letra in senha)

def verificador_minusculas(senha):
    return any(letra.islower() for letra in senha)

def verificador_tamanho(senha):
    return len(senha) >= 14


def verificador_numeros(senha):
    return any(caractere.isdigit() for caractere in senha)


def verificador_pontuacao(senha):
    return any(caractere in string.punctuation for caractere in senha)

senhas_comuns = carregar_lista("senhas_comuns.txt")

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
        "Tamanho mínimo de 14 caractéres": verificador_tamanho(senha),
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
    
    explicacao = " ".join(explicacao) 
    
    return pontos, criterios, explicacao

def classificar_senha(senha):

    pontos, criterios, explicacao = avaliar_senha(senha)

    if "Senha comum" in criterios:
        return niveis[0]

    return niveis[min(pontos, 4)]

def main():

    senha = input("Escreva a sua senha: ")
    pontos, criterios, explicacao = avaliar_senha(senha)
    nivel = classificar_senha(senha)

    print(f"\nClassificação: {nivel}")
    print(f"\nCritérios: ")

    for nome, ok in criterios.items():
        print(f"{nome} - {marca(ok)}")

    print(f"\nExplicação: {explicacao}")

if __name__ == "__main__":
    main()