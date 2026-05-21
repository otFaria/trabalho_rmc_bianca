from xmlrpc.server import SimpleXMLRPCServer
import datetime
import random


class SetorHidroponico:
    def __init__(self):
        self.irrigacao_ativa = False
        self.nivel_agua = 85.0
        self.tempo_irrigacao_restante = 0
        self.log_acoes = []

        print("[HIDROPÔNICO] Setor inicializado e pronto para receber comandos.")

    def ativar_irrigacao(self, tempo):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        self.irrigacao_ativa = True
        self.tempo_irrigacao_restante = tempo

        consumo = tempo * 0.5

        self.nivel_agua = max(0, self.nivel_agua - consumo)

        mensagem = (
            f"[{hora_formatada}] Irrigação ATIVADA por {tempo} minutos. "
            f"Nível de água agora: {self.nivel_agua:.1f}%"
        )

        self.log_acoes.append(mensagem)

        print(f"[HIDROPÔNICO] {mensagem}")

        return (
            f"✅ Irrigação ativada com sucesso por {tempo} minutos! "
            f"Nível de água: {self.nivel_agua:.1f}%"
        )

    def checar_nivel_agua(self):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        variacao = random.uniform(-1, 1)

        self.nivel_agua = max(
            0,
            min(100, self.nivel_agua + variacao)
        )

        if self.nivel_agua > 50:
            status = f"NORMAL ({self.nivel_agua:.1f}%)"

        elif self.nivel_agua > 20:
            status = (
                f"BAIXO ({self.nivel_agua:.1f}%) - "
                f"Considere reabastecer"
            )

        else:
            status = (
                f"CRÍTICO ({self.nivel_agua:.1f}%) - "
                f"REABASTECER URGENTE!"
            )

        mensagem = (
            f"[{hora_formatada}] "
            f"Nível de água verificado: {status}"
        )

        self.log_acoes.append(mensagem)

        print(f"[HIDROPÔNICO] {mensagem}")

        return f"💧 Nível de água: {status}"

    def ping(self):
        return "pong"

    def obter_relatorio(self):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        return {
            "setor": "Hidropônico",
            "hora_relatorio": hora_formatada,
            "irrigacao_ativa": self.irrigacao_ativa,
            "nivel_agua": round(self.nivel_agua, 1),
            "tempo_irrigacao_restante": self.tempo_irrigacao_restante,
            "total_acoes": len(self.log_acoes),
            "ultimo_log": (
                self.log_acoes[-1]
                if self.log_acoes
                else "Nenhuma ação registrada ainda."
            )
        }


if __name__ == '__main__':
    HOST = "0.0.0.0"
    PORTA = 8001

    print("=" * 60)
    print("   SERVIDOR - SETOR HIDROPÔNICO")
    print("=" * 60)
    print(f"   Endereço: {HOST}:{PORTA}")
    print("   Aguardando conexões do terminal controlador...")
    print("=" * 60)

    servidor = SimpleXMLRPCServer(
        (HOST, PORTA),
        allow_none=True,
        logRequests=False
    )

    setor = SetorHidroponico()

    servidor.register_instance(setor)

    servidor.serve_forever()