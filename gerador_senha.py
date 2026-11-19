# Responsável: Raul | Função 3 (Força de Senha): gerador de senhas fortes (funcionalidade extra).
import random, string
def gerar_senha_aleatoria():
    caracteres=string.ascii_letters+string.punctuation+string.digits
    senha=" ".join(random.choices(caracteres, k=16))
    print(f"Sua senha é: {senha}")
def gerar_senha_palavra():
    palavra_chave=input("Qual sua palavra chave: ")
    numero=str(random.randint(100,999))
    simbolo="!@#$%ˆ&*_-+="
    simbolo_aleatorio="".join(random.sample(simbolo, 2))
    senha_palavra=simbolo_aleatorio+palavra_chave.lower().replace("a", "@").replace("e", "3").replace("i", "1").replace("o", "0").replace("s", "$").replace("t", "7")+numero
    print(f"Sua senha é: {senha_palavra}")
def main():
    continuar="s"
    while continuar.lower()=="s":
        opcao=int(input("1-para senha aleatoria com palavra chave \n2-para senha 100%. aleatoria \nescolha: "))
        if opcao==2:
            gerar_senha_aleatoria()
        elif opcao==1:
            gerar_senha_palavra()
        else:
            print("opção invalida!")
        continuar=input("Deseja criar outra senha? (s/n): ")
    print("Progama encerrado.")
if __name__=="__main__":
    main()