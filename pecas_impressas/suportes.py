import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg
import medidas as med

def criar_suporte_rolamento() -> Part:
    """
    Suporte impresso em 3D para alojar o rolamento 608Z no furo de 40mm da madeira.
    - Corpo cilíndrico externo de Ø40mm com comprimento de 12mm (espessura da madeira).
    - Flange de parada de Ø46mm com espessura de 2mm.
    - Alojamento para o rolamento 608Z (Ø22mm por 7mm de profundidade).
    - Furo central passante de Ø10mm para passagem livre do parafuso M8.
    """
    od_corpo = med.DIAM_FURO_MADEIRA     # 40.0 mm
    od_flange = od_corpo + 6.0          # 46.0 mm
    espessura_madeira = cfg.CONFIG["ESPESSURA_MADEIRA"] # 12.0 mm
    espessura_flange = 2.0
    
    with BuildPart() as suporte:
        # Flange de parada externa
        with BuildSketch(Plane.XY):
            Circle(od_flange / 2)
        extrude(amount=espessura_flange)
        
        # Corpo que entra no furo da madeira (a partir do Z da flange)
        with BuildSketch(Plane.XY.offset(espessura_flange)):
            Circle(od_corpo / 2)
        extrude(amount=espessura_madeira)
        
        # Alojamento do rolamento (lado oposto à flange, entra 7.5mm para garantir que o rolamento fique bem alojado)
        # O rolamento entra a partir da face de trás (Z = espessura_flange + espessura_madeira)
        z_rebaixo = espessura_flange + espessura_madeira
        with BuildSketch(Plane.XY.offset(z_rebaixo)):
            Circle(med.OD_ROLAMENTO_608 / 2)
        extrude(amount=-med.ALTURA_ROLAMENTO_608, mode=Mode.SUBTRACT)
        
        # Furo central passante para o eixo M8
        with BuildSketch(Plane.XY):
            Circle(10.0 / 2) # Furo passante de 10mm (folga para M8)
        extrude(amount=espessura_flange + espessura_madeira, mode=Mode.SUBTRACT)
        
    suporte.part.color = Color("#E65100") # Laranja PETG
    return suporte.part

def criar_suporte_motor() -> Part:
    """
    Suporte impresso em 3D para fixar o motor Johnson 100 RPM no furo de 40mm da madeira.
    - Corpo cilíndrico de Ø40mm por 12mm de comprimento.
    - Flange de parada de Ø46mm por 2mm.
    - Furo passante central de Ø13.0mm para o ressalto do motor Johnson (Ø12.2mm).
    - 4 furos de montagem para parafusos M3 em X (raio de 14.0mm).
    """
    od_corpo = med.DIAM_FURO_MADEIRA     # 40.0 mm
    od_flange = od_corpo + 6.0          # 46.0 mm
    espessura_madeira = cfg.CONFIG["ESPESSURA_MADEIRA"] # 12.0 mm
    espessura_flange = 2.0
    
    with BuildPart() as suporte:
        # Flange de parada externa
        with BuildSketch(Plane.XY):
            Circle(od_flange / 2)
        extrude(amount=espessura_flange)
        
        # Corpo na madeira
        with BuildSketch(Plane.XY.offset(espessura_flange)):
            Circle(od_corpo / 2)
        extrude(amount=espessura_madeira)
        
        # Furo central para o ressalto do motor
        with BuildSketch(Plane.XY):
            Circle(13.0 / 2) # Furo passante com folga para pescoço de 12.2mm
            # 4 furos de fixação em padrão cruzado
            with PolarLocations(14.0, 4, start_angle=45):
                Circle(3.4 / 2, mode=Mode.SUBTRACT) # Furo de 3.4mm para parafusos M3
        extrude(amount=espessura_flange + espessura_madeira, mode=Mode.SUBTRACT)
        
    suporte.part.color = Color("#E65100") # Laranja PETG
    return suporte.part

if __name__ == "__main__":
    from ocp_vscode import show
    s_rol = criar_suporte_rolamento()
    s_mot = criar_suporte_motor().moved(Location((60, 0, 0)))
    show(s_rol, s_mot)
