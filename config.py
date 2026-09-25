"""
===============================================================================
ROBÔ DE INSPEÇÃO - COMPÊNDIO PARAMÉTRICO GLOBAL E OFICIAL
===============================================================================
Projeto: Robô de Inspeção Terrestre sobre Esteiras de Pneu MTB
Normas de Referência: NR-10 e NR-33 (Segurança Elétrica e Espaços Confinados)
Material Estrutural: Plástico PETG Preto Fosco / Texturizado (Não Condutivo)

Todas as medidas em milímetros (mm).
Fonte Única da Verdade (SSOT) para todos os subsistemas do robô.
===============================================================================
"""

CONFIG = {
    # =========================================================================
    # SEÇÃO 1: TOLERÂNCIAS E NORMAS DE IMPRESSÃO 3D (PETG)
    # =========================================================================
    "FOLGA_ROLAMENTO_608": 0.18,       # Ajuste sob pressão p/ rolamento 608-ZZ (Ø22.0mm nominal -> Ø22.18mm)
    "DIAM_FURO_M3": 3.2,               # Furo passante livre para parafusos M3 (Ø3.2mm)
    "DIAM_FURO_M4": 4.2,               # Furo passante livre para parafusos M4 do Cooler (Ø4.2mm)
    "DIAM_FURO_M8": 8.4,               # Furo passante livre para eixos M8 das polias livres (Ø8.4mm)
    "DIAM_FURO_M10": 10.2,             # Furo Ø10.2mm (Sensor MLX90614 e Faróis LED M10)
    "DIAM_FURO_ANTENA_SMA": 6.5,       # Furo Ø6.5mm na tampa para conector SMA fêmea Wi-Fi

    # =========================================================================
    # SEÇÃO 2: CHASSI MONOBLOCO INFERIOR ("BANHEIRA" EM PETG)
    # =========================================================================
    "COMPRIMENTO_CHASSI": 240.0,       # Comprimento total da banheira em X (cabe na mesa 256x256mm com brim)
    "LARGURA_CHASSI": 160.0,           # Largura total externa da banheira em Y (160mm)
    "ALTURA_CHASSI": 75.0,             # Altura estrutural da banheira em Z (75mm)
    "ESPESSURA_PAREDE": 2.5,           # Espessura uniforme das paredes estruturais (2.5mm / 5 perímetros)
    "COMP_RAMPA_FRONTAL": 40.0,        # Recuo horizontal do glacis frontal a 45° (40mm)
    "RAIO_CANTO_INFERIOR": 4.0,        # Raio dos filetes inferiores externos para absorção de choque
    "DIAM_PASSAGEM_GROMMET": 12.0,     # Furos Ø12.0mm para anéis de borracha passa-cabos

    # =========================================================================
    # SEÇÃO 3: CARENAGEM SUPERIOR E TAMPA REMOVÍVEL
    # =========================================================================
    "COMPRIMENTO_TAMPA": 240.0,        # Comprimento da tampa em X (240mm)
    "LARGURA_TAMPA": 160.0,            # Largura da tampa em Y (160mm)
    "ALTURA_TAMPA": 16.0,              # Altura da carenagem stealth chanfrada (16mm)
    "CHANFRO_TAMPA": 5.0,              # Chanfro perimetral a 45° nas bordas superiores
    "LARGURA_CANALETA_IP65": 3.0,      # Largura da canaleta inferior para gaxeta de silicone (3.0mm)
    "PROF_CANALETA_IP65": 2.0,         # Profundidade da canaleta IP65 (2.0mm)

    # =========================================================================
    # SEÇÃO 4: GESTÃO TÉRMICA (COOLER FAN RISE MODE 80MM / 12V)
    # =========================================================================
    "COMP_COOLER_FAN": 80.0,           # Dimensões da carcaça do cooler: 80 x 80 x 25mm
    "ALT_COOLER_FAN": 25.0,
    "DIAM_RECORTE_COOLER": 75.0,       # Recorte circular central de exaustão na tampa (Ø75mm)
    "LARG_FURACAO_COOLER": 71.5,       # 4x furos M4 em quadrado perfeito de 71.5 x 71.5mm
    "DIAM_FURO_COOLER": 4.2,           # Diâmetro dos furos de fixação do cooler (M4)
    "MOLDURA_COOLER_LARG": 85.0,       # Moldura/suporte em PETG: 85 x 85mm
    "MOLDURA_COOLER_ESP": 4.0,         # Espessura da moldura: 4.0mm

    # =========================================================================
    # SEÇÃO 5: MÓDULO FRONTAL DE VISÃO E SENSORES (SUPORTE ARTICULADO TILT)
    # =========================================================================
    "LARG_BLOCO_TILT": 55.0,           # Largura do bloco em PETG (55mm)
    "ALT_BLOCO_TILT": 22.0,            # Altura do bloco integrado (22mm)
    "PROF_BLOCO_TILT": 25.0,           # Profundidade do bloco em PETG (25mm)
    "JANELA_ESP32_CAM": 10.0,          # Recorte quadrado 10x10mm para a lente OV2640
    "DIAM_FURO_MLX90614": 10.2,        # Furo circular Ø10.2mm para sensor infravermelho
    "DIAM_FURO_FAROL_LED": 10.2,       # 2x Furos Ø10.2mm (M10) para faróis LED Olho de Águia
    "DIAM_FURO_ORELHA_TILT": 3.2,      # Furos de articulação Ø3.2mm para parafusos M3

    # =========================================================================
    # SEÇÃO 6: TREM DE RODAGEM, POLIAS E TRAÇÃO (TODAS 100% PROPORCIONAIS Ø60MM)
    # =========================================================================
    "DIAM_PRIMITIVO_MOTRIZ": 60.0,     # Polia Motriz Traseira: Diâmetro Ø60mm sólido em PETG
    "DIAM_POLIA_LIVRE": 60.0,          # Polias Livres (Central e Dianteira): Diâmetro Ø60mm idêntico
    "ALTURA_ABA_GUIA": 3.5,            # Abas anti-descarrilamento elegantes (3.5mm acima da pista, Ø67mm total)
    "ESPESSURA_ABA_RODA": 2.5,         # Espessura das abas guia (2.5mm)
    "LARGURA_PISTA_RODA": 35.0,        # Largura útil da pista para esteira MTB (35mm)
    "LARGURA_ESTEIRA": 35.0,           # Largura nominal da esteira (35mm)
    "ESPESSURA_ABA": 2.5,              # Alias para espessura da aba
    "ESPESSURA_ESTEIRA": 3.0,          # Espessura da carcaça de borracha do pneu MTB (3.0mm)
    "ALTURA_CRAVOS_PNEU": 2.0,         # Altura dos cravos de tração 3D da esteira (2.0mm)
    "TRANSPASSE_EMENDA": 30.0,         # Comprimento de transpasse da chapa de emenda (30mm)

    # =========================================================================
    # SEÇÃO 7: NÍVEL DE SOLO, ALTURA DOS EIXOS E VÃO LIVRE
    # =========================================================================
    # Chassi centrado em Z=0: Z de -37.5 a +37.5mm.
    # Solo em Z = -52.5mm (vão livre do fundo do chassi = 15.0mm).
    # Pista interna da esteira no solo: Z = -52.5 + 5.0 (3mm borracha + 2mm cravo) = -47.5mm.
    # Eixo Motor (Raio 30mm): Z = -47.5 + 30.0 = -17.5mm. Altura do eixo ao solo: 35.0mm exatos!
    # Eixos Livres (Raio 25mm): Z = -47.5 + 25.0 = -22.5mm. Tocam perfeitamente o solo nivelado a -47.5mm!
    # Topo da Tampa: Z = +37.5 + 5.0 = +42.5mm.
    # Altura Total do Robô (do solo ao topo da tampa): +42.5 - (-52.5) = 95.0mm exatos!
    "VAO_LIVRE_SOLO": 15.0,            # Vão livre entre o fundo do chassi e o solo (15.0mm)
    "POS_X_MOTOR": -100.0,             # Posição X da Roda Traseira Motriz (-100mm)
    "POS_X_CENTRAL": 0.0,              # Posição X da Roda Central de Apoio (0mm)
    "POS_X_TENSORA": 100.0,            # Posição X da Roda Dianteira Tensora (+100mm)
    "POS_Z_MOTOR": -17.5,              # Altura Z do eixo do motorredutor (-17.5mm, 35mm acima do solo)
    "POS_Z_EIXOS": -17.5,              # Altura Z dos eixos livres (idêntica à do motor: -17.5mm, mesma linha de centro)
    "CURSO_TENSIONADOR": 25.0,         # Rasgo oblongo horizontal dianteiro (25 x 8.4mm)

    # =========================================================================
    # SEÇÃO 8: BANDEJA INTERNA DE ELETRÔNICA E BERÇO CENTRAL DA BATERIA
    # =========================================================================
    "COMP_TRAY": 190.0,                # Comprimento da placa da bandeja (190mm, cabe no fundo plano)
    "LARG_TRAY": 140.0,                # Largura da placa da bandeja (140mm, cabe na largura interna de 155mm)
    "ESPESSURA_TRAY": 2.5,             # Espessura da chapa da bandeja (2.5mm)
    "ALTURA_STANDOFF": 5.0,            # Altura das torres espaçadoras M3 (5.0mm)
    "RAIO_EXT_STANDOFF": 4.0,          # Raio externo das torres M3 (Ø8.0mm)
    "COMP_BERCO_BATERIA": 70.0,        # Comprimento do berço central do Pack 3S 18650 (70mm)
    "LARG_BERCO_BATERIA": 58.0,        # Largura do berço central (58mm)
    "ALT_PAREDE_BERCO": 12.0,          # Altura da mureta de contenção do pack de baterias (12mm)
    "COMP_FENDA_PRESILHA": 15.0,       # 4x fendas para abraçadeiras de nylon zip-ties (15 x 3mm)
    "LARG_FENDA_PRESILHA": 3.0,

    # =========================================================================
    # SEÇÃO 9: MOTORREDUTOR JGB37-520 (12V DC)
    # =========================================================================
    "DIAM_PASSAGEM_MOTOR": 12.5,       # Furo excêntrico do gargalo da redução (Ø12.5mm)
    "PCD_MOTOR_M3": 31.0,              # Círculo de furação 6x M3 na carcaça frontal (PCD 31mm)
    "DIAM_CORPO_MOTOR": 37.0,          # Diâmetro externo da caixa de redução metálica (Ø37mm)
    "COMP_CORPO_MOTOR": 52.0,          # Comprimento do motorredutor (52mm)
    "COMP_EIXO_MOTOR": 38.0,           # Eixo motriz Ø6mm prolongado para acoplamento direto

    # =========================================================================
    # SEÇÃO 10: ELEMENTOS DE FIXAÇÃO E HARDWARE COMERCIAL (FLANGE, PARAFUSOS M8)
    # =========================================================================
    "DIAM_REBAIXO_FLANGE": 22.0,       # Diâmetro do rebaixo para flange de alumínio (Ø22.0mm)
    "PROF_REBAIXO_FLANGE": 4.0,        # Profundidade do rebaixo (4.0mm)
    "PCD_FLANGE_M3": 16.0,             # Círculo de furação 4x M3 do flange (PCD 16mm)
    "DIAM_EIXO_MOTOR": 6.5,            # Furo central livre para eixo do motor (Ø6.5mm)
    "DIAM_EXT_ROLAMENTO_608": 22.18,   # Diâmetro da cavidade para 2x rolamentos 608-ZZ (Ø22.18mm)
    "LARGURA_ROLAMENTO_608": 7.0,      # Largura de cada rolamento 608-ZZ (7.0mm)
    "COMPRIMENTO_EIXO_M8": 50.0,       # Comprimento do eixo M8 compacto rente ao cubo da roda
    "DIAM_ARRUELA_M8": 24.0,           # Diâmetro da arruela funileiro M8 (Ø24mm)
    "ESP_ARRUELA_M8": 2.0,             # Espessura da arruela funileiro M8 (2.0mm)

    # =========================================================================
    # SEÇÃO 11: PAINEL EXTERNO, INTERRUPTORES E ALARMES
    # =========================================================================
    "RECORTE_CHAVE_KCD1_X": 19.2,      # Interruptor gangorra liga/desliga KCD1 (19.2 x 13.0mm)
    "RECORTE_CHAVE_KCD1_Y": 13.0,
    "LARG_VOLTIMETRO": 22.5,           # Display voltímetro LED DC 0-30V (22.5 x 14.0mm)
    "ALT_VOLTIMETRO": 14.0,
    "DIAM_BUZZER_ALARME": 12.0,        # Buzzer piezoelétrico ativo 5V de alarme sonoro (Ø12mm)
    "DIAM_LED_ALARME": 5.0,            # LED difuso 5mm de alarme visual térmico (Ø5mm)
}

