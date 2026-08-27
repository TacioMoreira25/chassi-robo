from build123d import *
from ocp_vscode import show

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from pecas_madeira.paredes import _gerar_perfil_parede
from pecas_mecanicas.motor_johnson import criar_motor_johnson
from pecas_mecanicas.catraca_18t import criar_catraca_com_bucha
from pecas_mecanicas.flange_coupling import criar_flange_coupling

def visualizar_catalogo():
    """
    Exibe as peças individuais isoladas, lado a lado, para visualização de catálogo.
    Não altera absolutamente nada na montagem principal do chassi.
    """
    # 1. Parede Lateral Isolada (desconectada do chassi)
    parede_isolada = _gerar_perfil_parede()
    # Pinta de uma cor diferente para destaque
    parede_isolada.color = Color("#8b5a2b") 
    
    # 2. Motor Johnson
    motor = criar_motor_johnson()
    
    # 3. Catraca 18T com Bucha
    catraca = criar_catraca_com_bucha()
    
    # 4. Flange Acoplador (Novo da sua foto!)
    flange = criar_flange_coupling()
    
    # Vamos espaçar elas no eixo Y para criar um "mostruário" flutuante
    distancia_separacao = 150
    
    catalogo = Compound(label="Catálogo de Peças (Isoladas)", children=[
        parede_isolada.moved(Location((0, -distancia_separacao, 0))),
        catraca.moved(Location((0, 0, 50))),
        motor.moved(Location((0, distancia_separacao, 50))),
        flange.moved(Location((0, distancia_separacao * 2, 50)))
    ])
    
    return catalogo

if __name__ == "__main__":
    catalogo = visualizar_catalogo()
    print("Enviando catálogo isolado de peças para o OCP CAD Viewer...")
    show(catalogo, names=["Catálogo de Componentes"])
    print("Pronto! Peças exibidas separadamente.")
