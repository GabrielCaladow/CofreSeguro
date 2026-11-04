# Responsável: João Henrique | Função 3 (Força de Senha): classificar a senha, explicar o porquê e checar a lista de senhas comuns.
# Detalhes em ARQUITETURA.md.
import os
import string
os.system("cls")

contador_true = 0
categoria = ["Senha Fraca!!", "Senha Média!!", "Senha Forte!!", "Senha muito forte!!"]

with open("senhas_comuns.txt", "r", encoding="utf8") as senhas_comuns, \
    open("senhas_salvas.txt", "r", encoding="utf8") as senhas_cadastradas:

    senha_cadastrada = str(input("Escreva a sua senha: "))

    def verificador_maiusculas (senha_cadastrada):
        return any(letra.isupper() for letra in senha_cadastrada)

    def verificador_tamanho (senha_cadastrada):
        return len(senha_cadastrada) >= 14

    def verificador_numeros (senha_cadastrada):
        return any(digitos.isdigit() for digitos in senha_cadastrada)

    def verificador_pontuacao (senha_cadastrada):
        return any(caracteres_especiais in string.punctuation for caracteres_especiais in senha_cadastrada )

    lista_senhas_cadastradas = senhas_cadastradas.readlines()

    remocao_espacamento = [n.replace("\n", "") for n in lista_senhas_cadastradas]

    if senha_cadastrada in senhas_comuns.read():
        
        print("Senha fraca(está presente no arquivo de senhas comuns)")

    else:

        possui_maiuscula = verificador_maiusculas (senha_cadastrada)
        possui_caracteres_especiais = verificador_pontuacao (senha_cadastrada)
        possui_numeros = verificador_numeros (senha_cadastrada)
        possui_tamanho_minimo = verificador_tamanho (senha_cadastrada)

        check = [possui_maiuscula, possui_caracteres_especiais, possui_numeros, possui_tamanho_minimo]

        for i in check:
            if i == True:
                emoji = "✅"
                contador_true+=1
            elif i == False:
                emoji = "❌"

        for i in range(len(check)+1):   
            if contador_true == i:
                print(f"{categoria[i-1]}")
                print(f"Tamanho - {emoji}")
                print(f"Letras maiúsculas - {emoji}")
                print(f"Caractéres especiais - {emoji}")
                print(f"Números - {emoji}")


    








