from build123d import *
import config

def criar_paredes():
    centro_z = config.ESPESSURA_PISO + (config.ALT_PAREDE / 2)
    y_esq = config.LARG_EXTERNA/2 - config.ESPESSURA_PAREDE/2
    y_dir = -y_esq
    
    # O corpo do chassi (caixa seca) vai de 76.2 até 406.4
    centro_x_caixa = config.COMP_BAY + (config.COMP_CORPO / 2)
    
    with BuildPart() as p:
        # 1. Vigas Laterais (Apenas no comprimento da caixa!)
        with Locations((centro_x_caixa, y_esq, centro_z), 
                       (centro_x_caixa, y_dir, centro_z)):
            Box(config.COMP_CORPO, config.ESPESSURA_PAREDE, config.ALT_PAREDE)

        # 2. Paredes Transversais
        # Parede Frontal Extrema (Na ponta da língua)
        with Locations((config.ESPESSURA_PAREDE/2, 0, centro_z)):
            Box(config.ESPESSURA_PAREDE, config.LARG_LINGUA, config.ALT_PAREDE)
            
        # Parede Frontal da Caixa (Logo atrás da língua livre)
        with Locations((config.COMP_BAY + config.ESPESSURA_PAREDE/2, 0, centro_z)):
            Box(config.ESPESSURA_PAREDE, config.LARG_INTERNA, config.ALT_PAREDE)
            
        # Parede do Fundo (A parede que estava faltando!)
        with Locations((config.COMP_TOTAL - config.ESPESSURA_PAREDE/2, 0, centro_z)):
            Box(config.ESPESSURA_PAREDE, config.LARG_INTERNA, config.ALT_PAREDE)
            
        # Divisória Central
        with Locations((centro_x_caixa, 0, centro_z)):
            Box(config.ESPESSURA_PAREDE, config.LARG_INTERNA, config.ALT_PAREDE)

        # 3. Furos Ovais (No fundo do robô, lado oposto da língua)
        pos_furos_ovais = config.COMP_TOTAL - 55.0
        with BuildSketch(Plane.XZ):
            with Locations((pos_furos_ovais, centro_z)):
                SlotOverall(width=63.0, height=25.0)
        extrude(amount=config.LARG_EXTERNA, both=True, mode=Mode.SUBTRACT)

        # 4. Furos na Parede Frontal Interna (Furo central grande e dois menores para os motores)
        pos_parede_interna = config.COMP_BAY + config.ESPESSURA_PAREDE/2
        dist_furos_pequenos = config.LARG_INTERNA/2 - 25.0  # Furos pequenos perto dos cantos
        with BuildSketch(Plane.YZ.offset(pos_parede_interna)):
            # Furo central para passar os cabos
            with Locations((0, centro_z)):
                Circle(radius=19.05)  # Furo aproximado de 38mm (mesmo da serra copo)
            # Dois furos pequenos nos cantos
            with Locations((dist_furos_pequenos, centro_z), (-dist_furos_pequenos, centro_z)):
                Circle(radius=2.0)  # Furo para parafusos
        extrude(amount=config.ESPESSURA_PAREDE, both=True, mode=Mode.SUBTRACT)

        # 5. Furos Ovais (Alças) nas paredes transversais (Apenas Divisória central)
        # Cortar a divisória central
        with BuildSketch(Plane.YZ.offset(centro_x_caixa)):
            with Locations((0, centro_z)):
                SlotOverall(width=63.0, height=25.0)
        extrude(amount=config.ESPESSURA_PAREDE, both=True, mode=Mode.SUBTRACT)

    return p.part