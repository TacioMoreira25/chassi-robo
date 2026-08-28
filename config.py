"""
Configurações Globais Dimensionais - Creative Home Tank.
Todas as medidas em milímetros (mm).
"""

CONFIG = {
    # --- Dimensões Globais do Chassi ---
    "COMP_TOTAL": 400.0,          # Comprimento máximo (Topo reto horizontal com 400mm)
    "LARG_EXTERNA": 222.0,        # Largura total externa ajustada para alinhar com travessa e paredes
    "ESPESSURA_MADEIRA": 12.0,    # Compensado 12mm
    "ALT_PAREDE": 110.0,          # Altura total da parede lateral (110mm)
    "ALT_TRAVESSA": 20.0,         # Altura da travessa interna (20mm)
    
    # Valores derivados
    "LARG_INTERNA": 198.0,        # Largura interna correspondente à travessa de 198mm (222.0 - 2 * 12.0)
    
    # --- Geometria da Parede Lateral Trapezoidal (Perfil Real) ---
    "COMP_BASE": 290.0,           # Fundo reto (400mm - 2 * 55mm = 290mm)
    "CHANFRO_X": 55.0,            # Largura do chanfro nas extremidades (55mm)
    "CHANFRO_Z": 70.0,            # Altura do chanfro (70mm)
}
