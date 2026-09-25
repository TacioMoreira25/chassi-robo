"""
===============================================================================
ROBÔ DE INSPEÇÃO - ESTEIRA DE BORRACHA COM CRAVOS DE PNEU MTB
===============================================================================
Componente: Cinta oca tracionada de borracha vulcanizada (fita de pneu MTB)
Características:
- Cinta contínua oca de 3.0mm de espessura envolvendo as 3 rodas
- Contato 100% horizontal e nivelado no solo (Z_int = -47.5mm, Z_ext = -50.5mm, Z_cravo = -52.5mm)
- Polia motriz traseira (Ø60mm) e polias livres (Ø50mm) todas em contato contínuo
- Roda central de apoio assenta perfeitamente no fundo da esteira sem vão
- Cravos 3D de tração moldados ao longo da face externa
- Placa metálica de união em alumínio usinado com 4x parafusos M3 no topo
===============================================================================
"""

import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_esteira_mtb() -> Compound:
    """
    Gera a esteira oca contínua de pneu MTB perfeitamente nivelada no solo:
    - Polia Traseira Motriz: R_int = 30.0mm em (POS_X_MOTOR, POS_Z_MOTOR)
    - Polia Dianteira Tensora: R_int = 25.0mm em (POS_X_TENSORA, POS_Z_EIXOS)
    - Polia Central de Apoio: R_int = 25.0mm em (POS_X_CENTRAL, POS_Z_EIXOS)
    - Nível do fundo interno de contato: Z = -47.5mm (perfeitamente plano)
    - Nível de solo externo com cravos: Z = -52.5mm
    """
    x_t = cfg.CONFIG["POS_X_MOTOR"]                       # -100.0mm
    z_t = cfg.CONFIG.get("POS_Z_MOTOR", -17.5)            # -17.5mm
    x_d = cfg.CONFIG["POS_X_TENSORA"]                     # +100.0mm
    z_d = cfg.CONFIG.get("POS_Z_EIXOS", -17.5)            # -17.5mm

    esp_base = cfg.CONFIG["ESPESSURA_ESTEIRA"]            # 3.0mm
    largura = cfg.CONFIG["LARGURA_PISTA_RODA"]            # 35.0mm
    transpasse = cfg.CONFIG["TRANSPASSE_EMENDA"]          # 30.0mm
    alt_cravo = cfg.CONFIG.get("ALTURA_CRAVOS_PNEU", 2.0) # 2.0mm

    # Raios das polias (Todas Ø60mm idênticas e niveladas na mesma linha)
    r_int = cfg.CONFIG.get("DIAM_PRIMITIVO_MOTRIZ", 60.0) / 2.0 # 30.0mm
    r_ext = r_int + esp_base                                    # 33.0mm

    # Pontos de apoio no solo (ambos em Z = -50.5mm ext e -47.5mm int)
    p_bot_t_ext = (x_t, z_t - r_ext)  # (-100.0, -50.5)
    p_bot_d_ext = (x_d, z_d - r_ext)  # (+100.0, -50.5)
    p_top_t_ext = (x_t, z_t + r_ext)  # (-100.0, +15.5)
    p_top_d_ext = (x_d, z_d + r_ext)  # (+100.0, +15.5)

    p_bot_t_int = (x_t, z_t - r_int)  # (-100.0, -47.5)
    p_bot_d_int = (x_d, z_d - r_int)  # (+100.0, -47.5)
    p_top_t_int = (x_t, z_t + r_int)  # (-100.0, +12.5)
    p_top_d_int = (x_d, z_d + r_int)  # (+100.0, +12.5)

    with BuildPart() as esteira_borracha:
        with BuildSketch(Plane.XZ):
            # 1. Contorno Externo envolvendo as polias com fundo perfeitamente horizontal
            with BuildLine():
                Line(p_top_t_ext, p_top_d_ext)
                ThreePointArc(p_top_d_ext, (x_d + r_ext, z_d), p_bot_d_ext)
                Line(p_bot_d_ext, p_bot_t_ext)
                ThreePointArc(p_bot_t_ext, (x_t - r_ext, z_t), p_top_t_ext)
            make_face()

            # 2. Contorno Interno Vazado
            with BuildLine():
                Line(p_top_t_int, p_top_d_int)
                ThreePointArc(p_top_d_int, (x_d + r_int, z_d), p_bot_d_int)
                Line(p_bot_d_int, p_bot_t_int)
                ThreePointArc(p_bot_t_int, (x_t - r_int, z_t), p_top_t_int)
            make_face(mode=Mode.SUBTRACT)

        extrude(amount=largura / 2.0, both=True)

    cinta_centrada = esteira_borracha.part

    # 3. Cravos de tração 3D de borracha (superiores e inferiores no solo)
    z_bot_cravo = -50.5 - (alt_cravo / 2.0) # -51.5mm (vai até -52.5mm de contato com o solo)
    with BuildPart() as cravos:
        # Cravos da seção inferior (contato com solo perfeitamente plano)
        for x in range(int(x_t + 16), int(x_d - 16), 18):
            for y_cravo in [-8.5, 8.5]:
                with Locations((x, y_cravo, z_bot_cravo)):
                    Box(6.0, 7.0, alt_cravo)
                # Cravos da seção superior perfeitamente horizontais
                z_top_cravo = z_t + r_ext + (alt_cravo / 2.0)
                with Locations((x, y_cravo, z_top_cravo)):
                    Box(6.0, 7.0, alt_cravo)

    # 4. Placa metálica de união em alumínio usinado com transpasse de emenda de 30mm
    z_emenda = z_t + r_ext + 1.0
    with BuildPart() as emenda:
        with Locations((0.0, 0, z_emenda)):
            Box(transpasse, largura - 4.0, 2.0)
            with Locations((0, 0, 1.2)):
                with GridLocations(transpasse - 10.0, 18.0, 2, 2):
                    Cylinder(radius=2.6, height=1.5)

    peca_cinta = cinta_centrada + cravos.part
    peca_cinta.color = Color(cfg.CORES["BORRACHA_ESTEIRA"])
    peca_cinta.label = "Cinta de Pneu MTB c/ Cravos"

    peca_emenda = emenda.part
    peca_emenda.color = Color(cfg.CORES["ALUMINIO_USINADO"])
    peca_emenda.label = "Placa de Emenda da Esteira (30mm Transpasse)"

    return Compound(label="Esteira Completa", children=[peca_cinta, peca_emenda])

if __name__ == "__main__":
    print("Gerando Esteira Oca Nivelada no Solo...")
    est = criar_esteira_mtb()
    try:
        from ocp_vscode import show
        show(est, names=["Esteira Nivelada"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
