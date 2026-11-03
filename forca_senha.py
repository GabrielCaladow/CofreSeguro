# Responsável: João Henrique | Função 3 (Força de Senha): classificar a senha, explicar o porquê e checar a lista de senhas comuns.
# Detalhes em ARQUITETURA.md.

senha_cadastrada = str(input("Digite a senha para análise: "))
senhas_comuns = open("senhas_comuns.txt", "r", encoding="utf8") 

if senha_cadastrada in senhas_comuns.read():
    print("Senha fraca(está presente no arquivo de senhas comuns)")

