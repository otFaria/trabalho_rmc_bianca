
# =============================================================================
# SERVIDOR DO PAINEL DE ILUMINAÇÃO UV
# =============================================================================
# Este arquivo representa o computador do painel de iluminação UV da estufa.
# Ele controla as lâmpadas ultravioleta que simulam a luz solar para as plantas.
# Fica "ouvindo" na rede esperando comandos do cliente (terminal controlador).
# =============================================================================

# --- IMPORTAÇÕES DE BIBLIOTECAS ---

# Importa a classe SimpleXMLRPCServer do módulo xmlrpc.server
# Essa classe permite que este computador receba chamadas de função remotas
# (ou seja, outro computador pode chamar funções neste computador pela rede)
from xmlrpc.server import SimpleXMLRPCServer

# Importa o módulo datetime para trabalhar com datas e horas
# Usaremos para registrar quando cada ação foi executada
import datetime

# Importa o módulo random para gerar números aleatórios
# Usaremos para simular leituras de sensores de luminosidade
import random


# =============================================================================
# DEFINIÇÃO DA CLASSE PainelIluminacao
# =============================================================================
# Uma "classe" funciona como um molde. Assim como um molde de bolo define
# a forma do bolo, a classe PainelIluminacao define o que um painel de
# iluminação pode fazer e quais informações ele guarda.
# =============================================================================

