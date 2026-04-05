from build123d import *

def criar_suporte_motor():
    # Motor 33GB-520
    diam_motor = 33.0 
    pcd_motor = 26.0 
    comp_motor_body = 39.0 
    
    # Bloco Plástico (Dimensionado com base nas fotos)
    comp_bloco = 55.0  # Eixo X
    larg_bloco = 35.0  # Eixo Y (Espessura do bloco)
    alt_bloco = 55.0   # Eixo Z

    with BuildPart() as suporte:
        Box(comp_bloco, larg_bloco, alt_bloco)
        
        # Furo do motor
        with BuildSketch(Plane.YZ):
            Circle(radius=(diam_motor + 0.5) / 2)
        extrude(amount=comp_bloco, both=True, mode=Mode.SUBTRACT)
        
        # Furos frontais para fixar o motor (com escareado)
        face_frontal = suporte.faces().sort_by(Axis.X)[-1]
        with BuildSketch(face_frontal):
            with Locations((pcd_motor/2, pcd_motor/2), (pcd_motor/2, -pcd_motor/2),
                           (-pcd_motor/2, pcd_motor/2), (-pcd_motor/2, -pcd_motor/2)):
                Circle(radius=1.6) # Passante M3
        extrude(amount=-comp_bloco, mode=Mode.SUBTRACT)
        
        with BuildSketch(face_frontal):
            with Locations((pcd_motor/2, pcd_motor/2), (pcd_motor/2, -pcd_motor/2),
                           (-pcd_motor/2, pcd_motor/2), (-pcd_motor/2, -pcd_motor/2)):
                Circle(radius=3.0) # Escareado
        extrude(amount=-10.0, mode=Mode.SUBTRACT)

        # Furos laterais para insertos M4 (Fixam na parede do chassi)
        face_lateral = suporte.faces().sort_by(Axis.Y)[-1]
        with BuildSketch(face_lateral):
            with Locations((15, 15), (-15, 15), (15, -15), (-15, -15)): 
                Circle(radius=2.3) # Furo para inserto M4
        extrude(amount=-15.0, mode=Mode.SUBTRACT)

    # Mockup cilíndrico
    with BuildPart() as motor_mockup:
        with BuildSketch(Plane.YZ):
            Circle(radius=diam_motor / 2)
        extrude(amount=comp_motor_body)
        with BuildSketch(Plane.YZ.offset(comp_motor_body)):
            Circle(radius=10.0)
            Circle(radius=2.5) # Eixo
        extrude(amount=9.0)

    return {
        "suporte": suporte.part,
        "motor": motor_mockup.part
    }