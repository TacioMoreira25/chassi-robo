import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg
import medidas as med

def _gerar_perfil_parede() -> Part:
    """
    Gera a parede lateral trapezoidal idêntica ao modelo real das fotos:
    - Base reto de 400mm no chão (Z=0).
    - Topo reto de 290mm a 110mm de altura (Z=110mm).
    - Transição nas pontas em Z=40mm (X=±200mm).
    """
    z_top = cfg.CONFIG["ALT_PAREDE"]              # 110.0 mm
    comp = cfg.CONFIG["COMP_TOTAL"]               # 400.0 mm
    chanfro_x = cfg.CONFIG["CHANFRO_X"]           # 55.0 mm
    chanfro_z = cfg.CONFIG["CHANFRO_Z"]           # 40.0 mm
    
    # 6 Pontos do Perfil Trapezoidal (Origem X=0 no centro da peça, Z=0 na base)
    pts = [
        (-comp/2 + chanfro_x, z_top),             # Topo Traseiro (-120, 110)
        (comp/2 - chanfro_x, z_top),              # Topo Dianteiro (120, 110)
        (comp/2, chanfro_z),                      # Quina lateral dianteira (200, 90)
        (comp/2, 0.0),                            # Quina Inferior Dianteira (200, 0)
        (-comp/2, 0.0),                           # Quina Inferior Traseira (-200, 0)
        (-comp/2, chanfro_z)                      # Quina lateral traseira (-200, 90)
    ]
    
    with BuildPart() as parede:
        with BuildSketch(Plane.XZ):
            Polygon(*pts)
            
            # Furo 0: Motor Johnson (Inferior Traseira: X=-120, Z=25)
            with Locations((med.FUROS_RODAS[0][0], med.FUROS_RODAS[0][1])):
                Circle(med.DIAM_RESSALTO / 2 + 1.0, mode=Mode.SUBTRACT)
                with PolarLocations(14.0, 6):
                    Circle(2.0, mode=Mode.SUBTRACT)
                    
            # Furo 1: Eixo Fixo M8 (Superior Traseira: X=-120, Z=85)
            with Locations((med.FUROS_RODAS[1][0], med.FUROS_RODAS[1][1])):
                Circle(8.5 / 2, mode=Mode.SUBTRACT)
                
            # Furo 2: Eixo Fixo M8 (Superior Dianteira: X=120, Z=85)
            with Locations((med.FUROS_RODAS[2][0], med.FUROS_RODAS[2][1])):
                Circle(8.5 / 2, mode=Mode.SUBTRACT)
                
            # Furo 3: Slot Oblongo para tensionador (Inferior Dianteira: X=120, Z=25)
            with Locations((med.FUROS_RODAS[3][0], med.FUROS_RODAS[3][1])):
                SlotOverall(med.LARG_OBLONGO, med.ALT_OBLONGO, mode=Mode.SUBTRACT)
                
        extrude(amount=cfg.CONFIG["ESPESSURA_MADEIRA"] / 2, both=True)
        
    return parede.part

def criar_paredes() -> Part:
    """
    Retorna o conjunto (Esquerda e Direita) já na cor Cinza Escuro.
    """
    parede_dir = _gerar_perfil_parede()
    parede_esq = _gerar_perfil_parede()
    
    # y_esq define a posição central da parede no eixo Y.
    y_esq = cfg.CONFIG["LARG_EXTERNA"] / 2 - cfg.CONFIG["ESPESSURA_MADEIRA"] / 2
    
    with BuildPart() as paredes_completas:
        with Locations((0, -y_esq, 0)):
            add(parede_dir)
        with Locations((0, y_esq, 0)):
            add(parede_esq)
            
    paredes_completas.part.color = Color("#181818") # Preto Fosco
    return paredes_completas.part

if __name__ == "__main__":
    from ocp_vscode import show
    p = criar_paredes()
    show(p, names=["Paredes Laterais Tank"])