class PainelIluminacao:
    # -------------------------------------------------------------------------
    # MÉTODO __init__ (Inicializador / Construtor)
    # -------------------------------------------------------------------------
    # Este método é executado automaticamente quando criamos um painel novo.
    # Aqui definimos o "estado inicial" do painel — como ele começa.
    # "self" é uma referência ao próprio objeto (o painel em si)
    # -------------------------------------------------------------------------
    def __init__(self):
        # self.intensidade → guarda o nível de brilho das lâmpadas (0 a 100%)
        # Começa em 75% de intensidade
        self.intensidade = 75

        # self.espectro_atual → guarda qual cor/espectro está sendo usado
        # Espectros comuns: "azul" (crescimento), "vermelho" (floração), "branco" (geral)
        self.espectro_atual = "branco"

        # self.lâmpadas_ativas → indica se as lâmpadas estão ligadas (True) ou desligadas (False)
        self.lampadas_ativas = True

        # self.consumo_energia → consumo simulado de energia em Watts
        # Começa em 450W (valor simulado para lâmpadas UV de estufa)
        self.consumo_energia = 450.0

        # self.log_acoes → lista que guarda o histórico de todas as ações realizadas
        # Começa como uma lista vazia
        self.log_acoes = []

        # Exibe mensagem de confirmação no terminal deste servidor
        print("[ILUMINAÇÃO] Painel UV inicializado e pronto para receber comandos.")

    # -------------------------------------------------------------------------
    # MÉTODO ajustar_intensidade
    # -------------------------------------------------------------------------
    # Ajusta o brilho das lâmpadas UV para o valor especificado.
    # Parâmetros:
    #   - self  → referência ao próprio objeto (painel)
    #   - valor → número de 0 a 100 representando a porcentagem de brilho
    #             enviado pelo cliente via rede
    # -------------------------------------------------------------------------
    def ajustar_intensidade(self, valor):
        # Obtém a data e hora atual do sistema
        agora = datetime.datetime.now()

        # Converte data e hora para texto formatado
        # strftime() → método que formata data/hora como string (texto)
        # "%d/%m/%Y %H:%M:%S" → formato: dia/mês/ano hora:minuto:segundo
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Garante que o valor está dentro do intervalo válido (0 a 100)
        # max(0, valor) → se o valor for negativo, usa 0
        # min(100, ...) → se o valor for maior que 100, usa 100
        valor_seguro = max(0, min(100, valor))

        # Atualiza a intensidade do painel com o novo valor
        self.intensidade = valor_seguro

        # Atualiza o consumo de energia baseado na intensidade
        # Quanto maior a intensidade, maior o consumo
        # Na intensidade máxima (100%), consome 800W
        # A fórmula faz uma proporção: (valor / 100) * 800
        self.consumo_energia = (valor_seguro / 100) * 800

        # Determina um rótulo descritivo baseado no nível de intensidade
        if valor_seguro == 0:
            descricao = "DESLIGADO"
            self.lampadas_ativas = False  # Marca as lâmpadas como desligadas
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

        # Cria a mensagem de log
        mensagem = f"[{hora_formatada}] Intensidade ajustada para {valor_seguro}% ({descricao}). Consumo: {self.consumo_energia:.0f}W"

        # Adiciona a mensagem ao final da lista de log
        # append() → método que insere um elemento no fim de uma lista
        self.log_acoes.append(mensagem)

        # Exibe a mensagem no terminal deste servidor
        print(f"[ILUMINAÇÃO] {mensagem}")

        # Retorna uma mensagem de confirmação para o cliente
        return f"💡 Intensidade ajustada para {valor_seguro}% ({descricao}). Consumo estimado: {self.consumo_energia:.0f}W"

    # -------------------------------------------------------------------------
    # MÉTODO mudar_espectro
    # -------------------------------------------------------------------------
    # Muda a cor (espectro) das lâmpadas UV.
    # Cada cor tem um efeito diferente nas plantas:
    #   - Azul  → estimula o crescimento vegetativo (folhas)
    #   - Vermelho → estimula floração e frutificação
    #   - Branco → uso geral, equilibrado
    #   - UV    → controle de pragas e fungos
    # Parâmetros:
    #   - self → referência ao próprio objeto
    #   - cor  → texto indicando a cor desejada (enviado pelo cliente)
    # -------------------------------------------------------------------------
    def mudar_espectro(self, cor):
        # Obtém a data e hora atual
        agora = datetime.datetime.now()

        # Formata a data/hora como texto
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Define os espectros disponíveis e seus efeitos nas plantas
        # Este é um dicionário: estrutura com pares "chave": "valor"
        # Aqui: "nome_da_cor": "descrição do efeito"
        espectros_validos = {
            "azul": "Estimula crescimento vegetativo (folhas e caule)",
            "vermelho": "Estimula floração e frutificação",
            "branco": "Iluminação geral balanceada",
            "uv": "Controle de patógenos e fungos",
            "infravermelho": "Estimula crescimento noturno"
        }

        # Converte a cor para minúsculas para aceitar variações como "Azul", "AZUL", "azul"
        # .lower() → método que transforma todo texto em letras minúsculas
        cor_normalizada = cor.lower()

        # Verifica se a cor enviada pelo cliente é uma cor válida
        # "in espectros_validos" → verifica se a chave existe no dicionário
        if cor_normalizada in espectros_validos:
            # Guarda a cor anterior para exibir na mensagem
            cor_anterior = self.espectro_atual

            # Atualiza o espectro atual com a nova cor
            self.espectro_atual = cor_normalizada

            # Pega a descrição do efeito da nova cor
            # espectros_validos[cor_normalizada] → acessa o valor pela chave no dicionário
            efeito = espectros_validos[cor_normalizada]

            # Cria a mensagem de log
            mensagem = f"[{hora_formatada}] Espectro mudado de '{cor_anterior}' para '{cor_normalizada}'. Efeito: {efeito}"

            # Adiciona ao histórico
            self.log_acoes.append(mensagem)

            # Exibe no terminal do servidor
            print(f"[ILUMINAÇÃO] {mensagem}")

            # Retorna confirmação de sucesso para o cliente
            return f"🌈 Espectro alterado para '{cor_normalizada}'! Efeito: {efeito}"

        else:
            # Se a cor não for válida, cria uma mensagem de erro
            cores_disponiveis = ", ".join(espectros_validos.keys())
            # join() → método que une os itens de uma lista em um texto, separados por ", "

            mensagem_erro = f"[{hora_formatada}] ERRO: Espectro '{cor}' não reconhecido."

            # Registra o erro no log também
            self.log_acoes.append(mensagem_erro)

            print(f"[ILUMINAÇÃO] {mensagem_erro}")

            # Retorna mensagem de erro para o cliente
            return f"❌ Espectro '{cor}' inválido! Opções disponíveis: {cores_disponiveis}"

    # -------------------------------------------------------------------------
    # MÉTODO obter_relatorio
    # -------------------------------------------------------------------------
    # Gera e retorna um dicionário com todas as informações atuais do painel.
    # Este método é chamado pelo cliente para montar o relatório geral da estufa.
    # -------------------------------------------------------------------------
    def obter_relatorio(self):
        # Obtém data e hora atual para o relatório
        agora = datetime.datetime.now()

        # Formata a data/hora
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Retorna um dicionário (mapa de dados) com as informações do painel
        return {
            # Nome do setor
            "setor": "Iluminação UV",

            # Quando o relatório foi gerado
            "hora_relatorio": hora_formatada,

            # Nível de intensidade atual (0 a 100%)
            "intensidade": self.intensidade,

            # Espectro (cor) atual das lâmpadas
            "espectro_atual": self.espectro_atual,

            # Se as lâmpadas estão ativas ou não
            "lampadas_ativas": self.lampadas_ativas,

            # Consumo de energia atual em Watts
            "consumo_energia_w": round(self.consumo_energia, 1),

            # Quantidade de ações realizadas
            # len() → função que retorna o número de itens em uma lista
            "total_acoes": len(self.log_acoes),

            # Última ação registrada no log
            # self.log_acoes[-1] → último elemento da lista (índice -1 = último)
            # Se a lista estiver vazia, retorna a mensagem padrão
            "ultimo_log": self.log_acoes[-1] if self.log_acoes else "Nenhuma ação registrada ainda."
        }


