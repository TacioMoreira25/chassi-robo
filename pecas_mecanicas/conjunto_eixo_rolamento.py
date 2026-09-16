"""
===============================================================================
THE IRON VANGUARD UGV - CONJUNTO EIXO, ROLAMENTO 608-ZZ E PORCA M8
===============================================================================
Componente: Centro de fixação da roda livre (rolamento 608-ZZ + porca sextavada M8)
Retorna um Part único para árvore limpa no OCP CAD Viewer.
===============================================================================
"""

import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_centro_roda_m8() -> Compound:
    """
    Gera o centro de fixação M8 integrando o modelo CAD real 608zz.step e porca sextavada.
    """
    # 1. Carregamento do Rolamento 608-ZZ real em STEP
    caminho_step = os.path.join(os.path.dirname(__file__), "..", "modelos_cad", "rolamento_608zz.step")
    rolamento = None
    if os.path.exists(caminho_step):
        try:
            rolamento = import_step(caminho_step).moved(Rotation(0, 90, 0))
            rolamento.color = Color(cfg.CORES["METAL_CROMADO"])
            rolamento.label = "Rolamento 608-ZZ (STEP)"
        except Exception:
            rolamento = None

    if rolamento is None:
        with BuildPart() as b:
            with BuildSketch(Plane.XY):
                Circle(22.0 / 2.0)
                Circle(8.0 / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=7.0)
        rolamento = b.part.moved(Location((0, 0, -3.5)))
        rolamento.color = Color(cfg.CORES["METAL_CROMADO"])
        rolamento.label = "Rolamento 608-ZZ"

    # 2. Arruela Plana M8 (Ø15mm x 1.2mm) e Porca Sextavada M8 externa
    with BuildPart() as hardware:
        with Locations((0, 0, 3.5 + 0.6)):
            with BuildSketch(Plane.XY):
                Circle(15.0 / 2.0)
                Circle(8.4 / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=1.2)

        with Locations((0, 0, 3.5 + 1.2 + 2.75)):
            with BuildSketch(Plane.XY):
                RegularPolygon(radius=13.0 / math.sqrt(3), side_count=6)
                Circle(8.0 / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=5.5)
            # Ponta do parafuso M8
            with Locations((0, 0, 3.5)):
                Cylinder(radius=3.9, height=2.0)

    hardware_part = hardware.part
    hardware_part.color = Color(cfg.CORES["METAL_CROMADO"])
    hardware_part.label = "Porca Sextavada M8"

    return Compound(label="Centro M8 c/ Rolamento 608-ZZ", children=[rolamento, hardware_part])

if __name__ == "__main__":
    print("Gerando Centro de Roda M8...")
    c = criar_centro_roda_m8()
    try:
        from ocp_vscode import show
        show(c, names=["Centro M8"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
