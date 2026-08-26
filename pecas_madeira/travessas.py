from build123d import *
import config as cfg
import medidas as med

def criar_travessas() -> Part:
    """
    Cria as duas travessas retangulares de fechamento (frente e traseira).
    Dimensões: LARG_INTERNA x ALT_TRAVESSA x ESPESSURA_MADEIRA
    """
    comp = cfg.CONFIG["LARG_INTERNA"] # 196.0
    altura = cfg.CONFIG["ALT_TRAVESSA"] # 20.0
    espessura = cfg.CONFIG["ESPESSURA_MADEIRA"] # 12.0
    
    comp_base = cfg.CONFIG["COMP_TOTAL"]
    
    with BuildPart() as travessas:
        # Travessa Traseira (X próximo a -145)
        with Locations((-comp_base / 2 + espessura / 2, 0, altura / 2)):
            Box(espessura, comp, altura)
        # Travessa Frontal (X próximo a +145)
        with Locations((comp_base / 2 - espessura / 2, 0, altura / 2)):
            Box(espessura, comp, altura)
            

    travessas.part.color = Color("#181818") # Preto Fosco
    return travessas.part

if __name__ == "__main__":
    from ocp_vscode import show
    t = criar_travessas()
    show(t)
