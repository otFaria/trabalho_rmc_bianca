
import xmlrpc.client
import datetime
import sys

IP_HIDROPONICO = "172.30.0.1"
PORTA_HIDROPONICO = 8001

IP_ILUMINACAO = "172.30.0.121" #(L6-M13)
PORTA_ILUMINACAO = 8002

IP_CLIMATIZADOR = "172.30.0.120" #(L6-M12)
PORTA_CLIMATIZADOR = 8003


class Relatorio:
    def __init__(self, proxy_hidro, proxy_ilum, proxy_clima):
        self.proxy_hidro = proxy_hidro
        self.proxy_ilum = proxy_ilum
        self.proxy_clima = proxy_clima

    def gerar_relatorio_diario(self):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        print("\n" + "=" * 65)
        print("       📊  RELATÓRIO DIÁRIO — ESTUFA INTELIGENTE")
        print(f"       🕐  Gerado em: {hora_formatada}")
        print("=" * 65)

        dados_setores = []

        try:
            dados_hidro = self.proxy_hidro.obter_relatorio()
            dados_setores.append(("HIDROPÔNICO", dados_hidro, True))
        except Exception as erro:
            dados_setores.append(("HIDROPÔNICO", {"erro": str(erro)}, False))

        try:
            dados_ilum = self.proxy_ilum.obter_relatorio()
            dados_setores.append(("ILUMINAÇÃO UV", dados_ilum, True))
        except Exception as erro:
            dados_setores.append(("ILUMINAÇÃO UV", {"erro": str(erro)}, False))

        try:
            dados_clima = self.proxy_clima.obter_relatorio()
            dados_setores.append(("CLIMATIZADOR", dados_clima, True))
        except Exception as erro:
            dados_setores.append(("CLIMATIZADOR", {"erro": str(erro)}, False))

        for nome, dados, online in dados_setores:
            print(f"\n  🌿 SETOR: {nome}")
            print("  " + "-" * 60)

            if not online:
                print(f"  ❌ SERVIDOR OFFLINE — {dados.get('erro', 'Erro desconhecido')}")
                continue

            for chave, valor in dados.items():
                if chave in ("setor", "hora_relatorio"):
                    continue

                chave_formatada = chave.replace("_", " ").capitalize()

                if isinstance(valor, bool):
                    valor_exibido = "✅ SIM" if valor else "❌ NÃO"
                else:
                    valor_exibido = str(valor)

                print(f"  {'  '+chave_formatada:<30}: {valor_exibido}")

        print("\n" + "=" * 65)
        print("       ✅  FIM DO RELATÓRIO DIÁRIO")
        print("=" * 65 + "\n")


def conectar_servidor(ip, porta, nome):
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{ip}:{porta}", allow_none=True)
        proxy.ping()
        print(f"  ✅ Conectado ao servidor: {nome} ({ip}:{porta})")
        return proxy
    except Exception as erro:
        print(f"  ❌ Falha ao conectar em {nome} ({ip}:{porta}): {erro}")
        return None


def menu_hidroponico(proxy):
    while True:
        print("\n  --- SETOR HIDROPÔNICO ---")
        print("  [1] Ativar irrigação")
        print("  [2] Checar nível de água")
        print("  [0] Voltar ao menu principal")

        opcao = input("\n  Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                tempo = int(input("  Tempo de irrigação (minutos): "))
                resultado = proxy.ativar_irrigacao(tempo)
                print(f"\n  Resposta do servidor: {resultado}")
            except ValueError:
                print("  ❌ Por favor, digite um número inteiro válido.")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "2":
            try:
                resultado = proxy.checar_nivel_agua()
                print(f"\n  Resposta do servidor: {resultado}")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "0":
            break
        else:
            print("  ❌ Opção inválida. Tente novamente.")


def menu_iluminacao(proxy):
    while True:
        print("\n  --- PAINEL DE ILUMINAÇÃO UV ---")
        print("  [1] Ajustar intensidade das lâmpadas")
        print("  [2] Mudar espectro (cor)")
        print("  [0] Voltar ao menu principal")

        opcao = input("\n  Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                valor = int(input("  Intensidade (0 a 100%): "))
                resultado = proxy.ajustar_intensidade(valor)
                print(f"\n  Resposta do servidor: {resultado}")
            except ValueError:
                print("  ❌ Por favor, digite um número inteiro entre 0 e 100.")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "2":
            print("  Espectros disponíveis: azul, vermelho, branco, uv, infravermelho")
            cor = input("  Digite o espectro desejado: ").strip()
            try:
                resultado = proxy.mudar_espectro(cor)
                print(f"\n  Resposta do servidor: {resultado}")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "0":
            break
        else:
            print("  ❌ Opção inválida. Tente novamente.")


def menu_climatizador(proxy):
    while True:
        print("\n  --- CLIMATIZADOR ---")
        print("  [1] Definir temperatura")
        print("  [2] Abrir/Fechar exaustores")
        print("  [0] Voltar ao menu principal")

        opcao = input("\n  Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                graus = float(input("  Temperatura desejada (°C, entre 10 e 40): "))
                resultado = proxy.definir_temperatura(graus)
                print(f"\n  Resposta do servidor: {resultado}")
            except ValueError:
                print("  ❌ Por favor, digite um número válido (ex: 24 ou 24.5).")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "2":
            try:
                resultado = proxy.abrir_exaustores()
                print(f"\n  Resposta do servidor: {resultado}")
            except Exception as erro:
                print(f"  ❌ Erro de comunicação: {erro}")

        elif opcao == "0":
            break
        else:
            print("  ❌ Opção inválida. Tente novamente.")


if __name__ == '__main__':
    print("\n" + "=" * 65)
    print("   🌱  SISTEMA DE CONTROLE — ESTUFA INTELIGENTE")
    print("   Terminal Controlador — Estação do Agrônomo")
    print("=" * 65)
    print("\n  Conectando aos servidores da estufa...\n")

    proxy_hidro = conectar_servidor(IP_HIDROPONICO,  PORTA_HIDROPONICO,  "Hidropônico")
    proxy_ilum = conectar_servidor(IP_ILUMINACAO,   PORTA_ILUMINACAO,   "Iluminação UV")
    proxy_clima = conectar_servidor(IP_CLIMATIZADOR, PORTA_CLIMATIZADOR, "Climatizador")

    relatorio = Relatorio(proxy_hidro, proxy_ilum, proxy_clima)

    print("\n  Conexões estabelecidas. Sistema pronto!")

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