# =============================================================================
# BLOCO PRINCIPAL - INICIA O SERVIDOR
# =============================================================================
# Este bloco só executa quando rodamos ESTE arquivo diretamente com Python.
# "if __name__ == '__main__'" → condição que verifica se este é o arquivo principal
# =============================================================================

if __name__ == '__main__':
    # Define o endereço IP do servidor
    # "0.0.0.0" → aceita conexões de qualquer IP na rede local
    # Em produção, substitua pelo IP real desta máquina, ex: "192.168.1.102"
    HOST = "0.0.0.0"

    # Define a porta de comunicação do servidor de iluminação
    # Cada servidor usa uma porta diferente para não conflitar
    # Hidropônico: 8001 | Iluminação: 8002 | Climatizador: 8003
    PORTA = 8002

    # Exibe cabeçalho informativo no terminal
    print("=" * 60)
    print("   SERVIDOR - PAINEL DE ILUMINAÇÃO UV")
    print("=" * 60)
    print(f"   Endereço: {HOST}:{PORTA}")
    print("   Aguardando conexões do terminal controlador...")
    print("=" * 60)

    # Cria o servidor XML-RPC
    # SimpleXMLRPCServer → classe que cria o servidor de chamadas remotas
    # (HOST, PORTA) → onde o servidor vai "ouvir" por conexões
    # allow_none=True → permite retornar valores nulos sem erros
    # logRequests=False → não registra cada requisição (terminal mais limpo)
    servidor = SimpleXMLRPCServer((HOST, PORTA), allow_none=True, logRequests=False)

    # Cria um objeto (instância) da classe PainelIluminacao
    # É como "ligar" o painel — cria o objeto real a partir do molde (classe)
    painel = PainelIluminacao()

    # Registra o objeto no servidor para que seus métodos fiquem acessíveis remotamente
    # Agora o cliente pode chamar painel.ajustar_intensidade() e painel.mudar_espectro()
    servidor.register_instance(painel)

    # Inicia o servidor em loop infinito — ele fica esperando comandos sem parar
    # Para encerrar: pressione Ctrl+C no terminal
    servidor.serve_forever()
