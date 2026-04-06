from build123d import *
import config

def criar_suporte_motor():
    """Gera o corpo do suporte de motor (Peça de Impressão 3D)."""
    
    comp_x = config.COMP_SUPORTE_X 
    alt_z = config.ALT_PAREDE
    prof_y = config.PROF_SUPORTE_MOTOR
    raio_passante = config.RAIO_FURO_M4 + config.FOLGA_FURO_M4

    with BuildPart() as suporte_base:
        # Base sólida
        Box(comp_x, prof_y, alt_z)
        
        # Furo central livre do motor
        with BuildSketch(Plane.XZ):
            Circle(radius=config.DIAM_MOTOR / 2)
        extrude(amount=prof_y, both=True, mode=Mode.SUBTRACT)
        
        furos_motor_locs = [
            (config.DIST_X_FUROS_MOTOR, config.DIST_Z_FUROS_MOTOR), 
            (config.DIST_X_FUROS_MOTOR, -config.DIST_Z_FUROS_MOTOR),
            (-config.DIST_X_FUROS_MOTOR, config.DIST_Z_FUROS_MOTOR), 
            (-config.DIST_X_FUROS_MOTOR, -config.DIST_Z_FUROS_MOTOR)
        ]
        
        # Escareamentos para cabeças dos parafusos
        with BuildSketch(Plane.XZ.offset(-prof_y / 2)):
            with Locations(furos_motor_locs):
                Circle(radius=config.RAIO_REBAIXO_M4)
        extrude(amount=config.PROF_REBAIXO_M4, mode=Mode.SUBTRACT)

        # Furos passantes de fixação do motor
        with BuildSketch(Plane.XZ):
            with Locations(furos_motor_locs):
                Circle(radius=raio_passante)
        extrude(amount=prof_y, both=True, mode=Mode.SUBTRACT)

    # Posicionamento (Instâncias simétricas)
    pos_motor_x_real = config.POS_X_MOTOR_REAL 
    centro_z_real = config.ESPESSURA_PISO + (alt_z / 2)
    y_centro_peca = (config.LARG_LINGUA / 2) - config.RECUO_Y_MOTOR
    
    with BuildPart() as montagem:
        # Lado Direito
        with Locations((pos_motor_x_real, -y_centro_peca, centro_z_real)):
            add(suporte_base.part)
            
        # Lado Esquerdo
        with Locations((pos_motor_x_real, y_centro_peca, centro_z_real)):
            add(suporte_base.part, rotation=(0, 0, 180))
            
        # Subtrações de montagem no chassi
        margem_z = (alt_z / 2) - config.MARGEM_FURACOES_QUINA
        locs_y_base = ((config.LARG_LINGUA / 2) - config.RECUO_Y_TENSIONADOR, -((config.LARG_LINGUA / 2) - config.RECUO_Y_TENSIONADOR))
        locs_y_paredes = ((config.LARG_LINGUA / 2) - config.MARGEM_FURACOES_QUINA, -((config.LARG_LINGUA / 2) - config.MARGEM_FURACOES_QUINA))
        
        # Furos passantes no Assoalho
        with BuildSketch(Plane.XY.offset(config.ESPESSURA_PISO)):
            with Locations([(x, y) for x in (config.DIST_FRONTAIS_TENSIONADOR_1, config.DIST_FRONTAIS_TENSIONADOR_2) for y in locs_y_base]):
                Circle(radius=raio_passante)
        extrude(amount=config.CORTES_MONTAGEM_MOTOR, mode=Mode.SUBTRACT)
        
        # Furos passantes nas Paredes Frontais e Extremidades
        with BuildSketch(Plane.YZ.offset(config.ESPESSURA_PAREDE)):
            with Locations([(y, centro_z_real + z) for y in locs_y_paredes for z in (margem_z, -margem_z)]):
                Circle(radius=raio_passante)
        extrude(amount=config.CORTES_MONTAGEM_MOTOR, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.YZ.offset(config.COMP_BAY)):
            with Locations([(y, centro_z_real + z) for y in locs_y_paredes for z in (margem_z, -margem_z)]):
                Circle(radius=raio_passante)
        extrude(amount=-config.CORTES_MONTAGEM_MOTOR, mode=Mode.SUBTRACT)
            
    return montagem.part

if __name__ == "__main__":
    from ocp_vscode import show
    peca = criar_suporte_motor()
    show(peca, names=["Suporte Impresso (Motor)"], colors=["#e63946"])
