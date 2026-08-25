"""
Parâmetros dimensionais de ferragens e mecânica (Creative Home Tank).
"""

# --- Eixos e Rolamentos ---
RAIO_FURO_EIXO_M8 = 4.0
DIAM_EIXO_M8 = 8.0
OD_ROLAMENTO_608 = 22.0
ID_ROLAMENTO_608 = 8.0
ALTURA_ROLAMENTO_608 = 7.0

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
COMP_EIXO_MOTOR = 15.0

# --- Tensionador ---
LARG_OBLONGO = 25.0
ALT_OBLONGO = 8.5 # Para eixo M8 deslizar

# --- Coordenadas dos Furos (X, Z) das Rodas / Catracas ---
# X medido da traseira para a frente (0 a 400).
# Z medido da base plana para cima.
# O robô é um trapézio: Base 400, Topo 240. 
# As rodas inferiores ficam mais afastadas que as superiores.
FUROS_RODAS = [
    (90.0, 90.0),   # 0: Traseira Superior (Motriz - Motor)
    (40.0, 30.0),   # 1: Traseira Inferior (Livre - Oblongo)
    (360.0, 30.0),  # 2: Dianteira Inferior (Livre - Oblongo)
    (300.0, 75.0)   # 3: Dianteira Superior (Livre - Oblongo)
]

# --- Folgas e Montagem ---
DIST_CATRACA_PAREDE = 5.0 # Espaço entre a catraca e a madeira
