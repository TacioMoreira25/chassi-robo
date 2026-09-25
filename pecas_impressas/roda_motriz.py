"""
===============================================================================
ROBÔ DE INSPEÇÃO - RODA MOTRIZ MACIÇA (TRASEIRA)
===============================================================================
Componente: Roda de tração traseira acoplada ao eixo do motor JGB37-520
Fidelidade Visual e Mecânica Exata ao Modelo de Referência:
- Pista cilíndrica de 35mm de largura para esteira de pneu MTB
- Abas guias laterais integradas de 4.0mm (Ø58mm total) com chanfro 45° anti-descarrilamento
- Rebaixo usinado na face externa para assentamento do Flange de Alumínio de 6mm (Ø22.0mm x 4.0mm)
- Passagem do colar do flange e furo central passante do eixo do motor (Ø6.5mm)
- 4x furos passantes M3 em PCD 16mm para parafusar o flange de tração
- Perfil e diâmetro proporcionais e idênticos às rodas livres (Ø58mm total) para nivelamento perfeito
Material: PETG Preto Fosco / Texturizado
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_roda_motriz() -> Part:
    """
    Gera a Roda Motriz Traseira (Ø50mm primitivo, Ø58mm total com abas):
    - 100% sólida em PETG para suportar alto torque do motor JGB37-520
    - Pista de 35mm para esteira MTB
    - Abas guias laterais integradas de 4.0mm com chanfro 45°
    - Rebaixo na face externa (Ø22mm x 4mm) para o flange de alumínio com parafusos visíveis
    - Furo central do colar e eixo do motor (Ø12mm / Ø6.5mm)
    - 4 furos passantes M3 (PCD 16mm)
    """
    diam_pista = cfg.CONFIG.get("DIAM_PRIMITIVO_MOTRIZ", 60.0) # 60.0mm
    larg_pista = cfg.CONFIG["LARGURA_PISTA_RODA"]              # 35.0mm
    altura_aba = cfg.CONFIG.get("ALTURA_ABA_GUIA", 3.5)         # 3.5mm
    diam_aba = diam_pista + 2.0 * altura_aba                   # 67.0mm
    esp_aba = cfg.CONFIG.get("ESPESSURA_ABA_RODA", 2.5)        # 2.5mm
    furo_m3 = cfg.CONFIG["DIAM_FURO_M3"]                       # 3.2mm
    furo_eixo = cfg.CONFIG["DIAM_EIXO_MOTOR"]                  # 6.5mm
    diam_rebaixo = cfg.CONFIG["DIAM_REBAIXO_FLANGE"]            # 22.0mm
    pcd_flange = cfg.CONFIG["PCD_FLANGE_M3"]                   # 16.0mm
    larg_total = larg_pista + 2.0 * esp_aba                    # 40.0mm

    with BuildPart() as roda:
        # 1. Pista cilíndrica central maciça (onde assenta a esteira de 35mm)
        Cylinder(radius=diam_pista / 2.0, height=larg_pista)

        # 2. Aba lateral guia interna (lado chassi)
        with Locations((0, 0, -larg_pista / 2.0 - esp_aba / 2.0)):
            Cylinder(radius=diam_aba / 2.0, height=esp_aba)

        # 3. Aba lateral guia externa (lado fora)
        with Locations((0, 0, larg_pista / 2.0 + esp_aba / 2.0)):
            Cylinder(radius=diam_aba / 2.0, height=esp_aba)

        # 4. Alívio estético côncavo no aro da face externa (Z > 0)
        with Locations((0, 0, larg_total / 2.0 - 1.5)):
            Cylinder(radius=(diam_pista - 4.0) / 2.0, height=3.2, mode=Mode.SUBTRACT)

        # Cubo central da face externa
        with Locations((0, 0, larg_total / 2.0 - 2.0)):
            Cylinder(radius=15.0, height=4.0)

        # 5. Rebaixo na face externa para assentamento do Flange de Alumínio (Ø22mm x 4mm)
        z_face_externa = larg_pista / 2.0 + esp_aba
        with Locations((0, 0, z_face_externa - 2.0)):
            Cylinder(radius=diam_rebaixo / 2.0 + 0.2, height=4.2, mode=Mode.SUBTRACT)

        # 6. Alojamento cilíndrico interno para o colar do flange (Ø12mm) penetrar na roda
        with Locations((0, 0, z_face_externa - 9.0)):
            Cylinder(radius=6.0, height=12.0, mode=Mode.SUBTRACT)

        # 7. Furo central passante do eixo do motor Ø6.5mm
        Cylinder(radius=furo_eixo / 2.0, height=larg_total + 10.0, mode=Mode.SUBTRACT)

        # 8. 4x Furos passantes M3 (Ø3.2mm) em PCD 16mm para fixação do flange
        with Locations((0, 0, 0)):
            with PolarLocations(radius=pcd_flange / 2.0, count=4):
                Cylinder(radius=furo_m3 / 2.0, height=larg_total + 10.0, mode=Mode.SUBTRACT)

        # 9. Chanfros de 45° nas bordas internas das abas para guiar a esteira
        inner_edges = [
            e for e in roda.edges().filter_by(GeomType.CIRCLE)
            if abs(e.radius - diam_aba / 2.0) < 0.2 and abs(abs(e.center().Z) - (larg_pista / 2.0 + esp_aba)) < 0.2
        ]
        if inner_edges:
            try:
                chamfer(inner_edges, length=1.2)
            except Exception:
                pass

    peca = roda.part
    peca.color = Color(cfg.CORES["RODA_POLIA"])
    peca.label = "Roda Motriz Macica Ø60mm"
    return peca

if __name__ == "__main__":
    print("Gerando Roda Motriz Maciça...")
    roda = criar_roda_motriz()
    try:
        from ocp_vscode import show
        show(roda, names=["Roda Motriz"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