# --- Paleta de Cores Didática de Engenharia para o OCP CAD Viewer ---
CORES = {
    "CHASSI_BANHEIRA": "#2B303A",      # PETG Cinza Antracite Industrial
    "TAMPA_SUPERIOR": "#181A1C",       # PETG Preto Carbono Acetinado Stealth
    "RODA_POLIA": "#25282F",           # Grafite Técnico Escuro
    "BORRACHA_ESTEIRA": "#121315",     # Borracha Vulcanizada Fosca de Pneu MTB
    "CRAVOS_ESTEIRA": "#1C1E22",       # Relevo dos cravos de borracha
    "METAL_CROMADO": "#ECEFF1",        # Aço cromo polido (porcas M8 e rolamentos 608-ZZ)
    "ACO_EIXO": "#ECEFF1",             # Barras roscadas e porcas
    "ALUMINIO_USINADO": "#CFD8DC",     # Alumínio escovado (placa de emenda e flange de acoplamento)
    "ALUMINIO": "#CFD8DC",             # Alumínio torneado
    "ACO_MOTOR": "#78909C",            # Aço zincado do corpo do motorredutor
    "BANDEJA_ELETRONICA": "#3B4252",   # Azul Pizarra / PETG da bandeja
    "LENTE_CAMERA": "#0D47A1",         # Azul antirreflexo da lente OV2640
    "PCB_L298N": "#C62828",            # Vermelho clássico da Ponte H L298N
    "DISSIPADOR_L298N": "#212121",     # Dissipador de calor preto anodizado
    "PCB_LM2596": "#1565C0",           # Azul do Step-Down LM2596
    "BATERIA_3S": "#FBC02D",           # Amarelo industrial Li-Ion do pack 3S 18650
    "PCB_ESP32": "#2E7D32",            # Verde clássico do módulo ESP32-CAM
    "SENSOR_TERMICO": "#B0BEC5",       # Cápsula metálica TO-39 do MLX90614
    "FAROL_LED": "#FFF176",            # Amarelo translúcido dos faróis LED Olho de Águia
    "GROMMET_BORRACHA": "#212121",     # Borracha preta dos anéis passa-cabos
    "COOLER_FAN": "#37474F",           # Carcaça cinza escuro do cooler fan Rise Mode 80mm
    "VOLTIMETRO_LED": "#D32F2F",       # Display digital vermelho do voltímetro
    "CHAVE_KCD1": "#D32F2F",           # Interruptor vermelho KCD1
    "BUZZER_ALARME": "#212121",        # Buzzer piezoelétrico preto 5V
    "LED_ALARME": "#FF1744",           # LED difuso vermelho de alarme térmico
    "SILICONE_VEDACAO": "#90CAF9",     # Fita de vedação de silicone IP65
    
    # Aliases retrocompatíveis
    "PETG_PRETO": "#2B303A",
    "PETG_CHASSI": "#2B303A",
    "PETG_POLIA": "#25282F",
    "BORRACHA_PNEU": "#121315",
}
