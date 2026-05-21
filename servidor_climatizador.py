from xmlrpc.server import SimpleXMLRPCServer
import datetime
import random


class Climatizador:
    def __init__(self):
        self.temperatura_atual = 22.0
        self.temperatura_alvo = 22.0
        self.exaustores_abertos = False
        self.modo_operacao = "manutencao"
        self.umidade_relativa = 65.0
        self.consumo_energia = 1200.0
        self.log_acoes = []

        print("[CLIMATIZADOR] Sistema de climatização inicializado e pronto para receber comandos.")

    def definir_temperatura(self, graus):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        temperatura_anterior = self.temperatura_alvo

        graus_seguros = max(10, min(40, graus))

        self.temperatura_alvo = graus_seguros

        variacao_sensor = random.uniform(-0.5, 0.5)
        self.temperatura_atual = graus_seguros + variacao_sensor

        if graus_seguros > temperatura_anterior:
            self.modo_operacao = "aquecimento"
            self.consumo_energia = 2000.0
            icone = "🔴"
            descricao_modo = "AQUECENDO"

        elif graus_seguros < temperatura_anterior:
            self.modo_operacao = "resfriamento"
            self.consumo_energia = 1800.0
            icone = "🔵"
            descricao_modo = "RESFRIANDO"

        else:
            self.modo_operacao = "manutencao"
            self.consumo_energia = 800.0
            icone = "🟢"
            descricao_modo = "MANUTENÇÃO"

        mensagem = (
            f"[{hora_formatada}] Temperatura alvo definida para {graus_seguros}°C. "
            f"Modo: {descricao_modo}. "
            f"Temperatura medida: {self.temperatura_atual:.1f}°C"
        )

        self.log_acoes.append(mensagem)

        print(f"[CLIMATIZADOR] {mensagem}")

        return (
            f"{icone} Temperatura definida: {graus_seguros}°C | "
            f"Modo: {descricao_modo} | "
            f"Medição atual: {self.temperatura_atual:.1f}°C | "
            f"Consumo: {self.consumo_energia:.0f}W"
        )

    def abrir_exaustores(self):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        self.exaustores_abertos = not self.exaustores_abertos

        if self.exaustores_abertos:
            estado = "ABERTOS"
            icone = "🌬️"
            efeito = "Ventilação ativa — troca de ar em andamento"

            self.umidade_relativa = max(
                20,
                self.umidade_relativa - random.uniform(1, 5)
            )

        else:
            estado = "FECHADOS"
            icone = "🔒"
            efeito = "Ventilação desativada — ambiente selado"

            self.umidade_relativa = min(
                95,
                self.umidade_relativa + random.uniform(1, 3)
            )

        mensagem = (
            f"[{hora_formatada}] Exaustores {estado}. "
            f"{efeito}. "
            f"Umidade atual: {self.umidade_relativa:.1f}%"
        )

        self.log_acoes.append(mensagem)

        print(f"[CLIMATIZADOR] {mensagem}")

        return (
            f"{icone} Exaustores {estado}! {efeito} | "
            f"Umidade relativa: {self.umidade_relativa:.1f}%"
        )

    def ping(self):
        return "pong"

    def obter_relatorio(self):
        agora = datetime.datetime.now()
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        variacao = random.uniform(-0.3, 0.3)
        self.temperatura_atual = round(
            self.temperatura_atual + variacao,
            1
        )

        self.temperatura_atual = max(
            10,
            min(40, self.temperatura_atual)
        )

        return {
            "setor": "Climatizador",
            "hora_relatorio": hora_formatada,
            "temperatura_alvo": self.temperatura_alvo,
            "temperatura_atual": self.temperatura_atual,
            "exaustores_abertos": self.exaustores_abertos,
            "modo_operacao": self.modo_operacao,
            "umidade_relativa": round(self.umidade_relativa, 1),
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
    PORTA = 8003

    print("=" * 60)
    print("   SERVIDOR - CLIMATIZADOR")
    print("=" * 60)
    print(f"   Endereço: {HOST}:{PORTA}")
    print("   Aguardando conexões do terminal controlador...")
    print("=" * 60)

    servidor = SimpleXMLRPCServer(
        (HOST, PORTA),
        allow_none=True,
        logRequests=False
    )

    climatizador = Climatizador()

    servidor.register_instance(climatizador)

    servidor.serve_forever()