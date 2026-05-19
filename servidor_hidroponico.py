
# =============================================================================
# SERVIDOR DO SETOR HIDROPÔNICO
# =============================================================================
# Este arquivo representa o computador do setor hidropônico da estufa.
# Ele fica "ouvindo" na rede esperando comandos do cliente (terminal controlador).
# Quando o cliente enviar um comando, este servidor executa a ação correspondente.
# =============================================================================

# --- IMPORTAÇÕES DE BIBLIOTECAS ---

# "from xmlrpc.server import SimpleXMLRPCServer" significa:
#   - xmlrpc     → é o módulo (pacote) que cuida da comunicação RPC via rede
#   - .server    → é a parte do módulo que trata do lado SERVIDOR
#   - SimpleXMLRPCServer → é a classe (molde) que cria um servidor RPC simples
# RPC = Remote Procedure Call = Chamada de Procedimento Remoto
# Ou seja: permite que outro computador (o cliente) chame funções neste computador
from xmlrpc.server import SimpleXMLRPCServer

# "import datetime" importa o módulo de data e hora do Python
# Usaremos ele para registrar quando cada ação foi realizada
import datetime

# "import random" importa o módulo que gera números aleatórios
# Usaremos para simular leituras de sensores (nível de água, etc.)
import random


# =============================================================================
# DEFINIÇÃO DA CLASSE SETORhidroponico
# =============================================================================
# Uma "classe" é como um molde ou planta de uma casa — ela define como algo
# vai se comportar. Aqui, a classe SetorHidroponico define todas as ações
# que o setor hidropônico pode realizar.
# =============================================================================

