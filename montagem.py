"""
===============================================================================
ROBÔ DE INSPEÇÃO - MONTAGEM GERAL DIDÁTICA E HIERÁRQUICA
===============================================================================
Engenharia Mecatrônica - Orquestração e Integração Modular no Espaço 3D
===============================================================================
Montagem rigorosamente alinhada e didática para visualização no OCP CAD Viewer:
- Subsistema 1: Carenagem Superior Stealth (Suporte Tilt + Cooler 80mm + Painel)
- Subsistema 2: Chassi Banheira Inferior (Glacis 45°, Grelhas, Aletas e Passa-Cabos)
- Subsistema 3: Bandeja Interna Eletrônica (PETG c/ Berço Central 3S)
- Subsistema 4: Circuitos Eletrônicos Embarcados (L298N, LM2596, ESP32-CAM, 3S)
- Subsistema 5: Trem de Rodagem Esquerdo (Polia Motriz 60mm, Livres 50mm, Esteira)
- Subsistema 6: Trem de Rodagem Direito (Polia Motriz 60mm, Livres 50mm, Esteira)
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
    alt_chassi = cfg.CONFIG["ALTURA_CHASSI"] # 75.0
    esp_parede = cfg.CONFIG["ESPESSURA_PAREDE"] # 2.5
    esp_tray = cfg.CONFIG["ESPESSURA_TRAY"] # 2.5
    alt_standoff = cfg.CONFIG["ALTURA_STANDOFF"] # 5.0

    # -------------------------------------------------------------
    # 1. CARENAGEM SUPERIOR STEALTH (TAMPA)
    # -------------------------------------------------------------
    z_borda_chassi = alt_chassi / 2.0 # 37.5mm
    tampa = tampa_superior.criar_tampa_superior().moved(Location((0, 0, z_borda_chassi)))

    # -------------------------------------------------------------
    # 2. CHASSI BANHEIRA INFERIOR (CASCO FECHADO)
    # -------------------------------------------------------------
    chassi = chassi_banheira.criar_chassi()

    # -------------------------------------------------------------
    # 3. BANDEJA INTERNA DA ELETRÔNICA
    # -------------------------------------------------------------
    z_fundo_interno = -alt_chassi / 2.0 + esp_parede + esp_tray / 2.0 # -33.75mm
    x_centro_tray = 0.0
    tray = suporte_eletronica.criar_suporte_eletronica().moved(Location((x_centro_tray, 0, z_fundo_interno)))

    # -------------------------------------------------------------
    # 4. CIRCUITOS ELETRÔNICOS EMBARCADOS (LAYOUT COM CG CENTRAL BALANCEADO)
    # -------------------------------------------------------------
    z_topo_standoff = z_fundo_interno + esp_tray / 2.0 + alt_standoff # -30.0mm

    # Pack 3S 18650 instalado no BERÇO CENTRAL GEOMÉTRICO (0, 0) para equilibrar o CG
    bateria_3s = eletronica.criar_pack_bateria_3s().moved(Location((0, 0, z_fundo_interno + esp_tray / 2.0 + 9.5)))
    bateria_3s.label = "Pack 3S 18650 (CG Central)"

    # Ponte H L298N nas torres traseiras entre os motores
    placa_l298n = eletronica.criar_ponte_h_l298n().moved(Location((-68.0, 0, z_topo_standoff + 0.8)))
    placa_l298n.label = "Ponte H L298N (12V)"

    # Regulador Step-Down LM2596 nas torres dianteiras direitas
    placa_lm2596 = eletronica.criar_step_down_lm2596().moved(Location((48.0, -32.0, z_topo_standoff + 0.8)))
    placa_lm2596.label = "Step-Down LM2596 (5V)"

    # Módulo ESP32-CAM nas torres dianteiras esquerdas
    esp32_cam = eletronica.criar_esp32_cam().moved(Location((48.0, 32.0, z_topo_standoff + 0.8)))
    esp32_cam.label = "Modulo ESP32-CAM"

    eletronica_conjunto = Compound(
        label="Eletronica Embarcada",
        children=[placa_l298n, placa_lm2596, bateria_3s, esp32_cam]
    )

    # -------------------------------------------------------------
    # 5 & 6. TREM DE RODAGEM ESQUERDO E DIREITO
    # -------------------------------------------------------------
    roda_livre_tensora_base = roda_livre.criar_roda_livre(com_abas=True)
    roda_livre_central_base = roda_livre.criar_roda_livre(com_abas=True)
    roda_motriz_base = roda_motriz.criar_roda_motriz()
    centro_m8_base = conjunto_eixo_rolamento.criar_centro_roda_m8()
    flange_base = flange_aluminio.criar_flange_aluminio()
    motor_base = motor_jgb37_520.criar_motor_jgb37()
    esteira_base = esteira_pneu_mtb.criar_esteira_mtb()

    x_motriz = cfg.CONFIG["POS_X_MOTOR"]            # -95.0mm
    x_central = cfg.CONFIG["POS_X_CENTRAL"]          # 0.0mm
    x_tensora = cfg.CONFIG["POS_X_TENSORA"]          # +95.0mm
    z_motriz = cfg.CONFIG.get("POS_Z_MOTOR", -17.5)  # -17.5mm (35mm acima do solo)
    z_eixos = cfg.CONFIG.get("POS_Z_EIXOS", -22.5)   # -22.5mm (assentadas no solo)

    larg_chassi = cfg.CONFIG["LARGURA_CHASSI"]       # 160.0mm
    larg_pista = cfg.CONFIG["LARGURA_PISTA_RODA"]    # 35.0mm
    esp_aba = cfg.CONFIG.get("ESPESSURA_ABA_RODA", 2.5) # 2.5mm
    folga_parede = 1.0                              # 1.0mm folga livre da aba à parede

    trens_tracao = {}

    for lado in ["ESQUERDO", "DIREITO"]:
        sinal_y = 1 if lado == "ESQUERDO" else -1
        esp_boss_motor = 2.0
        y_parede_int = sinal_y * (larg_chassi / 2.0 - esp_parede - esp_boss_motor)
        
        # Centro da pista da roda garantindo largura total ~230mm ponta a ponta das esteiras
        y_centro_roda = sinal_y * 98.0 # ±98.0mm (borda externa da esteira em ±115.5mm -> Largura total = 231mm)

        rot_roda = Rotation(-90, 0, 0) if lado == "ESQUERDO" else Rotation(90, 0, 0)
        rot_motor = Rotation(-90, 0, 0) if lado == "ESQUERDO" else Rotation(90, 0, 0)

        # Roda Traseira Motriz Maciça com Flange de Alumínio embutido no rebaixo
        r_m = roda_motriz_base.moved(rot_roda).moved(Location((x_motriz, y_centro_roda, z_motriz)))
        offset_flange = (larg_pista / 2.0 + esp_aba - 2.0) * sinal_y
        flange = flange_base.moved(rot_roda).moved(Location((x_motriz, y_centro_roda + offset_flange, z_motriz)))
        roda_traseira = Compound(label=f"Roda Traseira Motriz ({lado})", children=[r_m, flange])

        # Roda Central Livre de Apoio (Rolamentos e porcas embutidos no cubo)
        r_c = roda_livre_central_base.moved(rot_roda).moved(Location((x_central, y_centro_roda, z_eixos)))
        c_m8_c = centro_m8_base.moved(rot_roda).moved(Location((x_central, y_centro_roda, z_eixos)))
        roda_central = Compound(label=f"Roda Central Apoio ({lado})", children=[r_c, c_m8_c])

        # Roda Dianteira Tensora (Rolamentos e porcas embutidos no cubo)
        r_t = roda_livre_tensora_base.moved(rot_roda).moved(Location((x_tensora, y_centro_roda, z_eixos)))
        c_m8_t = centro_m8_base.moved(rot_roda).moved(Location((x_tensora, y_centro_roda, z_eixos)))
        roda_dianteira = Compound(label=f"Roda Dianteira Tensora ({lado})", children=[r_t, c_m8_t])

        # Motorredutor assentado no boss interno da parede
        m = motor_base.moved(rot_motor).moved(Location((x_motriz, y_parede_int, z_motriz)))
        m.label = f"Motorredutor JGB37-520 ({lado})"

        # Esteira de Borracha Oca c/ Cravos 3D perfeitamente nivelada no solo
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

def montar_robo_inspecao() -> Compound:
    """
    Retorna o Compound global do Robô de Inspeção com a árvore unificada.
    """
    sub = montar_subsistemas()
    return Compound(
        label="Robô de Inspeção",
        children=[
            sub["carenagem"],
            sub["chassi"],
            sub["bandeja"],
            sub["eletronica"],
            sub["tracao_esq"],
            sub["tracao_dir"]
        ]
    )

# Alias retrocompatível
montar_ugv = montar_robo_inspecao

if __name__ == "__main__":
    print("Gerando Montagem Hierárquica do Robô de Inspeção...")
    robo = montar_robo_inspecao()
    try:
        from ocp_vscode import show
        show(robo, names=["Robô de Inspeção"])
        print("Montagem renderizada no OCP CAD Viewer com sucesso!")
    except Exception as err:
        print(f"Montagem gerada com sucesso! (OCP CAD Viewer: {err})")
