"""
===============================================================================
THE IRON VANGUARD UGV - RODA LIVRE CÔNCAVA (DEEP DISH)
===============================================================================
Componente: Roda livre intermediária e dianteira com aro profundo
Características:
- Perfil côncavo tipo copo (deep dish) exatamente como no UGV real
- Pista larga de 35mm para assentamento da fita de pneu MTB
- Aba interna alta anti-descarrilamento
- Alojamento duplo para 2x Rolamentos 608-ZZ (ajuste sob pressão Ø22.18mm)
- Furo passante M8 para parafuso/eixo morto
Material: PETG Preto Fosco
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_roda_livre() -> Part:
    """
    Gera a Roda Livre com perfil côncavo realista.
    """
    diam_pista = cfg.CONFIG["DIAM_PISTA_RODA"]
    larg_pista = cfg.CONFIG["LARGURA_PISTA_RODA"]
    diam_aba = cfg.CONFIG["DIAM_ABA_GUIA"]
    esp_aba = cfg.CONFIG["ESPESSURA_ABA_RODA"]
    furo_608 = cfg.CONFIG["FOLGA_ROLAMENTO_608"] + 22.0
    furo_m8 = cfg.CONFIG["DIAM_FURO_M8"]

    with BuildPart() as roda:
        # 1. Pista cilíndrica da roda (onde a esteira de borracha apoia)
        Cylinder(radius=diam_pista / 2.0, height=larg_pista)

        # 2. Aba lateral guia interna (lado chassi) para impedir a esteira de entrar
        with Locations((0, 0, -larg_pista / 2.0 + esp_aba / 2.0)):
            Cylinder(radius=diam_aba / 2.0, height=esp_aba)

        # 3. Rebaixo côncavo frontal (deep dish) criando a borda da roda
        with Locations((0, 0, 4.0)):
            Cylinder(radius=(diam_pista - 7.0) / 2.0, height=larg_pista, mode=Mode.SUBTRACT)

        # 4. Cubo central cilíndrico
        Cylinder(radius=15.0, height=larg_pista)

        # 5. Alojamento frontal para rolamento 608-ZZ (Ø22.18mm x 7.1mm)
        with Locations((0, 0, larg_pista / 2.0 - 3.5)):
            Cylinder(radius=furo_608 / 2.0, height=7.2, mode=Mode.SUBTRACT)

        # 6. Alojamento traseiro para rolamento 608-ZZ (Ø22.18mm x 7.1mm)
        with Locations((0, 0, -larg_pista / 2.0 + 3.5)):
            Cylinder(radius=furo_608 / 2.0, height=7.2, mode=Mode.SUBTRACT)

        # 7. Furo central passante M8
        Cylinder(radius=furo_m8 / 2.0, height=larg_pista + 6.0, mode=Mode.SUBTRACT)

        # 8. Chanfros de acabamento nas bordas
        circulos = roda.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)
        if len(circulos) >= 2:
            chamfer(circulos[-1], length=1.5)

    peca = roda.part
    peca.color = Color(cfg.CORES["RODA_POLIA"])
    peca.label = "Roda Livre Côncava (Deep Dish)"
    return peca

if __name__ == "__main__":
    print("Gerando Roda Livre Côncava...")
    roda = criar_roda_livre()
    try:
        from ocp_vscode import show
        show(roda, names=["Roda Livre Côncava"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