class SetorHidroponico:
    # -------------------------------------------------------------------------
    # MÉTODO __init__ (Construtor da classe)
    # -------------------------------------------------------------------------
    # O __init__ é chamado automaticamente quando criamos um objeto dessa classe.
    # É como o "nascimento" do objeto — aqui definimos os valores iniciais.
    # "self" representa o próprio objeto sendo criado (como se dissesse "eu mesmo")
    # -------------------------------------------------------------------------
    def __init__(self):
        # self.irrigacao_ativa → atributo que guarda se a irrigação está ligada ou não
        # False = desligada, True = ligada
        self.irrigacao_ativa = False

        # self.nivel_agua → atributo que guarda o nível de água no reservatório
        # Começa com 85.0 (85% cheio)
        self.nivel_agua = 85.0

        # self.tempo_irrigacao_restante → quantos minutos faltam para a irrigação terminar
        # Começa em 0 (nenhuma irrigação em andamento)
        self.tempo_irrigacao_restante = 0

        # self.log_acoes → uma lista que guarda o histórico de tudo que aconteceu
        # Começa vazia [] e vai sendo preenchida conforme as ações são realizadas
        self.log_acoes = []

        # Exibe uma mensagem no terminal informando que o setor foi inicializado
        print("[HIDROPÔNICO] Setor inicializado e pronto para receber comandos.")

    # -------------------------------------------------------------------------
    # MÉTODO ativar_irrigacao
    # -------------------------------------------------------------------------
    # Um "método" é uma função dentro de uma classe. Assim como uma função,
    # ele executa um conjunto de instruções. 
    # Este método ATIVA o sistema de irrigação por um determinado tempo.
    # Parâmetros:
    #   - self  → referência ao próprio objeto (sempre presente nos métodos)
    #   - tempo → número de minutos que a irrigação deve ficar ativa (enviado pelo cliente)
    # -------------------------------------------------------------------------
    def ativar_irrigacao(self, tempo):
        # Obtém a data e hora atual para registrar no log
        # datetime.datetime.now() → chama a função now() do módulo datetime.datetime
        # Ela retorna o momento exato agora (dia, mês, ano, hora, minuto, segundo)
        agora = datetime.datetime.now()

        # Formata a data/hora como texto legível, exemplo: "19/05/2026 10:30:00"
        # .strftime() → método que converte data/hora em texto formatado
        # "%d/%m/%Y %H:%M:%S" → máscara de formato: dia/mês/ano hora:minuto:segundo
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Marca a irrigação como ativa
        # True = ligado/ativo
        self.irrigacao_ativa = True

        # Guarda o tempo que foi solicitado
        self.tempo_irrigacao_restante = tempo

        # Simula o consumo de água durante a irrigação
        # O nível de água diminui proporcionalmente ao tempo de irrigação
        # Se o tempo for 10 minutos, consome 10 * 0.5 = 5% do reservatório
        consumo = tempo * 0.5

        # Subtrai o consumo do nível atual de água
        # max(0, ...) garante que o nível nunca fique negativo (abaixo de 0%)
        self.nivel_agua = max(0, self.nivel_agua - consumo)

        # Cria a mensagem que será guardada no histórico (log)
        mensagem = f"[{hora_formatada}] Irrigação ATIVADA por {tempo} minutos. Nível de água agora: {self.nivel_agua:.1f}%"

        # Adiciona a mensagem ao final da lista de log
        # .append() → método que adiciona um item ao final de uma lista
        self.log_acoes.append(mensagem)

        # Exibe a mensagem também no terminal do servidor
        print(f"[HIDROPÔNICO] {mensagem}")

        # Retorna uma resposta para o cliente saber que o comando foi recebido
        # Essa mensagem vai aparecer no computador do cliente
        return f"✅ Irrigação ativada com sucesso por {tempo} minutos! Nível de água: {self.nivel_agua:.1f}%"

    # -------------------------------------------------------------------------
    # MÉTODO checar_nivel_agua
    # -------------------------------------------------------------------------
    # Este método verifica e retorna o nível atual de água no reservatório.
    # Não precisa de parâmetros além do "self" porque apenas lê um valor.
    # -------------------------------------------------------------------------
    def checar_nivel_agua(self):
        # Obtém data e hora atual
        agora = datetime.datetime.now()

        # Formata a data/hora como texto
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Simula uma pequena variação no nível de água (como se fosse um sensor real)
        # random.uniform(-1, 1) → gera um número decimal aleatório entre -1.0 e +1.0
        # Isso simula a imprecisão natural de um sensor físico
        variacao = random.uniform(-1, 1)

        # Aplica a variação ao nível atual
        # max(0, ...) garante que não seja negativo
        # min(100, ...) garante que não passe de 100%
        self.nivel_agua = max(0, min(100, self.nivel_agua + variacao))

        # Cria a mensagem de status
        if self.nivel_agua > 50:
            # f-string → forma de texto com variáveis incorporadas
            # O {self.nivel_agua:.1f} coloca o valor do nível com 1 casa decimal
            status = f"NORMAL ({self.nivel_agua:.1f}%)"
        elif self.nivel_agua > 20:
            status = f"BAIXO ({self.nivel_agua:.1f}%) - Considere reabastecer"
        else:
            status = f"CRÍTICO ({self.nivel_agua:.1f}%) - REABASTECER URGENTE!"

        # Cria o log da verificação
        mensagem = f"[{hora_formatada}] Nível de água verificado: {status}"

        # Adiciona ao histórico
        self.log_acoes.append(mensagem)

        # Exibe no terminal do servidor
        print(f"[HIDROPÔNICO] {mensagem}")

        # Retorna o status para o cliente
        return f"💧 Nível de água: {status}"

    # -------------------------------------------------------------------------
    # MÉTODO obter_relatorio
    # -------------------------------------------------------------------------
    # Este método é especial: ele é chamado pelo cliente quando quer o RELATÓRIO GERAL.
    # Retorna um dicionário (estrutura de dados chave→valor) com todas as informações
    # do setor para que o cliente possa montar o relatório completo.
    # -------------------------------------------------------------------------
    def obter_relatorio(self):
        # Obtém data e hora atual para o relatório
        agora = datetime.datetime.now()

        # Formata a data/hora
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

        # Cria e retorna um dicionário com os dados do setor
        # Um dicionário em Python usa {} e tem pares de "chave": valor
        # Exemplo: {"nome": "Maria", "idade": 25}
        return {
            # "setor" → nome do setor
            "setor": "Hidropônico",

            # "hora_relatorio" → quando o relatório foi gerado
            "hora_relatorio": hora_formatada,

            # "irrigacao_ativa" → se a irrigação está ligada (True) ou desligada (False)
            "irrigacao_ativa": self.irrigacao_ativa,

            # "nivel_agua" → nível de água em porcentagem
            "nivel_agua": round(self.nivel_agua, 1),

            # "tempo_irrigacao_restante" → minutos restantes de irrigação
            "tempo_irrigacao_restante": self.tempo_irrigacao_restante,

            # "total_acoes" → quantas ações foram realizadas desde o início
            # len() → função que conta o número de itens em uma lista
            "total_acoes": len(self.log_acoes),

            # "ultimo_log" → a última ação registrada no histórico
            # Se não houver nenhuma ação ainda, retorna a mensagem padrão
            # self.log_acoes[-1] → pega o ÚLTIMO item da lista (índice -1 = último)
            "ultimo_log": self.log_acoes[-1] if self.log_acoes else "Nenhuma ação registrada ainda."
        }


