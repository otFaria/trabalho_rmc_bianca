
# =============================================================================
# SERVIDOR DO CLIMATIZADOR
# =============================================================================
# Este arquivo representa o computador do setor de climatização da estufa.
# Ele controla a temperatura e a ventilação do ambiente para as plantas.
# Fica "ouvindo" na rede esperando comandos do cliente (terminal controlador).
# =============================================================================

# --- IMPORTAÇÕES DE BIBLIOTECAS ---

# Importa SimpleXMLRPCServer do módulo xmlrpc.server
# xmlrpc → protocolo de comunicação pela internet (XML Remote Procedure Call)
# server → parte do módulo responsável pelo lado SERVIDOR da comunicação
# SimpleXMLRPCServer → a classe que cria o servidor de chamadas remotas
from xmlrpc.server import SimpleXMLRPCServer

# Importa o módulo datetime para trabalhar com datas e horas do sistema
import datetime

# Importa o módulo random para simular variações de temperatura (como sensores reais)
import random


# =============================================================================
# DEFINIÇÃO DA CLASSE Climatizador
# =============================================================================
# Esta classe modela o comportamento do sistema de climatização da estufa.
# Pense nela como o "manual de instruções" do climatizador:
# ela define o que o climatizador pode fazer e que informações ele mantém.
# =============================================================================

