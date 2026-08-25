import montagem
from ocp_vscode import show

if __name__ == "__main__":
    print("Gerando montagem global do Robô UGV de Esteiras...")
    chassi = montagem.montar_chassi()
    
    print("Enviando modelo para o OCP CAD Viewer...")
    show(chassi, names=["Robo UGV Esteiras"])
    print("Modelo renderizado com sucesso!")