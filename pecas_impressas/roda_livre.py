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

def criar_roda_livre(com_abas: bool = True) -> Part:
    """
    Gera a Roda Livre Côncava (Deep Dish).
    - com_abas=True: Roda Tensora Dianteira com abas duplas de 12mm e chanfros 45° anti-descarrilamento.
    - com_abas=False: Roda Central de Apoio lisa (sem abas altas para não colidir com rodas vizinhas).
    """
    diam_pista = cfg.CONFIG["DIAM_PISTA_RODA"]
    larg_pista = cfg.CONFIG["LARGURA_PISTA_RODA"]
    diam_aba = cfg.CONFIG["DIAM_ABA_GUIA"]       # 92mm (12mm acima da pista)
    esp_aba = cfg.CONFIG["ESPESSURA_ABA_RODA"]   # 3.5mm
    larg_total = larg_pista + 2.0 * esp_aba     # 42mm total
    furo_608 = cfg.CONFIG["DIAM_EXT_ROLAMENTO_608"] # 22.18mm (+0.18mm para prensa justa)
    furo_m8 = cfg.CONFIG["DIAM_FURO_M8"]         # 8.4mm passante

    with BuildPart() as roda:
        if com_abas:
            # 1. Pista cilíndrica central da roda (35mm)
            Cylinder(radius=diam_pista / 2.0, height=larg_pista)

            # 2. Aba lateral guia interna (12mm de altura)
            with Locations((0, 0, -larg_pista / 2.0 - esp_aba / 2.0)):
                Cylinder(radius=diam_aba / 2.0, height=esp_aba)

            # 3. Aba lateral guia externa (12mm de altura)
            with Locations((0, 0, larg_pista / 2.0 + esp_aba / 2.0)):
                Cylinder(radius=diam_aba / 2.0, height=esp_aba)

            # 4. Rebaixo côncavo frontal (deep dish) criando a borda da roda
            with Locations((0, 0, 4.0)):
                Cylinder(radius=(diam_pista - 7.0) / 2.0, height=larg_total, mode=Mode.SUBTRACT)

            # 5. Cubo central cilíndrico
            Cylinder(radius=15.0, height=larg_total)

            # 6. Alojamento frontal para rolamento 608-ZZ (Ø22.18mm x 7.2mm)
            z_max = larg_total / 2.0
            with Locations((0, 0, z_max - 3.6)):
                Cylinder(radius=furo_608 / 2.0, height=7.2, mode=Mode.SUBTRACT)

            # 7. Alojamento traseiro para rolamento 608-ZZ (Ø22.18mm x 7.2mm)
            with Locations((0, 0, -z_max + 3.6)):
                Cylinder(radius=furo_608 / 2.0, height=7.2, mode=Mode.SUBTRACT)

            # 8. Furo central passante M8 (Ø8.4mm)
            Cylinder(radius=furo_m8 / 2.0, height=larg_total + 10.0, mode=Mode.SUBTRACT)

            # 9. Chanfro interno de 45° (2.0mm) nas bordas das abas
            inner_edges = [
                e for e in roda.edges().filter_by(GeomType.CIRCLE)
                if abs(e.radius - diam_aba / 2.0) < 0.2 and abs(abs(e.center().Z) - larg_pista / 2.0) < 0.2
            ]
            if inner_edges:
                chamfer(inner_edges, length=2.0)
        else:
            # Roda intermediária lisa de apoio (sem abas altas)
            Cylinder(radius=diam_pista / 2.0, height=larg_total)

            # Rebaixo côncavo frontal
            with Locations((0, 0, 4.0)):
                Cylinder(radius=(diam_pista - 7.0) / 2.0, height=larg_total, mode=Mode.SUBTRACT)

            # Cubo central
            Cylinder(radius=15.0, height=larg_total)

            # Alojamentos de rolamento 608-ZZ (Ø22.18mm x 7.2mm)
            z_max = larg_total / 2.0
            with Locations((0, 0, z_max - 3.6)):
                Cylinder(radius=furo_608 / 2.0, height=7.2, mode=Mode.SUBTRACT)
            with Locations((0, 0, -z_max + 3.6)):
                Cylinder(radius=furo_608 / 2.0, height=7.2, mode=Mode.SUBTRACT)

            # Furo passante M8 (Ø8.4mm)
            Cylinder(radius=furo_m8 / 2.0, height=larg_total + 10.0, mode=Mode.SUBTRACT)

    peca = roda.part
    peca.color = Color(cfg.CORES["RODA_POLIA"])
    peca.label = "Roda Livre Tensora" if com_abas else "Roda Livre Central Apoio"
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
