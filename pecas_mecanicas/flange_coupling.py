from build123d import *

def criar_flange_coupling() -> Compound:
    """
    Acoplador Flange (Flange Coupling) para conectar o eixo do motor de 6mm à catraca/madeira.
    Baseado nas especificações padrão de Flanges M6:
    - Diâmetro da Base (Flange): ~28mm
    - Furos de montagem: 6 furos em um diâmetro de furação de ~20-22mm
    - Diâmetro do Cilindro Central: ~12mm
    - Furo central (Eixo): 6mm
    """
    diam_flange = 28.0
    espessura_flange = 2.5
    diam_cilindro = 12.0
    altura_cilindro = 10.0
    diam_eixo = 6.2 # Leve folga para o eixo de 6mm
    diam_furos_parafuso = 3.2 # Para parafusos M3
    
    with BuildPart() as flange:
        # Base da Flange
        with BuildSketch(Plane.XY):
            Circle(diam_flange / 2)
            # 6 furos de montagem na borda (Circunferência de furação de 20mm)
            with PolarLocations(10.0, 6):
                Circle(diam_furos_parafuso / 2, mode=Mode.SUBTRACT)
            # Furo central
            Circle(diam_eixo / 2, mode=Mode.SUBTRACT)
        extrude(amount=espessura_flange)
        
        # Cilindro central do acoplador
        with BuildSketch(Plane.XY.offset(espessura_flange)):
            Circle(diam_cilindro / 2)
            Circle(diam_eixo / 2, mode=Mode.SUBTRACT)
        extrude(amount=altura_cilindro)
        
    flange.part.color = Color("silver")
    return Compound(label="Flange Coupling 6mm", children=[flange.part])

if __name__ == "__main__":
    from ocp_vscode import show
    f = criar_flange_coupling()
    show(f)
