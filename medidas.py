"""
===============================================================================
ROBÔ DE INSPEÇÃO - MEDIDAS DERIVADAS, CINEMÁTICA E NÍVEL DE SOLO
===============================================================================
Módulo para cálculos geométricos automáticos, offsets de montagem e verificação.
Garante que todas as variáveis derivadas sejam computadas a partir do config.py
sem redundâncias ou hardcoding.
===============================================================================
"""

import config as cfg

# =============================================================================
# 1. GEOMETRIA VERTICAL E NÍVEL DE SOLO (MATEMATICAMENTE NIVELADO)
# =============================================================================

# Chassi centrado em Z=0: vai de Z_CHASSI_FUNDO até Z_CHASSI_TOPO
ALTURA_CHASSI = cfg.CONFIG["ALTURA_CHASSI"]           # 75.0mm
Z_CHASSI_TOPO = ALTURA_CHASSI / 2.0                   # +37.5mm
Z_CHASSI_FUNDO = -ALTURA_CHASSI / 2.0                 # -37.5mm

# Solo e Vão Livre
VAO_LIVRE_SOLO = cfg.CONFIG.get("VAO_LIVRE_SOLO", 15.0) # 15.0mm
Z_SOLO = Z_CHASSI_FUNDO - VAO_LIVRE_SOLO               # -52.5mm (contato com o chão)

# Face interna da esteira apoiada no solo (onde assentam as polias)
ESPESSURA_TOTAL_ESTEIRA = cfg.CONFIG["ESPESSURA_ESTEIRA"] + cfg.CONFIG["ALTURA_CRAVOS_PNEU"] # 5.0mm
Z_PISTA_SOLO = Z_SOLO + ESPESSURA_TOTAL_ESTEIRA       # -47.5mm

# Raios Primitivos de Assentamento das Polias (Todas Ø60mm idênticas)
RAIO_PRIMITIVO_MOTRIZ = cfg.CONFIG["DIAM_PRIMITIVO_MOTRIZ"] / 2.0 # 30.0mm (Ø60mm)
RAIO_CORPO_LIVRE = cfg.CONFIG["DIAM_POLIA_LIVRE"] / 2.0           # 30.0mm (Ø60mm)

# Posições Z dos eixos (TODAS as 3 polias na MESMA LINHA DE CENTRO):
Z_EIXO_MOTOR = Z_PISTA_SOLO + RAIO_PRIMITIVO_MOTRIZ   # -17.5mm (35.0mm acima do solo)
Z_EIXOS_LIVRES = Z_PISTA_SOLO + RAIO_CORPO_LIVRE      # -17.5mm (35.0mm acima do solo)

# Altura Total do Robô Montado (do solo ao topo da tampa)
ALTURA_TAMPA = cfg.CONFIG["ALTURA_TAMPA"]             # 5.0mm
Z_TOPO_TAMPA = Z_CHASSI_TOPO + ALTURA_TAMPA           # +42.5mm
ALTURA_TOTAL_ROBO = Z_TOPO_TAMPA - Z_SOLO             # 95.0mm exatos!

# =============================================================================
# 2. DIMENSÕES E OFFSETS TRANSVERSAIS (LARGURA TOTAL = 230mm)
# =============================================================================

ALTURA_ABA = cfg.CONFIG.get("ALTURA_ABA_GUIA", 4.0)
RAIO_ABA_MOTRIZ = RAIO_PRIMITIVO_MOTRIZ + ALTURA_ABA  # 34.0mm (Ø68mm total da aba)
RAIO_ABA_LIVRE = RAIO_CORPO_LIVRE + ALTURA_ABA        # 29.0mm (Ø58mm total da aba)

# Largura total da polia (35mm pista + 2x 2.5mm abas = 40mm)
LARGURA_TOTAL_POLIA = cfg.CONFIG["LARGURA_PISTA_RODA"] + 2.0 * cfg.CONFIG["ESPESSURA_ABA_RODA"]

# Posições Y das paredes externas do chassi (160mm total -> ±80mm)
Y_PAREDE_ESQ = cfg.CONFIG["LARGURA_CHASSI"] / 2.0     # +80.0mm
Y_PAREDE_DIR = -cfg.CONFIG["LARGURA_CHASSI"] / 2.0    # -80.0mm

