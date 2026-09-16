"""
===============================================================================
THE IRON VANGUARD UGV - MEDIDAS DERIVADAS E PINAGEM DO SISTEMA
===============================================================================
Módulo para cálculos geométricos, offsets de montagem e mapeamento elétrico.
===============================================================================
"""

import config as cfg

# ==========================================
# 1. DIMENSÕES CALCULADAS E DERIVADAS
# ==========================================

# Largura total das polias (pista do pneu + 2 abas de guia)
LARGURA_TOTAL_POLIA = cfg.CONFIG["LARGURA_ESTEIRA"] + 2 * cfg.CONFIG["ESPESSURA_ABA"]

# Raios das polias
RAIO_PRIMITIVO_MOTRIZ = cfg.CONFIG["DIAM_PRIMITIVO_MOTRIZ"] / 2.0
RAIO_ABA_MOTRIZ = RAIO_PRIMITIVO_MOTRIZ + cfg.CONFIG["ALTURA_ABA_GUIA"]

RAIO_CORPO_LIVRE = cfg.CONFIG["DIAM_POLIA_LIVRE"] / 2.0
RAIO_ABA_LIVRE = RAIO_CORPO_LIVRE + cfg.CONFIG["ALTURA_ABA_GUIA"]

# Dimensões internas da banheira
COMP_INTERNO_CHASSI = cfg.CONFIG["COMPRIMENTO_CHASSI"] - 2 * cfg.CONFIG["ESPESSURA_PAREDE"]
LARG_INTERNA_CHASSI = cfg.CONFIG["LARGURA_CHASSI"] - 2 * cfg.CONFIG["ESPESSURA_PAREDE"]
ALT_INTERNA_CHASSI = cfg.CONFIG["ALTURA_CHASSI"] - cfg.CONFIG["ESPESSURA_PAREDE"]

# Dimensões da bandeja eletrônica (Tray)
COMP_TRAY = COMP_INTERNO_CHASSI - (2 * cfg.CONFIG["FOLGA_TRAY_CHASSI"])
LARG_TRAY = LARG_INTERNA_CHASSI - (2 * cfg.CONFIG["FOLGA_TRAY_CHASSI"])
Z_FUNDO_INTERNO = -cfg.CONFIG["ALTURA_CHASSI"] / 2.0 + cfg.CONFIG["ESPESSURA_PAREDE"]

# Posições Y das paredes laterais (onde as polias são montadas)
Y_PAREDE_ESQ = cfg.CONFIG["LARGURA_CHASSI"] / 2.0
Y_PAREDE_DIR = -cfg.CONFIG["LARGURA_CHASSI"] / 2.0

# Posição Y do centro das polias no exterior do chassi (com 3.0mm de folga da parede)
FOLGA_POLIA_PAREDE = 3.0
Y_CENTRO_POLIA_ESQ = Y_PAREDE_ESQ + FOLGA_POLIA_PAREDE + (LARGURA_TOTAL_POLIA / 2.0)
Y_CENTRO_POLIA_DIR = Y_PAREDE_DIR - FOLGA_POLIA_PAREDE - (LARGURA_TOTAL_POLIA / 2.0)

# Eixos e rodas: lista com tuplas (nome, x, z)
EIXOS_RODAS = [
    ("traseira_motriz", cfg.CONFIG["POS_X_MOTOR"], cfg.CONFIG["POS_Z_EIXOS"]),
    ("central_apoio", cfg.CONFIG["POS_X_CENTRAL"], cfg.CONFIG["POS_Z_EIXOS"]),
    ("dianteira_tensora", cfg.CONFIG["POS_X_TENSORA"], cfg.CONFIG["POS_Z_EIXOS"]),
]


# ==========================================
# 2. ESPECIFICAÇÃO ELÉTRICA E PINAGEM OFICIAL
# ==========================================
"""
Topologia de Alimentação:
- Bateria Pack 3S Li-Ion 18650 (Nominal: 11.1V, Carga Total: 12.6V, Corte: 9.0V)
- A bateria alimenta diretamente o barramento de alta potência do Driver L298N (VMS / 12V).
- O Step-Down LM2596 recebe os 11.1V~12.6V e regula uma saída de precisão em 5.0V estáveis.
- Os 5.0V do LM2596 alimentam o pino 5V do ESP32-CAM.
- GND de todos os módulos (Bateria, LM2596, ESP32-CAM e L298N) são interligados em ponto estrela comum.
"""

PINAGEM_SISTEMA = {
    "ALIMENTACAO": {
        "BATERIA": "Pack 3S 18650 (11.1V ~ 12.6V)",
        "L298N_VMS": "Conectado diretamente ao VCC da bateria 3S (12V)",
        "LM2596_IN": "Conectado ao VCC da bateria 3S (12V)",
        "LM2596_OUT": "5.0V regulados para o pino 5V do ESP32-CAM",
        "GND_COMUM": "GND 3S + GND LM2596 + GND ESP32-CAM + GND L298N",
    },
    "MOTOR_ESQUERDO": {
        "ENA": {"gpio": 14, "funcao": "PWM Controle de Velocidade", "timer": "LEDC_CH0"},
        "IN1": {"gpio": 12, "funcao": "Sentido de Giro Frente"},
        "IN2": {"gpio": 13, "funcao": "Sentido de Giro Ré"},
    },
    "MOTOR_DIREITO": {
        "ENB": {"gpio": 15, "funcao": "PWM Controle de Velocidade", "timer": "LEDC_CH1"},
        "IN3": {"gpio": 2,  "funcao": "Sentido de Giro Frente"},
        "IN4": {"gpio": 4,  "funcao": "Sentido de Giro Ré (Atenção: GPIO 4 controla o Flash LED do ESP32-CAM)"},
    }
}
