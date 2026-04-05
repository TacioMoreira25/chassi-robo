# main.py completo e modular
from build123d import *
from ocp_vscode import show

# Importando os módulos locais
import config
from pecas_madeira import chapa_base, paredes
# from pecas_impressas import suporte_motor # Descomente quando voltarmos aos motores

# --- 1. Geração das Peças Separadas ---
assoalho_com_furos = chapa_base.criar_chapa_base()
paredes_madeira = paredes.criar_paredes()

# --- 2. Renderização Agrupada mas Separada ---
# Ao passar como objetos separados no show(), eles aparecem individuais na árvore ("Group")
show(
    assoalho_com_furos,
    paredes_madeira,
    names=["1. Chapa Base (Furos Dianteiros)", "2. Paredes de Madeira"],
    colors=["#d2b48c", "#d2b48c"], # Tons diferentes de madeira para distinguir
    alphas=[1.0, 1.0] # Paredes levemente transparentes para ajudar na inspeção
)