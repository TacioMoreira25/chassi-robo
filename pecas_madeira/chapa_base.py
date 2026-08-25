from build123d import *
import config as cfg
import medidas as med

def criar_chapa_base() -> Part:
    """ 
    Cria a chapa base retangular que sustenta o chassi de madeira.
    """
    comp_base = cfg.CONFIG["COMP_TOTAL"]
    largura = cfg.CONFIG["LARG_INTERNA"]
    espessura = cfg.CONFIG["ESPESSURA_MADEIRA"]
    
    # A chapa base será centralizada em X = 200, na altura Z = 0
    centro_x = cfg.CONFIG["COMP_TOTAL"] / 2
    
    with BuildPart() as base:
        with Locations((centro_x, 0, espessura / 2)):
            Box(comp_base, largura, espessura)
            
    base.part.color = Color("#181818") # Preto Fosco
    return base.part

def criar_parede_pequena() -> Part:
    """
    Parede vertical pequena que fecha as extremidades inferior da frente e traseira.
    """
    comp = cfg.CONFIG["ESPESSURA_MADEIRA"] # 12mm
    largura = cfg.CONFIG["LARG_INTERNA"] # 198mm
    altura = 40.0
    
    with BuildPart() as parede:
        Box(comp, largura, altura)
        
    parede.part.color = Color("#181818") # Preto Fosco
    return parede.part

if __name__ == "__main__":
    from ocp_vscode import show
    chapa = criar_chapa_base()
    p_pequena = criar_parede_pequena()
    show(chapa, p_pequena)