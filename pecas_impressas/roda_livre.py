"""
===============================================================================
ROBÔ DE INSPEÇÃO - RODA LIVRE CÔNCAVA (DEEP DISH)
===============================================================================
Componente: Roda livre intermediária e dianteira com aro profundo
Características:
- Perfil côncavo tipo copo (deep dish) exatamente como no robô real
- Pista larga de 35mm para assentamento da fita de pneu MTB
- Aba interna alta anti-descarrilamento de 12mm
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
    Gera a Roda Livre Côncava (Deep Dish) de Ø50mm:
    - Cavidade usinada de Ø22.18mm em ambas as faces para prensar 2x rolamentos 608-ZZ por roda.
    - Abas duplas integradas de 4.0mm (Ø58mm total) com chanfro 45° anti-descarrilamento.
    - Furo passante M8 (Ø8.4mm) para barra roscada.
    - Perfil côncavo esportivo/militar (deep dish).
    """
    diam_pista = cfg.CONFIG["DIAM_POLIA_LIVRE"]     # 50.0mm
    larg_pista = cfg.CONFIG["LARGURA_PISTA_RODA"]   # 35.0mm
    altura_aba = cfg.CONFIG.get("ALTURA_ABA_GUIA", 3.5) # 3.5mm
    diam_aba = diam_pista + 2.0 * altura_aba        # 67.0mm
    esp_aba = cfg.CONFIG.get("ESPESSURA_ABA_RODA", 2.5) # 2.5mm
    larg_total = larg_pista + 2.0 * esp_aba         # 40.0mm
    furo_608 = cfg.CONFIG["DIAM_EXT_ROLAMENTO_608"] # 22.18mm
    furo_m8 = cfg.CONFIG["DIAM_FURO_M8"]            # 8.4mm

    with BuildPart() as roda:
        # 1. Pista cilíndrica central da roda (onde assenta a esteira de 35mm)
        Cylinder(radius=diam_pista / 2.0, height=larg_pista)

        # 2. Aba lateral guia interna
        with Locations((0, 0, -larg_pista / 2.0 - esp_aba / 2.0)):
            Cylinder(radius=diam_aba / 2.0, height=esp_aba)

        # 3. Aba lateral guia externa
        with Locations((0, 0, larg_pista / 2.0 + esp_aba / 2.0)):
            Cylinder(radius=diam_aba / 2.0, height=esp_aba)

        # 4. Rebaixo côncavo frontal (deep dish) criando o aro estético e alívio de peso
        with Locations((0, 0, 3.0)):
            Cylinder(radius=(diam_pista - 6.0) / 2.0, height=larg_total, mode=Mode.SUBTRACT)

        # 5. Cubo central cilíndrico
        Cylinder(radius=15.0, height=larg_total)

        # 6. Alojamento frontal para 1º rolamento 608-ZZ (Ø22.18mm x 7.2mm de profundidade)
        z_max = larg_total / 2.0
        with Locations((0, 0, z_max - 3.6)):
            Cylinder(radius=furo_608 / 2.0, height=7.3, mode=Mode.SUBTRACT)

        # 7. Alojamento traseiro para 2º rolamento 608-ZZ (Ø22.18mm x 7.2mm de profundidade)
        with Locations((0, 0, -z_max + 3.6)):
            Cylinder(radius=furo_608 / 2.0, height=7.3, mode=Mode.SUBTRACT)

        # 8. Furo central passante M8 (Ø8.4mm) ligando os dois alojamentos
        Cylinder(radius=furo_m8 / 2.0, height=larg_total + 10.0, mode=Mode.SUBTRACT)

        # 9. Chanfros de 45° nas bordas das abas para guiar o pneu MTB
        inner_edges = [
            e for e in roda.edges().filter_by(GeomType.CIRCLE)
            if abs(e.radius - diam_aba / 2.0) < 0.2 and abs(abs(e.center().Z) - (larg_pista / 2.0 + esp_aba)) < 0.2
        ]
        if inner_edges:
            try:
                chamfer(inner_edges, length=1.5)
            except Exception:
                pass

    peca = roda.part
    peca.color = Color(cfg.CORES["RODA_POLIA"])
    peca.label = "Roda Livre Côncava Ø50mm (2x 608-ZZ)"
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
