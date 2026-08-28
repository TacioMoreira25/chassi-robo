"""
Parâmetros dimensionais de ferragens e mecânica (Creative Home Tank).
"""

# --- Eixos e Rolamentos ---
RAIO_FURO_EIXO_M8 = 4.0
DIAM_EIXO_M8 = 8.0
OD_ROLAMENTO_608 = 22.0
ID_ROLAMENTO_608 = 8.0
ALTURA_ROLAMENTO_608 = 7.0
COMP_PARAFUSO_M8 = 75.0   # Comprimento nominal de 75mm para os eixos
DIAM_FURO_MADEIRA = 40.0  # Furo circular de 40mm na lateral de madeira para os suportes de rolamento/motor

# --- Catracas de Bicicleta 18T ---
DIAM_CATRACA = 76.0      # Diametro externo total aproximado
ESPESSURA_CATRACA = 15.0 # Espessura 
DIAM_FURO_CATRACA = 32.9 # Furo interno roscado
DENTES_CATRACA = 18

# --- Bucha de Madeira (Adaptador Catraca -> Rolamento) ---
OD_BUCHA = 33.0          # Ligeiramente maior para prensar na catraca (tolerancia de aperto na rosca)
DIAM_REBAIXO_BUCHA = 22.0 # Para o rolamento 608zz
PROF_REBAIXO_BUCHA = 7.0  # Altura do rolamento
ESPESSURA_BUCHA = 15.0

# --- Motores Johnson 100 RPM ---
DIAM_MOTOR_JOHNSON = 37.0
COMP_MOTOR_JOHNSON = 60.0 # Valor tipico
DIAM_RESSALTO = 12.2
ALTURA_RESSALTO = 4.0
DIAM_EIXO_MOTOR = 6.0
COMP_EIXO_MOTOR = 30.0

# --- Tensionador ---
LARG_OBLONGO = 25.0
ALT_OBLONGO = 8.5 # Para eixo M8 deslizar

# --- FUROS DAS CATRACAS ---
# Origem X=0 no centro da parede, Z=0 na base (fundo).
FUROS_RODAS = [
    (-175.0, 85.0), # 0: Superior Traseira (Motriz - Motor Johnson) -> Fica perto do teto/chapa_base
    (-120.0, 40.0), # 1: Inferior Traseira (Livre - Eixo Fixo M8) -> Fica embaixo, tocando o chão
    (175.0, 85.0),  # 2: Superior Dianteira (Tensionadora - Slot Oblongo)
    (120.0, 40.0)   # 3: Inferior Dianteira (Livre - Eixo Fixo M8)
]


# Dimensões do rasgo oblongo para tensionamento
LARG_OBLONGO = 25.0
ALT_OBLONGO = 8.5

# --- Folgas e Montagem ---
DIST_CATRACA_PAREDE = 13.0 # Espaço exato para as duas porcas M8 (6.5mm cada) atuarem como espaçador
