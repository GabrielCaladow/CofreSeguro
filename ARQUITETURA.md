# Arquitetura do CofreSeguro

Documento de referência do grupo. **Antes de mudar qualquer coisa da seção "Combinados", combine com o grupo.**

## 1. Equipe e arquivos

Cada arquivo tem **um único dono**. Só o Calado edita o arquivo. Quem precisar de algo diferente pede a Calado.

| Função | Pessoa | Arquivos |
|---|---|---|
| 1. Interface e Integração | Heitor | `main.py`, `README.md` (manual) |
| 1. Interface e Integração | Gabriel Calado | `entrada.py` + revisão/integração dos Pull Requests |
| 2. Dados | Gabriel Calado | `armazenamento.py`, `credenciais.py` |
| 3. Força de Senha | João Henrique | `forca_senha.py`, `senhas_comuns.txt` |
| 3. Força de Senha | Raul | `gerador_senha.py` (funcionalidade extra) |
| 4. Auditoria e Relatório | João Felipe | `auditoria.py`, `tempo.py` |
| 4. Auditoria e Relatório | Bruno Parente | `relatorio.py` |

Os arquivos de dados ficam na pasta `dados/`. Quem cria a pasta, se ela não existir, é o programa, e não uma pessoa.

| Arquivo de dados | Calado (quem lê e grava) |
|---|---|
| `dados/credenciais.csv` | Gabriel (`armazenamento.py`) |
| `dados/categorias.csv` | Gabriel (`armazenamento.py`) |
| `dados/auditoria.log` | João Felipe (`auditoria.py`) |
| `senhas_comuns.txt` | João Henrique (`forca_senha.py`). Uma senha por linha, **sem comentários** (um comentário seria lido como senha). |

## 2. Camadas e quem pode importar quem

```
                 main.py  (Heitor)  ── único lugar que conversa com o usuário
                    │      entrada.py (Gabriel) ── input() validado
    ┌───────────┬───┴────────┬──────────────┬──────────────┐
    ▼           ▼            ▼              ▼              ▼
credenciais  forca_senha  gerador_senha  relatorio     auditoria
 (Gabriel)  (João Henr.)    (Raul)        (Bruno)     (João Felipe)
    │                        │  └► forca_senha   │  └► forca_senha  │
    ▼                                             ▼                 ▼
armazenamento                                   tempo ◄─────────────┘
 (Gabriel)                                   (João Felipe)
```

Regras:

1. **As setas só descem.** Um módulo de baixo nunca importa um de cima. Por exemplo, `credenciais.py` nunca importa `main.py`.
2. **Só `main.py` e `entrada.py` usam `print()` e `input()`.** Os outros módulos **recebem dados e devolvem dados**. Exemplo: `forca_senha` devolve a classificação e a lista de motivos, e quem mostra isso na tela é o `main.py`.
3. **Quem registra no log é o `main.py`.** Ele chama a auditoria depois de cada operação que deu certo. `credenciais.py` não sabe que o log existe.
4. **`relatorio.py` não lê arquivo.** Ele recebe a lista de credenciais pronta, que o `main.py` pega em `credenciais.py`.
5. Bibliotecas permitidas: **só `os`, `datetime`, `random`**. O módulo `csv` **não** é permitido, então o CSV é lido e escrito "na mão".

## 3. Combinados

### 3.1 Formato dos dados

**Credencial**: um dicionário com as chaves abaixo.

| Chave | Exemplo | Observação |
|---|---|---|
| `id` | `3` | inteiro, gerado pelo sistema. Dois logins no mesmo serviço são permitidos. |
| `servico` | `Gmail` | |
| `usuario` | `lucas@email.com` | |
| `senha` | `abc123` | texto simples (sistema didático!) |
| `categoria` | `banco` | precisa existir nas categorias |
| `observacoes` | `conta antiga` | pode ser vazio |
| `data_alteracao` | `2026-10-26 14:30` | formato definido em `tempo.py` |

**Categoria**: dicionário com `nome` e `forca_minima`. O valor de `forca_minima` é `"fraca"`, `"media"` ou `"forte"`.
Se `categorias.csv` não existir, o sistema cria o padrão: banco, rede social, estudo, trabalho, outros.

**Arquivos CSV**: separador `;`, uma linha de cabeçalho, uma linha por registro.
**`entrada.py` recusa textos que contenham `;` ou quebra de linha**, porque esses caracteres quebrariam o arquivo. Essa é a fronteira de validação.

**Linha do log**: `data_hora;operacao;servico`. Exemplo: `2026-10-26 14:30;REVELAR;Gmail`.
Operações válidas: `ADICIONAR`, `EDITAR`, `EXCLUIR`, `REVELAR`, `CRIAR_CATEGORIA`, `GERAR_SENHA`, `VER_RELATORIO`, `VER_LOG`.

