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
    buscar_categoria,
    criar_categorias_padrao
)

from forca_senha import (
    avaliar_senha,
    classificar_senha,
    senha_atende_categoria
)

from auditoria import (
    registrar_operacao,
    consultar_log,
    formatar_log,
    OP_ADICIONAR,
    OP_EDITAR,
    OP_EXCLUIR,
    OP_REVELAR,
    OP_CADASTRAR_CATEGORIA,
    OP_GERAR_SENHA,
    OP_GERAR_RELATORIO,
    OP_PERGUNTAR_IA
)

from gerador_senha import (
    gerar_senha_aleatoria,
    gerar_senha_palavra
)

from relatorio import relatorio_de_seguranca, montar_dados_ia

from agente import falar_com_agente_texto

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione ENTER para continuar...")


def ler_senha(mensagem):
    # A senha não pode ser "limpa" na hora de salvar como os outros campos,
    # senão o usuário cadastraria uma senha e o arquivo guardaria outra.
    # Por isso o ";" é recusado já na digitação.
    while True:
        senha = input(mensagem)

        if not senha:
            print("A senha não pode ficar vazia.")

        elif ";" in senha:
            print("A senha não pode ter ';' (é o separador do arquivo).")

        else:
            return senha


def ler_categoria(mensagem):
    # Só aceita categoria cadastrada, porque é dela que vem a força mínima.
    while True:
        nome_categoria = input(mensagem)
        categoria = buscar_categoria(nome_categoria)

        if categoria is not None:
            return categoria["nome"]

        nomes = []

        for categoria in listar_categorias():
            nomes.append(categoria["nome"])

        print(f"Categoria não cadastrada. Opções: {', '.join(nomes)}")


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

    if "Senha comum" in criterios:
        print(
            "\nAVISO: Essa senha está presente na lista "
            "de senhas comuns."
        )

    elif not senha_atende_categoria(senha, categoria["forca_minima"]):
        print(
            f"\nAVISO: A senha não atende à exigência mínima "
            f"da categoria {categoria['nome']}."
        )

    else:
        print(
            f"\nA senha atende à exigência mínima "
            f"da categoria {categoria['nome']}."
        )


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
            senha = ler_senha("Senha: ")
            categoria = ler_categoria("Categoria: ")
            observacoes = input("Observações: ")

            analisar_senha_categoria(senha, categoria)

            credencial = adicionar_credencial(
                servico,
                usuario,
                senha,
                categoria,
                observacoes
            )

            if credencial is None:
                print(
                    "\nNão foi possível adicionar. O nome do serviço "
                    "está vazio ou já existe uma credencial com ele."
                )

            else:
                registrar_operacao(OP_ADICIONAR, credencial["servico"])

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
                nova_senha = ler_senha("Nova senha: ")
                nova_categoria = ler_categoria("Nova categoria: ")
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

                registrar_operacao(OP_EDITAR, servico)

                print("\nCredencial editada com sucesso!")

            pausar()

        elif opcao == "5":
            servico = input(
                "Serviço que deseja excluir: "
            )

            resultado = excluir_credencial(servico)

            if resultado:
                registrar_operacao(OP_EXCLUIR, servico)
                print("\nCredencial excluída com sucesso!")

            else:
                print("\nCredencial não encontrada!")

            pausar()

        elif opcao == "6":
            servico = input(
                "Serviço cuja senha deseja revelar: "
            )

            credencial = buscar_credencial(servico)

            if credencial is not None:
                registrar_operacao(OP_REVELAR, credencial["servico"])

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
                    registrar_operacao(OP_CADASTRAR_CATEGORIA, nome)

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


def menu_auditoria():
    while True:
        limpar_tela()

        print("===== LOG DE AUDITORIA =====")
        print("1. Ver log completo")
        print("2. Filtrar por operação")
        print("3. Filtrar por serviço")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            break

        elif opcao == "1":
            print()
            print(formatar_log(consultar_log()))
            pausar()

        elif opcao == "2":
            filtro = input(
                "Operação (ex.: REVELAR, EXCLUIR, ADICIONAR): "
            )
            print()
            print(formatar_log(consultar_log(filtro_operacao=filtro)))
            pausar()

        elif opcao == "3":
            filtro = input("Nome do serviço: ")
            print()
            print(formatar_log(consultar_log(filtro_servico=filtro)))
            pausar()

        else:
            print("\nOpção inválida!")
            pausar()

