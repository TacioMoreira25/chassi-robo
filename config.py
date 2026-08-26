"""
Configurações Globais Dimensionais - Creative Home Tank.
Todas as medidas em milímetros (mm).
"""

CONFIG = {
    # --- Dimensões Globais do Chassi ---
    "COMP_TOTAL": 400.0,          # Base do robô (a parte mais comprida no chão)
    "LARG_EXTERNA": 220.0,
    "ESPESSURA_MADEIRA": 12.0,    # Compensado 12mm
    "ALT_PAREDE": 110.0,
    "ALT_TRAVESSA": 20.0,
    
    # Valores derivados
    "LARG_INTERNA": 220.0 - (2 * 12.0), # 196.0
    
    # --- Geometria Calculada (Perfil Trapezoidal Normal) ---
    "COMP_TOPO": 290.0,           # Topo reto (400 - 55 - 55)
    "CHANFRO_X": 55.0,            # Chanfro horizontal no topo
    "CHANFRO_Z": 40.0,            # Altura reta nas pontas antes de subir (110-70)
}
