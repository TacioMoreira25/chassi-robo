"""
===============================================================================
THE IRON VANGUARD UGV - MONTAGEM GERAL DIDÁTICA E HIERÁRQUICA
===============================================================================
Engenharia Mecatrônica - Orquestração e Integração Modular no Espaço 3D
===============================================================================
Montagem rigorosamente alinhada e didática para visualização no OCP CAD Viewer:
- Subsistema 1: Carenagem Superior Stealth (Tampa Chanfrada c/ Torre FPV)
- Subsistema 2: Chassi Banheira Inferior (Fechado c/ Glacis e Grelhas)
- Subsistema 3: Bandeja Interna Eletrônica (PETG anti-vibração)
- Subsistema 4: Circuitos Eletrônicos Embarcados (L298N, LM2596, ESP32-CAM, 3S)
- Subsistema 5: Trem de Rodagem Esquerdo (Rodas Raiadas/Côncavas, Esteira, Motor)
- Subsistema 6: Trem de Rodagem Direito (Rodas Raiadas/Côncavas, Esteira, Motor)
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from build123d import *
import config as cfg

# Peças Estruturais Impressas (PETG)
from pecas_impressas import (
    chassi_banheira,
    tampa_superior,
    roda_livre,
    roda_motriz,
    suporte_eletronica,
)

# Componentes Mecânicos e Eletroeletrônicos
from pecas_mecanicas import (
    motor_jgb37_520,
    flange_aluminio,
    esteira_pneu_mtb,
    conjunto_eixo_rolamento,
    eletronica,
)

def montar_subsistemas() -> dict:
    """
    Gera todos os subsistemas do robô com geometria 100% alinhada e
    hierarquia limpa para a árvore lateral do OCP CAD Viewer.
    """
    alt_chassi = cfg.CONFIG["ALTURA_CHASSI"] # 65.0
    esp_parede = cfg.CONFIG["ESPESSURA_PAREDE"] # 3.5

    # -------------------------------------------------------------
    # 1. CARENAGEM SUPERIOR STEALTH (TAMPA)
    # -------------------------------------------------------------
    z_borda_chassi = alt_chassi / 2.0 # 32.5mm
    tampa = tampa_superior.criar_tampa_superior().moved(Location((0, 0, z_borda_chassi)))

    # -------------------------------------------------------------
    # 2. CHASSI BANHEIRA INFERIOR (CASCO FECHADO)
    # -------------------------------------------------------------
    chassi = chassi_banheira.criar_chassi()

    # -------------------------------------------------------------
    # 3. BANDEJA INTERNA DA ELETRÔNICA
    # -------------------------------------------------------------
    z_fundo_interno = -alt_chassi / 2.0 + esp_parede + 1.25 # -27.75mm
    x_centro_tray = -10.0
    tray = suporte_eletronica.criar_suporte_eletronica().moved(Location((x_centro_tray, 0, z_fundo_interno)))

    # -------------------------------------------------------------
    # 4. CIRCUITOS ELETRÔNICOS EMBARCADOS (LAYOUT DIDÁTICO SEM COLISÕES)
    # -------------------------------------------------------------
    z_topo_standoff = z_fundo_interno + 1.25 + 6.0

    # Ponte H L298N no centro-traseiro da bandeja
    placa_l298n = eletronica.criar_ponte_h_l298n().moved(Location((x_centro_tray - 5.0, 0, z_topo_standoff + 0.8)))
    placa_l298n.label = "Ponte H L298N (12V)"

    # Regulador Step-Down LM2596 ao lado da ponte H
    placa_lm2596 = eletronica.criar_step_down_lm2596().moved(Location((x_centro_tray - 5.0, -42.0, z_topo_standoff + 0.8)))
    placa_lm2596.label = "Step-Down LM2596 (5V)"

    # Pack 3S 18650 instalado longitudinalmente no berço central entre os motores
    bateria_3s = eletronica.criar_pack_bateria_3s().moved(Location((x_centro_tray - 75.0, 0, z_fundo_interno + 2.0)))
    bateria_3s.label = "Pack 3S 18650 (12V)"

    # Módulo ESP32-CAM na seção frontal da bandeja, alinhado à torre da câmera
    esp32_cam = eletronica.criar_esp32_cam().moved(Location((x_centro_tray + 60.0, 0, z_fundo_interno + 4.0)))
    esp32_cam.label = "Modulo ESP32-CAM"

    eletronica_conjunto = Compound(
        label="Eletronica Embarcada",
        children=[placa_l298n, placa_lm2596, bateria_3s, esp32_cam]
    )

    # -------------------------------------------------------------
    # 5 & 6. TREM DE RODAGEM ESQUERDO E DIREITO
    # -------------------------------------------------------------
    roda_livre_base = roda_livre.criar_roda_livre()
    roda_motriz_base = roda_motriz.criar_roda_motriz()
    centro_m8_base = conjunto_eixo_rolamento.criar_centro_roda_m8()
    flange_base = flange_aluminio.criar_flange_aluminio()
    motor_base = motor_jgb37_520.criar_motor_jgb37()
    esteira_base = esteira_pneu_mtb.criar_esteira_mtb()

    x_motriz = cfg.CONFIG["POS_X_MOTOR"]     # -85.0
    x_central = cfg.CONFIG["POS_X_CENTRAL"]   # 0.0
    x_tensora = cfg.CONFIG["POS_X_TENSORA"]   # +85.0
    z_eixos = cfg.CONFIG["POS_Z_EIXOS"]       # -12.0

    larg_chassi = cfg.CONFIG["LARGURA_CHASSI"]    # 180.0
    larg_pista = cfg.CONFIG["LARGURA_PISTA_RODA"] # 35.0

    trens_tracao = {}

    for lado in ["ESQUERDO", "DIREITO"]:
        sinal_y = 1 if lado == "ESQUERDO" else -1
        esp_boss_motor = 2.0
        y_parede_int = sinal_y * (larg_chassi / 2.0 - esp_parede - esp_boss_motor)
        
        folga_parede = 3.0
        y_centro_roda = sinal_y * (larg_chassi / 2.0 + folga_parede + larg_pista / 2.0) # ±110.5mm

        rot_roda = Rotation(-90, 0, 0) if lado == "ESQUERDO" else Rotation(90, 0, 0)
        rot_motor = Rotation(-90, 0, 0) if lado == "ESQUERDO" else Rotation(90, 0, 0)

        # Motorredutor assentado no boss interno da parede
        m = motor_base.moved(rot_motor).moved(Location((x_motriz, y_parede_int, z_eixos)))
        m.label = f"Motorredutor JGB37-520 ({lado})"

        # Roda Traseira Motriz com Flange
        r_m = roda_motriz_base.moved(rot_roda).moved(Location((x_motriz, y_centro_roda, z_eixos)))
        offset_flange = (larg_pista / 2.0 - 2.0) * sinal_y
        flange = flange_base.moved(rot_roda).moved(Location((x_motriz, y_centro_roda + offset_flange, z_eixos)))
        roda_traseira = Compound(label=f"Roda Traseira Motriz ({lado})", children=[r_m, flange])

        # Roda Central Livre com Centro M8
        r_c = roda_livre_base.moved(rot_roda).moved(Location((x_central, y_centro_roda, z_eixos)))
        offset_centro_m8 = (larg_pista / 2.0 - 3.5) * sinal_y
        c_m8_c = centro_m8_base.moved(rot_roda).moved(Location((x_central, y_centro_roda + offset_centro_m8, z_eixos)))
        roda_central = Compound(label=f"Roda Central Apoio ({lado})", children=[r_c, c_m8_c])

        # Roda Dianteira Tensora com Centro M8
        r_t = roda_livre_base.moved(rot_roda).moved(Location((x_tensora, y_centro_roda, z_eixos)))
        c_m8_t = centro_m8_base.moved(rot_roda).moved(Location((x_tensora, y_centro_roda + offset_centro_m8, z_eixos)))
        roda_dianteira = Compound(label=f"Roda Dianteira Tensora ({lado})", children=[r_t, c_m8_t])

        # Esteira de Borracha Oca
        est = esteira_base.moved(Location((0, y_centro_roda, 0)))
        est.label = f"Esteira Pneu MTB ({lado})"

        trens_tracao[lado] = Compound(
            label=f"Trem de Rodagem {lado}",
            children=[roda_traseira, roda_central, roda_dianteira, est, m]
        )

    return {
        "carenagem": tampa,
        "chassi": chassi,
        "bandeja": tray,
        "eletronica": eletronica_conjunto,
        "tracao_esq": trens_tracao["ESQUERDO"],
        "tracao_dir": trens_tracao["DIREITO"]
    }

def montar_ugv() -> Compound:
    """
    Retorna o Compound global com a árvore unificada.
    """
    sub = montar_subsistemas()
    return Compound(
        label="The Iron Vanguard UGV",
        children=[
            sub["carenagem"],
            sub["chassi"],
            sub["bandeja"],
            sub["eletronica"],
            sub["tracao_esq"],
            sub["tracao_dir"]
        ]
    )

if __name__ == "__main__":
    print("Gerando Montagem Hierárquica do UGV...")
    ugv = montar_ugv()
    try:
        from ocp_vscode import show
        show(ugv, names=["The Iron Vanguard UGV"])
        print("Montagem renderizada no OCP CAD Viewer com sucesso!")
    except Exception as err:
        print(f"Montagem gerada com sucesso! (OCP CAD Viewer: {err})")
