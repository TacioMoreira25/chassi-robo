from build123d import *
import medidas as med

def criar_motor_johnson() -> Compound:
    """
    Mockup procedural do Motor DC Johnson 100 RPM com caixa de redução.
    O ponto de origem (Z=0) será a face FRONTAL do motor (onde fica o ressalto).
    Isso facilita acoplá-lo rentinho à parede de madeira.
    """
    with BuildPart() as motor_body:
        # Corpo do motor (Prateado, ligeiramente mais fino)
        # Assumindo que DIAM_MOTOR_JOHNSON é da caixa de redução. O corpo é um pouco menor (ex: -4mm)
        diam_corpo = med.DIAM_MOTOR_JOHNSON - 4.0
        comp_corpo = med.COMP_MOTOR_JOHNSON * 0.7 # 70% do comprimento é motor
        with BuildSketch(Plane.XY.offset(-med.COMP_MOTOR_JOHNSON)):
            Circle(diam_corpo / 2)
        extrude(amount=comp_corpo)
        
    with BuildPart() as gearbox:
        # Caixa de redução (Cinza escuro, mais larga) encosta na madeira (Z=0)
        comp_gearbox = med.COMP_MOTOR_JOHNSON * 0.3
        with BuildSketch(Plane.XY.offset(-comp_gearbox)):
            Circle(med.DIAM_MOTOR_JOHNSON / 2)
        extrude(amount=comp_gearbox)
        
    with BuildPart() as ressalto:
        # Ressalto começa em Z=0 e vai até ALTURA_RESSALTO
        with BuildSketch(Plane.XY):
            Circle(med.DIAM_RESSALTO / 2)
        extrude(amount=med.ALTURA_RESSALTO)
        
    with BuildPart() as eixo:
        # Eixo começa no topo do ressalto
        with BuildSketch(Plane.XY.offset(med.ALTURA_RESSALTO)):
            Circle(med.DIAM_EIXO_MOTOR / 2)
        extrude(amount=med.COMP_EIXO_MOTOR)
        
        # Furo transversal no eixo
        with BuildSketch(Plane.XZ):
            with Locations((0, med.ALTURA_RESSALTO + med.COMP_EIXO_MOTOR - 4.0)):
                Circle(1.5) # Furo de 3mm
        extrude(amount=med.DIAM_EIXO_MOTOR, both=True, mode=Mode.SUBTRACT)
        
    motor_body.part.color = Color("silver")
    gearbox.part.color = Color("#444444")
    ressalto.part.color = Color("gold")
    eixo.part.color = Color("#E0E0E0")
        
    return Compound(label="Motor Johnson 100RPM", children=[motor_body.part, gearbox.part, ressalto.part, eixo.part])

if __name__ == "__main__":
    from ocp_vscode import show
    m = criar_motor_johnson()
    show(m, colors=["#b0c4de"])
