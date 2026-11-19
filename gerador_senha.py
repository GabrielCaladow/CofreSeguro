# Responsável: Raul | Função 3 (Força de Senha): gerador de senhas fortes (funcionalidade extra).
import random, string
def gerar_senha_aleatoria():
    caracteres=string.ascii_letters+string.punctuation+string.digits
    senha="".join(random.choices(caracteres, k=16))
    print(f"Sua senha é: {senha}")
def gerar_senha_palavra():
    palavra_chave=input("Qual sua palavra chave: ")
    numero=str(random.randint(100,999))
    simbolo="!@#$%^&*_-+="
    simbolo_aleatorio="".join(random.sample(simbolo, 2))
    # troca letras por símbolos parecidos (a vira @, e vira 3...)
    senha_palavra=simbolo_aleatorio+palavra_chave.lower().replace("a", "@").replace("e", "3").replace("i", "1").replace("o", "0").replace("s", "$").replace("t", "7")+numero
    print(f"Sua senha é: {senha_palavra}")