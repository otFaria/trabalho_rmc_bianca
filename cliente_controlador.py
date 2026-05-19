
# =============================================================================
# CLIENTE CONTROLADOR - TERMINAL DE CONTROLE DA ESTUFA
# =============================================================================
# Este arquivo representa o computador do AGRÔNOMO (máquina cliente).
# Ele se conecta remotamente aos 3 servidores da estufa e permite:
#   - Controlar cada setor individualmente
#   - Gerar um relatório completo de todos os setores com um único comando
# =============================================================================

# --- IMPORTAÇÕES ---

# "import xmlrpc.client" importa o módulo que cria conexões RPC para o CLIENTE
# É o "lado oposto" do SimpleXMLRPCServer usado nos servidores
# Com ele, podemos chamar funções que estão em outros computadores pela rede
import xmlrpc.client

# Importa datetime para registrar quando o relatório foi gerado
import datetime

# Importa o módulo "sys" para controlar o encerramento do programa
# sys.exit() → encerra o programa imediatamente
import sys


# =============================================================================
# CONFIGURAÇÕES DE REDE - ENDEREÇOS DOS SERVIDORES
# =============================================================================
# Aqui definimos onde estão os 3 servidores da estufa na rede.
# IMPORTANTE: Substitua os IPs abaixo pelos IPs reais das máquinas no laboratório.
#
# Para descobrir o IP de uma máquina Windows: abra o CMD e digite "ipconfig"
# Procure por "Endereço IPv4" - exemplo: 192.168.1.101
#
# Formato da URL: "http://IP_DA_MAQUINA:PORTA"
# =============================================================================

# IP e porta do servidor hidropônico (máquina 1)
# Altere "192.168.1.101" para o IP real do computador do setor hidropônico
IP_HIDROPONICO  = "172.22.112.1"
PORTA_HIDROPONICO = 8001

# IP e porta do servidor de iluminação UV (máquina 2)
# Altere "192.168.1.102" para o IP real do computador do painel de iluminação
IP_ILUMINACAO = "172.19.32.1"
PORTA_ILUMINACAO = 8002

# IP e porta do servidor do climatizador (máquina 3)
# Altere "192.168.1.103" para o IP real do computador do climatizador
IP_CLIMATIZADOR = "172.25.4.47"
PORTA_CLIMATIZADOR = 8003


# =============================================================================
# CLASSE Relatorio
# =============================================================================
# Esta é a classe DIFERENCIAL do projeto!
# Com um único método, o agrônomo recebe dados de TODOS os setores ao mesmo tempo,
# sem precisar consultar cada servidor individualmente.
# É como um "dashboard" — um painel que agrega tudo num só lugar.
# =============================================================================

