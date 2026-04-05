# chapa_base.py
from build123d import *
import config

def criar_chapa_base():
    with BuildPart() as chapa:
        # 1. Contorno principal (No plano XY global)
        with BuildSketch(Plane.XY):
            # A parte estreita (Vão dianteiro) vai de X=0 até X=76.2
            # Esta é a 'língua' que você cortou
            with Locations((config.COMP_BAY / 2, 0)):
                Rectangle(config.COMP_BAY, config.LARG_LINGUA)
            
            # A parte larga vai de X=76.2 até X=406.4
            with Locations((config.COMP_BAY + (config.COMP_CORPO / 2), 0)):
                Rectangle(config.COMP_CORPO, config.LARG_EXTERNA)
                
        extrude(amount=config.ESPESSURA_PISO)

        # 2. Furações para o tensionador dianteiro (Validadas "mais pra baixo")
        # Mantemos as medidas que você validou. Elas desceram (eixo X) 
        # para o meio do vão de 3 polegadas.
        dist_frente_1 = 38.1  # 1.5 polegadas da borda frontal (X=0)
        dist_frente_2 = 63.5  # 2.5 polegadas da borda frontal (X=0)
        
        # Recuo lateral (eixo Y) de 0.5 polegadas das bordas estreitas
        dist_lateral = 12.7
        pos_y_furos = (config.LARG_LINGUA / 2) - dist_lateral

        # Desenhando os furos passantes no plano XY global
        with BuildSketch(Plane.XY):
            with Locations(
                (dist_frente_1, pos_y_furos), 
                (dist_frente_2, pos_y_furos),
                (dist_frente_1, -pos_y_furos), 
                (dist_frente_2, -pos_y_furos)
            ):
                Circle(radius=2.5) # Furos de 5mm

        # Corte passante (nos dois sentidos para ter certeza)
        extrude(amount=config.ESPESSURA_PISO * 2, both=True, mode=Mode.SUBTRACT)
        
    return chapa.part

if __name__ == "__main__":
    from ocp_vscode import show
    chapa = criar_chapa_base()
    show(chapa, names=["Chapa Base (Assoalho)"], colors=["#d2b48c"])