def menu_gerador_senha():
    while True:
        limpar_tela()
        print("========== GERADOR DE SENHA ==========")
        # compara como texto: com int(input()) qualquer letra derrubava o programa
        opcao=input("1. Senha aleatoria com palavra chave \n2. Senha 100%. aleatoria\n0. Voltar \nEscolha uma opção: ")
        if opcao=="2":
            gerar_senha_aleatoria()
            registrar_operacao(OP_GERAR_SENHA)
        elif opcao=="1":
            gerar_senha_palavra()
            registrar_operacao(OP_GERAR_SENHA)
        elif opcao == "0":
            break
        else:
            print("opção invalida!")
        pausar()

def menu_relatorio():
    while True:
        limpar_tela()
        print("===== RELATÓRIO DE SEGURANÇA =====")
        print("1. Ver relatório")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            break

        elif opcao == "1":
            print()
            print(relatorio_de_seguranca())
            registrar_operacao(OP_GERAR_RELATORIO)
            pausar()

        else:
            print("\nOpção inválida!")
            pausar()

def menu_ia():
    limpar_tela()
    print("===== PERGUNTAR À IA =====")

    credenciais = listar_credenciais()

    if not credenciais:
        print("\nCadastre alguma credencial antes de perguntar à IA.")
        pausar()
        return

    print("\nA IA recebe apenas: serviço, categoria, força da senha, se a senha")
    print("é comum, com quais serviços ela se repete e há quantos dias não muda.")
    print("Senhas, usuários e observações NÃO são enviados.")

    confirmacao = input(
        "\nSeus dados vão sair do computador. Continuar? (s/n): "
    ).strip().lower()

    if confirmacao != "s":
        print("\nConsulta cancelada.")
        pausar()
        return

    pergunta = input(
        "\nO que você quer perguntar sobre suas credenciais? > "
    ).strip()

    if not pergunta:
        print("\nNenhuma pergunta foi digitada.")
        pausar()
        return

    # Registra antes de enviar: se a consulta falhar no meio do caminho,
    # o log ainda mostra que alguém tentou mandar os dados para fora.
    registrar_operacao(OP_PERGUNTAR_IA, "-", pergunta)

    # O agente já trata falta de chave, falta da biblioteca groq e erro de
    # internet: nesses casos ele mostra o motivo e devolve None.
    resposta = falar_com_agente_texto(
        montar_dados_ia(credenciais),
        pergunta,
        "CofreSeguro"
    )

    if resposta is None:
        print("\nNão foi possível consultar a IA.")

    else:
        # A resposta só é mostrada na tela. Nada que a IA diz altera o cofre.
        print("\nA resposta é gerada por IA e pode conter erros.")
        print("A classificação oficial das senhas é a do relatório (opção 4).")

    pausar()

def menu_principal():
    criar_categorias_padrao()

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

        # Erro de arquivo (sem permissão, disco cheio, CSV com acento estragado)
        # cai aqui em vez de fechar o programa. Como a exceção interrompe a
        # operação no meio, nada é salvo pela metade.
        try:
            if opcao == "0":
                print("\nSaindo do Cofre Seguro...")
                break

            elif opcao == "1":
                menu_credenciais()

            elif opcao == "2":
                menu_categorias()

            elif opcao == "3":
                menu_gerador_senha()

            elif opcao == "4":
                menu_relatorio()

            elif opcao == "5":
                menu_auditoria()

            elif opcao == "6":
                menu_ia()

            else:
                print("\nOpção inválida!")
                pausar()

        except (OSError, UnicodeDecodeError) as erro:
            print(f"\nErro ao acessar os arquivos de dados: {erro}")
            pausar()

if __name__ == "__main__":
    # Ctrl+C ou fim da entrada encerram o programa sem mostrar o erro do Python
    try:
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

    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
