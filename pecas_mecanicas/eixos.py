from build123d import *
import config as cfg
import medidas as med

def criar_eixo_m8() -> Part:
    """
    Cria um Parafuso Sextavado M8x75mm.
    A cabeça do parafuso fica na origem (Z=0).
    A rosca se estende até Z=75.
    """
    comp = 75.0 
    
    with BuildPart() as parafuso:
        # Cabeça Sextavada (chave 13mm para M8)
        with BuildSketch(Plane.XY):
            RegularPolygon(radius=13.0/2, side_count=6)
        extrude(amount=-5.3) # Altura da cabeça do parafuso M8
        
        # Corpo cilíndrico
        with BuildSketch(Plane.XY):
            Circle(med.RAIO_FURO_EIXO_M8)
        extrude(amount=comp)
        
    parafuso.part.color = Color("silver")
    return parafuso.part

def criar_arruela_e_porca() -> Part:
    """
    Cria uma arruela e uma porca M8 juntas para montar na parte interna.
    Origem em Z=0 (face da arruela que encosta na madeira).
    """
    with BuildPart() as arruela_porca:
        # Arruela
        with BuildSketch(Plane.XY):
            Circle(24.0/2) # Arruela larga (fender washer) OD 24mm
            Circle(8.2/2, mode=Mode.SUBTRACT) # Furo interno 8.2mm
        extrude(amount=2.0)
        
        # Porca M8 (chave 13mm)
        with BuildSketch(Plane.XY.offset(2.0)):
            RegularPolygon(radius=13.0/2, side_count=6)
            Circle(8.0/2, mode=Mode.SUBTRACT)
        extrude(amount=6.5) # Altura da porca M8
        
    arruela_porca.part.color = Color("#D4AF37") # Zincado amarelo (como nas fotos)
    return arruela_porca.part

def criar_rolamento_608zz() -> Part:
    """
    Cria o rolamento 608zz (22x8x7mm).
    """
    with BuildPart() as rolamento:
        with BuildSketch(Plane.XY):
            Circle(22.0 / 2)
            Circle(8.0 / 2, mode=Mode.SUBTRACT)
        extrude(amount=7.0)
        
        with BuildSketch(Plane.XY.offset(1.0)):
            Circle(19.0 / 2)
            Circle(11.0 / 2, mode=Mode.SUBTRACT)
        extrude(amount=5.0, mode=Mode.SUBTRACT)
        
    rolamento.part.color = Color("silver")
    return rolamento.part

if __name__ == "__main__":
    from ocp_vscode import show
    e = criar_eixo_m8()
    ap = criar_arruela_e_porca()
    show(e, ap)
