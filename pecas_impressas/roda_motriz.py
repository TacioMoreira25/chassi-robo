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
    Gera a Roda Motriz com raios estruturais, abas duplas anti-descarrilamento (12mm) e acoplamento ao motor.
    """
    diam_pista = cfg.CONFIG["DIAM_PISTA_RODA"]
    larg_pista = cfg.CONFIG["LARGURA_PISTA_RODA"]
    diam_aba = cfg.CONFIG["DIAM_ABA_GUIA"]       # 92mm (12mm acima da pista)
    esp_aba = cfg.CONFIG["ESPESSURA_ABA_RODA"]   # 3.5mm
    furo_m3 = cfg.CONFIG["DIAM_FURO_M3"]         # 3.2mm
    furo_eixo = 6.5
    larg_total = larg_pista + 2.0 * esp_aba     # 42mm total

    with BuildPart() as roda:
        # 1. Pista cilíndrica central (onde assenta a esteira de 35mm)
        Cylinder(radius=diam_pista / 2.0, height=larg_pista)

        # 2. Aba lateral guia interna (lado chassi) - 12mm de altura
        with Locations((0, 0, -larg_pista / 2.0 - esp_aba / 2.0)):
            Cylinder(radius=diam_aba / 2.0, height=esp_aba)

        # 3. Aba lateral guia externa (lado fora) - 12mm de altura
        with Locations((0, 0, larg_pista / 2.0 + esp_aba / 2.0)):
            Cylinder(radius=diam_aba / 2.0, height=esp_aba)

        # 4. Alívio côncavo interno do aro
        with Locations((0, 0, 0)):
            Cylinder(radius=(diam_pista - 8.0) / 2.0, height=larg_total + 2.0, mode=Mode.SUBTRACT)

        # 5. Cubo central sólido
        Cylinder(radius=16.0, height=larg_total)

        # 6. 5x Raios estruturais vazados conectando o aro ao cubo central
        with PolarLocations(radius=22.5, count=5):
            Box(17.0, 5.5, larg_total)

        # 7. Rebaixo na face externa para flange de alumínio de 6mm (Ø22mm x 4mm)
        z_face_externa = larg_pista / 2.0 + esp_aba
        with Locations((0, 0, z_face_externa - 2.0)):
            Cylinder(radius=22.0 / 2.0, height=4.2, mode=Mode.SUBTRACT)

        # 8. Furo central do eixo do motor Ø6.5mm
        Cylinder(radius=furo_eixo / 2.0, height=larg_total + 6.0, mode=Mode.SUBTRACT)

        # 9. 4x Furos passantes M3 (Ø3.2mm) para parafusar o flange (PCD 16mm)
        with PolarLocations(radius=16.0 / 2.0, count=4):
            Cylinder(radius=furo_m3 / 2.0, height=larg_total + 6.0, mode=Mode.SUBTRACT)

        # 10. Chanfro interno de 45° (2.0mm) nas bordas das abas para guiar o pneu MTB
        inner_edges = [
            e for e in roda.edges().filter_by(GeomType.CIRCLE)
            if abs(e.radius - diam_aba / 2.0) < 0.2 and abs(abs(e.center().Z) - larg_pista / 2.0) < 0.2
        ]
        if inner_edges:
            chamfer(inner_edges, length=2.0)

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
