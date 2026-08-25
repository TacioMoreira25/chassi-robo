import config

# Variáveis Derivadas
LARG_LINGUA = config.LARG_EXTERNA - (2 * config.PROF_RECORTE)
LARG_INTERNA = config.LARG_EXTERNA - (2 * config.ESPESSURA_PAREDE)
COMP_CORPO = config.COMP_TOTAL - config.COMP_BAY # Comprimento de interseção piso/paredes

# Acoplamentos e Furações Padronizadas (Radios em mm)
RAIO_FURO_BASE = 1.5           # Fixação de chapas (M3/M4)
RAIO_FURO_M4 = 2.0             # Suportes e tensionadores
RAIO_PASSAGEM_CABO = 19.05     # Furo grande para chicotes
MARGEM_FURACOES_QUINA = 7.5    # Recuo seguro (Metade da espessura)

# Parâmetros do Motor e Suporte (Bloco Plástico 3D)
RECUO_MOTOR = 50.0             # Distância do centro do motor até o centro da caixa (X)
DIAM_MOTOR = 38.0              # Diâmetro do motor RS-555 + folga
RAIO_EIXO_MOTOR = 6.0          # Furo da madeira para passagem do eixo do motor
DIST_X_FUROS_MOTOR = 22.0      # Espaçamento X dos furos de fixação
DIST_Z_FUROS_MOTOR = 26.0      # Espaçamento Z dos furos de fixação
COMP_SUPORTE_MOTOR = 56.0      # Largura total cobrindo os furos com 8mm de margem
ALT_SUPORTE_MOTOR = 66.0       # Altura total cobrindo os furos com 8mm de margem
PROF_SUPORTE_MOTOR = 35.0      # Profundidade/Espessura do bloco plástico
RAIO_REBAIXO_M4 = 4.5          # Rebaixo p/ esconder a cabeça do parafuso M4
PROF_REBAIXO_M4 = 10.0         # Profundidade de mergulho da cabeça do parafuso

# Rodas / Oblongos
RECUO_OVAL_RODA = 65.0
LARG_OBLONGO_RODA = 95.0
ALT_OBLONGO_RODA = 50.0
SP_X_RODAS = 47.0
SP_Z_RODAS = 28.5

# Alça de Transporte
LARG_OVAL_ALCA = 95.0
ALT_OVAL_ALCA = 36.0

# Tensionador e Base
DIST_FRONTAIS_TENSIONADOR_1 = 38.1
DIST_FRONTAIS_TENSIONADOR_2 = 63.5
RECUO_Y_TENSIONADOR = 12.7
RAIO_FURO_M5 = 2.5

# Suporte Impresso
FOLGA_FURO_M4 = 0.2
COMP_SUPORTE_X = 61.2
POS_X_MOTOR_REAL = 45.6
RECUO_Y_MOTOR = 17.7
CORTES_MONTAGEM_MOTOR = 15.0
