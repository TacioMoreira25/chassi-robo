"""
===============================================================================
THE IRON VANGUARD UGV - BANDEJA DE ELETRÔNICA INTERNA (TRAY)
===============================================================================
Componente: Placa interna removível para montagem anti-vibração da eletrônica
Dimensões: 215mm (C) x 165mm (L) x 2.5mm (E) - 100% contida dentro da banheira
Alojamentos:
- Standoffs M3 para Ponte H L298N (furação 43x43mm)
- Standoffs M3 para Regulador LM2596 (furação 35x20mm)
- Berço para Pack de Baterias 3S 18650 com rasgos para presilhas
- Passagens para fiação dos motores e sensores
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
    Gera a Bandeja Interna de Eletrônica ajustada para o interior do chassi banheira.
    """
    comp_tray = 210.0
    larg_tray = 165.0
    esp_tray = cfg.CONFIG["ESPESSURA_TRAY"]
    alt_standoff = cfg.CONFIG["ALTURA_STANDOFF"]
    furo_m3 = cfg.CONFIG["DIAM_FURO_M3"]

    with BuildPart() as tray:
        # 1. Base plana da bandeja
        Box(comp_tray, larg_tray, esp_tray)

        # 2. Recortes laterais traseiros para passagem livre dos motores JGB37-520
        with Locations((-77.5, 60.0, 0), (-77.5, -60.0, 0)):
            Box(60.0, 50.0, esp_tray + 2.0, mode=Mode.SUBTRACT)

        # 3. Torres de elevação (Standoffs M3) para Driver Ponte H L298N (43x43mm)
        pos_l298n = (-5.0, 0.0, esp_tray / 2.0 + alt_standoff / 2.0)
        with Locations(pos_l298n):
            with GridLocations(x_spacing=43.0, y_spacing=43.0, x_count=2, y_count=2):
                Cylinder(radius=3.5, height=alt_standoff)
                Cylinder(radius=furo_m3 / 2.0, height=alt_standoff * 2, mode=Mode.SUBTRACT)

        # 4. Torres de elevação para o Regulador Step-Down LM2596 (35x20mm)
        pos_lm2596 = (-5.0, -42.0, esp_tray / 2.0 + alt_standoff / 2.0)
        with Locations(pos_lm2596):
            with GridLocations(x_spacing=35.0, y_spacing=20.0, x_count=2, y_count=2):
                Cylinder(radius=3.0, height=alt_standoff)
                Cylinder(radius=furo_m3 / 2.0, height=alt_standoff * 2, mode=Mode.SUBTRACT)

        # 5. Berço rebaixado e rasgos para cintas do Pack 3S 18650 (entre os motores)
        with Locations((-75.0, 0.0, 0)):
            Box(75.0, 42.0, esp_tray + 1.0, mode=Mode.SUBTRACT)

        # 6. Rasgos para passagem de chicotes de cabos
        with Locations((40.0, 45.0, 0), (40.0, -45.0, 0)):
            Box(35.0, 8.0, esp_tray + 2.0, mode=Mode.SUBTRACT)

    peca = tray.part
    peca.color = Color(cfg.CORES["BANDEJA_ELETRONICA"])
    peca.label = "Bandeja Interna Eletrônica"
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
