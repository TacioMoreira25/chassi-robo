from build123d import *
import config

def _construir_vigas(centro_z, centro_x_caixa, y_esq) -> Part:
    """ Gera as vigas longitudinais e transversais """
    with BuildPart() as base:
        with Locations((centro_x_caixa, y_esq, centro_z), (centro_x_caixa, -y_esq, centro_z)):
            Box(config.COMP_CORPO, config.ESPESSURA_PAREDE, config.ALT_PAREDE)
        
        crosses = [
            (config.ESPESSURA_PAREDE/2, config.LARG_LINGUA),
            (config.COMP_BAY + config.ESPESSURA_PAREDE/2, config.LARG_INTERNA),
            (config.COMP_TOTAL - config.ESPESSURA_PAREDE/2, config.LARG_INTERNA),
            (centro_x_caixa, config.LARG_INTERNA)
        ]
        
        for pos_x, larg in crosses:
            with Locations((pos_x, 0, centro_z)):
                Box(config.ESPESSURA_PAREDE, larg, config.ALT_PAREDE)
    return base.part

def _cortar_oblongos_rodas(part: Part, centro_z) -> Part:
    """ Cortes oblongos e furações para o eixo das rodas """
    pos_ovais = config.COMP_TOTAL - config.RECUO_OVAL_RODA
    sp_x, sp_z = config.SP_X_RODAS, config.SP_Z_RODAS
    
    with BuildPart() as montada:
        add(part)
        with BuildSketch(Plane.XZ):
            with Locations((pos_ovais, centro_z)):
                SlotOverall(width=config.LARG_OBLONGO_RODA, height=config.ALT_OBLONGO_RODA)
                with Locations([(x, y) for x in (sp_x, -sp_x) for y in (sp_z, -sp_z)]):
                    Circle(radius=config.RAIO_FURO_M4)
        extrude(amount=config.LARG_EXTERNA, both=True, mode=Mode.SUBTRACT)
    return montada.part

def _cortar_passagem_cabos(part: Part, centro_z) -> Part:
    """ Furos de passagem para cabeamento """
    pos_interna = config.COMP_BAY + config.ESPESSURA_PAREDE/2
    y_quina = config.LARG_LINGUA/2 - config.MARGEM_FURACOES_QUINA
    z_quina = config.ALT_PAREDE/2 - config.MARGEM_FURACOES_QUINA

    with BuildPart() as montada:
        add(part)
        with BuildSketch(Plane.YZ.offset(pos_interna)):
            with Locations((0, centro_z)):
                Circle(radius=config.RAIO_PASSAGEM_CABO)
            with Locations([(x, centro_z + y) for x in (y_quina, -y_quina) for y in (z_quina, -z_quina)]):
                Circle(radius=config.RAIO_FURO_M4)
        extrude(amount=config.ESPESSURA_PAREDE, both=True, mode=Mode.SUBTRACT)
    return montada.part

def _furo_oval_alca(part: Part, centro_z, centro_x_caixa) -> Part:
    """ Abertura central para alça de transporte """
    with BuildPart() as montada:
        add(part)
        with BuildSketch(Plane.YZ.offset(centro_x_caixa)):
            with Locations((0, centro_z)):
                SlotOverall(width=config.LARG_OVAL_ALCA, height=config.ALT_OVAL_ALCA)
        extrude(amount=config.ESPESSURA_PAREDE, both=True, mode=Mode.SUBTRACT)
    return montada.part

def _furos_motor_central(part: Part, centro_z, centro_x_caixa) -> Part:
    """ Furações de fixação (XZ) para o motor central """
    pos_motor = centro_x_caixa - config.RECUO_MOTOR
    sp_x, sp_z = config.DIST_X_FUROS_MOTOR, config.DIST_Z_FUROS_MOTOR

    with BuildPart() as montada:
        add(part)
        with BuildSketch(Plane.XZ):
            with Locations((pos_motor, centro_z)):
                Circle(radius=config.RAIO_EIXO_MOTOR)  
                with Locations([(x, y) for x in (sp_x, -sp_x) for y in (sp_z, -sp_z)]):
                    Circle(radius=config.RAIO_FURO_M4)  
        extrude(amount=config.LARG_EXTERNA, both=True, mode=Mode.SUBTRACT)
    return montada.part

def _furos_verticais_fixacao(part: Part, centro_z, y_esq) -> Part:
    """ Furos verticais (M5) para fixação da tampa superior """
    locs = [
        (config.COMP_BAY + config.ESPESSURA_PAREDE/2, y_esq),
        (config.COMP_TOTAL - config.ESPESSURA_PAREDE/2, y_esq)
    ]
    with BuildPart() as montada:
        add(part)
        with BuildSketch(Plane.XY.offset(centro_z + config.ALT_PAREDE/2)):
            with Locations([(x, y) for x, y_fix in locs for y in (y_fix, -y_fix)]):
                Circle(radius=config.RAIO_FURO_M5) # Raio maior (M5) teto
        extrude(amount=-config.ALT_PAREDE, mode=Mode.SUBTRACT)
    return montada.part

def _furos_tensionador_dianteiro(part: Part, centro_z) -> Part:
    """ Furações frontais (M4) para o módulo tensionador """
    d_y = config.LARG_LINGUA/2 - config.MARGEM_FURACOES_QUINA
    d_z = config.ALT_PAREDE/2 - config.MARGEM_FURACOES_QUINA
    
    with BuildPart() as subtraida:
        add(part)
        with BuildSketch(Plane.YZ.offset(0)):
            with Locations([(x, centro_z + y) for x in (d_y, -d_y) for y in (d_z, -d_z)]):
                Circle(radius=config.RAIO_FURO_M4)
        extrude(amount=config.ESPESSURA_PAREDE, both=True, mode=Mode.SUBTRACT)
    return subtraida.part

def criar_paredes():
    """ Gera o conjunto de chicanas e laterais estruturais """
    centro_z = config.ESPESSURA_PISO + (config.ALT_PAREDE / 2)
    y_esq = config.LARG_EXTERNA/2 - config.ESPESSURA_PAREDE/2
    centro_x_caixa = config.COMP_BAY + (config.COMP_CORPO / 2)
    
    # Executa o Pipeline Funcional (Adições -> Subtrações -> Finalização)
    p = _construir_vigas(centro_z, centro_x_caixa, y_esq)
    p = _cortar_oblongos_rodas(p, centro_z)
    p = _cortar_passagem_cabos(p, centro_z)
    p = _furo_oval_alca(p, centro_z, centro_x_caixa)
    p = _furos_motor_central(p, centro_z, centro_x_caixa)
    p = _furos_verticais_fixacao(p, centro_z, y_esq)
    p = _furos_tensionador_dianteiro(p, centro_z)
    return p