**Níveis de força**: sempre as strings `"fraca"`, `"media"` e `"forte"`, sem acento, iguais em todos os módulos.

### 3.2 Funções que cada módulo oferece aos outros

São nomes sugeridos. O dono pode criar outras funções internas à vontade, mas **estas assinaturas são o contrato**.

**`entrada.py` (Gabriel)**
- `ler_texto(mensagem, obrigatorio)`: devolve um texto sem `;` nem quebra de linha e repete a pergunta até a entrada ser válida
- `ler_inteiro(mensagem, minimo, maximo)`: devolve um inteiro e trata `ValueError`
- `confirmar(mensagem)`: devolve `True`/`False` (s/n)
- `limpar_tela()` e `pausar()`

**`armazenamento.py` (Gabriel)**
- `carregar_credenciais()`: devolve a lista de dicionários (lista vazia se o arquivo não existir)
- `salvar_credenciais(lista)`
- `carregar_categorias()` e `salvar_categorias(lista)`
- Trata `FileNotFoundError` e `PermissionError`

**`credenciais.py` (Gabriel)**
- `listar_credenciais()`, `buscar_credencial(id)`
- `adicionar_credencial(servico, usuario, senha, categoria, observacoes)`: devolve a credencial criada
- `editar_credencial(id, campos_novos)` e `excluir_credencial(id)`: devolvem `True`/`False`
- `mascarar_senha(senha)`: `"abc123"` vira `"ab****"`
- `listar_categorias()`, `adicionar_categoria(nome, forca_minima)`, `buscar_categoria(nome)`

**`forca_senha.py` (João Henrique)**
- `avaliar_senha(senha)`: devolve `(nivel, motivos)`, com `nivel` em `"fraca"/"media"/"forte"` e `motivos` como lista de frases explicando o porquê
- `eh_senha_comum(senha)`: devolve `True`/`False` (lê `senhas_comuns.txt`)
- `atende_minimo(nivel, forca_minima)`: devolve `True`/`False`

**`gerador_senha.py` (Raul)**
- `gerar_senha_forte(tamanho)`: usa `random` e confere com `avaliar_senha` que o resultado sai `"forte"`

**`tempo.py` (João Felipe)**
- `agora_texto()`: devolve `"AAAA-MM-DD HH:MM"`
- `dias_desde(data_texto)`: devolve um inteiro

**`auditoria.py` (João Felipe)**
- `registrar_operacao(operacao, servico)`
- `ler_log()`: devolve a lista de dicionários `{data_hora, operacao, servico}`

**`relatorio.py` (Bruno)**
- `encontrar_senhas_repetidas(credenciais)`: devolve uma lista de grupos de serviços que compartilham a mesma senha (**sem devolver a senha**)
- `gerar_relatorio(credenciais)`: devolve um dicionário com total, quantas são fracas, quantas repetidas, quantas comuns e os dias sem alteração de cada uma

## 4. Menu (dono: Heitor)

```
1. Credenciais  (listar mascarado / adicionar / editar / excluir / revelar senha)
2. Categorias   (listar / cadastrar)
3. Gerar senha forte
4. Relatório de segurança
5. Log de auditoria
6. Perguntar à IA  (reservado para o módulo da aula)
0. Sair
```

Fluxo de "adicionar credencial" (exemplo de integração no `main.py`):
`entrada.ler_texto` → `forca_senha.avaliar_senha` + `eh_senha_comum` + `atende_minimo` → mostra os motivos e, se a senha estiver abaixo do mínimo, pede `confirmar` → `credenciais.adicionar_credencial` → `auditoria.registrar_operacao("ADICIONAR", servico)`.

## 5. Como trabalhar

1. **Contrato primeiro.** Na primeira semana, cada um cria **as funções do seu contrato devolvendo valores falsos**. Exemplo: `avaliar_senha` sempre devolve `("media", ["em construção"])`. Assim o Heitor já consegue montar o menu inteiro sem esperar ninguém.
2. **Uma branch por pessoa** (`git checkout -b forca-senha`), **Pull Request** para a `main`, e o Gabriel revisa e faz o merge. Ninguém faz push direto na `main`.
3. **Commits pequenos e frequentes**, com mensagem dizendo o que mudou (`"forca_senha: verifica símbolos"`).
4. **Integrar toda semana.** Esperar todo mundo terminar para juntar no fim é a maior causa de projeto que não roda no dia da entrega.
5. **Cada um testa o próprio módulo** com um bloco `if __name__ == "__main__":` no fim do arquivo, chamando as próprias funções com dados fictícios.
6. **Exceções ficam com o dono do recurso.** Erros de arquivo são tratados por quem lê ou grava aquele arquivo (Gabriel e João Felipe). Erros de digitação são tratados no `entrada.py`. O `main.py` não deve precisar de `try/except` espalhado.
7. **Só dados fictícios.** Nunca use uma senha real.