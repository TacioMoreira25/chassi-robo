"""
===============================================================================
ROBÔ DE INSPEÇÃO - MAPA DE CONEXÕES ELÉTRICAS E PINAGEM
===============================================================================
Engenharia Mecatrônica - Sistema de Potência, Controle e Acionamento
===============================================================================

ESPECIFICAÇÕES DO SISTEMA:
1. ALIMENTAÇÃO:
   - Fonte Primária: Pack 3S Li-Ion 18650 (11.1V nominal ~ 12.6V carga plena).
   - Barramento de Potência (Motores): Ligado diretamente ao borne VMS (+12V) do L298N.
   - Barramento de Lógica (ESP32-CAM): Bateria 3S -> Conversor Step-Down LM2596 -> 5.0V regulados -> Pino 5V do ESP32-CAM.
   - Referência Elétrica: GND Comum unificado (Bateria 3S, L298N, LM2596 e ESP32-CAM).

2. PINAGEM OFICIAL ESP32-CAM -> DRIVER L298N:
   -----------------------------------------------------------------------------
   Sinal      | ESP32-CAM | L298N Pin | Função Técnica / Notas Mecatrônicas
   -----------------------------------------------------------------------------
   Motor Esq  |           |           |
     ENA      | GPIO 14   | ENA       | Sinal PWM de velocidade do motor esquerdo
     IN1      | GPIO 12   | IN1       | Direção lógica frente / Horário
     IN2      | GPIO 13   | IN2       | Direção lógica ré / Anti-horário
   -----------------------------------------------------------------------------
   Motor Dir  |           |           |
     ENB      | GPIO 15   | ENB       | Sinal PWM de velocidade do motor direito
     IN3      | GPIO 2    | IN3       | Direção lógica frente / Horário
     IN4      | GPIO 4    | IN4       | Direção lógica ré / Anti-horário (Flash LED)
   -----------------------------------------------------------------------------

NOTAS TÉCNICAS DO ENGENHEIRO MECATRÔNICO:
* Jumper 5V do L298N: DEVE SER REMOVIDO se a tensão da bateria exceder 12V para
  proteger o regulador 78M05 interno da ponte H, ou mantido como fonte secundária
  isolada. O ESP32-CAM NUNCA deve ser alimentado pelo 5V do L298N, pois o ESP32-CAM
  apresenta picos de corrente de até 500mA no acionamento do Wi-Fi, o que sobreaquece
  e derruba o 78M05 do L298N, provocando brownout reset no microcontrolador.
* GPIO 4 (IN4): Está conectado internamente ao Flash LED de alta intensidade da
  placa ESP32-CAM. Quando o motor direito for acionado em ré, o flash acenderá levemente
  ou pode ser aproveitado como iluminação de ré em inspeção confinada.
* Strapping Pins: GPIO 12 e GPIO 2 são strapping pins durante o boot. O L298N possui
  resistores pull-down internos que garantem nível baixo no boot, prevenindo falha de inicialização.
===============================================================================
"""

PINOS_MOTORES = {
    "ESQUERDO": {
        "ENA": 14, # PWM Velocidade
        "IN1": 12, # Direção A
        "IN2": 13, # Direção B
    },
    "DIREITO": {
        "ENB": 15, # PWM Velocidade
        "IN3": 2,  # Direção A
        "IN4": 4,  # Direção B (Flash LED)
    }
}

TENSOES_SISTEMA = {
    "BATERIA_NOMINAL": 11.1,
    "BATERIA_MAXIMA": 12.6,
    "BATERIA_MINIMA_CORTE": 9.6,
    "LOGICA_ESP32_VCC": 5.0,
    "LOGICA_ESP32_IO": 3.3,
    "POTENCIA_MOTORES_VMS": 12.0
}

def imprimir_relatorio_eletrico():
    print("=" * 70)
    print("ROBÔ DE INSPEÇÃO - ARQUITETURA ELÉTRICA E DE CONTROLE")
    print("=" * 70)
    print(f"Alimentação Primária: Pack 3S 18650 ({TENSOES_SISTEMA['BATERIA_NOMINAL']}V ~ {TENSOES_SISTEMA['BATERIA_MAXIMA']}V)")
    print(f"Regulador Lógico: LM2596 Step-Down -> {TENSOES_SISTEMA['LOGICA_ESP32_VCC']}V estáveis para ESP32-CAM")
    print("\n--- MAPEAMENTO DE PINAGEM ESP32-CAM -> PONTE H L298N ---")
    print(f"Motor Esquerdo: ENA (PWM) -> GPIO {PINOS_MOTORES['ESQUERDO']['ENA']}")
    print(f"                IN1 (DIR) -> GPIO {PINOS_MOTORES['ESQUERDO']['IN1']}")
    print(f"                IN2 (DIR) -> GPIO {PINOS_MOTORES['ESQUERDO']['IN2']}")
    print(f"Motor Direito:  ENB (PWM) -> GPIO {PINOS_MOTORES['DIREITO']['ENB']}")
    print(f"                IN3 (DIR) -> GPIO {PINOS_MOTORES['DIREITO']['IN3']}")
    print(f"                IN4 (DIR) -> GPIO {PINOS_MOTORES['DIREITO']['IN4']}")
    print("=" * 70)

if __name__ == "__main__":
    imprimir_relatorio_eletrico()
