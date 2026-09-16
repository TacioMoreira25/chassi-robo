"""
===============================================================================
THE IRON VANGUARD UGV - FLANGE DE ACOPLAMENTO DE ALUMÍNIO (6mm -> M3)
===============================================================================
Componente: Flange metálico usinado em alumínio para transmissão de torque
Dimensões: Diâmetro externo da base: 22.0mm, Altura da base: 4.0mm
Retorna um Part sólido único para árvore limpa no OCP CAD Viewer.
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_flange_aluminio():
    """
    Gera o flange de alumínio de 22mm x 4mm carregando STEP oficial se disponível ou via modelo paramétrico 1:1.
    """
    caminho_step = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modelos_cad", "flange_acoplamento_6mm.step"))
    if os.path.exists(caminho_step):
        try:
            peca = import_step(caminho_step).moved(Rotation(-90, 0, 0))
            peca.color = Color(cfg.CORES["ALUMINIO_USINADO"])
            peca.label = "Flange Alumínio 6mm (STEP Oficial)"
            return peca
        except Exception:
            pass

    diam_base = cfg.CONFIG["DIAM_REBAIXO_FLANGE"]
    esp_base = cfg.CONFIG["PROF_REBAIXO_FLANGE"]
    pcd = cfg.CONFIG["PCD_FLANGE_M3"]
    furo_m3 = cfg.CONFIG["DIAM_FURO_M3"]

    with BuildPart() as flange:
        # Base em disco (22mm x 4mm) que entra no rebaixo da roda motriz
        with Locations((0, 0, esp_base / 2.0)):
            Cylinder(radius=diam_base / 2.0, height=esp_base)

        # Cubo saliente de aperto (Ø11mm x 6mm)
        with Locations((0, 0, -3.0)):
            Cylinder(radius=5.5, height=6.0)

        # Furo central do eixo Ø6mm
        Cylinder(radius=3.0, height=20.0, mode=Mode.SUBTRACT)

        # 4x Furos passantes M3 em PCD 16mm
        with Locations((0, 0, 0)):
            with PolarLocations(radius=pcd / 2.0, count=4):
                Cylinder(radius=furo_m3 / 2.0, height=20.0, mode=Mode.SUBTRACT)

    peca = flange.part
    peca.color = Color(cfg.CORES["ALUMINIO"])
    peca.label = "Flange Alumínio 22mm"
    return peca

if __name__ == "__main__":
    print("Gerando Flange de Alumínio...")
    f = criar_flange_aluminio()
    try:
        from ocp_vscode import show
        show(f, names=["Flange Alumínio"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
