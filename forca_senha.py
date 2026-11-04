# Responsável: João Henrique | Função 3 (Força de Senha): classificar a senha, explicar o porquê e checar a lista de senhas comuns.
# Detalhes em ARQUITETURA.md.
import os
import string
os.system("cls")

contador_true = 0
categoria = ["Senha Fraca!!", "Senha Média!!", "Senha Forte!!", "Senha muito forte!!"]

with open("senhas_comuns.txt", "r", encoding="utf8") as senhas_comuns, \
    open("senhas_salvas.txt", "r", encoding="utf8") as senha:

    def verificador_maiusculas (senha_cadastrada):
        return any(letra.isupper() for letra in senha_cadastrada)

    def verificador_tamanho (senha_cadastrada):
        return len(senha_cadastrada) >= 14

    def verificador_numeros (senha_cadastrada):
        return any(digitos.isdigit() for digitos in senha_cadastrada)

    def verificador_pontuacao (senha_cadastrada):
        return any(caracteres_especiais in string.punctuation for caracteres_especiais in senha_cadastrada )

    def carregar_lista(caminho):
        with open(caminho, "r", encoding="utf8") as arquivo:
            return {linha.strip() for linha in arquivo}

    def marca(ok):
        return "✅" if ok else "❌"
    
    def main(categoria):
        
        os.system("cls")

        senha = str(input("Escreva a sua senha: "))
        senhas_comuns = carregar_lista("senhas_comuns.txt")

        if senha in senhas_comuns:
            print("Senha fraca (está presente no arquivo de senhas comuns)")
            return

        criterios = {
            "Tamanho": verificador_tamanho(senha),
            "Letras maiúsculas": verificador_maiusculas(senha),
            "Caracteres especiais": verificador_pontuacao(senha),
            "Números": verificador_numeros(senha),
        }

        pontos = sum(criterios.values())  # True conta como 1
        print(categoria[pontos])

        for nome, ok in criterios.items():
            print(f"{nome} - {marca(ok)}")


main(categoria)








