from build123d import *
import config
import medidas

def criar_suporte_motor():
    """Gera o corpo do suporte de motor (Peça de Impressão 3D)."""
    
    comp_x = medidas.COMP_SUPORTE_X 
    alt_z = config.ALT_PAREDE
    prof_y = medidas.PROF_SUPORTE_MOTOR
    raio_passante = medidas.RAIO_FURO_M4 + medidas.FOLGA_FURO_M4

    with BuildPart() as suporte_base:
        # Base sólida
        Box(comp_x, prof_y, alt_z)
        
        # Furo central livre do motor
        with BuildSketch(Plane.XZ):
            Circle(radius=medidas.DIAM_MOTOR / 2)
        extrude(amount=prof_y, both=True, mode=Mode.SUBTRACT)
        
        furos_motor_locs = [
            (medidas.DIST_X_FUROS_MOTOR, medidas.DIST_Z_FUROS_MOTOR), 
            (medidas.DIST_X_FUROS_MOTOR, -medidas.DIST_Z_FUROS_MOTOR),
            (-medidas.DIST_X_FUROS_MOTOR, medidas.DIST_Z_FUROS_MOTOR), 
            (-medidas.DIST_X_FUROS_MOTOR, -medidas.DIST_Z_FUROS_MOTOR)
        ]
        
        # Escareamentos para cabeças dos parafusos
        with BuildSketch(Plane.XZ.offset(-prof_y / 2)):
            with Locations(furos_motor_locs):
                Circle(radius=medidas.RAIO_REBAIXO_M4)
        extrude(amount=medidas.PROF_REBAIXO_M4, mode=Mode.SUBTRACT)

        # Furos passantes de fixação do motor
        with BuildSketch(Plane.XZ):
            with Locations(furos_motor_locs):
                Circle(radius=raio_passante)
        extrude(amount=prof_y, both=True, mode=Mode.SUBTRACT)

    # Posicionamento (Instâncias simétricas)
    pos_motor_x_real = medidas.POS_X_MOTOR_REAL 
    centro_z_real = config.ESPESSURA_PISO + (alt_z / 2)
    y_centro_peca = (medidas.LARG_LINGUA / 2) - medidas.RECUO_Y_MOTOR
    
    with BuildPart() as montagem:
        # Lado Direito
        with Locations((pos_motor_x_real, -y_centro_peca, centro_z_real)):
            add(suporte_base.part)
            
        # Lado Esquerdo
        with Locations((pos_motor_x_real, y_centro_peca, centro_z_real)):
            add(suporte_base.part, rotation=(0, 0, 180))
            
        # Subtrações de montagem no chassi
        margem_z = (alt_z / 2) - medidas.MARGEM_FURACOES_QUINA
        locs_y_base = ((medidas.LARG_LINGUA / 2) - medidas.RECUO_Y_TENSIONADOR, -((medidas.LARG_LINGUA / 2) - medidas.RECUO_Y_TENSIONADOR))
        locs_y_paredes = ((medidas.LARG_LINGUA / 2) - medidas.MARGEM_FURACOES_QUINA, -((medidas.LARG_LINGUA / 2) - medidas.MARGEM_FURACOES_QUINA))
        
        # Furos passantes no Assoalho
        with BuildSketch(Plane.XY.offset(config.ESPESSURA_PISO)):
            with Locations([(x, y) for x in (medidas.DIST_FRONTAIS_TENSIONADOR_1, medidas.DIST_FRONTAIS_TENSIONADOR_2) for y in locs_y_base]):
                Circle(radius=raio_passante)
        extrude(amount=medidas.CORTES_MONTAGEM_MOTOR, mode=Mode.SUBTRACT)
        
        # Furos passantes nas Paredes Frontais e Extremidades
        with BuildSketch(Plane.YZ.offset(config.ESPESSURA_PAREDE)):
            with Locations([(y, centro_z_real + z) for y in locs_y_paredes for z in (margem_z, -margem_z)]):
                Circle(radius=raio_passante)
        extrude(amount=medidas.CORTES_MONTAGEM_MOTOR, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.YZ.offset(config.COMP_BAY)):
            with Locations([(y, centro_z_real + z) for y in locs_y_paredes for z in (margem_z, -margem_z)]):
                Circle(radius=raio_passante)
        extrude(amount=-medidas.CORTES_MONTAGEM_MOTOR, mode=Mode.SUBTRACT)
            
    return montagem.part

if __name__ == "__main__":
    from ocp_vscode import show
    peca = criar_suporte_motor()
    show(peca, names=["Suporte Impresso (Motor)"], colors=["#e63946"])
