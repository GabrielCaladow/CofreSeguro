# Responsável: João Henrique | Função 3 (Força de Senha): classificar a senha, explicar o porquê e checar a lista de senhas comuns.
# Detalhes em ARQUITETURA.md.
import os
import string
os.system("cls")

tamanho_senha = False
caracteres_senha = False
maisculas_senha = False
digitos_senha = False
pontuacao_senha = False


senha_cadastrada = str(input("Digite a senha para análise: "))
senha_separada = list(senha_cadastrada)
senhas_comuns = open("senhas_comuns.txt", "r", encoding="utf8") 

if senha_cadastrada in senhas_comuns.read():
    print("Senha fraca(está presente no arquivo de senhas comuns)")

else:


    caracteres_senha = len(senha_cadastrada) >= 14
    maiusculas_senha = any(letra.isupper() for letra in senha_cadastrada)
    digitos_senha = any(digitos.isdigit() for digitos in senha_cadastrada)
    pontuacao_senha = any(caracteres_especiais in string.punctuation for caracteres_especiais in senha_cadastrada )

if all([caracteres_senha, maiusculas_senha, digitos_senha, pontuacao_senha]):
    print("Senha segura!!")








