from build123d import *
from pecas_madeira import chapa_base, paredes
from pecas_impressas import suporte_motor
from pecas_mecanicas import motor_rs555
import config
import medidas
import os

def montar_chassi():
    """ Agrega e retorna as sub-montagens do chassi completo """
    assoalho = chapa_base.criar_chapa_base()
    paredes_laterais = paredes.criar_paredes()
    suporte = suporte_motor.criar_suporte_motor()
    
    # Adicionando visualização dos motores
    try:
        motor_model = motor_rs555.criar_motor()
        
        pos_motor_x_real = medidas.POS_X_MOTOR_REAL 
        centro_z_real = config.ESPESSURA_PISO + (config.ALT_PAREDE / 2)
        y_centro_peca = (medidas.LARG_LINGUA / 2) - medidas.RECUO_Y_MOTOR

        # X=90 faz o eixo apontar pro eixo negativo Y (lado direito do robô, para fora da caixa)         
        loc_direito = Location((pos_motor_x_real, -y_centro_peca, centro_z_real), (90, 0, 0))
        motor_direito = motor_model.moved(loc_direito * Location((0, 0, -28.5))) # -57/2 = -28.5
        
        # X=-90 faz o eixo apontar pro eixo positivo Y (lado esquerdo do robô, para fora da caixa)
        loc_esquerdo = Location((pos_motor_x_real, y_centro_peca, centro_z_real), (-90, 0, 0))
        motor_esquerdo = motor_model.moved(loc_esquerdo * Location((0, 0, -28.5)))
                
        motores = Compound(label="Motores", children=[motor_direito, motor_esquerdo])
    except Exception as e:
        print(f"Erro ao carregar o motor dummy: {e}")
        motores = Compound(label="Motor Dummy", children=[])
    
    chassi_global = Compound(label="Chassi Global", children=[
        assoalho, 
        paredes_laterais, 
        suporte,
        motores
    ])
    
    return assoalho, paredes_laterais, suporte, motores, chassi_global
