"""
===============================================================================
THE IRON VANGUARD UGV - CONFIGURAÇÕES PARAMÉTRICAS GLOBAIS
===============================================================================
Projeto: Robô Terrestre Não Tripulado sobre Esteiras de Pneu Reutilizado
Estilo: Carcaça Militar Stealth Chanfrada com Torre FPV de Câmera Frontal
Material Estrutural: PETG Preto Fosco / Texturizado
===============================================================================
"""

CONFIG = {
    # --- Tolerâncias de Impressão FDM (PETG) ---
    "FOLGA_ROLAMENTO_608": 0.18,       # Ajuste sob pressão (Ø22.0mm nominal -> Ø22.18mm)
    "DIAM_FURO_M3": 3.2,               # Passante livre M3 (Ø3.2mm)
    "DIAM_FURO_M8": 8.4,               # Passante livre M8 (Ø8.4mm)
    
    # --- Trem de Rodagem e Rodas ---
    "DIAM_PISTA_RODA": 68.0,           # Diâmetro externo da pista onde assenta a esteira (mm)
    "DIAM_ABA_GUIA": 74.0,             # Diâmetro das abas guia (74mm < 78.8mm da esteira com cravos)
    "LARGURA_PISTA_RODA": 35.0,        # Largura útil da pista (mm)
    "ESPESSURA_ABA_RODA": 3.5,         # Espessura das abas guia da roda (mm)
    "LARGURA_ESTEIRA": 35.0,           # Alias para largura útil da esteira (mm)
    "ESPESSURA_ABA": 3.5,              # Alias para espessura da aba (mm)
    "ALTURA_ABA_GUIA": 3.0,            # Altura da aba guia (3.0mm retém a carcaça do pneu sem tocar no chão)
    "DIAM_PRIMITIVO_MOTRIZ": 68.0,     # Diâmetro da roda motriz (mm)
    "DIAM_POLIA_LIVRE": 68.0,          # Diâmetro da roda livre (mm)
    "ESPESSURA_ESTEIRA": 3.0,          # Espessura da fita de pneu MTB (mm)
    "ALTURA_CRAVOS_PNEU": 2.4,         # Altura dos cravos de borracha da esteira (mm)
    "DIAM_REBAIXO_FLANGE": 22.0,       # Diâmetro do rebaixo do flange (mm)
    "PROF_REBAIXO_FLANGE": 4.0,        # Profundidade do rebaixo (mm)
    "PCD_FLANGE_M3": 16.0,             # Círculo de furação do flange (mm)
    "DIAM_EIXO_MOTOR": 6.5,            # Furo central livre do eixo do motor (mm)
    "DIAM_EXT_ROLAMENTO_608": 22.18,   # Diâmetro externo para ajuste sob pressão (mm)
    "LARGURA_ROLAMENTO_608": 7.0,      # Largura do rolamento (mm)
    
    # --- Posições dos Eixos das Rodas (3 Rodas no Mesmo Nível de Solo) ---
    "POS_X_MOTOR": -85.0,              # Roda Traseira Motriz Raiada (mm)
    "POS_X_CENTRAL": 0.0,              # Roda Central Livre de Apoio (mm)
    "POS_X_TENSORA": 85.0,             # Roda Dianteira Livre Tensora (mm)
    "POS_Z_EIXOS": -12.0,              # Altura Z dos eixos em relação ao centro do chassi (mm)
    
    # --- Chassi Inferior (Banheira c/ Glacis Frontal Inclinado) ---
    "COMPRIMENTO_CHASSI": 280.0,       # Comprimento total da banheira em X (mm)
    "LARGURA_CHASSI": 180.0,           # Largura da banheira em Y (mm)
    "ALTURA_CHASSI": 65.0,             # Altura da banheira inferior em Z (mm)
    "ESPESSURA_PAREDE": 3.5,           # Espessura estrutural das paredes em PETG (mm)
    "COMP_RAMPA_FRONTAL": 45.0,        # Recuo horizontal da rampa frontal/glacis (mm)
    "CURSO_TENSIONADOR": 25.0,         # Rasgo oblongo de ajuste da esteira (mm)
    "FOLGA_TRAY_CHASSI": 5.0,          # Folga da bandeja de eletrônica (mm)
    "ESPESSURA_TRAY": 2.5,             # Espessura da chapa da bandeja (mm)
    "ALTURA_STANDOFF": 6.0,            # Altura das torres de circuito (mm)
    "DIAM_EXT_STANDOFF": 8.0,          # Diâmetro externo reforçado das torres M3 (mm)
    "RAIO_EXT_STANDOFF": 4.0,          # Raio externo reforçado das torres M3 (mm)
    
    # --- Carenagem Superior (Tampa Chanfrada Militar / Stealth) ---
    "COMPRIMENTO_TAMPA": 284.0,        # Comprimento da tampa superior (mm)
    "LARGURA_TAMPA": 184.0,            # Largura da tampa superior (mm)
    "ALTURA_TAMPA": 26.0,              # Altura da tampa (mm)
    "CHANFRO_TAMPA": 14.0,             # Chanfro perimetral a 45° nas bordas superiores (mm)
    "COMP_TORRE_CAM": 28.0,            # Comprimento do case protetor da câmera (mm)
    "LARG_TORRE_CAM": 34.0,            # Largura do case da câmera (mm)
    "ALT_TORRE_CAM": 22.0,             # Altura do case da câmera (mm)
    
    # --- Motorredutor JGB37-520 (12V) ---
    "DIAM_PASSAGEM_MOTOR": 12.5,       # Furo do gargalo da redução (mm)
    "PCD_MOTOR_M3": 31.0,              # Furação 6x M3 PCD 31mm
    "DIAM_CORPO_MOTOR": 37.0,          # Diâmetro externo da carcaça metálica (mm)
    "COMP_CORPO_MOTOR": 52.0,          # Comprimento do motorredutor (mm)
    "COMP_EIXO_MOTOR": 15.0,           # Comprimento do eixo motriz exposto (mm)
    
    # --- Eletrônica Interna ---
    "L298N_FUROS_X": 43.0,
    "L298N_FUROS_Y": 43.0,
    "LM2596_FUROS_X": 35.0,
    "LM2596_FUROS_Y": 20.0,
}

