"""
Configurações Globais Dimensionais - Creative Home Tank.
Todas as medidas em milímetros (mm).
"""

CONFIG = {
    # --- Dimensões Globais do Chassi ---
    "COMP_TOTAL": 400.0,          # Comprimento máximo (Topo reto horizontal com 400mm / 40cm)
    "LARG_EXTERNA": 220.0,        # Largura total externa (220mm / 22cm)
    "ESPESSURA_MADEIRA": 12.0,    # Compensado 12mm
    "ALT_PAREDE": 110.0,          # Altura total da parede lateral (110mm / 11cm)
    "ALT_TRAVESSA": 20.0,         # Altura da travessa interna (20mm / 2cm)
    
    # Valores derivados
    "LARG_INTERNA": 220.0 - (2 * 12.0), # 196.0 mm (Espaço interno entre as paredes)
    
    # --- Geometria da Parede Lateral Trapezoidal (Perfil Real) ---
    "COMP_BASE": 240.0,           # Fundo reto no chão (240mm) - corrigido do blueprint
    "CHANFRO_X": 80.0,            # Recuo horizontal do chanfro (80mm de cada lado)
    "CHANFRO_Z": 85.0,            # Altura Z onde o chanfro começa (quina lateral começa a descer a 85mm do chão)
}
