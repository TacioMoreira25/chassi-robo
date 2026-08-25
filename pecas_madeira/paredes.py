from build123d import *
import config as cfg
import medidas as med

def _gerar_perfil_parede() -> Part:
    """
    Gera a parede lateral trapezoidal idêntica ao vídeo do Creative Home Tank.
    Sem rasgos centrais (removido o furo não desejado) e com quinas retas simples.
    """
    z_top = cfg.CONFIG["ALT_PAREDE"] # 110
    x_recuo_top = cfg.CONFIG["RECUO_CHANFRO_X"] # 80
    
    # 4 Pontos do Trapézio perfeito (Base=400, Topo=240)
    pts = [
        (x_recuo_top, z_top),                                # Quina Traseira Superior (80, 110)
        (cfg.CONFIG["COMP_TOTAL"] - x_recuo_top, z_top),     # Quina Dianteira Superior (320, 110)
        (cfg.CONFIG["COMP_TOTAL"], 0),                       # Quina Dianteira Inferior (400, 0)
        (0, 0)                                               # Quina Traseira Inferior (0, 0)
    ]
    
    with BuildPart() as parede:
        with BuildSketch(Plane.XZ):
            Polygon(*pts)
            
            # Oblongos (Slots) para tensionamento nas 3 catracas livres
            with Locations((med.FUROS_RODAS[1][0], med.FUROS_RODAS[1][1]),
                           (med.FUROS_RODAS[2][0], med.FUROS_RODAS[2][1]),
                           (med.FUROS_RODAS[3][0], med.FUROS_RODAS[3][1])):
                SlotOverall(med.LARG_OBLONGO, med.ALT_OBLONGO, mode=Mode.SUBTRACT)
                
            # Furo central do Motor Johnson (Traseira Superior)
            with Locations((med.FUROS_RODAS[0][0], med.FUROS_RODAS[0][1])):
                Circle(med.DIAM_RESSALTO / 2 + 1.0, mode=Mode.SUBTRACT)
                # 6 furos M4 para fixar o motor (raio 14mm)
                with PolarLocations(14.0, 6):
                    Circle(2.0, mode=Mode.SUBTRACT)
                
        extrude(amount=cfg.CONFIG["ESPESSURA_MADEIRA"])
        
    return parede.part

def criar_paredes() -> Part:
    """
    Retorna o conjunto (Esquerda e Direita) já na cor Cinza Escuro.
    """
    parede_dir = _gerar_perfil_parede()
    parede_esq = _gerar_perfil_parede()
    
    y_esq = cfg.CONFIG["LARG_INTERNA"] / 2 + cfg.CONFIG["ESPESSURA_MADEIRA"] / 2
    
    with BuildPart() as paredes_completas:
        with Locations((0, -y_esq, 0)):
            add(parede_dir)
        with Locations((0, y_esq, 0)):
            add(parede_esq)
            
    paredes_completas.part.color = Color("#181818") # Preto Fosco
    return paredes_completas.part

if __name__ == "__main__":
    from ocp_vscode import show
    p = criar_paredes()
    show(p, names=["Paredes Laterais Tank"])