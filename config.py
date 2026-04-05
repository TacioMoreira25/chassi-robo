from build123d import *

# Medidas Globais da Madeira
COMP_TOTAL = 406.4       # 16 polegadas (Tamanho total do chassi)
LARG_EXTERNA = 254.0     # 10 polegadas (Largura máxima)
ESPESSURA_PAREDE = 15.0  # Madeira estrutural
ALT_PAREDE = 89.0        # Altura da viga
ESPESSURA_PISO = 6.0     # Compensado de piso

# Medida do Vão Dianteiro (Tension Bay)
COMP_BAY = 76.2          # 3 polegadas (O comprimento da 'língua' exposta)
PROF_RECORTE = 38.1      # 1.5 polegadas de cada lado (Quanto afina o piso)

# Cálculos Derivados (para uso nos outros módulos)
LARG_LINGUA = LARG_EXTERNA - (2 * PROF_RECORTE)
LARG_INTERNA = LARG_EXTERNA - (2 * ESPESSURA_PAREDE)
# O corpo largo do chassi (a caixa seca)
COMP_CORPO = COMP_TOTAL - COMP_BAY # 330.2 mm (Área onde piso e paredes se sobrepõem)