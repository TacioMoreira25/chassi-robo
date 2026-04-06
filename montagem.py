from build123d import *
from pecas_madeira import chapa_base, paredes
from pecas_impressas import suporte_motor

def montar_chassi():
    """ Agrega e retorna as sub-montagens do chassi completo """
    assoalho = chapa_base.criar_chapa_base()
    paredes_laterais = paredes.criar_paredes()
    motor = suporte_motor.criar_suporte_motor()
    
    chassi_global = Compound(label="Chassi Global", children=[
        assoalho, 
        paredes_laterais, 
        motor
    ])
    
    return assoalho, paredes_laterais, motor, chassi_global
