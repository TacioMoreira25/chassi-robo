"""
===============================================================================
THE IRON VANGUARD UGV - PONTO DE ENTRADA PRINCIPAL (MAIN)
===============================================================================
Projeto: Veículo Terrestre Não Tripulado sobre Esteiras de Pneu MTB (UGV)
Visualizador: OCP CAD Viewer (Extensão VS Code)
Árvore Didática: 6 Subsistemas Principais Independentes e Numerados
===============================================================================
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from ocp_vscode import show, set_viewer_config
import montagem
import pinagem_eletronica as pin

def executar_visualizacao():
    print("=" * 75)
    print("       THE IRON VANGUARD UGV - SISTEMA CAD PARAMÉTRICO (build123d)")
    print("=" * 75)
    
    # Exibe especificações mecatrônicas e pinagem oficial no terminal
    pin.imprimir_relatorio_eletrico()
    
    print("\n[1/3] Construindo subsistemas hierárquicos e didáticos...")
    sub = montagem.montar_subsistemas()
    
    print("[2/3] Configurando iluminação e perspectiva no visualizador OCP...")
    try:
        set_viewer_config(
            default_opacity=0.92,
            grid=(True, False, False),
            axes=True,
            ortho=False
        )
        
        print("[3/3] Enviando os 6 subsistemas estruturados para o OCP CAD Viewer...")
        show(
            sub["carenagem"],
            sub["chassi"],
            sub["bandeja"],
            sub["eletronica"],
            sub["tracao_esq"],
            sub["tracao_dir"],
            names=[
                "1. Carenagem Superior Stealth (Torre FPV)",
                "2. Chassi Banheira (Glacis e Grelhas)",
                "3. Bandeja Interna (PETG)",
                "4. Circuitos Eletronicos (L298N, LM2596, 3S)",
                "5. Trem de Rodagem Esquerdo",
                "6. Trem de Rodagem Direito"
            ]
        )
        
        print("\n" + "=" * 75)
        print(">>> SUCESSO! Modelo enviado ao OCP CAD Viewer com árvore didática.")
        print(">>>")
        print(">>> NAVEGAÇÃO NA BARRA LATERAL DO OCP CAD VIEWER:")
        print(">>> [1. Carenagem Superior] -> Clique no olho para ocultar a tampa e ver o interior.")
        print(">>> [2. Chassi Banheira]    -> Clique no olho para inspecionar os motores por trás.")
        print(">>> [3. Bandeja Interna]    -> Acomodação dos módulos eletrônicos.")
        print(">>> [4. Circuitos]          -> L298N, LM2596, ESP32-CAM e bateria 3S.")
        print(">>> [5 & 6. Trem de Rodagem]-> Rodas raiadas, côncavas e esteiras MTB.")
        print("=" * 75)
    except Exception as err:
        print(f"\n[AVISO OCP CAD VIEWER]: {err}")
        print("Certifique-se de que a extensão OCP CAD Viewer está ativa no VS Code.")
        print("Caso ocorra erro de lock, feche o VS Code ou remova ~/.ocpvscode.lock")

if __name__ == "__main__":
    executar_visualizacao()