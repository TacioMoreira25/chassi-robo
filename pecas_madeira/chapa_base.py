from build123d import *
import config as cfg
import medidas as med

def criar_chapa_base() -> Part:
    """ 
    Cria a chapa base retangular que sustenta o chassi de madeira.
    """
    # O comprimento real do assoalho é a base de 400mm.
    comp_base = cfg.CONFIG["COMP_TOTAL"]
    largura = cfg.CONFIG["LARG_EXTERNA"]
    espessura = cfg.CONFIG["ESPESSURA_MADEIRA"]
    
    # A chapa base será centralizada em X = 0, na altura Z = 0
    centro_x = 0.0
    
    with BuildPart() as base:
        with Locations((centro_x, 0, espessura / 2)):
            Box(comp_base, largura, espessura)
            
    base.part.color = Color("#181818") # Preto Fosco
    return base.part

if __name__ == "__main__":
    from ocp_vscode import show
    chapa = criar_chapa_base()
    show(chapa)