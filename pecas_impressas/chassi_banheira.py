"""
===============================================================================
ROBÔ DE INSPEÇÃO - CHASSI BANHEIRA INFERIOR (PETG)
===============================================================================
Componente: Casco monobloco fechado com glacis frontal a ~45°, cantos inferiores arredondados e grelhas
Características:
- Parede frontal fechada e sólida com rampa a ~45° e espessura uniforme de 2.5mm
- Filete suave (R4mm) nos cantos inferiores externos para absorção de impactos
- 2x Conjuntos de 5 ranhuras de ventilação frontais paralelas no glacis
- Aletas defletoras traseiras inclinadas para baixo (louvered vents) para exaustão passiva
- Furações laterais traseiras para motores JGB37-520 (gargalo Ø12.5mm + 6x M3 PCD 31mm)
- Furos centrais para eixo M8 de apoio e rasgos oblongos dianteiros de 25mm para tensionador
- Furos laterais para fixação roscada M3 da tampa superior
Material: PETG Preto Fosco / Texturizado
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_chassi() -> Part:
    """
    Gera o chassi banheira inferior perfeitamente centrado na origem (0, 0, 0).
    Dimensões definitivas: 240mm (C) x 160mm (L) x 75mm (A) com parede uniforme de 2.5mm em PETG.
    """
    comp = cfg.CONFIG["COMPRIMENTO_CHASSI"] # 240.0
    larg = cfg.CONFIG["LARGURA_CHASSI"]     # 160.0
    alt = cfg.CONFIG["ALTURA_CHASSI"]       # 75.0
    esp = cfg.CONFIG["ESPESSURA_PAREDE"]    # 2.5
    rampa = cfg.CONFIG["COMP_RAMPA_FRONTAL"] # 40.0

    x_motor = cfg.CONFIG["POS_X_MOTOR"]     # -85.0
    x_central = cfg.CONFIG["POS_X_CENTRAL"]   # 0.0
    x_tensora = cfg.CONFIG["POS_X_TENSORA"]   # 85.0
    z_motor = cfg.CONFIG.get("POS_Z_MOTOR", -17.5) # -17.5mm
    z_eixo = cfg.CONFIG.get("POS_Z_EIXOS", -17.5)  # -17.5mm (mesma linha de centro)

    diam_passagem_motor = cfg.CONFIG["DIAM_PASSAGEM_MOTOR"] # 12.5
    pcd_motor = cfg.CONFIG["PCD_MOTOR_M3"] # 31.0
    furo_m3 = cfg.CONFIG["DIAM_FURO_M3"]   # 3.2
    furo_m8 = cfg.CONFIG["DIAM_FURO_M8"]   # 8.4
    curso_tensionador = cfg.CONFIG["CURSO_TENSIONADOR"] # 25.0

    with BuildPart() as chassi:
        # 1. Perfil longitudinal externo com glacis inclinado e base perfeitamente plana
        with BuildSketch(Plane.XZ):
            with BuildLine():
                p_bot_t = (-comp / 2.0, -alt / 2.0)
                p_bot_f = (comp / 2.0 - rampa, -alt / 2.0)
                p_top_f = (comp / 2.0, alt / 2.0)
                p_top_t = (-comp / 2.0, alt / 2.0)
                Polyline(p_bot_t, p_bot_f, p_top_f, p_top_t, close=True)
            make_face()
        extrude(amount=larg / 2.0, both=True)

        # Filete suave nos cantos inferiores externos
        bottom_edges = [e for e in chassi.edges() if e.center().Z < -alt / 2.0 + 1.0]
        try:
            fillet(bottom_edges, radius=cfg.CONFIG.get("RAIO_CANTO_INFERIOR", 4.0))
        except Exception:
            pass

        # 2. Escavação interna paralela de precisão (espessura uniforme de 2.5mm sem artefatos)
        slope = alt / rampa # 75.0 / 40.0 = 1.875
        x_corner_int = (comp / 2.0 - esp) - (alt - esp) / slope
        with BuildSketch(Plane.XZ):
            with BuildLine():
                pi_bot_t = (-comp / 2.0 + esp, -alt / 2.0 + esp)
                pi_bot_f = (x_corner_int, -alt / 2.0 + esp)
                pi_top_f = (comp / 2.0 - esp, alt / 2.0 + 5.0)
                pi_top_t = (-comp / 2.0 + esp, alt / 2.0 + 5.0)
                Polyline(pi_bot_t, pi_bot_f, pi_top_f, pi_top_t, close=True)
            make_face()
        extrude(amount=(larg - 2 * esp) / 2.0, both=True, mode=Mode.SUBTRACT)

        # 3. Grelhas de ventilação frontais na rampa inclinada do glacis
        for y_grelha in [-35.0, 35.0]:
            with Locations((comp / 2.0 - rampa / 2.0, y_grelha, 0.0)):
                with Locations(Rotation(0, -28.0, 0)):
                    with GridLocations(x_spacing=1.0, y_spacing=5.5, x_count=1, y_count=5):
                        Box(esp * 4, 2.0, 14.0, mode=Mode.SUBTRACT)

        # 4. Aletas defletoras traseiras inclinadas para baixo a 30° (louvered vents)
        for y_aleta in [-35.0, 35.0]:
            with Locations((-comp / 2.0, y_aleta, 15.0)):
                with Locations(Rotation(0, 30.0, 0)):
                    with GridLocations(x_spacing=1.0, y_spacing=6.0, x_count=1, y_count=4):
                        Box(esp * 4, 2.2, 16.0, mode=Mode.SUBTRACT)

        # 5. Reforços e Furações funcionais nas paredes laterais (Y = -80 e Y = +80)
        for sinal_y in [-1, 1]:
            y_parede = sinal_y * (larg / 2.0)
            y_parede_int = sinal_y * (larg / 2.0 - esp)

            # Boss circular estrutural na face interna para assentamento do motorredutor (Ø39mm)
            with Locations(Location((x_motor, y_parede_int - sinal_y * 1.0, z_motor), (90, 0, 0))):
                Cylinder(radius=19.5, height=2.0)

            # Trilhos laterais internos de apoio para a bandeja de eletrônica
            z_trilho = -alt / 2.0 + esp + 2.0
            with Locations((0, y_parede_int - sinal_y * 1.5, z_trilho)):
                Box(140.0, 3.0, 3.0)

            # Furação do motorredutor JGB37-520 (gargalo central Ø12.5mm + 6x M3 PCD 31mm)
            with Locations(Location((x_motor, y_parede, z_motor), (90, 0, 0))):
                Cylinder(radius=diam_passagem_motor / 2.0, height=esp * 6, mode=Mode.SUBTRACT)
                with PolarLocations(radius=pcd_motor / 2.0, count=6):
                    Cylinder(radius=furo_m3 / 2.0, height=esp * 6, mode=Mode.SUBTRACT)

            # Eixo M8 Central de apoio passante pela parede
            with Locations(Location((x_central, y_parede, z_eixo), (90, 0, 0))):
                Cylinder(radius=furo_m8 / 2.0, height=esp * 6, mode=Mode.SUBTRACT)

            # Rasgo Oblongo Dianteiro M8 (25mm x 8.4mm) para tensionamento na mesma linha de centro
            dx_slot = curso_tensionador - furo_m8
            with Locations(Location((x_tensora, y_parede, z_eixo), (90, 0, 0))):
                with Locations((-dx_slot / 2.0, 0, 0), (dx_slot / 2.0, 0, 0)):
                    Cylinder(radius=furo_m8 / 2.0, height=esp * 6, mode=Mode.SUBTRACT)
                Box(dx_slot, furo_m8, esp * 6, mode=Mode.SUBTRACT)

            # Furos circulares de Ø12.0mm para passa-cabos de borracha (grommets)
            diam_grommet = cfg.CONFIG.get("DIAM_PASSAGEM_GROMMET", 12.0)
            for x_grommet in [-45.0, 45.0]:
                with Locations(Location((x_grommet, y_parede, 10.0), (90, 0, 0))):
                    Cylinder(radius=diam_grommet / 2.0, height=esp * 6, mode=Mode.SUBTRACT)

            # Furos para parafusos M3 de fixação da tampa superior ao longo da borda
            for x_furo in [-85.0, -25.0, 25.0, 85.0]:
                with Locations(Location((x_furo, y_parede, alt / 2.0 - 5.0), (90, 0, 0))):
                    Cylinder(radius=furo_m3 / 2.0, height=esp * 4, mode=Mode.SUBTRACT)

    peca = chassi.part
    peca.color = Color(cfg.CORES["CHASSI_BANHEIRA"])
    peca.label = "Chassi Banheira (Robô de Inspeção)"
    return peca

if __name__ == "__main__":
    print("Gerando Chassi Banheira (Robô de Inspeção)...")
    c = criar_chassi()
    try:
        from ocp_vscode import show
        show(c, names=["Chassi Banheira (Robô de Inspeção)"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")

