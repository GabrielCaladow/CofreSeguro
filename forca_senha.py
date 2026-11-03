# Responsável: João Henrique | Função 3 (Força de Senha): classificar a senha, explicar o porquê e checar a lista de senhas comuns.
# Detalhes em ARQUITETURA.md.
import os
import string
os.system("cls")

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

    if all([possui_maiuscula, possui_caracteres_especiais, possui_numeros, possui_tamanho_minimo]):
        print("Senha segura!!")








