"""
===============================================================================
THE IRON VANGUARD UGV - CHASSI BANHEIRA INFERIOR (PETG)
===============================================================================
Componente: Casco monobloco fechado com glacis frontal a ~45° e grelhas
Características:
- Parede frontal fechada e sólida com rampa a ~45° e espessura uniforme de 3.5mm
- 2x Conjuntos de 5 ranhuras de ventilação frontais paralelas
- Furações laterais traseiras para motores JGB37-520 (gargalo Ø12.5mm + 6x M3 PCD 31mm)
- Furos centrais para eixo M8 de apoio e rasgos oblongos dianteiros de 25mm
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
    Dimensões: 280mm (C) x 180mm (L) x 65mm (A).
    """
    comp = cfg.CONFIG["COMPRIMENTO_CHASSI"] # 280.0
    larg = cfg.CONFIG["LARGURA_CHASSI"]     # 180.0
    alt = cfg.CONFIG["ALTURA_CHASSI"]       # 65.0
    esp = cfg.CONFIG["ESPESSURA_PAREDE"]    # 3.5
    rampa = cfg.CONFIG["COMP_RAMPA_FRONTAL"] # 45.0

    x_motor = cfg.CONFIG["POS_X_MOTOR"]     # -85.0
    x_central = cfg.CONFIG["POS_X_CENTRAL"]   # 0.0
    x_tensora = cfg.CONFIG["POS_X_TENSORA"]   # 85.0
    z_eixo = cfg.CONFIG["POS_Z_EIXOS"]       # -12.0

    diam_passagem_motor = cfg.CONFIG["DIAM_PASSAGEM_MOTOR"] # 12.5
    pcd_motor = cfg.CONFIG["PCD_MOTOR_M3"] # 31.0
    furo_m3 = cfg.CONFIG["DIAM_FURO_M3"]   # 3.2
    furo_m8 = cfg.CONFIG["DIAM_FURO_M8"]   # 8.4
    curso_tensionador = cfg.CONFIG["CURSO_TENSIONADOR"] # 25.0

    with BuildPart() as chassi:
        # 1. Perfil longitudinal externo centrado em Y (extrusão simétrica)
        with BuildSketch(Plane.XZ):
            with BuildLine():
                p_bot_t = (-comp / 2.0, -alt / 2.0)
                p_bot_f = (comp / 2.0 - rampa, -alt / 2.0)
                p_rampa_top = (comp / 2.0, alt / 2.0 - 15.0)
                p_top_f = (comp / 2.0, alt / 2.0)
                p_top_t = (-comp / 2.0, alt / 2.0)
                Polyline(p_bot_t, p_bot_f, p_rampa_top, p_top_f, p_top_t, close=True)
            make_face()
        extrude(amount=larg / 2.0, both=True)

        # 2. Escavação interna paralela mantendo 3.5mm de parede sólida em tudo
        with BuildSketch(Plane.XZ):
            with BuildLine():
                pi_bot_t = (-comp / 2.0 + esp, -alt / 2.0 + esp)
                pi_bot_f = (comp / 2.0 - rampa, -alt / 2.0 + esp)
                pi_rampa_top = (comp / 2.0 - esp, alt / 2.0 - 15.0)
                pi_top_f = (comp / 2.0 - esp, alt / 2.0 + 5.0)
                pi_top_t = (-comp / 2.0 + esp, alt / 2.0 + 5.0)
                Polyline(pi_bot_t, pi_bot_f, pi_rampa_top, pi_top_f, pi_top_t, close=True)
            make_face()
        extrude(amount=(larg - 2 * esp) / 2.0, both=True, mode=Mode.SUBTRACT)

        # 3. Grelhas de ventilação frontais na rampa inclinada
        for y_grelha in [-40.0, 40.0]:
            with Locations((comp / 2.0 - rampa / 2.0 + 6.0, y_grelha, -2.0)):
                with Locations(Rotation(0, -38, 0)):
                    with GridLocations(x_spacing=1.0, y_spacing=6.0, x_count=1, y_count=5):
                        Box(esp * 4, 2.2, 16.0, mode=Mode.SUBTRACT)

        # 4. Reforços e Furações nas paredes laterais (Y = -90 e Y = +90)
        for sinal_y in [-1, 1]:
            y_parede = sinal_y * (larg / 2.0)
            y_parede_int = sinal_y * (larg / 2.0 - esp)

            # Boss circular estrutural na face interna para assentamento rígido do motorredutor (Ø39mm)
            with Locations(Location((x_motor, y_parede_int - sinal_y * 1.0, z_eixo), (90, 0, 0))):
                Cylinder(radius=19.5, height=2.0)

            # Trilhos laterais internos de apoio para a bandeja de eletrônica
            z_trilho = -alt / 2.0 + esp + 2.0
            with Locations((0, y_parede_int - sinal_y * 1.5, z_trilho)):
                Box(160.0, 3.0, 3.0)

            # Furação do motor JGB37-520 (gargalo central Ø12.5mm + 6x M3 PCD 31mm)
            with Locations(Location((x_motor, y_parede, z_eixo), (90, 0, 0))):
                Cylinder(radius=diam_passagem_motor / 2.0, height=esp * 6, mode=Mode.SUBTRACT)
                with PolarLocations(radius=pcd_motor / 2.0, count=6):
                    Cylinder(radius=furo_m3 / 2.0, height=esp * 6, mode=Mode.SUBTRACT)

            # Eixo M8 Central de apoio passante pela parede
            with Locations(Location((x_central, y_parede, z_eixo), (90, 0, 0))):
                Cylinder(radius=furo_m8 / 2.0, height=esp * 6, mode=Mode.SUBTRACT)

            # Rasgo Oblongo Dianteiro M8 (25mm) para tensionamento (corte 3D direto)
            dx_slot = curso_tensionador - furo_m8
            with Locations(Location((x_tensora, y_parede, z_eixo), (90, 0, 0))):
                with Locations((-dx_slot / 2.0, 0, 0), (dx_slot / 2.0, 0, 0)):
                    Cylinder(radius=furo_m8 / 2.0, height=esp * 6, mode=Mode.SUBTRACT)
                Box(dx_slot, furo_m8, esp * 6, mode=Mode.SUBTRACT)

            # Furos para parafusos M3 da tampa superior
            for x_furo in [-100.0, -30.0, 40.0, 100.0]:
                with Locations(Location((x_furo, y_parede, alt / 2.0 - 5.0), (90, 0, 0))):
                    Cylinder(radius=furo_m3 / 2.0, height=esp * 4, mode=Mode.SUBTRACT)

    peca = chassi.part
    peca.color = Color(cfg.CORES["CHASSI_BANHEIRA"])
    peca.label = "Chassi Banheira Fechado"
    return peca

if __name__ == "__main__":
    print("Gerando Chassi Banheira Fechado e Simétrico...")
    c = criar_chassi()
    try:
        from ocp_vscode import show
        show(c, names=["Chassi Banheira Fechado"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
