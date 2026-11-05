# Responsável: Raul | Função 3 (Força de Senha): gerador de senhas fortes (funcionalidade extra).
opcao=int(input("1-para senha aleatoria com palavra chave \n2-para senha 100%. aleatoria\nEscolha: "))
if opcao==2:
    import random, string
    caracteres=string.ascii_letters+string.punctuation+string.digits
    senha=" ".join(random.choices(caracteres, k=16))
    print(f"Sua senha é: {senha}")
elif opcao==1:
    palavra_chave=input("Qual sua palavra chave: ")
    