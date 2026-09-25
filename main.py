"""
===============================================================================
ROBÔ DE INSPEÇÃO - PONTO DE ENTRADA PRINCIPAL (MAIN)
===============================================================================
Projeto: Robô de Inspeção Terrestre sobre Esteiras de Pneu MTB
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
    print("       ROBÔ DE INSPEÇÃO - SISTEMA CAD PARAMÉTRICO (build123d)")
    print("=" * 75)
    
    # Exibe especificações mecatrônicas, pinagem e relatório geométrico no terminal
    pin.imprimir_relatorio_eletrico()
    import medidas
    medidas.imprimir_resumo_geometrico()
    
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
                "1. Carenagem Superior Stealth (Visão + Cooler 80mm + Painel)",
                "2. Chassi Banheira (Glacis 45° + Grelhas + Aletas)",
                "3. Bandeja Interna (PETG c/ Berço Central 3S)",
                "4. Circuitos Eletronicos (L298N, LM2596, ESP32-CAM, 3S)",
                "5. Trem de Rodagem Esquerdo",
                "6. Trem de Rodagem Direito"
            ]
        )
        
        print("\n" + "=" * 75)
        print(">>> SUCESSO! Robô de Inspeção enviado ao OCP CAD Viewer com árvore didática.")
        print(">>>")
        print(">>> NAVEGAÇÃO NA BARRA LATERAL DO OCP CAD VIEWER:")
        print(">>> [1. Carenagem Superior] -> Clique no olho para ocultar a tampa e ver o interior.")
        print(">>> [2. Chassi Banheira]    -> Clique no olho para inspecionar os motores e reforços.")
        print(">>> [3. Bandeja Interna]    -> Acomodação dos módulos e berço central da bateria.")
        print(">>> [4. Circuitos]          -> L298N, LM2596, ESP32-CAM e bateria 3S 18650.")
        print(">>> [5 & 6. Trem de Rodagem]-> Polias motrizes 60mm, livres 50mm e esteiras MTB.")
        print("=" * 75)
    except Exception as err:
        print(f"\n[AVISO OCP CAD VIEWER]: {err}")
        print("Certifique-se de que a extensão OCP CAD Viewer está ativa no VS Code.")
        print("Caso ocorra erro de lock, remova ~/.ocpvscode.lock")

if __name__ == "__main__":
    executar_visualizacao()