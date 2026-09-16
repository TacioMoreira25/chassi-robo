"""
===============================================================================
THE IRON VANGUARD UGV - RODA MOTRIZ RAIADA (TRASEIRA)
===============================================================================
Componente: Roda de tração traseira acoplada ao eixo do motor JGB37-520
Características:
- Design com 5 raios estruturais vazados (estilo roda esportiva robótica como no robô real)
- Pista de 35mm de largura para a esteira de pneu MTB
- Aba lateral guia interna anti-descarrilamento
- Rebaixo usinado para flange de alumínio de 22mm x 4mm com 4x parafusos M3 em PCD 16mm
Material: PETG Preto Fosco
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_roda_motriz() -> Part:
    """
    Gera a Roda Motriz com raios estruturais e acoplamento ao motor.
    """
    diam_pista = cfg.CONFIG["DIAM_PISTA_RODA"]
    larg_pista = cfg.CONFIG["LARGURA_PISTA_RODA"]
    diam_aba = cfg.CONFIG["DIAM_ABA_GUIA"]
    esp_aba = cfg.CONFIG["ESPESSURA_ABA_RODA"]
    furo_m3 = cfg.CONFIG["DIAM_FURO_M3"]
    furo_eixo = 6.5

    with BuildPart() as roda:
        # 1. Aro cilíndrico externo da pista
        Cylinder(radius=diam_pista / 2.0, height=larg_pista)

        # 2. Aba lateral guia interna (lado chassi)
        with Locations((0, 0, -larg_pista / 2.0 + esp_aba / 2.0)):
            Cylinder(radius=diam_aba / 2.0, height=esp_aba)

        # 3. Cavidade frontal rebaixada do aro
        with Locations((0, 0, 3.0)):
            Cylinder(radius=(diam_pista - 7.0) / 2.0, height=larg_pista, mode=Mode.SUBTRACT)

        # 4. Cubo central sólido
        Cylinder(radius=16.0, height=larg_pista)

        # 5. 5x Raios estruturais vazados conectando o aro ao cubo central
        with PolarLocations(radius=22.5, count=5):
            Box(17.0, 5.5, larg_pista - 6.0)

        # 6. Rebaixo na face externa para embutir o flange de alumínio (Ø22mm x 4mm)
        with Locations((0, 0, larg_pista / 2.0 - 2.0)):
            Cylinder(radius=22.0 / 2.0, height=4.2, mode=Mode.SUBTRACT)

        # 7. Furo central do eixo do motor Ø6.5mm
        Cylinder(radius=furo_eixo / 2.0, height=larg_pista + 6.0, mode=Mode.SUBTRACT)

        # 8. 4x Furos passantes M3 para parafusar o flange de alumínio (PCD 16mm)
        with PolarLocations(radius=16.0 / 2.0, count=4):
            Cylinder(radius=furo_m3 / 2.0, height=larg_pista + 6.0, mode=Mode.SUBTRACT)

        # 9. Chanfros nas arestas externas
        circulos = roda.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)
        if len(circulos) >= 2:
            chamfer(circulos[-1], length=1.5)

    peca = roda.part
    peca.color = Color(cfg.CORES["RODA_POLIA"])
    peca.label = "Roda Motriz Raiada 5-Spoke"
    return peca

if __name__ == "__main__":
    print("Gerando Roda Motriz Raiada...")
    roda = criar_roda_motriz()
    try:
        from ocp_vscode import show
        show(roda, names=["Roda Motriz Raiada"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
