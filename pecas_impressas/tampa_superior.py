"""
===============================================================================
ROBÔ DE INSPEÇÃO - TAMPA SUPERIOR / CARENAGEM STEALTH
===============================================================================
Componente: Cobertura superior chanfrada ("Stealth Hood") e Suporte Tilt
Especificações Oficiais Definitivas:
- Dimensões da tampa: 240 mm (X) x 160 mm (Y) x 5.0 mm (Z)
- Canaleta perimetral de vedação IP65 na face inferior: 3.0 mm largura x 2.0 mm profundidade
- Suporte Frontal Articulado Tilt em PETG: 55 mm (largura Y) x 38 mm (altura Z) x 25 mm (profundidade X)
  * Janela da Câmera (ESP32-CAM): Recorte de 10 x 10 mm
  * Sensor Térmico MLX90614: Furo circular de Ø10.2 mm
  * Faróis LED Olho de Águia (2x): Furos Ø10.2 mm (M10)
  * Furos de Articulação (Tilt): Furos laterais Ø3.2 mm para parafuso M3 e Nyloc
- Cooler Fan Rise Mode 80mm: Abertura circular Ø75 mm, 4 furos Ø4.2 mm em 71.5 x 71.5 mm
  * Moldura/suporte em PETG: 85 x 85 x 4 mm
- Painel Externo:
  * Recorte Chave KCD1: 19.2 x 13.0 mm
  * Nicho Voltímetro Digital: 22.5 x 14.0 mm com trava snap-fit
  * Furo Antena Wi-Fi SMA: Ø6.5 mm (M8)
Material: PETG Preto Carbono Acetinado Stealth
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg

def criar_tampa_superior() -> Compound:
    """
    Gera a Carenagem Superior Stealth exatamente conforme o compêndio técnico oficial.
    """
    comp = cfg.CONFIG["COMPRIMENTO_TAMPA"]       # 240.0
    larg = cfg.CONFIG["LARGURA_TAMPA"]           # 160.0
    alt = cfg.CONFIG["ALTURA_TAMPA"]              # 5.0
    esp = cfg.CONFIG["ESPESSURA_PAREDE"]          # 2.5
    h_lip = 2.5

    # Bloco do Suporte Articulado Frontal de Sensores (55 largura Y x 25 prof X x 38 altura Z)
    larg_tilt = cfg.CONFIG.get("LARG_BLOCO_TILT", 55.0)
    prof_tilt = cfg.CONFIG.get("PROF_BLOCO_TILT", 25.0)
    alt_tilt = cfg.CONFIG.get("ALT_BLOCO_TILT", 38.0)
    pos_x_tilt = comp / 2.0 - prof_tilt / 2.0 - 5.0 # ~102.5mm
    pos_z_tilt = alt + alt_tilt / 2.0

    # Cooler Fan Rise Mode 80mm
    diam_recorte_cooler = cfg.CONFIG.get("DIAM_RECORTE_COOLER", 75.0)
    pcd_cooler = cfg.CONFIG.get("LARG_FURACAO_COOLER", 71.5)
    furo_cooler = cfg.CONFIG.get("DIAM_FURO_COOLER", 4.2)
    larg_moldura_cooler = cfg.CONFIG.get("MOLDURA_COOLER_LARG", 85.0)
    esp_moldura_cooler = cfg.CONFIG.get("MOLDURA_COOLER_ESP", 4.0)
    pos_x_cooler = -15.0

    # Painel externo
    pos_x_kcd1 = 55.0
    pos_y_kcd1 = -25.0
    pos_x_voltimetro = 55.0
    pos_y_voltimetro = 25.0
    pos_antena = (-90.0, 50.0)

    # Canaleta IP65
    larg_canaleta = cfg.CONFIG.get("LARGURA_CANALETA_IP65", 3.0)
    prof_canaleta = cfg.CONFIG.get("PROF_CANALETA_IP65", 2.0)

    with BuildPart() as tampa:
        # 1. Chapa principal da tampa (240 x 160 x 5 mm)
        with Locations((0, 0, alt / 2.0)):
            Box(comp, larg, alt)

        # 2. Chanfro perimetral suave nas arestas superiores
        top_face = tampa.faces().sort_by(Axis.Z)[-1]
        try:
            chamfer(top_face.edges(), length=cfg.CONFIG.get("CHANFRO_TAMPA", 4.0))
        except Exception:
            pass

        # 3. Lábio macho inferior de encaixe na banheira
        with Locations((0, 0, -h_lip / 2.0)):
            Box(comp - 2 * esp - 0.4, larg - 2 * esp - 0.4, h_lip)

        # 4. Canaleta IP65 perimetral para gaxeta de silicone (3.0mm largura x 2.0mm prof)
        with Locations((0, 0, -prof_canaleta / 2.0)):
            with BuildSketch(Plane.XY):
                Rectangle(comp - 2 * esp + 1.0, larg - 2 * esp + 1.0)
                Rectangle(comp - 2 * esp + 1.0 - 2 * larg_canaleta, larg - 2 * esp + 1.0 - 2 * larg_canaleta, mode=Mode.SUBTRACT)
            extrude(amount=prof_canaleta, mode=Mode.SUBTRACT)

        # 5. Moldura do Cooler Fan Rise Mode 80mm (85 x 85 x 4 mm) no teto
        with Locations((pos_x_cooler, 0, alt + esp_moldura_cooler / 2.0)):
            Box(larg_moldura_cooler, larg_moldura_cooler, esp_moldura_cooler)

        # 6. Recorte circular central de ar Ø75mm e 4 furos M4 em 71.5 x 71.5mm
        with Locations((pos_x_cooler, 0, (alt + esp_moldura_cooler) / 2.0)):
            Cylinder(radius=diam_recorte_cooler / 2.0, height=alt * 4, mode=Mode.SUBTRACT)
            with GridLocations(pcd_cooler, pcd_cooler, 2, 2):
                Cylinder(radius=furo_cooler / 2.0, height=alt * 4, mode=Mode.SUBTRACT)

        # 7. Bloco do Suporte Articulado Frontal de Sensores (Tilt)
        with Locations((pos_x_tilt, 0, pos_z_tilt)):
            Box(prof_tilt, larg_tilt, alt_tilt)

        # 8. Furações dos sensores na face frontal do Suporte Tilt:
        face_x_front = pos_x_tilt + prof_tilt / 2.0
        # Abertura retangular/quadrada 10 x 10 mm para câmera ESP32-CAM
        with Locations((face_x_front, -8.0, pos_z_tilt)):
            Box(prof_tilt * 2, 10.0, 10.0, mode=Mode.SUBTRACT)
        # Furo circular Ø10.2mm para sensor infravermelho MLX90614
        with Locations((face_x_front, 8.0, pos_z_tilt)):
            with Locations(Rotation(0, 90, 0)):
                Cylinder(radius=cfg.CONFIG["DIAM_FURO_MLX90614"] / 2.0, height=prof_tilt * 2, mode=Mode.SUBTRACT)
        # 2x Furos Ø10.2mm (M10) para faróis LED Olho de Águia
        for y_led in [-20.0, 20.0]:
            with Locations((face_x_front, y_led, pos_z_tilt)):
                with Locations(Rotation(0, 90, 0)):
                    Cylinder(radius=cfg.CONFIG["DIAM_FURO_FAROL_LED"] / 2.0, height=prof_tilt * 2, mode=Mode.SUBTRACT)
        # Furos laterais Ø3.2mm das orelhas de articulação Tilt
        for y_orelha in [-larg_tilt / 2.0, larg_tilt / 2.0]:
            with Locations((pos_x_tilt, y_orelha, pos_z_tilt - 10.0)):
                with Locations(Rotation(90, 0, 0)):
                    Cylinder(radius=cfg.CONFIG["DIAM_FURO_ORELHA_TILT"] / 2.0, height=10.0, mode=Mode.SUBTRACT)

        # 9. Recorte da Chave KCD1 (19.2 x 13.0 mm)
        with Locations((pos_x_kcd1, pos_y_kcd1, alt / 2.0)):
            Box(cfg.CONFIG["RECORTE_CHAVE_KCD1_X"], cfg.CONFIG["RECORTE_CHAVE_KCD1_Y"], alt * 4, mode=Mode.SUBTRACT)

        # 10. Nicho do Voltímetro Digital LED (22.5 x 14.0 mm)
        with Locations((pos_x_voltimetro, pos_y_voltimetro, alt / 2.0)):
            Box(cfg.CONFIG["LARG_VOLTIMETRO"], cfg.CONFIG["ALT_VOLTIMETRO"], alt * 4, mode=Mode.SUBTRACT)

        # 11. Furo passante para Antena SMA Wi-Fi (Ø6.5mm)
        with Locations((pos_antena[0], pos_antena[1], alt / 2.0)):
            Cylinder(radius=cfg.CONFIG["DIAM_FURO_ANTENA_SMA"] / 2.0, height=alt * 4, mode=Mode.SUBTRACT)

        # 12. Furos laterais M3 para fixação ao chassi banheira
        for x_furo in [-85.0, -25.0, 25.0, 85.0]:
            for y_sinal in [-1, 1]:
                with Locations((x_furo, y_sinal * (larg / 2.0), -h_lip / 2.0)):
                    with Locations(Rotation(90, 0, 0)):
                        Cylinder(radius=cfg.CONFIG["DIAM_FURO_M3"] / 2.0, height=esp * 4, mode=Mode.SUBTRACT)

    peca_tampa = tampa.part
    peca_tampa.color = Color(cfg.CORES["TAMPA_SUPERIOR"])
    peca_tampa.label = "Carenagem Superior Stealth"

    # --- Componentes e Sensores Integrados com Cores Didáticas ---
    face_x = pos_x_tilt + prof_tilt / 2.0

    # Lente Câmera OV2640 (azul antirreflexo)
    with BuildPart() as lente:
        with Locations((face_x + 0.5, -8.0, pos_z_tilt)):
            with Locations(Rotation(0, 90, 0)):
                Cylinder(radius=4.0, height=1.5)
                with Locations((0, 0, -1.0)):
                    Cylinder(radius=4.8, height=1.0)
    peca_lente = lente.part
    peca_lente.color = Color(cfg.CORES["LENTE_CAMERA"])
    peca_lente.label = "Lente OV2640 (10x10mm)"

    # Cápsula Sensor Térmico MLX90614 (metal cromo TO-39)
    with BuildPart() as mlx:
        with Locations((face_x + 0.5, 8.0, pos_z_tilt)):
            with Locations(Rotation(0, 90, 0)):
                Cylinder(radius=4.8, height=1.8)
                with Locations((0, 0, 0.8)):
                    Cylinder(radius=2.5, height=1.5)
    peca_mlx = mlx.part
    peca_mlx.color = Color(cfg.CORES["METAL_CROMADO"])
    peca_mlx.label = "Sensor Termico MLX90614"

    # Faróis LED Olho de Águia (2x amarelo translúcido M10)
    with BuildPart() as leds:
        for y_led in [-20.0, 20.0]:
            with Locations((face_x + 0.5, y_led, pos_z_tilt)):
                with Locations(Rotation(0, 90, 0)):
                    Cylinder(radius=4.8, height=1.5)
                    with Locations((0, 0, -0.8)):
                        Cylinder(radius=5.4, height=0.8)
    peca_leds = leds.part
    peca_leds.color = Color(cfg.CORES["FAROL_LED"])
    peca_leds.label = "Farois LED Olho de Aguia (2x M10)"

    # Interruptor Gangorra KCD1 (tecla vermelha)
    with BuildPart() as kcd1:
        with Locations((pos_x_kcd1, pos_y_kcd1, alt + 1.5)):
            Box(16.0, 11.0, 3.0)
    peca_kcd1 = kcd1.part
    peca_kcd1.color = Color(cfg.CORES["CHAVE_KCD1"])
    peca_kcd1.label = "Chave KCD1 (19.2x13mm)"

    # Voltímetro Digital LED (display digital vermelho)
    with BuildPart() as voltimetro:
        with Locations((pos_x_voltimetro, pos_y_voltimetro, alt + 1.0)):
            Box(20.0, 12.0, 2.0)
    peca_voltimetro = voltimetro.part
    peca_voltimetro.color = Color(cfg.CORES["VOLTIMETRO_LED"])
    peca_voltimetro.label = "Voltimetro Digital (22.5x14mm)"

    # Antena Wi-Fi SMA (base metálica + haste vertical)
    with BuildPart() as antena:
        with Locations((pos_antena[0], pos_antena[1], alt + 1.0)):
            Cylinder(radius=3.2, height=3.0)
            with Locations((0, 0, 10.0)):
                Cylinder(radius=2.5, height=18.0)
    peca_antena = antena.part
    peca_antena.color = Color("#37474F")
    peca_antena.label = "Antena Wi-Fi SMA (Ø6.5mm)"

    # Gaxeta de silicone IP65 na canaleta
    with BuildPart() as gaxeta:
        with Locations((0, 0, -prof_canaleta / 2.0)):
            with BuildSketch(Plane.XY):
                Rectangle(comp - 2 * esp + 0.8, larg - 2 * esp + 0.8)
                Rectangle(comp - 2 * esp + 0.8 - 2 * (larg_canaleta - 0.4), larg - 2 * esp + 0.8 - 2 * (larg_canaleta - 0.4), mode=Mode.SUBTRACT)
            extrude(amount=prof_canaleta)
    peca_gaxeta = gaxeta.part
    peca_gaxeta.color = Color(cfg.CORES["SILICONE_VEDACAO"])
    peca_gaxeta.label = "Gaxeta Silicone IP65 (3x2mm)"

    return Compound(
        label="Carenagem Superior Stealth (Robô de Inspeção)",
        children=[
            peca_tampa, peca_lente, peca_mlx, peca_leds,
            peca_kcd1, peca_voltimetro, peca_antena, peca_gaxeta
        ]
    )

if __name__ == "__main__":
    print("Gerando Carenagem Superior Stealth (Robô de Inspeção)...")
    t = criar_tampa_superior()
    try:
        from ocp_vscode import show
        show(t, names=["Carenagem Superior Stealth (Robô de Inspeção)"])
        print("Visualização enviada para o OCP CAD Viewer!")
    except Exception as err:
        print(f"Peça construída com sucesso! (OCP CAD Viewer: {err})")