class Relatorio:
    # -------------------------------------------------------------------------
    # MÉTODO __init__ (Construtor)
    # -------------------------------------------------------------------------
    # Recebe as 3 conexões RPC já estabelecidas com os servidores.
    # Parâmetros:
    #   - self           → referência ao próprio objeto Relatorio
    #   - proxy_hidro    → conexão com o servidor hidropônico
    #   - proxy_ilum     → conexão com o servidor de iluminação
    #   - proxy_clima    → conexão com o servidor do climatizador
    # -------------------------------------------------------------------------
    def __init__(self, proxy_hidro, proxy_ilum, proxy_clima):
        # Guarda as referências para os 3 servidores como atributos do objeto
        # Esses "proxies" são objetos especiais que representam os servidores remotos
        # Quando chamamos proxy_hidro.algum_metodo(), a chamada vai pela rede até o servidor
        self.proxy_hidro = proxy_hidro  # Conexão com o setor hidropônico
        self.proxy_ilum  = proxy_ilum   # Conexão com o painel de iluminação
        self.proxy_clima = proxy_clima  # Conexão com o climatizador

    # -------------------------------------------------------------------------
    # MÉTODO gerar_relatorio_diario
    # -------------------------------------------------------------------------
    # Coleta dados de todos os servidores e exibe um relatório formatado.
    # Este é o método que o agrônomo chama com "um clique" para ver tudo.
    # -------------------------------------------------------------------------
    def gerar_relatorio_diario(self):
        # Obtém data e hora atual para o cabeçalho do relatório
        agora = datetime.datetime.now()
        # Formata como texto: "Dia/Mês/Ano Hora:Minuto:Segundo"
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Exibe o cabeçalho do relatório
        print("\n" + "=" * 65)
        print("       📊  RELATÓRIO DIÁRIO — ESTUFA INTELIGENTE")
        print(f"       🕐  Gerado em: {hora_formatada}")
        print("=" * 65)

        # --- COLETA DE DADOS DE CADA SERVIDOR ---
        # Para cada servidor, tentamos buscar o relatório.
        # Se um servidor estiver offline, capturamos o erro e continuamos.

        # Lista que vai acumular os dados de cada setor
        # Começamos com lista vazia e vamos adicionando os dados
        dados_setores = []

        # ---- SETOR 1: HIDROPÔNICO ----
        try:
            # Chama o método obter_relatorio() no servidor hidropônico pela rede
            # self.proxy_hidro → o proxy (representante) do servidor hidropônico
            # .obter_relatorio() → o método que queremos chamar naquele servidor
            # Esta chamada viaja pela rede até o servidor e volta com a resposta
            dados_hidro = self.proxy_hidro.obter_relatorio()

            # Adiciona os dados na lista
            dados_setores.append(("HIDROPÔNICO", dados_hidro, True))

        except Exception as erro:
            # "except Exception as erro" → captura qualquer erro que ocorra
            # Se o servidor estiver desligado ou inacessível, isso evita que o programa trave
            # "erro" contém a descrição do problema
            dados_setores.append(("HIDROPÔNICO", {"erro": str(erro)}, False))

        # ---- SETOR 2: ILUMINAÇÃO UV ----
        try:
            # Chama obter_relatorio() no servidor de iluminação
            dados_ilum = self.proxy_ilum.obter_relatorio()
            dados_setores.append(("ILUMINAÇÃO UV", dados_ilum, True))
        except Exception as erro:
            dados_setores.append(("ILUMINAÇÃO UV", {"erro": str(erro)}, False))

        # ---- SETOR 3: CLIMATIZADOR ----
        try:
            # Chama obter_relatorio() no servidor do climatizador
            dados_clima = self.proxy_clima.obter_relatorio()
            dados_setores.append(("CLIMATIZADOR", dados_clima, True))
        except Exception as erro:
            dados_setores.append(("CLIMATIZADOR", {"erro": str(erro)}, False))

        # --- EXIBIÇÃO DOS DADOS ---
        # Percorre a lista de setores e exibe os dados de cada um
        # "for nome, dados, online in dados_setores" → desempacota cada tupla (grupo de 3 valores)
        for nome, dados, online in dados_setores:
            print(f"\n  🌿 SETOR: {nome}")
            print("  " + "-" * 60)

            if not online:
                # Se o servidor estiver offline, exibe mensagem de erro
                print(f"  ❌ SERVIDOR OFFLINE — {dados.get('erro', 'Erro desconhecido')}")
                continue  # "continue" → pula para o próximo item do loop

            # Exibe cada dado do dicionário recebido do servidor
            # "for chave, valor in dados.items()" → percorre todos os pares chave/valor
            for chave, valor in dados.items():
                # Ignora as chaves "setor" e "hora_relatorio" pois já exibimos
                if chave in ("setor", "hora_relatorio"):
                    continue

                # Formata o nome da chave: substitui "_" por espaço e coloca em maiúsculas
                # .replace("_", " ") → troca underline por espaço: "nivel_agua" → "nivel agua"
                # .capitalize() → primeira letra maiúscula: "nivel agua" → "Nivel agua"
                chave_formatada = chave.replace("_", " ").capitalize()

                # Formata valores booleanos (True/False) para texto em português
                if isinstance(valor, bool):
                    # isinstance(valor, bool) → verifica se "valor" é do tipo booleano
                    valor_exibido = "✅ SIM" if valor else "❌ NÃO"
                else:
                    # Para outros tipos, converte direto para texto
                    valor_exibido = str(valor)

                # Exibe a chave e o valor alinhados
                print(f"  {'  '+chave_formatada:<30}: {valor_exibido}")

        # Rodapé do relatório
        print("\n" + "=" * 65)
        print("       ✅  FIM DO RELATÓRIO DIÁRIO")
        print("=" * 65 + "\n")


# =============================================================================
# FUNÇÃO conectar_servidor
# =============================================================================
# Tenta criar uma conexão RPC com um servidor.
# Se não conseguir conectar, retorna None (vazio) em vez de travar o programa.
# Parâmetros:
#   - ip    → endereço IP do servidor
#   - porta → porta de comunicação do servidor
#   - nome  → nome descritivo do servidor (para exibir na tela)
# =============================================================================

