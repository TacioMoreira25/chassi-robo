"""
===============================================================================
ROBÔ DE INSPEÇÃO - MÓDULOS E CIRCUITOS ELETRÔNICOS
===============================================================================
Modelagem visual didática dos componentes do subsistema eletrônico:
1. Driver Ponte H L298N (Módulo de Potência para os Motores 12V)
2. Conversor DC-DC Step-Down LM2596 (Regulação de precisão 12V -> 5V)
3. Módulo ESP32-CAM (Cérebro computacional com Câmera OV2640 e Wi-Fi)
4. Pack de Baterias 3S Li-Ion 18650 (Fonte Primária de Energia 11.1V ~ 12.6V)
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_ponte_h_l298n():
    """
    Gera a placa Driver Ponte H L298N integrando o arquivo oficial em modelos_cad.
    """
    caminho_step = os.path.join(os.path.dirname(__file__), "..", "modelos_cad", "ponte_h_l298n.step")
    if not os.path.exists(caminho_step):
        caminho_step = os.path.join(os.path.dirname(__file__), "..", "L298N Motor Driver.STEP")
    if os.path.exists(caminho_step):
        try:
            peca = import_step(caminho_step).moved(Rotation(90, 0, 0))
            z_min = peca.bounding_box().min.Z
            peca = peca.moved(Location((0, 0, -z_min)))
            peca.color = Color(cfg.CORES["PCB_L298N"])
            peca.label = "Ponte H L298N (STEP Oficial)"
            return peca
        except Exception:
            pass

    # Fallback sintetizado
    with BuildPart() as pcb:
        Box(43.0, 43.0, 1.6)
        with Locations((0, 0, 0)):
            with GridLocations(43.0, 43.0, 2, 2):
                Cylinder(radius=3.2 / 2.0, height=5.0, mode=Mode.SUBTRACT)
    pcb_part = pcb.part
    pcb_part.color = Color(cfg.CORES["PCB_L298N"])

    with BuildPart() as dissipador:
        with Locations((0, 0, 12.5 + 0.8)):
            Box(25.0, 14.0, 25.0)
    diss_part = dissipador.part
    diss_part.color = Color("#212121")

    with BuildPart() as bornes:
        with Locations((0, 17.0, 5.0)):
            Box(30.0, 8.0, 10.0)
        with Locations((-17.0, 0, 5.0)):
            Box(8.0, 20.0, 10.0)
        with Locations((17.0, 0, 5.0)):
            Box(8.0, 20.0, 10.0)
    bornes_part = bornes.part
    bornes_part.color = Color("#1976D2")

    return Compound(label="Ponte H L298N", children=[pcb_part, diss_part, bornes_part])

def criar_step_down_lm2596():
    """
    Gera o Conversor DC-DC Step-Down LM2596 integrando o arquivo oficial em modelos_cad.
    """
    caminho_step = os.path.join(os.path.dirname(__file__), "..", "modelos_cad", "step_down_lm2596_hw411.step")
    if not os.path.exists(caminho_step):
        caminho_step = os.path.join(os.path.dirname(__file__), "..", "HW-411.STEP")
    if os.path.exists(caminho_step):
        try:
            peca = import_step(caminho_step).moved(Rotation(90, 0, 0))
            bb = peca.bounding_box()
            cx = (bb.min.X + bb.max.X) / 2.0
            cy = (bb.min.Y + bb.max.Y) / 2.0
            cz = bb.min.Z
            peca = peca.moved(Location((-cx, -cy, -cz)))
            peca.color = Color(cfg.CORES["PCB_LM2596"])
            peca.label = "Step-Down LM2596 (HW-411 STEP)"
            return peca
        except Exception:
            pass

    # Fallback sintetizado
    with BuildPart() as pcb:
        Box(43.0, 21.0, 1.6)
        with Locations((0, 0, 0)):
            with GridLocations(35.0, 20.0, 2, 2):
                Cylinder(radius=3.2 / 2.0, height=5.0, mode=Mode.SUBTRACT)
    pcb_part = pcb.part
    pcb_part.color = Color(cfg.CORES["PCB_LM2596"])

    with BuildPart() as indutor:
        with Locations((-5.0, 0, 4.0 + 0.8)):
            Cylinder(radius=6.0, height=8.0)
    ind_part = indutor.part
    ind_part.color = Color("#212121")

    with BuildPart() as trimpot:
        with Locations((12.0, 3.0, 4.5 + 0.8)):
            Box(9.0, 4.5, 9.0)
    trim_part = trimpot.part
    trim_part.color = Color("#0D47A1")

    with BuildPart() as caps:
        with Locations((-15.0, 0, 5.0 + 0.8)):
            Cylinder(radius=4.0, height=10.0)
        with Locations((8.0, -5.0, 5.0 + 0.8)):
            Cylinder(radius=3.5, height=10.0)
    caps_part = caps.part
    caps_part.color = Color("#90A4AE")

    return Compound(label="Step-Down LM2596", children=[pcb_part, ind_part, trim_part, caps_part])

def criar_pack_bateria_3s() -> Compound:
    """
    Gera representação CAD do Pack de Baterias 3S 18650 Li-Ion (11.1V ~ 12.6V).
    Dimensões exatas: 70mm (C) x 58mm (L) x 19mm (A).
    Composto por 3 células 18650 em série envoltas em termo-retrátil industrial amarelo.
    """
    comp_pack = cfg.CONFIG["COMP_BERCO_BATERIA"] # 70.0
    larg_pack = cfg.CONFIG["LARG_BERCO_BATERIA"] # 58.0
    r_cel = 18.0 / 2.0
    comp_cel = 65.0

    with BuildPart() as celulas:
        # Invólucro termo-retrátil amortecedor
        Box(comp_pack - 1.0, larg_pack - 1.0, 18.5)
        # 3 células cilíndricas salientes
        for offset_y in [-18.5, 0.0, 18.5]:
            with Locations((0, offset_y, 0)):
                with Locations(Rotation(0, 90, 0)):
                    Cylinder(radius=r_cel, height=comp_cel)
    
    pack_part = celulas.part
    pack_part.color = Color(cfg.CORES["BATERIA_3S"])

    # Conector de saída XT30/XT60 com cabos de silicone 14AWG
    with BuildPart() as conector:
        with Locations((comp_pack / 2.0 + 2.0, 0, 0)):
            Box(8.0, 12.0, 7.0)
            with Locations((4.0, 0, 0)):
                for y_fio in [-3.0, 3.0]:
                    with Locations((0, y_fio, 0)):
                        with Locations(Rotation(0, 90, 0)):
                            Cylinder(radius=1.8, height=12.0)
    conector_part = conector.part
    conector_part.color = Color("#E65100")
    conector_part.label = "Conector Bateria XT60"

    return Compound(label="Bateria 3S Li-Ion 18650 (12V)", children=[pack_part, conector_part])

def criar_esp32_cam() -> Compound:
    """
    Gera representação CAD do Módulo ESP32-CAM (27mm x 40.5mm) com lente de câmera.
    """
    # 1. PCB Verde
    with BuildPart() as pcb:
        Box(27.0, 40.5, 1.6)
    pcb_part = pcb.part
    pcb_part.color = Color(cfg.CORES["PCB_ESP32"])

    # 2. Blindagem metálica do microcontrolador ESP32
    with BuildPart() as shield:
        with Locations((0, -8.0, 1.5 + 0.8)):
            Box(18.0, 18.0, 3.0)
    shield_part = shield.part
    shield_part.color = Color("#CFD8DC")

    # 3. Lente OV2640 da Câmera
    with BuildPart() as cam:
        with Locations((0, 12.0, 3.0 + 0.8)):
            Box(8.0, 8.0, 5.0)
            with Locations((0, 0, 3.0)):
                Cylinder(radius=3.0, height=2.0)
    cam_part = cam.part
    cam_part.color = Color("#000000")

    return Compound(label="ESP32-CAM", children=[pcb_part, shield_part, cam_part])

if __name__ == "__main__":
    print("Gerando Módulos Eletrônicos...")
    l298 = criar_ponte_h_l298n().moved(Location((0, 0, 0)))
    lm = criar_step_down_lm2596().moved(Location((60, 0, 0)))
    esp = criar_esp32_cam().moved(Location((-50, 0, 0)))
    bat = criar_pack_bateria_3s().moved(Location((0, 60, 0)))
    try:
        from ocp_vscode import show
        show(l298, lm, esp, bat)
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Módulos construídos com sucesso! (OCP CAD Viewer: {err})")