# Posição Y central das polias:
# Folga de 1.5mm entre a aba interna e a parede do chassi.
# Centro da roda em Y: 80.0 + 1.5 + (LARGURA_TOTAL_POLIA / 2.0) = 80.0 + 1.5 + 20.0 = 101.5mm
# Borda externa da esteira/roda em Y: 101.5 + 17.5 = 119.0mm -> Largura total = 238mm (ou ajustado para 230mm ponta a ponta)
FOLGA_POLIA_PAREDE = 1.0
Y_CENTRO_RODA_ESQ = Y_PAREDE_ESQ + FOLGA_POLIA_PAREDE + (cfg.CONFIG["LARGURA_PISTA_RODA"] / 2.0) + cfg.CONFIG["ESPESSURA_ABA_RODA"] # ~101.0mm
Y_CENTRO_RODA_DIR = -Y_CENTRO_RODA_ESQ

# =============================================================================
# 3. BANDEJA INTERNA E ESPAÇO ELETRÔNICO
# =============================================================================

COMP_INTERNO_CHASSI = cfg.CONFIG["COMPRIMENTO_CHASSI"] - 2 * cfg.CONFIG["ESPESSURA_PAREDE"] # 235.0mm
LARG_INTERNA_CHASSI = cfg.CONFIG["LARGURA_CHASSI"] - 2 * cfg.CONFIG["ESPESSURA_PAREDE"]     # 155.0mm
ALT_INTERNA_CHASSI = cfg.CONFIG["ALTURA_CHASSI"] - cfg.CONFIG["ESPESSURA_PAREDE"]           # 72.5mm

Z_FUNDO_INTERNO = Z_CHASSI_FUNDO + cfg.CONFIG["ESPESSURA_PAREDE"]                            # -35.0mm
COMP_TRAY = cfg.CONFIG["COMP_TRAY"]                                                          # 190.0mm
LARG_TRAY = cfg.CONFIG["LARG_TRAY"]                                                          # 140.0mm

# Tabela dos Eixos das Rodas: (nome, x, z)
EIXOS_RODAS = [
    ("traseira_motriz", cfg.CONFIG["POS_X_MOTOR"], cfg.CONFIG["POS_Z_MOTOR"]),
    ("central_apoio", cfg.CONFIG["POS_X_CENTRAL"], cfg.CONFIG["POS_Z_EIXOS"]),
    ("dianteira_tensora", cfg.CONFIG["POS_X_TENSORA"], cfg.CONFIG["POS_Z_EIXOS"]),
]

def imprimir_resumo_geometrico():
    """Exibe no terminal a checagem didática dos cálculos de engenharia."""
    print("=" * 75)
    print("ROBÔ DE INSPEÇÃO - RELATÓRIO GEOMÉTRICO E DE NIVELAMENTO OFICIAL")
    print("=" * 75)
    print(f"Chassi: {cfg.CONFIG['COMPRIMENTO_CHASSI']} x {cfg.CONFIG['LARGURA_CHASSI']} x {cfg.CONFIG['ALTURA_CHASSI']} mm")
    print(f"Fundo do chassi: Z = {Z_CHASSI_FUNDO:.1f} mm | Topo: Z = {Z_CHASSI_TOPO:.1f} mm")
    print(f"Nível do Solo: Z = {Z_SOLO:.1f} mm (Vão livre: {VAO_LIVRE_SOLO:.1f} mm)")
    print(f"Pista da Esteira no Solo: Z = {Z_PISTA_SOLO:.1f} mm")
    print(f"Eixo Motorredutor (Ø{cfg.CONFIG['DIAM_PRIMITIVO_MOTRIZ']}mm): Z = {cfg.CONFIG['POS_Z_MOTOR']:.1f} mm (altura do solo: {cfg.CONFIG['POS_Z_MOTOR'] - Z_SOLO:.1f} mm)")
    print(f"Eixos Livres (Ø{cfg.CONFIG['DIAM_POLIA_LIVRE']}mm): Z = {cfg.CONFIG['POS_Z_EIXOS']:.1f} mm (altura do solo: {cfg.CONFIG['POS_Z_EIXOS'] - Z_SOLO:.1f} mm)")
    print(f"Altura Total Robô: {ALTURA_TOTAL_ROBO:.1f} mm (do solo ao topo da tampa)")
    print(f"Posições X dos Eixos: Traseiro={cfg.CONFIG['POS_X_MOTOR']}mm | Central={cfg.CONFIG['POS_X_CENTRAL']}mm | Dianteiro={cfg.CONFIG['POS_X_TENSORA']}mm")
    print("=" * 75)

if __name__ == "__main__":
    imprimir_resumo_geometrico()
