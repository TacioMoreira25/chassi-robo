from build123d import *
import medidas as med

def criar_motor_johnson() -> Compound:
    """
    Mockup procedural do Motor DC Johnson 100 RPM com caixa de redução.
    O ponto de origem (Z=0) será a face FRONTAL do motor (onde fica o ressalto).
    Isso facilita acoplá-lo rentinho à parede de madeira.
    """
    with BuildPart() as corpo:
        # Extrude do -COMP_MOTOR até 0
        with BuildSketch(Plane.XY.offset(-med.COMP_MOTOR_JOHNSON)):
            Circle(med.DIAM_MOTOR_JOHNSON / 2)
        extrude(amount=med.COMP_MOTOR_JOHNSON)
        
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
        
    corpo.part.color = Color("silver")
    ressalto.part.color = Color("gold")
    eixo.part.color = Color("#E0E0E0")
        
    return Compound(label="Motor Johnson 100RPM", children=[corpo.part, ressalto.part, eixo.part])

if __name__ == "__main__":
    from ocp_vscode import show
    m = criar_motor_johnson()
    show(m, colors=["#b0c4de"])