class Climatizador:
    # -------------------------------------------------------------------------
    # MÉTODO __init__ (Construtor/Inicializador)
    # -------------------------------------------------------------------------
    # Este método é chamado automaticamente quando criamos um Climatizador novo.
    # "self" é como o climatizador se referindo a si mesmo ("eu, o climatizador...")
    # Aqui definimos todos os valores iniciais do equipamento ao ser "ligado".
    # -------------------------------------------------------------------------
    def __init__(self):
        # self.temperatura_atual → temperatura real medida no ambiente (em graus Celsius)
        # Começa em 22°C, uma temperatura típica de estufa
        self.temperatura_atual = 22.0

        # self.temperatura_alvo → temperatura que desejamos atingir
        # Começa igual à atual (nenhum ajuste necessário)
        self.temperatura_alvo = 22.0

        # self.exaustores_abertos → indica se as janelas/exaustores de ventilação estão abertos
        # False = fechados, True = abertos
        self.exaustores_abertos = False

        # self.modo_operacao → modo atual do climatizador
        # Opções: "resfriamento", "aquecimento", "manutencao" (manutenção)
        self.modo_operacao = "manutencao"

        # self.umidade_relativa → porcentagem de umidade do ar no ambiente
        # 65% é um valor ideal para a maioria das culturas em estufa
        self.umidade_relativa = 65.0

        # self.consumo_energia → consumo elétrico simulado em Watts
        self.consumo_energia = 1200.0

        # self.log_acoes → lista com o histórico de todas as ações realizadas
        # Começa como uma lista vazia []
        self.log_acoes = []

        # Exibe mensagem de inicialização no terminal deste servidor
        print("[CLIMATIZADOR] Sistema de climatização inicializado e pronto para receber comandos.")

    # -------------------------------------------------------------------------
    # MÉTODO definir_temperatura
    # -------------------------------------------------------------------------
    # Define a temperatura alvo que o climatizador deve atingir.
    # O sistema então decide automaticamente se precisa aquecer ou resfriar.
    # Parâmetros:
    #   - self   → referência ao próprio objeto (climatizador)
    #   - graus  → temperatura desejada em graus Celsius (enviada pelo cliente)
    # -------------------------------------------------------------------------
    def definir_temperatura(self, graus):
        # Obtém a data e hora atual do computador
        agora = datetime.datetime.now()

        # Converte data/hora para um texto legível
        # strftime() → method que formata a data como string de texto
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Guarda a temperatura anterior para comparar depois
        temperatura_anterior = self.temperatura_alvo

        # Garante que a temperatura pedida está num intervalo seguro para plantas (10°C a 40°C)
        # max(10, graus) → se pedir abaixo de 10°C, usa 10°C
        # min(40, ...) → se pedir acima de 40°C, usa 40°C
        graus_seguros = max(10, min(40, graus))

        # Atualiza a temperatura alvo com o novo valor seguro
        self.temperatura_alvo = graus_seguros

        # Simula a temperatura atual se aproximando da temperatura alvo
        # random.uniform(-0.5, 0.5) → gera um número decimal entre -0.5 e +0.5
        # Isso simula a imprecisão e variação natural do sistema de climatização
        variacao_sensor = random.uniform(-0.5, 0.5)
        self.temperatura_atual = graus_seguros + variacao_sensor

        # Determina o modo de operação comparando temperatura atual com a anterior
        if graus_seguros > temperatura_anterior:
            # Se a nova temperatura é maior, o sistema vai aquecer
            self.modo_operacao = "aquecimento"
            self.consumo_energia = 2000.0  # Aquecimento consome mais energia
            icone = "🔴"
            descricao_modo = "AQUECENDO"
        elif graus_seguros < temperatura_anterior:
            # Se a nova temperatura é menor, o sistema vai resfriar
            self.modo_operacao = "resfriamento"
            self.consumo_energia = 1800.0  # Resfriamento também consome bastante
            icone = "🔵"
            descricao_modo = "RESFRIANDO"
        else:
            # Mesma temperatura → apenas manutenção
            self.modo_operacao = "manutencao"
            self.consumo_energia = 800.0  # Manutenção consome menos
            icone = "🟢"
            descricao_modo = "MANUTENÇÃO"

        # Cria a mensagem de log registrando a ação
        mensagem = (f"[{hora_formatada}] Temperatura alvo definida para {graus_seguros}°C. "
                    f"Modo: {descricao_modo}. Temperatura medida: {self.temperatura_atual:.1f}°C")

        # Adiciona a mensagem ao final da lista de log
        # append() → método que insere um item no final de uma lista
        self.log_acoes.append(mensagem)

        # Exibe a mensagem no terminal do servidor
        print(f"[CLIMATIZADOR] {mensagem}")

        # Retorna a confirmação para o cliente
        return (f"{icone} Temperatura definida: {graus_seguros}°C | "
                f"Modo: {descricao_modo} | "
                f"Medição atual: {self.temperatura_atual:.1f}°C | "
                f"Consumo: {self.consumo_energia:.0f}W")

    # -------------------------------------------------------------------------
    # MÉTODO abrir_exaustores
    # -------------------------------------------------------------------------
    # Abre (ou fecha, se já estiverem abertos) os exaustores de ventilação.
    # Exaustores abertos permitem troca de ar, controlando CO₂ e umidade.
    # Este método funciona como um "interruptor" — alterna entre aberto e fechado.
    # -------------------------------------------------------------------------
    def abrir_exaustores(self):
        # Obtém data e hora atual
        agora = datetime.datetime.now()

        # Formata a data/hora como texto
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Alterna o estado dos exaustores (True vira False, False vira True)
        # "not" → operador de negação lógica. "not True" = False, "not False" = True
        self.exaustores_abertos = not self.exaustores_abertos

        # Prepara a mensagem baseada no novo estado dos exaustores
        if self.exaustores_abertos:
            # Exaustores abertos: maior circulação de ar, umidade diminui um pouco
            estado = "ABERTOS"
            icone = "🌬️"
            efeito = "Ventilação ativa — troca de ar em andamento"

            # Simula redução de umidade quando os exaustores estão abertos
            # (o ar externo, geralmente mais seco, entra na estufa)
            # random.uniform(1, 5) → redução aleatória entre 1% e 5%
            self.umidade_relativa = max(20, self.umidade_relativa - random.uniform(1, 5))
        else:
            # Exaustores fechados: ambiente mais estável, umidade aumenta um pouco
            estado = "FECHADOS"
            icone = "🔒"
            efeito = "Ventilação desativada — ambiente selado"

            # Simula aumento de umidade quando os exaustores estão fechados
            self.umidade_relativa = min(95, self.umidade_relativa + random.uniform(1, 3))

        # Cria a mensagem de log
        mensagem = (f"[{hora_formatada}] Exaustores {estado}. {efeito}. "
                    f"Umidade atual: {self.umidade_relativa:.1f}%")

        # Adiciona ao histórico de ações
        self.log_acoes.append(mensagem)

        # Exibe no terminal do servidor
        print(f"[CLIMATIZADOR] {mensagem}")

        # Retorna confirmação para o cliente
        return (f"{icone} Exaustores {estado}! {efeito} | "
                f"Umidade relativa: {self.umidade_relativa:.1f}%")

    # -------------------------------------------------------------------------
    # MÉTODO ping
    # -------------------------------------------------------------------------
    # Método simples para o cliente verificar se este servidor está online.
    # O cliente chama ping() e, se receber "pong" de volta, a conexão está funcionando.
    # -------------------------------------------------------------------------
    def ping(self):
        # Retorna a string "pong" como sinal de que o servidor está ativo e respondendo
        return "pong"

    # -------------------------------------------------------------------------
    # MÉTODO obter_relatorio
    # -------------------------------------------------------------------------
    # Retorna um dicionário com todas as informações atuais do climatizador.
    # Chamado pelo cliente quando ele solicita o relatório geral da estufa.
    # Um dicionário é uma estrutura de dados do tipo "chave: valor",
    # similar a uma tabela com duas colunas: nome do dado e valor do dado.
    # -------------------------------------------------------------------------
    def obter_relatorio(self):
        # Obtém data e hora atual
        agora = datetime.datetime.now()

        # Formata a data/hora como texto
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Simula uma pequena variação na temperatura atual (comportamento de sensor real)
        # random.uniform(-0.3, 0.3) → variação de -0.3°C a +0.3°C
        variacao = random.uniform(-0.3, 0.3)
        self.temperatura_atual = round(self.temperatura_atual + variacao, 1)

        # Garante que a temperatura atual não saia de limites razoáveis
        # Aplica os limites de 10°C a 40°C
        self.temperatura_atual = max(10, min(40, self.temperatura_atual))

        # Cria e retorna o dicionário com os dados do climatizador
        return {
            # Nome do setor
            "setor": "Climatizador",

            # Quando o relatório foi gerado
            "hora_relatorio": hora_formatada,

            # Temperatura que o sistema está tentando atingir
            "temperatura_alvo": self.temperatura_alvo,

            # Temperatura medida atualmente pelo sensor
            "temperatura_atual": self.temperatura_atual,

            # Se os exaustores estão abertos (True) ou fechados (False)
            "exaustores_abertos": self.exaustores_abertos,

            # Modo atual: "aquecimento", "resfriamento" ou "manutencao"
            "modo_operacao": self.modo_operacao,

            # Umidade relativa do ar (em %)
            "umidade_relativa": round(self.umidade_relativa, 1),

            # Consumo de energia em Watts
            "consumo_energia_w": round(self.consumo_energia, 1),

            # Número total de ações realizadas
            # len() → função que conta itens em uma lista
            "total_acoes": len(self.log_acoes),

            # Última ação registrada no log
            # self.log_acoes[-1] → acessa o último item da lista (índice -1)
            # "if self.log_acoes else ..." → se a lista estiver vazia, retorna mensagem padrão
            "ultimo_log": self.log_acoes[-1] if self.log_acoes else "Nenhuma ação registrada ainda."
        }


