from build123d import *
import config as cfg
import medidas as med

def _gerar_perfil_parede() -> Part:
    """
    Gera a parede lateral trapezoidal com o perfil físico correto.
    A base é 400mm e o topo é menor.
    """
    z_top = cfg.CONFIG["ALT_PAREDE"] # 110
    comp = cfg.CONFIG["COMP_TOTAL"] # 400
    chanfro_x = cfg.CONFIG["CHANFRO_X"] # 55
    chanfro_z = cfg.CONFIG["CHANFRO_Z"] # 70
    z_subida = z_top - chanfro_z # 110 - 70 = 40 (onde termina a subida vertical da base)
    
    # 6 Pontos do Perfil (Origem X=0 no centro, base no Z=0)
    # A base tem 400mm de comprimento tocando o chão.
    # O topo (Z=110) começa só depois de recuar 55mm no eixo X de cada lado.
    # E a altura de 70mm é onde o chanfro morre nas pontas.
    pts = [
        (-comp/2 + chanfro_x, z_top),                    # Topo Traseiro (-145, 110)
        (comp/2 - chanfro_x, z_top),                     # Topo Dianteiro (145, 110)
        (comp/2, chanfro_z),                             # Quina de transição dianteira (200, 70)
        (comp/2, 0),                                     # Quina Inferior Dianteira (200, 0)
        (-comp/2, 0),                                    # Quina Inferior Traseira (-200, 0)
        (-comp/2, chanfro_z)                             # Quina de transição traseira (-200, 70)
    ]
    
    with BuildPart() as parede:
        with BuildSketch(Plane.XZ):
            Polygon(*pts)
            
            # Oblongo (Slot) para tensionamento apenas na catraca Superior Dianteira (índice 2)
            with Locations((med.FUROS_RODAS[2][0], med.FUROS_RODAS[2][1])):
                SlotOverall(med.LARG_OBLONGO, med.ALT_OBLONGO, mode=Mode.SUBTRACT)
                
            # Furos fixos (8mm para passar o eixo M8) nas catracas livres fixas (índices 1 e 3)
            with Locations((med.FUROS_RODAS[1][0], med.FUROS_RODAS[1][1]),
                           (med.FUROS_RODAS[3][0], med.FUROS_RODAS[3][1])):
                Circle(8.5 / 2, mode=Mode.SUBTRACT) # Furo com folga para M8
                
            # Furo central do Motor Johnson (Traseira Superior)
            with Locations((med.FUROS_RODAS[0][0], med.FUROS_RODAS[0][1])):
                Circle(med.DIAM_RESSALTO / 2 + 1.0, mode=Mode.SUBTRACT)
                # 6 furos M4 para fixar o motor (raio 14mm)
                with PolarLocations(14.0, 6):
                    Circle(2.0, mode=Mode.SUBTRACT)
                
        extrude(amount=cfg.CONFIG["ESPESSURA_MADEIRA"] / 2, both=True)
        
    return parede.part

def criar_paredes() -> Part:
    """
    Retorna o conjunto (Esquerda e Direita) já na cor Cinza Escuro.
    """
    parede_dir = _gerar_perfil_parede()
    parede_esq = _gerar_perfil_parede()
    
    # y_esq define a posição central da parede no eixo Y.
    y_esq = cfg.CONFIG["LARG_EXTERNA"] / 2 - cfg.CONFIG["ESPESSURA_MADEIRA"] / 2
    
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