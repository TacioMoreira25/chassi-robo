"""
===============================================================================
THE IRON VANGUARD UGV - ESTEIRA DE BORRACHA COM CRAVOS DE PNEU MTB
===============================================================================
Componente: Cinta oca tracionada de borracha vulcanizada (fita de pneu MTB)
Características:
- Geometria de cinta oca verdadeira de 3.0mm de espessura que envolve as 3 rodas
- Perfeitamente centrada no eixo Y (-17.5mm a +17.5mm) com 35mm de largura útil
- Cravos de tração em relevo 3D na face externa superior e inferior
- Placa metálica de união em alumínio usinado com 4x parafusos M3 no topo
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_esteira_mtb() -> Compound:
    """
    Gera a esteira oca contínua de pneu MTB perfeitamente centrada em Y=0.
    """
    x_t = cfg.CONFIG["POS_X_MOTOR"]     # -85.0
    x_d = cfg.CONFIG["POS_X_TENSORA"]   # +85.0
    z_eixo = cfg.CONFIG["POS_Z_EIXOS"]   # -12.0
    r_int = cfg.CONFIG["DIAM_PISTA_RODA"] / 2.0 # 34.0
    esp_base = cfg.CONFIG["ESPESSURA_ESTEIRA"]  # 3.0
    r_ext = r_int + esp_base                    # 37.0
    largura = cfg.CONFIG["LARGURA_PISTA_RODA"]  # 35.0

    # 1. Cinta oca de borracha (perfil fechado e vazado no plano XZ)
    with BuildPart() as esteira_borracha:
        with BuildSketch(Plane.XZ):
            # Contorno Externo
            with BuildLine():
                l1 = Line((x_t, z_eixo - r_ext), (x_d, z_eixo - r_ext))
                a1 = TangentArc(l1@1, (x_d + r_ext, z_eixo), tangent=(1, 0))
                a2 = TangentArc(a1@1, (x_d, z_eixo + r_ext), tangent=(0, 1))
                l2 = Line(a2@1, (x_t, z_eixo + r_ext))
                a3 = TangentArc(l2@1, (x_t - r_ext, z_eixo), tangent=(-1, 0))
                a4 = TangentArc(a3@1, l1@0, tangent=(0, -1))
            make_face()
            # Contorno Interno (subtração para criar a fita oca contínua)
            with BuildLine():
                l3 = Line((x_t, z_eixo - r_int), (x_d, z_eixo - r_int))
                a5 = TangentArc(l3@1, (x_d + r_int, z_eixo), tangent=(1, 0))
                a6 = TangentArc(a5@1, (x_d, z_eixo + r_int), tangent=(0, 1))
                l4 = Line(a6@1, (x_t, z_eixo + r_int))
                a7 = TangentArc(l4@1, (x_t - r_int, z_eixo), tangent=(-1, 0))
                a8 = TangentArc(a7@1, l3@0, tangent=(0, -1))
            make_face(mode=Mode.SUBTRACT)
        extrude(amount=largura / 2.0, both=True)

    cinta_centrada = esteira_borracha.part

    # 2. Cravos de tração 3D de borracha centrados em Y=0
    with BuildPart() as cravos:
        z_top = z_eixo + r_ext + 1.2
        z_bot = z_eixo - r_ext - 1.2
        for x in range(int(x_t + 12), int(x_d - 12), 16):
            for y_cravo in [-9.0, 9.0]:
                with Locations((x, y_cravo, z_top)):
                    Box(6.0, 7.0, 2.4)
                with Locations((x, y_cravo, z_bot)):
                    Box(6.0, 7.0, 2.4)

    # 3. Placa metálica de união em alumínio centrada em Y=0
    with BuildPart() as emenda:
        pos_x_emenda = 15.0
        z_emenda = z_eixo + r_ext + 0.9
        with Locations((pos_x_emenda, 0, z_emenda)):
            Box(28.0, largura - 4.0, 1.8)
            with Locations((0, 0, 1.0)):
                with GridLocations(18.0, 18.0, 2, 2):
                    Cylinder(radius=2.6, height=1.5)

    peca_cinta = cinta_centrada + cravos.part
    peca_cinta.color = Color(cfg.CORES["BORRACHA_ESTEIRA"])
    peca_cinta.label = "Cinta de Pneu MTB c/ Cravos"

    peca_emenda = emenda.part
    peca_emenda.color = Color(cfg.CORES["ALUMINIO_USINADO"])
    peca_emenda.label = "Placa de Emenda da Esteira"

    return Compound(label="Esteira Completa", children=[peca_cinta, peca_emenda])

if __name__ == "__main__":
    print("Gerando Esteira Oca Centrada...")
    est = criar_esteira_mtb()
    try:
        from ocp_vscode import show
        show(est, names=["Esteira Centrada"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
