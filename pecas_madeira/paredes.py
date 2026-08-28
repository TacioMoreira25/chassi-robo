import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build123d import *
import config as cfg
import medidas as med

def _gerar_perfil_parede() -> Part:
    """
    Gera a parede lateral trapezoidal idêntica ao modelo real das fotos:
    - Base reto de 400mm no chão (Z=0).
    - Topo reto de 290mm a 110mm de altura (Z=110mm).
    - Transição nas pontas em Z=40mm (X=±200mm).
    """
    z_top = cfg.CONFIG["ALT_PAREDE"]              # 110.0 mm
    comp_topo = cfg.CONFIG["COMP_TOTAL"]          # 400.0 mm (Borda reta maior)
    comp_base = cfg.CONFIG["COMP_BASE"]           # 240.0 mm (Borda reta menor)
    chanfro_z = cfg.CONFIG["CHANFRO_Z"]           # 85.0 mm
    
    # 6 Pontos do Perfil Trapezoidal (Origem X=0, Z=0 na base menor centralizada)
    # Desenho na orientação correta (Topo = 400mm em Z=110, Base = 240mm em Z=0)
    pts = [
        (-comp_topo/2, z_top),             # Topo Traseiro (-200, 110)
        (comp_topo/2, z_top),              # Topo Dianteiro (200, 110)
        (comp_topo/2, chanfro_z),          # Quina lateral dianteira desce reta (200, 85)
        (comp_base/2, 0.0),                # Fundo Dianteiro, fim do chanfro (120, 0)
        (-comp_base/2, 0.0),               # Fundo Traseiro, início do chanfro (-120, 0)
        (-comp_topo/2, chanfro_z)          # Quina lateral traseira sobe reta (-200, 85)
    ]
    
    with BuildPart() as parede:
        with BuildSketch(Plane.XZ):
            Polygon(*pts)
            # 4 furos circulares de Ø=40mm para os suportes de rolamento/motor
            with Locations(med.FUROS_RODAS):
                Circle(med.DIAM_FURO_MADEIRA / 2, mode=Mode.SUBTRACT)
                
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