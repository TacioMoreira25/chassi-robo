"""
===============================================================================
ROBÔ DE INSPEÇÃO - BANDEJA DE ELETRÔNICA INTERNA (TRAY)
===============================================================================
Componente: Placa interna removível para montagem anti-vibração da eletrônica
Dimensões: 180mm (C) x 142mm (L) x 2.5mm (E) - 100% contida dentro da banheira
Alojamentos:
- Berço central de bateria 3S 18650 (70 x 58 mm com borda de contenção de 12mm) no centro geométrico (0, 0)
- 4 fendas vazadas de 15 x 3 mm para presilhas/velcro de fixação da bateria
- Standoffs M3 para Ponte H L298N (furação 43x43mm)
- Standoffs M3 para Regulador LM2596 (furação 35x20mm)
- Standoffs M3 para Módulo ESP32
- Recortes laterais traseiros para passagem dos motores JGB37-520
Material: PETG Preto / Grafite
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_suporte_eletronica() -> Part:
    """
    Gera a Bandeja Interna de Eletrônica (Tray) em PETG:
    - Dimensões: 180mm x 142mm x 2.5mm (X de -110mm a +70mm, 100% contida no fundo plano)
    - Berço central de bateria 3S 18650 (70 x 58 mm com borda de 12mm) em X=0, Y=0
    - 4 fendas vazadas de 15 x 3 mm para presilhas/velcro
    - Torres cilíndricas (stand-offs) elevadas a 5mm do fundo com furos M3
    - Recortes laterais para motores JGB37-520
    """
    comp_tray = cfg.CONFIG.get("COMP_TRAY", 180.0) # 180.0
    larg_tray = cfg.CONFIG.get("LARG_TRAY", 142.0) # 142.0
    esp_tray = cfg.CONFIG.get("ESPESSURA_TRAY", 2.5) # 2.5
    alt_standoff = cfg.CONFIG.get("ALTURA_STANDOFF", 5.0) # 5.0
    raio_ext_standoff = cfg.CONFIG.get("RAIO_EXT_STANDOFF", 4.0) # 4.0
    furo_m3 = cfg.CONFIG.get("DIAM_FURO_M3", 3.2) # 3.2

    comp_berco = cfg.CONFIG.get("COMP_BERCO_BATERIA", 70.0) # 70.0
    larg_berco = cfg.CONFIG.get("LARG_BERCO_BATERIA", 58.0) # 58.0
    alt_parede_berco = cfg.CONFIG.get("ALT_PAREDE_BERCO", 12.0) # 12.0
    esp_parede_berco = 2.0

    pos_x_motor = cfg.CONFIG.get("POS_X_MOTOR", -100.0)

    # A bandeja vai de X = -110.0 a X = +70.0 (centro geométrico da chapa em X = -20.0)
    # Isso garante que a frente termine a 7.5mm antes do início do glacis frontal
    x_centro_placa = -20.0

    with BuildPart() as tray:
        # 1. Base plana estrutural da bandeja contida no fundo plano da banheira
        with Locations((x_centro_placa, 0, 0)):
            Box(comp_tray, larg_tray, esp_tray)

        # 2. Recortes laterais traseiros para passagem dos motorredutores JGB37-520
        for y_mot in [-larg_tray / 2.0, larg_tray / 2.0]:
            with Locations((pos_x_motor, y_mot, 0)):
                Box(55.0, 40.0, esp_tray * 3, mode=Mode.SUBTRACT)

        # 3. Berço da Bateria 3S no CENTRO GEOMÉTRICO (0, 0) para equilíbrio perfeito de CG
        z_parede = esp_tray / 2.0 + alt_parede_berco / 2.0
        with Locations((0, 0, z_parede)):
            Box(comp_berco + 2 * esp_parede_berco, larg_berco + 2 * esp_parede_berco, alt_parede_berco)
            Box(comp_berco, larg_berco, alt_parede_berco + 1.0, mode=Mode.SUBTRACT)

        # 4. 4x Fendas vazadas de 15 x 3 mm para presilhas (zip-ties) ou velcro
        for x_fenda in [-20.0, 20.0]:
            for y_fenda in [-larg_berco / 2.0 - 2.5, larg_berco / 2.0 + 2.5]:
                with Locations((x_fenda, y_fenda, 0)):
                    Box(cfg.CONFIG.get("COMP_FENDA_PRESILHA", 15.0), cfg.CONFIG.get("LARG_FENDA_PRESILHA", 3.0), esp_tray + 2.0, mode=Mode.SUBTRACT)

        # 5. Torres cilíndricas (stand-offs) de 5mm para Ponte H L298N (43x43mm)
        # Posicionada no vão traseiro entre os motores
        pos_l298n = (-68.0, 0.0, esp_tray / 2.0 + alt_standoff / 2.0)
        with Locations(pos_l298n):
            with GridLocations(x_spacing=43.0, y_spacing=43.0, x_count=2, y_count=2):
                Cylinder(radius=raio_ext_standoff, height=alt_standoff)
                Cylinder(radius=furo_m3 / 2.0, height=alt_standoff * 2, mode=Mode.SUBTRACT)

        # 6. Torres de 5mm para Step-Down LM2596 (35x20mm) no quadrante dianteiro direito
        pos_lm2596 = (48.0, -32.0, esp_tray / 2.0 + alt_standoff / 2.0)
        with Locations(pos_lm2596):
            with GridLocations(x_spacing=35.0, y_spacing=20.0, x_count=2, y_count=2):
                Cylinder(radius=raio_ext_standoff, height=alt_standoff)
                Cylinder(radius=furo_m3 / 2.0, height=alt_standoff * 2, mode=Mode.SUBTRACT)

        # 7. Torres de 5mm para Módulo ESP32 no quadrante dianteiro esquerdo
        pos_esp32 = (48.0, 32.0, esp_tray / 2.0 + alt_standoff / 2.0)
        with Locations(pos_esp32):
            with GridLocations(x_spacing=26.0, y_spacing=38.0, x_count=2, y_count=2):
                Cylinder(radius=raio_ext_standoff, height=alt_standoff)
                Cylinder(radius=furo_m3 / 2.0, height=alt_standoff * 2, mode=Mode.SUBTRACT)

        # 8. Rasgos para chicotes e cabos dianteiros
        with Locations((62.0, 0, 0)):
            Box(6.0, 40.0, esp_tray + 2.0, mode=Mode.SUBTRACT)

    peca = tray.part
    peca.color = Color(cfg.CORES["BANDEJA_ELETRONICA"])
    peca.label = "Bandeja Interna Eletronica (CG Central)"
    return peca

if __name__ == "__main__":
    print("Gerando Bandeja de Eletrônica Interna...")
    suporte = criar_suporte_eletronica()
    try:
        from ocp_vscode import show
        show(suporte, names=["Bandeja Eletrônica"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
