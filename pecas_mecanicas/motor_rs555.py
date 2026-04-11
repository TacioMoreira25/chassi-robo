from build123d import *

def criar_motor() -> Solid:
    """ Cria uma variação procedural do motor RS-550 baseada no desenho técnico, com dimensões aproximadas. """
    with BuildPart() as motor:
        # Corpo principal (Levemente achatado nas laterais top/bottom)
        with BuildSketch(Plane.XY):
            Circle(37.2 / 2)
            Rectangle(37.2, 35.6, mode=Mode.INTERSECT)
        extrude(amount=57.0)

        # Degrau frontal (resalto)
        with BuildSketch(motor.faces().sort_by(Axis.Z)[-1]):
            Circle(13.0 / 2)
        extrude(amount=4.5)

        # Eixo (Eixo que passa na madeira)
        with BuildSketch(motor.faces().sort_by(Axis.Z)[-1]):
            Circle(4.0 / 2)
        extrude(amount=8.2)

        # Engrenagem
        with BuildSketch(motor.faces().sort_by(Axis.Z)[-1]):
            Circle(8.2 / 2)
        extrude(amount=6.8)
        
    return motor.part