def conectar_servidor(ip, porta, nome):
    try:
        # Cria o "proxy" — um objeto que representa o servidor remoto
        # xmlrpc.client.ServerProxy() → função que cria a conexão com o servidor
        # f"http://{ip}:{porta}" → monta a URL do servidor, ex: "http://192.168.1.101:8001"
        proxy = xmlrpc.client.ServerProxy(f"http://{ip}:{porta}", allow_none=True)

        # Testa a conexão chamando o método "ping()" definido nos servidores
        # Se o servidor estiver offline ou inacessível, vai gerar um erro e cair no "except"
        # Isso é melhor que "system.listMethods" porque é um método que nós mesmos criamos
        proxy.ping()

        # Se chegou aqui sem erro, a conexão funcionou!
        print(f"  ✅ Conectado ao servidor: {nome} ({ip}:{porta})")

        # Retorna o proxy para ser usado posteriormente
        return proxy

    except Exception as erro:
        # Se não conseguiu conectar, exibe a mensagem de erro
        print(f"  ❌ Falha ao conectar em {nome} ({ip}:{porta}): {erro}")

        # Retorna None — indica que este servidor não está disponível
        return None


# =============================================================================
# FUNÇÃO menu_hidroponico
# =============================================================================
# Exibe e processa o menu de ações do setor hidropônico.
# Parâmetros:
#   - proxy → conexão com o servidor hidropônico
# =============================================================================

