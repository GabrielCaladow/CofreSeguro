
# Responsável: Heitor | Função 1 (Interface e Integração)
# Menu principal, submenus, telas e chamada dos outros módulos.

import os

from credenciais import (
    adicionar_credencial,
    listar_credenciais,
    buscar_credencial,
    editar_credencial,
    excluir_credencial,
    mascarar_senha
)

from categorias import (
    cadastrar_categoria,
    listar_categorias,
    buscar_categoria
)

from forca_senha import (
    avaliar_senha,
    classificar_senha
)


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione ENTER para continuar...")


def exibir_credencial(credencial, revelar=False):
    if credencial is None:
        print("Credencial não encontrada!")
        return

    senha = credencial["senha"]

    if not revelar:
        senha = mascarar_senha(senha)

    print("\n--- Credencial ---")
    print(f"Serviço:   {credencial['servico']}")
    print(f"Usuário:   {credencial['usuario']}")
    print(f"Senha:     {senha}")
    print(f"Categoria: {credencial['categoria']}")
    print(f"Observações: {credencial.get('observacoes', '')}")
    print(f"Última alteração: {credencial.get('data_alteracao', '')}")

def analisar_senha_categoria(senha, nome_categoria):
    categoria = buscar_categoria(nome_categoria)

    if categoria is None:
        print(
            f"\nA categoria '{nome_categoria}' não está cadastrada. "
            "Não foi possível verificar a força mínima da senha."
        )
        return False

    pontos, criterios, explicacao = avaliar_senha(senha)
    nivel = classificar_senha(senha)

    print("\n===== ANÁLISE DA SENHA =====")
    print(f"Classificação: {nivel}")

    print("\nCritérios:")

    for nome, resultado in criterios.items():
        if resultado:
            print(f"{nome}: ✅")
        else:
            print(f"{nome}: ❌")

    print(f"\nExplicação: {explicacao}")

    forca_minima = int(categoria["forca_minima"])

    if "Senha comum" in criterios:
        print(
            "\nAVISO: Essa senha está presente na lista "
            "de senhas comuns."
        )

    elif pontos < forca_minima:
        print(
            f"\nAVISO: A senha não atende à exigência mínima "
            f"da categoria {categoria['nome']}."
        )

    else:
        print(
            f"\nA senha atende à exigência mínima "
            f"da categoria {categoria['nome']}."
        )

    return True


def menu_credenciais():
    while True:
        limpar_tela()

        print("===== CREDENCIAIS =====")
        print("1. Listar credenciais")
        print("2. Adicionar credencial")
        print("3. Buscar credencial")
        print("4. Editar credencial")
        print("5. Excluir credencial")
        print("6. Revelar senha")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            break

        elif opcao == "1":
            credenciais = listar_credenciais()

            if not credenciais:
                print("\nNenhuma credencial cadastrada.")

            else:
                for credencial in credenciais:
                    exibir_credencial(credencial)

            pausar()

        elif opcao == "2":
            servico = input("Nome do serviço: ")
            usuario = input("Usuário ou e-mail: ")
            senha = input("Senha: ")
            categoria = input("Categoria: ")
            observacoes = input("Observações: ")

            analisar_senha_categoria(senha, categoria)

            adicionar_credencial(
                servico,
                usuario,
                senha,
                categoria,
                observacoes
            )

            print("\nCredencial adicionada com sucesso!")

            pausar()

        elif opcao == "3":
            servico = input(
                "Digite o serviço que deseja buscar: "
            )

            credencial = buscar_credencial(servico)

            exibir_credencial(credencial)

            pausar()

        elif opcao == "4":
            servico = input(
                "Serviço que deseja editar: "
            )

            credencial = buscar_credencial(servico)

            if credencial is None:
                print("\nCredencial não encontrada!")

            else:
                print("\nDigite os novos dados:")

                novo_usuario = input("Novo usuário ou e-mail: ")
                nova_senha = input("Nova senha: ")
                nova_categoria = input("Nova categoria: ")
                novas_observacoes = input("Novas observações: ")

                analisar_senha_categoria(
                    nova_senha,
                    nova_categoria
                )

                editar_credencial(
                    servico,
                    novo_usuario,
                    nova_senha,
                    nova_categoria,
                    novas_observacoes
                )

                print("\nCredencial editada com sucesso!")

            pausar()

        elif opcao == "5":
            servico = input(
                "Serviço que deseja excluir: "
            )

            resultado = excluir_credencial(servico)

            if resultado:
                print("\nCredencial excluída com sucesso!")

            else:
                print("\nCredencial não encontrada!")

            pausar()

        elif opcao == "6":
            servico = input(
                "Serviço cuja senha deseja revelar: "
            )

            credencial = buscar_credencial(servico)

            exibir_credencial(
                credencial,
                revelar=True
            )

            pausar()

        else:
            print("\nOpção inválida!")

            pausar()


def menu_categorias():
    while True:
        limpar_tela()

        print("===== CATEGORIAS =====")
        print("1. Listar categorias")
        print("2. Cadastrar categoria")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            break

        elif opcao == "1":
            categorias = listar_categorias()

            if not categorias:
                print("\nNenhuma categoria cadastrada.")

            else:
                print("\nCategorias cadastradas:")

                for categoria in categorias:
                    forca = int(categoria["forca_minima"])

                    print(
                        f"{categoria['nome']} - "
                        f"Força mínima: {forca}"
                    )

            pausar()

        elif opcao == "2":
            nome = input("Nome da categoria: ")

            print("\nNíveis de força:")
            print("0. Muito fraca")
            print("1. Fraca")
            print("2. Média")
            print("3. Forte")
            print("4. Muito forte")

            try:
                forca_minima = int(
                    input("Força mínima exigida: ")
                )

                categoria = cadastrar_categoria(
                    nome,
                    forca_minima
                )

                if categoria is None:
                    print(
                        "\nNão foi possível cadastrar a categoria. "
                        "Verifique o nome e a força mínima."
                    )

                else:
                    print(
                        "\nCategoria cadastrada com sucesso!"
                    )

            except ValueError:
                print(
                    "\nDigite um número válido para a força mínima."
                )

            pausar()

        else:
            print("\nOpção inválida!")

            pausar()


def menu_principal():
    while True:
        limpar_tela()

        print("========== COFRE SEGURO ==========")
        print("1. Credenciais")
        print("2. Categorias")
        print("3. Gerar senha forte")
        print("4. Relatório de segurança")
        print("5. Log de auditoria")
        print("6. Perguntar à IA")
        print("0. Sair")

        opcao = input(
            "\nDigite o número da opção desejada: "
        )

        if opcao == "0":
            print("\nSaindo do Cofre Seguro...")
            break

        elif opcao == "1":
            menu_credenciais()

        elif opcao == "2":
            menu_categorias()

        elif opcao == "3":
            limpar_tela()
            print("Gerar senha forte em construção...")
            pausar()

        elif opcao == "4":
            limpar_tela()
            print("Relatório de segurança em construção...")
            pausar()

        elif opcao == "5":
            limpar_tela()
            print("Log de auditoria em construção...")
            pausar()

        elif opcao == "6":
            limpar_tela()
            print("Perguntar à IA em construção...")
            pausar()

        else:
            print("\nOpção inválida!")
            pausar()


while True:
    app = input(
        "Deseja acessar o Cofre Seguro? (Digite sim ou não): "
    ).lower().strip()

    if app == "sim":
        menu_principal()
        break

    elif app == "não" or app == "nao":
        print("Encerrando o programa...")
        break

    else:
        print("Resposta inválida. Digite sim ou não.")
