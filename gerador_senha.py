# Responsável: Raul | Função 3 (Força de Senha): gerador de senhas fortes (funcionalidade extra).
opcao=int(input("1-para senha aleatoria com palavra chave \n2-para senha 100%. aleatoria\nEscolha: "))
import random, string
if opcao==2:
    caracteres=string.ascii_letters+string.punctuation+string.digits
    senha=" ".join(random.choices(caracteres, k=16))
    print(f"Sua senha é: {senha}")
elif opcao==1:
    palavra_chave=input("Qual sua palavra chave: ")
    numero=str(random.randint(100,999))
    simbolo="!@#$%ˆ&*_-+="
    simbolo_aleatorio="".join(random.sample(simbolo, 2))
    senha_palavra=simbolo_aleatorio+palavra_chave.lower().replace("a", "@").replace("e", "3").replace("i", "1").replace("o", "0").replace("s", "$").replace("t", "7")+numero
    print(f"Sua senha é: {senha_palavra}")