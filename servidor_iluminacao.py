from xmlrpc.server import SimpleXMLRPCServer
import datetime
import random


class PainelIluminacao:
    def __init__(self):
        self.intensidade = 75
        self.espectro_atual = "branco"
        self.lampadas_ativas = True
        self.consumo_energia = 450.0
        self.log_acoes = []

        print("[ILUMINAÇÃO] Painel UV inicializado e pronto para receber comandos.")

    def ajustar_intensidade(self, valor):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        valor_seguro = max(0, min(100, valor))

        self.intensidade = valor_seguro

        self.consumo_energia = (valor_seguro / 100) * 800

        if valor_seguro == 0:
            descricao = "DESLIGADO"
            self.lampadas_ativas = False

        elif valor_seguro < 30:
            descricao = "MUITO BAIXO"
            self.lampadas_ativas = True

        elif valor_seguro < 60:
            descricao = "MODERADO"
            self.lampadas_ativas = True

        elif valor_seguro < 85:
            descricao = "ALTO"
            self.lampadas_ativas = True

        else:
            descricao = "MÁXIMO"
            self.lampadas_ativas = True

        mensagem = (
            f"[{hora_formatada}] Intensidade ajustada para "
            f"{valor_seguro}% ({descricao}). "
            f"Consumo: {self.consumo_energia:.0f}W"
        )

        self.log_acoes.append(mensagem)

        print(f"[ILUMINAÇÃO] {mensagem}")

        return (
            f"💡 Intensidade ajustada para {valor_seguro}% "
            f"({descricao}). "
            f"Consumo estimado: {self.consumo_energia:.0f}W"
        )

    def mudar_espectro(self, cor):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        espectros_validos = {
            "azul": "Estimula crescimento vegetativo (folhas e caule)",
            "vermelho": "Estimula floração e frutificação",
            "branco": "Iluminação geral balanceada",
            "uv": "Controle de patógenos e fungos",
            "infravermelho": "Estimula crescimento noturno"
        }

        cor_normalizada = cor.lower()

        if cor_normalizada in espectros_validos:
            cor_anterior = self.espectro_atual

            self.espectro_atual = cor_normalizada

            efeito = espectros_validos[cor_normalizada]

            mensagem = (
                f"[{hora_formatada}] Espectro mudado de "
                f"'{cor_anterior}' para '{cor_normalizada}'. "
                f"Efeito: {efeito}"
            )

            self.log_acoes.append(mensagem)

            print(f"[ILUMINAÇÃO] {mensagem}")

            return (
                f"🌈 Espectro alterado para "
                f"'{cor_normalizada}'! "
                f"Efeito: {efeito}"
            )

        else:
            cores_disponiveis = ", ".join(espectros_validos.keys())

            mensagem_erro = (
                f"[{hora_formatada}] "
                f"ERRO: Espectro '{cor}' não reconhecido."
            )

            self.log_acoes.append(mensagem_erro)

            print(f"[ILUMINAÇÃO] {mensagem_erro}")

            return (
                f"❌ Espectro '{cor}' inválido! "
                f"Opções disponíveis: {cores_disponiveis}"
            )

    def ping(self):
        return "pong"

    def obter_relatorio(self):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        return {
            "setor": "Iluminação UV",
            "hora_relatorio": hora_formatada,
            "intensidade": self.intensidade,
            "espectro_atual": self.espectro_atual,
            "lampadas_ativas": self.lampadas_ativas,
            "consumo_energia_w": round(self.consumo_energia, 1),
            "total_acoes": len(self.log_acoes),
            "ultimo_log": (
                self.log_acoes[-1]
                if self.log_acoes
                else "Nenhuma ação registrada ainda."
            )
        }


if __name__ == '__main__':
    HOST = "0.0.0.0"
    PORTA = 8002

    print("=" * 60)
    print("   SERVIDOR - PAINEL DE ILUMINAÇÃO UV")
    print("=" * 60)
    print(f"   Endereço: {HOST}:{PORTA}")
    print("   Aguardando conexões do terminal controlador...")
    print("=" * 60)

    servidor = SimpleXMLRPCServer(
        (HOST, PORTA),
        allow_none=True,
        logRequests=False
    )

    painel = PainelIluminacao()

    servidor.register_instance(painel)

    servidor.serve_forever()