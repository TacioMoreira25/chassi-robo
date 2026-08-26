import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg
import medidas as med

def criar_travessas() -> Part:
    """
    Cria as duas travessas retangulares de fechamento (frente e traseira).
    Dimensões: LARG_INTERNA (196mm) x ALT_TRAVESSA (20mm) x ESPESSURA_MADEIRA (12mm)
    """
    comp = cfg.CONFIG["LARG_INTERNA"]            # 196.0 mm
    altura = cfg.CONFIG["ALT_TRAVESSA"]          # 20.0 mm
    espessura = cfg.CONFIG["ESPESSURA_MADEIRA"]  # 12.0 mm
    
    comp_base = cfg.CONFIG["COMP_TOTAL"]         # 400.0 mm
    
    with BuildPart() as travessas:
        # Travessa Traseira (na extremidade da base de 400mm)
        with Locations((-comp_base / 2 + espessura / 2, 0, altura / 2)):
            Box(espessura, comp, altura)
        # Travessa Frontal (na extremidade da base de 400mm)
        with Locations((comp_base / 2 - espessura / 2, 0, altura / 2)):
            Box(espessura, comp, altura)
            

    travessas.part.color = Color("#181818") # Preto Fosco
    return travessas.part

if __name__ == "__main__":
    from ocp_vscode import show
    t = criar_travessas()
    show(t)