# --- Paleta de Cores Didática de Engenharia para o OCP CAD Viewer ---
CORES = {
    "CHASSI_BANHEIRA": "#2B303A",      # Cinza Antracite Industrial (diferencia do preto da tampa e rodas)
    "TAMPA_SUPERIOR": "#181A1C",       # Preto Carbono Acetinado Stealth
    "RODA_POLIA": "#25282F",           # Grafite Técnico Escuro
    "BORRACHA_ESTEIRA": "#121315",     # Borracha Vulcanizada Fosca de Pneu MTB
    "CRAVOS_ESTEIRA": "#1C1E22",       # Relevo dos cravos de borracha
    "METAL_CROMADO": "#ECEFF1",        # Aço cromo polido (porcas M8 e rolamentos 608-ZZ)
    "ACO_EIXO": "#ECEFF1",             # Eixos e porcas
    "ALUMINIO_USINADO": "#CFD8DC",     # Alumínio escovado (placa de emenda e flange de acoplamento)
    "ALUMINIO": "#CFD8DC",             # Alumínio torneado
    "ACO_MOTOR": "#78909C",            # Aço zincado do corpo do motorredutor
    "BANDEJA_ELETRONICA": "#3B4252",   # Azul Pizarra / Alumínio Anodizado da bandeja
    "LENTE_CAMERA": "#0D47A1",         # Azul antirreflexo da lente OV2640
    "PCB_L298N": "#C62828",            # Vermelho clássico da Ponte H L298N
    "DISSIPADOR_L298N": "#212121",     # Dissipador de calor preto anodizado
    "PCB_LM2596": "#1565C0",           # Azul do Step-Down LM2596
    "BATERIA_3S": "#FBC02D",           # Amarelo industrial Li-Ion do pack 3S
    "PCB_ESP32": "#2E7D32",            # Verde clássico do módulo ESP32-CAM
    
    # Aliases retrocompatíveis
    "PETG_PRETO": "#2B303A",
    "PETG_CHASSI": "#2B303A",
    "PETG_POLIA": "#25282F",
    "BORRACHA_PNEU": "#121315",
}

