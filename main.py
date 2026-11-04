# Responsável: Heitor | Função 1 (Interface e Integração): menu principal, submenus, telas e chamada dos outros módulos.
# Regra: só este arquivo e entrada.py usam print()/input(). Detalhes em ARQUITETURA.md.

import os

def menu_principal(opcao):
    while True:
        opcao = int(input("1. Credenciais (listar mascarado / adicionar / editar / excluir / revelar senha)\n2. Categorias (listar / cadastrar)\n3. Gerar senha forte\n4. Relatório de segurança\n5. Log de auditoria\n6. Perguntar à IA  (reservado para o módulo da aula)\n0. Sair\n\nDigite o número da opção desejada: "))

        if opcao == 0:
            print("Saindo...")
            break
    
        else:
            if opcao == 1:
                os.system("cls")
                print("Credenciais em construção...")
        
            elif opcao == 2:
                os.system("cls")
                print("Categorias em construção...")
        
            elif opcao == 3:
                os.system("cls")
                print("Gerar senha forte em construção...")
        
            elif opcao == 4:
                os.system("cls")
                print("Relatório de segurança em construção...")
        
            elif opcao == 5:
                os.system("cls")
                print("Log de auditoria em construção...")
        
            elif opcao == 6:
                os.system("cls")
                print("Perguntar à IA emconstrução...")
                
            else:
                os.system("cls")
                print("Opção inválida!")


while True:
    app = input("Deseja acessar o Cofre Seguro? (Digite sim ou não): ").lower()
    
    if app == "sim":
        os.system("cls")
        menu_principal(app)
        break
    
    elif app == "não":
        os.system("cls")
        print("Encerrando o programa...")
        break
    
    else:
        continue