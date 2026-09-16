"""
===============================================================================
THE IRON VANGUARD UGV - TAMPA SUPERIOR / CARENAGEM STEALTH
===============================================================================
Componente: Cobertura superior chanfrada militar ("Stealth Hood")
Características:
- Geometria com chanfro perimetral a 45° de proteção contra choques
- Encaixe inferior tipo macho-fêmea perimetral de 2.5mm para vedação estanque na banheira
- Torre FPV frontal integrada no nariz com alojamento para módulo ESP32-CAM e lente OV2640
- Furações laterais com parafusos M3 prateados alinhados aos furos do chassi
Material: PETG Preto Fosco / Texturizado
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_tampa_superior() -> Compound:
    """
    Gera a Carenagem Superior Stealth com torre de câmera frontal integrada.
    A base inferior da tampa coincide com a linha superior da banheira (Z=0 na peça local).
    """
    comp = cfg.CONFIG["COMPRIMENTO_CHASSI"] # 280.0
    larg = cfg.CONFIG["LARGURA_CHASSI"]     # 180.0
    alt = cfg.CONFIG["ALTURA_TAMPA"]        # 26.0
    esp = cfg.CONFIG["ESPESSURA_PAREDE"]    # 3.5
    chanfro_len = 6.0
    h_lip = 3.0

    comp_torre = cfg.CONFIG["COMP_TORRE_CAM"] # 28.0
    larg_torre = cfg.CONFIG["LARG_TORRE_CAM"] # 34.0
    alt_torre = cfg.CONFIG["ALT_TORRE_CAM"]   # 22.0

    pos_x_torre = comp / 2.0 - comp_torre / 2.0 - 10.0
    pos_z_torre = alt + alt_torre / 2.0

    with BuildPart() as tampa:
        # 1. Corpo principal maciço da cobertura (Z de 0 a alt)
        with Locations((0, 0, alt / 2.0)):
            Box(comp, larg, alt)

        # 2. Chanfro perimetral de 45° no teto da tampa
        top_face = tampa.faces().sort_by(Axis.Z)[-1]
        chamfer(top_face.edges(), length=chanfro_len)

        # 3. Encaixe macho inferior contínuo (entra na banheira de Z=-h_lip a 0)
        with Locations((0, 0, -h_lip / 2.0)):
            Box(comp - 2 * esp - 0.6, larg - 2 * esp - 0.6, h_lip)

        # 4. Cavidade interna oca (mantendo teto e paredes de 3.5mm de espessura uniforme)
        h_vazio = alt - esp + h_lip
        with Locations((0, 0, -h_lip + h_vazio / 2.0)):
            Box(comp - 4 * esp, larg - 4 * esp, h_vazio, mode=Mode.SUBTRACT)

        # 5. Torre FPV Frontal Protetora da Câmera integrada no teto
        with Locations((pos_x_torre, 0, pos_z_torre)):
            Box(comp_torre, larg_torre, alt_torre)

        # 6. Alojamento e furos para lente da câmera e parafusos M2
        with Locations((pos_x_torre + comp_torre / 2.0, 0, pos_z_torre)):
            with Locations(Rotation(0, 90, 0)):
                Cylinder(radius=4.8, height=8.0, mode=Mode.SUBTRACT)
                with PolarLocations(radius=10.5, count=2, start_angle=90):
                    Cylinder(radius=1.1, height=6.0, mode=Mode.SUBTRACT)

        # 7. Furos laterais com parafusos M3 ao longo da borda
        for x_furo in [-100.0, -30.0, 40.0, 100.0]:
            for y_sinal in [-1, 1]:
                with Locations((x_furo, y_sinal * (larg / 2.0), 5.0)):
                    with Locations(Rotation(90, 0, 0)):
                        Cylinder(radius=cfg.CONFIG["DIAM_FURO_M3"] / 2.0, height=esp * 4, mode=Mode.SUBTRACT)

    peca_tampa = tampa.part
    peca_tampa.color = Color(cfg.CORES["TAMPA_SUPERIOR"])
    peca_tampa.label = "Carenagem Superior Stealth"

    # Lente de Vidro OV2640 em azul escuro antirreflexo
    with BuildPart() as lente:
        pos_x_lente = pos_x_torre + comp_torre / 2.0 + 0.5
        with Locations((pos_x_lente, 0, pos_z_torre)):
            with Locations(Rotation(0, 90, 0)):
                Cylinder(radius=4.0, height=2.0)
    peca_lente = lente.part
    peca_lente.color = Color(cfg.CORES["LENTE_CAMERA"])
    peca_lente.label = "Lente Câmera OV2640"

    # Parafusos frontais M2 prateados da moldura da câmera
    with BuildPart() as parafusos:
        pos_x_parafuso = pos_x_torre + comp_torre / 2.0 + 0.2
        with Locations((pos_x_parafuso, 0, pos_z_torre)):
            with Locations(Rotation(0, 90, 0)):
                with PolarLocations(radius=10.5, count=2, start_angle=90):
                    Cylinder(radius=1.8, height=1.2)
    peca_parafusos = parafusos.part
    peca_parafusos.color = Color(cfg.CORES["METAL_CROMADO"])
    peca_parafusos.label = "Parafusos Máscara Câmera"

    return Compound(label="Carenagem Superior c/ Torre FPV", children=[peca_tampa, peca_lente, peca_parafusos])

if __name__ == "__main__":
    print("Gerando Carenagem Superior Stealth...")
    t = criar_tampa_superior()
    try:
        from ocp_vscode import show
        show(t, names=["Tampa Superior Stealth"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
