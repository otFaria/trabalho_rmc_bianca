
# =============================================================================
# COMO RODAR O SISTEMA — ESTUFA INTELIGENTE
# =============================================================================
#
# PASSO 1 — Descobrir o IP de cada máquina
# -----------------------------------------
# Em cada computador, abra o CMD (Prompt de Comando) e digite:
#
#     ipconfig
#
# Procure a linha "Endereço IPv4". Anote o IP de cada máquina.
# Exemplo:
#   Máquina 1 (Hidropônico):  192.168.1.101
#   Máquina 2 (Iluminação):   192.168.1.102
#   Máquina 3 (Climatizador): 192.168.1.103
#   Máquina 4 (Cliente):      192.168.1.104
#
#
# PASSO 2 — Editar os IPs no arquivo do cliente
# -----------------------------------------------
# Abra o arquivo "cliente_controlador.py" e altere as linhas:
#
#   IP_HIDROPONICO  = "192.168.1.101"   ← IP da máquina 1
#   IP_ILUMINACAO   = "192.168.1.102"   ← IP da máquina 2
#   IP_CLIMATIZADOR = "192.168.1.103"   ← IP da máquina 3
#
#
# PASSO 3 — Iniciar os servidores (cada um em sua máquina)
# ----------------------------------------------------------
# Na MÁQUINA 1 (Hidropônico), abra o terminal e execute:
#     python servidor_hidroponico.py
#
# Na MÁQUINA 2 (Iluminação), abra o terminal e execute:
#     python servidor_iluminacao.py
#
# Na MÁQUINA 3 (Climatizador), abra o terminal e execute:
#     python servidor_climatizador.py
#
# IMPORTANTE: Os servidores devem ser iniciados ANTES do cliente!
#
#
# PASSO 4 — Iniciar o cliente (na máquina do agrônomo)
# -----------------------------------------------------
# Na MÁQUINA 4 (Cliente), abra o terminal e execute:
#     python cliente_controlador.py
#
#
# PASSO 5 — Usar o sistema
# -------------------------
# O menu interativo irá aparecer. Use os números para navegar:
#
#   [1] → Controla o setor hidropônico
#          - Ativar irrigação (você digita o tempo em minutos)
#          - Checar nível de água
#
#   [2] → Controla o painel de iluminação UV
#          - Ajustar intensidade (0 a 100%)
#          - Mudar espectro: azul, vermelho, branco, uv, infravermelho
#
#   [3] → Controla o climatizador
#          - Definir temperatura (10°C a 40°C)
#          - Abrir/fechar exaustores
#
#   [4] → Gera o RELATÓRIO GERAL de todos os setores de uma vez
#
#   [0] → Sair do sistema
#
#
# SOLUÇÃO DE PROBLEMAS
# ---------------------
# ❌ "Erro de conexão": Verifique se o servidor da máquina correspondente está rodando.
# ❌ "Porta em uso": Outro programa está usando a porta. Reinicie o servidor.
# ❌ "IP não encontrado": Verifique se todas as máquinas estão na mesma rede Wi-Fi/cabo.
# ❌ Firewall bloqueando: Pode ser necessário liberar as portas 8001, 8002 e 8003
#    no Firewall do Windows (Painel de Controle → Firewall → Regras de entrada).
#
# =============================================================================
# RESUMO DOS ARQUIVOS
# =============================================================================
#
#  servidor_hidroponico.py  → Roda na MÁQUINA 1 | Porta 8001
#  servidor_iluminacao.py   → Roda na MÁQUINA 2 | Porta 8002
#  servidor_climatizador.py → Roda na MÁQUINA 3 | Porta 8003
#  cliente_controlador.py   → Roda na MÁQUINA 4 (terminal do agrônomo)
#
# Tecnologia usada: XML-RPC (embutido no Python, sem instalar nada extra!)
# Versão Python recomendada: 3.8 ou superior
# =============================================================================
