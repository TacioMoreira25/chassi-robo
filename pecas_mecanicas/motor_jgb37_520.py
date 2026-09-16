"""
===============================================================================
THE IRON VANGUARD UGV - MOTORREDUTOR JGB37-520 (12V DC)
===============================================================================
Componente: Representação CAD do motorredutor de 12V com redução de 37mm
Dimensões: Caixa de redução Ø37mm x 22mm, corpo motor Ø36mm x 30mm, eixo Ø6mm x 15mm
Retorna um Part sólido único para árvore limpa no OCP CAD Viewer.
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_motor_jgb37():
    """
    Gera o motorredutor JGB37-520 integrando o modelo CAD real 'motor medrano-Body.step'.
    """
    caminho_step = os.path.join(os.path.dirname(__file__), "..", "modelos_cad", "motor_jgb37_520.step")
    if os.path.exists(caminho_step):
        try:
            peca = import_step(caminho_step).moved(Rotation(0, 180, 0))
            peca.color = Color(cfg.CORES["ACO_MOTOR"])
            peca.label = "Motorredutor JGB37-520 (STEP)"
            return peca
        except Exception:
            pass

    diam_caixa = cfg.CONFIG["DIAM_CORPO_MOTOR"] # 37.0
    pcd = cfg.CONFIG["PCD_MOTOR_M3"]           # 31.0
    furo_m3 = cfg.CONFIG["DIAM_FURO_M3"]       # 3.2
    comp_eixo = cfg.CONFIG["COMP_EIXO_MOTOR"]   # 15.0

    with BuildPart() as motor:
        with Locations((0, 0, -11.0)):
            Cylinder(radius=diam_caixa / 2.0, height=22.0)
        
        with Locations((0, 0, 1.5)):
            Cylinder(radius=6.0, height=3.0)

        with Locations((0, 0, -37.0)):
            Cylinder(radius=36.0 / 2.0, height=30.0)

        with Locations((0, 0, 0)):
            with PolarLocations(radius=pcd / 2.0, count=6):
                Cylinder(radius=furo_m3 / 2.0, height=8.0, mode=Mode.SUBTRACT)

        with Locations((0, 0, comp_eixo / 2.0 + 3.0)):
            Cylinder(radius=3.0, height=comp_eixo)

    peca = motor.part
    peca.color = Color(cfg.CORES["ACO_MOTOR"])
    peca.label = "Motorredutor JGB37-520"
    return peca

if __name__ == "__main__":
    print("Gerando Motorredutor JGB37-520...")
    m = criar_motor_jgb37()
    try:
        from ocp_vscode import show
        show(m, names=["Motor JGB37-520"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
