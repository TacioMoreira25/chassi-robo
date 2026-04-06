from build123d import *
import config

def _gerar_perfil_base()-> Part:
    """ Extrusão do perfil 2D base (assoalho) """
    with BuildPart() as base:
        with BuildSketch(Plane.XY):
            with Locations((config.COMP_BAY / 2, 0)):
                Rectangle(config.COMP_BAY, config.LARG_LINGUA)
            with Locations((config.COMP_BAY + (config.COMP_CORPO / 2), 0)):
                Rectangle(config.COMP_CORPO, config.LARG_EXTERNA)
        extrude(amount=config.ESPESSURA_PISO)
    return base.part

def _aplicar_furos_tensionador(part: Part) -> Part:
    """ Furações frontais de fixação do tensionador """
    dist_frontais = [config.DIST_FRONTAIS_TENSIONADOR_1, config.DIST_FRONTAIS_TENSIONADOR_2]
    pos_y_furos = (config.LARG_LINGUA / 2) - config.RECUO_Y_TENSIONADOR
    
    with BuildPart() as subtraida:
        add(part)
        with BuildSketch(Plane.XY):
            with Locations(
                [(x, y) for x in dist_frontais for y in (pos_y_furos, -pos_y_furos)]
            ):
                Circle(radius=config.RAIO_FURO_M4)
        extrude(amount=config.ESPESSURA_PISO * 2, both=True, mode=Mode.SUBTRACT)
    return subtraida.part

def _aplicar_furos_paredes(part: Part) -> Part:
    """ Escareamentos de fixação vertical das paredes de madeira """
    y_ext = config.LARG_EXTERNA / 2 - config.ESPESSURA_PAREDE / 2
    y_ling= config.LARG_LINGUA / 2 - config.ESPESSURA_PAREDE / 2
    
    x_pos = [
        config.ESPESSURA_PAREDE / 2,                       # Frente Extrema
        config.COMP_BAY + config.ESPESSURA_PAREDE / 2,     # Frente Caixa
        config.COMP_BAY + (config.COMP_CORPO / 2),         # Divisória
        config.COMP_TOTAL - config.ESPESSURA_PAREDE / 2    # Atrás
    ]
    
    with BuildPart() as montada:
        add(part)
        with BuildSketch(Plane.XY):
            with Locations(
                [(x_pos[0], y) for y in (y_ling, -y_ling)],                # Ponta menor
                [(x, y) for x in x_pos[1:] for y in (y_ext, -y_ext)]       # Caixa larga
            ):
                Circle(radius=config.RAIO_FURO_BASE)
        extrude(amount=config.ESPESSURA_PISO * 2, both=True, mode=Mode.SUBTRACT)
    return montada.part

def criar_chapa_base():
    """ Orquestra a montagem geométrica e furos da chapa base """
    chapa = _gerar_perfil_base()
    chapa = _aplicar_furos_tensionador(chapa)
    chapa = _aplicar_furos_paredes(chapa)
    return chapa

if __name__ == "__main__":
    from ocp_vscode import show
    chapa = criar_chapa_base()
    show(chapa, names=["Chapa Base (Assoalho)"], colors=["#d2b48c"])