# =============================================================================
# BLOCO PRINCIPAL - PONTO DE ENTRADA DO PROGRAMA
# =============================================================================
# Este bloco só é executado quando rodamos ESTE arquivo diretamente.
# A condição "if __name__ == '__main__'" garante isso:
#   - Quando você roda: python servidor_climatizador.py → __name__ é '__main__' → EXECUTA
#   - Quando outro arquivo importa este → __name__ é o nome do arquivo → NÃO EXECUTA
# =============================================================================

if __name__ == '__main__':
    # Define o endereço IP onde o servidor vai "ouvir"
    # "0.0.0.0" = aceita conexões de qualquer endereço na rede
    # Substitua pelo IP real da máquina se necessário, ex: "192.168.1.103"
    HOST = "0.0.0.0"

    # Define a porta de comunicação deste servidor
    # Cada servidor tem uma porta diferente:
    #   Hidropônico → 8001
    #   Iluminação  → 8002
    #   Climatizador → 8003  ← esta
    PORTA = 8003

    # Exibe cabeçalho no terminal
    print("=" * 60)
    print("   SERVIDOR - CLIMATIZADOR")
    print("=" * 60)
    print(f"   Endereço: {HOST}:{PORTA}")
    print("   Aguardando conexões do terminal controlador...")
    print("=" * 60)

    # Cria o servidor XML-RPC
    # SimpleXMLRPCServer → classe que cria o servidor
    # (HOST, PORTA) → endereço e porta onde o servidor vai ouvir
    # allow_none=True → permite que métodos retornem None sem gerar erro
    # logRequests=False → não exibe log de cada requisição (terminal mais limpo)
    servidor = SimpleXMLRPCServer((HOST, PORTA), allow_none=True, logRequests=False)

    # Cria um objeto (instância) da classe Climatizador
    # É como "ligar" o climatizador — cria o equipamento virtual
    climatizador = Climatizador()

    # Registra o objeto climatizador no servidor
    # Isso torna todos os métodos públicos do climatizador acessíveis remotamente
    # O cliente poderá chamar: definir_temperatura() e abrir_exaustores()
    servidor.register_instance(climatizador)

    # Inicia o servidor — ele fica rodando infinitamente esperando comandos
    # Para parar: pressione Ctrl+C no terminal
    servidor.serve_forever()
