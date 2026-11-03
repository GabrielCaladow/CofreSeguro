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

    if len(senha_cadastrada) >= 14:

        caracteres_senha = True
    
    for letra_maiuscula in string.ascii_uppercase:

        if  letra_maiuscula in senha_separada:
            
            maisculas_senha = True

    for digitos in string.digits:
        
        if digitos in senha_separada:
            
            digitos_senha = True

    for pontuacao in string.punctuation:
        
        if pontuacao in senha_separada:
            
            pontuacao_senha = True

    if maisculas_senha == True and digitos_senha == True and pontuacao_senha == True and caracteres_senha == True:
        print("Senha segura!!")



