"""
===============================================================================
ROBÔ DE INSPEÇÃO - CONJUNTO EIXO, ROLAMENTO 608-ZZ E PORCA M8
===============================================================================
Componente: Centro de fixação da roda livre (rolamento 608-ZZ + porca sextavada M8)
Características:
- 2x Rolamentos 608-ZZ embutidos nas cavidades da roda
- Parafuso passante M8 de comprimento compacto (~50mm) sem sobras excessivas
- Porca Nyloc externa com arruela plana alojada dentro do rebaixo do cubo da roda (100% rente, sem ponta saliente)
- Arruela funileiro M8 interna (Ø24mm) encostada na parede interna de PETG
- Porca Nyloc interna compacta rente à parede, deixando o vão interno 100% desobstruído
Material: Aço polido / cromo
===============================================================================
"""

import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_centro_roda_m8() -> Compound:
    """
    Gera o centro de fixação M8 com rolamentos e hardware compacto:
    - 2x Rolamentos 608-ZZ assentados nas cavidades interna e externa da roda
    - Parafuso M8 compacto (comprimento total ~50mm)
    - Porca Nyloc M8 externa com arruela plana embutida no cubo (rente ao aro)
    - Arruela funileiro M8 (Ø24mm) e porca Nyloc M8 interna encostadas na parede do chassi
    """
    diam_arruela = cfg.CONFIG.get("DIAM_ARRUELA_M8", 24.0)   # 24.0mm
    esp_arruela_int = cfg.CONFIG.get("ESP_ARRUELA_M8", 2.0)  # 2.0mm
    larg_pista = cfg.CONFIG["LARGURA_PISTA_RODA"]            # 35.0mm
    esp_aba = cfg.CONFIG.get("ESPESSURA_ABA_RODA", 2.5)      # 2.5mm
    larg_total = larg_pista + 2.0 * esp_aba                  # 40.0mm

    z_face_ext = larg_total / 2.0                            # +20.0mm
    z_face_int = -larg_total / 2.0                           # -20.0mm

    esp_folga_chassi = 1.0                                   # 1.0mm
    esp_parede_chassi = cfg.CONFIG["ESPESSURA_PAREDE"]       # 2.5mm
    alt_porca = 6.0                                          # 6.0mm
    esp_arruela_ext = 1.2                                    # 1.2mm

    # Z do parafuso M8: termina rente à face externa da roda no aro
    z_bolt_max = z_face_ext                                  # +20.0mm
    z_parede_interna = z_face_int - esp_folga_chassi - esp_parede_chassi # -23.5mm
    z_bolt_min = z_parede_interna - esp_arruela_int - alt_porca - 1.0   # -32.5mm
    comp_bolt = z_bolt_max - z_bolt_min                     # 52.5mm

    # 1. Carregamento do Rolamento 608-ZZ
    caminho_step = os.path.join(os.path.dirname(__file__), "..", "modelos_cad", "rolamento_608zz.step")
    rolamento_base = None
    if os.path.exists(caminho_step):
        try:
            rolamento_base = import_step(caminho_step).moved(Rotation(0, 90, 0))
            rolamento_base.color = Color(cfg.CORES["METAL_CROMADO"])
        except Exception:
            rolamento_base = None

    if rolamento_base is None:
        with BuildPart() as b:
            with BuildSketch(Plane.XY):
                Circle(22.0 / 2.0)
                Circle(8.0 / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=7.0)
        rolamento_base = b.part.moved(Location((0, 0, -3.5)))
        rolamento_base.color = Color(cfg.CORES["METAL_CROMADO"])

    # 2 rolamentos: um em cada face da roda
    z_rol_ext = larg_total / 2.0 - 5.0
    z_rol_int = -larg_total / 2.0 + 3.5
    rol_ext = rolamento_base.moved(Location((0, 0, z_rol_ext)))
    rol_ext.label = "Rolamento 608-ZZ Externo"
    rol_int = rolamento_base.moved(Location((0, 0, z_rol_int)))
    rol_int.label = "Rolamento 608-ZZ Interno"

    # 2. Hardware Compacto M8: Arruela e Porca externa, Parafuso, Arruela e Porca interna
    with BuildPart() as hardware:
        # Haste do Parafuso M8 (Ø8.0mm) perfeitamente dimensionada
        with Locations((0, 0, (z_bolt_max + z_bolt_min) / 2.0)):
            Cylinder(radius=4.0, height=comp_bolt)

        # Arruela plana externa M8 (Ø16mm x 1.2mm) alojada no rebaixo
        with Locations((0, 0, z_face_ext - alt_porca - esp_arruela_ext / 2.0)):
            with BuildSketch(Plane.XY):
                Circle(16.0 / 2.0)
                Circle(8.4 / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=esp_arruela_ext / 2.0, both=True)

        # Porca sextavada Nyloc M8 externa alojada no cubo (face externa rente a z_face_ext)
        with Locations((0, 0, z_face_ext - alt_porca / 2.0)):
            with BuildSketch(Plane.XY):
                RegularPolygon(radius=13.0 / math.sqrt(3), side_count=6)
                Circle(8.0 / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=alt_porca / 2.0, both=True)

        # Espaçador entre a roda e a face externa da parede do chassi
        with Locations((0, 0, z_face_int - esp_folga_chassi / 2.0)):
            with BuildSketch(Plane.XY):
                Circle(16.0 / 2.0)
                Circle(8.4 / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=esp_folga_chassi / 2.0, both=True)

        # Arruela funileiro M8 (Ø24mm x 2.0mm) encostada na face interna do chassi
        with Locations((0, 0, z_parede_interna - esp_arruela_int / 2.0)):
            with BuildSketch(Plane.XY):
                Circle(diam_arruela / 2.0)
                Circle(8.4 / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=esp_arruela_int / 2.0, both=True)

        # Porca sextavada Nyloc M8 interna de fixação estrutural
        with Locations((0, 0, z_parede_interna - esp_arruela_int - alt_porca / 2.0)):
            with BuildSketch(Plane.XY):
                RegularPolygon(radius=13.0 / math.sqrt(3), side_count=6)
                Circle(8.0 / 2.0, mode=Mode.SUBTRACT)
            extrude(amount=alt_porca / 2.0, both=True)

    hardware_part = hardware.part
    hardware_part.color = Color(cfg.CORES["ACO_EIXO"])
    hardware_part.label = "Hardware M8 Compacto"

    return Compound(label="Conjunto Eixo M8 Compacto", children=[rol_ext, rol_int, hardware_part])

if __name__ == "__main__":
    print("Gerando Centro de Roda M8 Compacto...")
    c = criar_centro_roda_m8()
    try:
        from ocp_vscode import show
        show(c, names=["Centro M8 Compacto"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
