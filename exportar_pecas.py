"""
===============================================================================
ROBÔ DE INSPEÇÃO - EXPORTAÇÃO AUTOMÁTICA DE MODELOS (.STEP / .STL)
===============================================================================
Script para exportar as peças estruturais e funcionais em:
- .STL (Pronto para fatiamento FDM em PETG)
- .STEP (Normalizado para manufatura / usinagem / CAD industrial)
===============================================================================
"""

import os
import sys
from build123d import export_step, export_stl

from pecas_impressas import (
    chassi_banheira,
    tampa_superior,
    roda_motriz,
    roda_livre,
    suporte_eletronica,
)

def exportar_todas():
    pasta_export = os.path.join(os.path.dirname(__file__), "exportacoes")
    os.makedirs(pasta_export, exist_ok=True)

    print(">>> Iniciando exportação dos modelos definitivos do Robô de Inspeção...")

    pecas = [
        ("chassi_banheira_robo_inspecao", chassi_banheira.criar_chassi()),
        ("carenagem_superior_stealth", tampa_superior.criar_tampa_superior()),
        ("polia_motriz_traseira", roda_motriz.criar_roda_motriz()),
        ("polia_livre_central_dianteira", roda_livre.criar_roda_livre()),
        ("suporte_interna_eletronica", suporte_eletronica.criar_suporte_eletronica()),
    ]

    for nome, objeto in pecas:
        caminho_step = os.path.join(pasta_export, f"{nome}.step")
        caminho_stl = os.path.join(pasta_export, f"{nome}.stl")

        print(f"Exportando {nome}...")
        export_step(objeto, caminho_step)
        export_stl(objeto, caminho_stl)

    print(f">>> Sucesso! 5 componentes exportados em .STEP e .STL na pasta '{pasta_export}'!")

if __name__ == "__main__":
    exportar_todas()
