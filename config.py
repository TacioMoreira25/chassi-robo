"""
Configurações Globais Dimensionais - Creative Home Tank.
Todas as medidas em milímetros (mm).
"""

CONFIG = {
    # --- Dimensões Globais do Chassi ---
    "COMP_TOTAL": 400.0,          # Base do robô (a parte mais comprida no chão)
    "LARG_EXTERNA": 220.0,
    "LARG_INTERNA": 198.0,
    "ALT_PAREDE": 110.0,
    "ESPESSURA_MADEIRA": 12.0,    # Compensado 12mm
    "COMP_TOPO": 240.0,           # Topo da lateral (a parte reta mais curta no ar)
    "RECUO_CHANFRO_X": 80.0,      # (400 - 240) / 2 = 80mm
    "ALTURA_CHANFRO_Z": 110.0,
    
    # --- Geometria Calculada (Perfil Trapezoidal) ---
    # Os chanfros removem as pontas inferiores.
    # O início da base plana está em X = RECUO_CHANFRO_X.
    # Base plana vai de X=55 até X=55+240=295? Mas se COMP_TOTAL=400, o chanfro final deveria ser 400-55=345?
    # Vamos considerar que o chanfro tem recuo de 55 de cada lado:
    # 400 - 55 - 55 = 290mm. A spec fala COMP_BASE_INFERIOR = 240. 
    # Então (400 - 240) / 2 = 80mm de recuo na base? 
    # Assumirei o RECUO_CHANFRO_X como o ponto onde o chanfro começa em X na parte superior.
}