def menu_hidroponico(proxy):
    # Loop que mantém o menu ativo até o usuário escolher "voltar"
    while True:
        print("\n  --- SETOR HIDROPÔNICO ---")
        print("  [1] Ativar irrigação")
        print("  [2] Checar nível de água")
        print("  [0] Voltar ao menu principal")

        # input() → pausa o programa e espera o usuário digitar algo
        # .strip() → remove espaços extras antes e depois do texto digitado
        opcao = input("\n  Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                # Pede ao usuário o tempo de irrigação
                # int() → converte o texto digitado em número inteiro
                tempo = int(input("  Tempo de irrigação (minutos): "))

                # Chama o método ativar_irrigacao() no servidor hidropônico pela rede
                # proxy.ativar_irrigacao(tempo) → envia o comando ao servidor remoto
                resultado = proxy.ativar_irrigacao(tempo)

                # Exibe a resposta recebida do servidor
                print(f"\n  Resposta do servidor: {resultado}")

            except ValueError:
                # ValueError ocorre quando o usuário digita algo que não é número
                print("  ❌ Por favor, digite um número inteiro válido.")
            except Exception as erro:
                # Outros erros (ex: servidor offline)
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "2":
            try:
                # Chama checar_nivel_agua() no servidor — sem parâmetros
                resultado = proxy.checar_nivel_agua()
                print(f"\n  Resposta do servidor: {resultado}")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "0":
            # Sai do loop e volta ao menu principal
            break

        else:
            print("  ❌ Opção inválida. Tente novamente.")


# =============================================================================
# FUNÇÃO menu_iluminacao
# =============================================================================
# Exibe e processa o menu de ações do painel de iluminação UV.
# =============================================================================

def menu_iluminacao(proxy):
    while True:
        print("\n  --- PAINEL DE ILUMINAÇÃO UV ---")
        print("  [1] Ajustar intensidade das lâmpadas")
        print("  [2] Mudar espectro (cor)")
        print("  [0] Voltar ao menu principal")

        opcao = input("\n  Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                # Pede o valor de intensidade (0 a 100)
                # int() → converte texto em número inteiro
                valor = int(input("  Intensidade (0 a 100%): "))

                # Chama ajustar_intensidade() no servidor de iluminação
                resultado = proxy.ajustar_intensidade(valor)
                print(f"\n  Resposta do servidor: {resultado}")

            except ValueError:
                print("  ❌ Por favor, digite um número inteiro entre 0 e 100.")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "2":
            # Exibe as opções de espectro disponíveis
            print("  Espectros disponíveis: azul, vermelho, branco, uv, infravermelho")
            cor = input("  Digite o espectro desejado: ").strip()

            try:
                # Chama mudar_espectro() no servidor com a cor escolhida
                resultado = proxy.mudar_espectro(cor)
                print(f"\n  Resposta do servidor: {resultado}")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "0":
            break
        else:
            print("  ❌ Opção inválida. Tente novamente.")


# =============================================================================
# FUNÇÃO menu_climatizador
# =============================================================================
# Exibe e processa o menu de ações do climatizador.
# =============================================================================

def menu_climatizador(proxy):
    while True:
        print("\n  --- CLIMATIZADOR ---")
        print("  [1] Definir temperatura")
        print("  [2] Abrir/Fechar exaustores")
        print("  [0] Voltar ao menu principal")

        opcao = input("\n  Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                # float() → converte o texto digitado em número decimal
                # Permite temperaturas como 22.5°C
                graus = float(input("  Temperatura desejada (°C, entre 10 e 40): "))

                # Chama definir_temperatura() no servidor do climatizador
                resultado = proxy.definir_temperatura(graus)
                print(f"\n  Resposta do servidor: {resultado}")

            except ValueError:
                print("  ❌ Por favor, digite um número válido (ex: 24 ou 24.5).")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "2":
            try:
                # Chama abrir_exaustores() no servidor — sem parâmetros
                resultado = proxy.abrir_exaustores()
                print(f"\n  Resposta do servidor: {resultado}")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "0":
            break
        else:
            print("  ❌ Opção inválida. Tente novamente.")


# =============================================================================
# BLOCO PRINCIPAL - PONTO DE ENTRADA DO PROGRAMA CLIENTE
# =============================================================================

if __name__ == '__main__':
    # Exibe o cabeçalho de boas-vindas
    print("\n" + "=" * 65)
    print("   🌱  SISTEMA DE CONTROLE — ESTUFA INTELIGENTE")
    print("   Terminal Controlador — Estação do Agrônomo")
    print("=" * 65)
    print("\n  Conectando aos servidores da estufa...\n")

    # --- CONEXÃO COM OS SERVIDORES ---
    # Tenta se conectar aos 3 servidores
    # Se um servidor estiver offline, retorna None e o sistema continua

    proxy_hidro = conectar_servidor(IP_HIDROPONICO,  PORTA_HIDROPONICO,  "Hidropônico")
    proxy_ilum  = conectar_servidor(IP_ILUMINACAO,   PORTA_ILUMINACAO,   "Iluminação UV")
    proxy_clima = conectar_servidor(IP_CLIMATIZADOR, PORTA_CLIMATIZADOR, "Climatizador")

    # Cria o objeto Relatorio passando as 3 conexões
    # Mesmo que algum servidor esteja offline (None), o objeto é criado
    # (o método gerar_relatorio_diario trata isso com try/except)
    relatorio = Relatorio(proxy_hidro, proxy_ilum, proxy_clima)

    print("\n  Conexões estabelecidas. Sistema pronto!")

    # --- MENU PRINCIPAL ---
    # Loop infinito que mantém o programa rodando até o usuário sair
    while True:
        print("\n" + "=" * 65)
        print("   MENU PRINCIPAL")
        print("=" * 65)
        print("  [1] 💧 Setor Hidropônico")
        print("  [2] 💡 Painel de Iluminação UV")
        print("  [3] 🌡️  Climatizador")
        print("  [4] 📊 Gerar Relatório Geral (todos os setores)")
        print("  [0] 🚪 Sair do sistema")
        print("-" * 65)

        opcao = input("  Escolha uma opção: ").strip()

        if opcao == "1":
            # Verifica se a conexão com o servidor hidropônico está disponível
            if proxy_hidro is None:
                print("\n  ❌ Servidor Hidropônico está OFFLINE. Não é possível controlar.")
            else:
                # Chama a função que exibe o submenu do setor hidropônico
                menu_hidroponico(proxy_hidro)

        elif opcao == "2":
            if proxy_ilum is None:
                print("\n  ❌ Servidor de Iluminação está OFFLINE. Não é possível controlar.")
            else:
                menu_iluminacao(proxy_ilum)

        elif opcao == "3":
            if proxy_clima is None:
                print("\n  ❌ Servidor Climatizador está OFFLINE. Não é possível controlar.")
            else:
                menu_climatizador(proxy_clima)

        elif opcao == "4":
            # Chama o método da classe Relatorio
            # relatorio → o objeto da classe Relatorio que criamos antes
            # .gerar_relatorio_diario() → o método que coleta e exibe tudo de uma vez
            relatorio.gerar_relatorio_diario()

        elif opcao == "0":
            print("\n  👋 Encerrando o sistema. Até logo!\n")
            # sys.exit(0) → encerra o programa com código 0 (sucesso)
            sys.exit(0)

        else:
            print("  ❌ Opção inválida. Por favor, escolha entre as opções listadas.")