# =============================================================================
# BLOCO PRINCIPAL DE EXECUÇÃO
# =============================================================================
# O trecho abaixo só é executado quando rodamos ESTE arquivo diretamente.
# "if __name__ == '__main__':" → verifica se este é o arquivo principal sendo rodado
# (não quando é importado por outro arquivo)
# =============================================================================

if __name__ == '__main__':
    # --- CONFIGURAÇÕES DO SERVIDOR ---

    # Define o IP do servidor
    # "0.0.0.0" significa "aceitar conexões de qualquer endereço IP na rede"
    # Em um cenário real, você colocaria o IP fixo desta máquina na rede local
    # Exemplo: HOST = "192.168.1.101"
    HOST = "0.0.0.0"

    # Define a porta de comunicação
    # Uma porta é como uma "porta de entrada" específica no computador
    # O cliente usará esta mesma porta para se conectar
    # Portas acima de 1024 são livres para uso; 8001 é uma escolha arbitrária
    PORTA = 8001

    # Exibe informação de início no terminal
    print("=" * 60)
    print("   SERVIDOR - SETOR HIDROPÔNICO")
    print("=" * 60)
    print(f"   Endereço: {HOST}:{PORTA}")
    print("   Aguardando conexões do terminal controlador...")
    print("=" * 60)

    # --- CRIAÇÃO DO SERVIDOR RPC ---

    # Cria o servidor RPC
    # SimpleXMLRPCServer → a classe que cria o servidor
    # (HOST, PORTA) → tupla com endereço e porta onde o servidor vai "ouvir"
    # allow_none=True → permite que funções retornem None (valor vazio) sem erro
    # logRequests=False → não exibe cada requisição no terminal (mantém limpo)
    servidor = SimpleXMLRPCServer((HOST, PORTA), allow_none=True, logRequests=False)

    # Cria um objeto da classe SetorHidroponico
    # Isso instancia a classe, ou seja, cria um "exemplar" real a partir do molde
    setor = SetorHidroponico()

    # Registra o objeto "setor" no servidor RPC
    # Isso faz com que TODOS os métodos públicos do objeto fiquem disponíveis remotamente
    # O cliente poderá chamar setor.ativar_irrigacao(), setor.checar_nivel_agua(), etc.
    servidor.register_instance(setor)

    # Inicia o servidor em loop infinito
    # serve_forever() → o servidor fica rodando e esperando comandos indefinidamente
    # Pressione Ctrl+C no terminal para encerrar o servidor
    servidor.serve_forever()
