from montagem import montar_chassi
from ocp_vscode import show

assoalho_com_furos, paredes_madeira, suporte_motor_peca, motores, chassi_global = montar_chassi()

show(
    assoalho_com_furos,
    paredes_madeira,
    suporte_motor_peca,
    motores,
    names=["1. Chapa Base", "2. Paredes de Madeira", "3. Suporte do Motor", "4. Motores RS-555"],
    colors=["#d2b48c", "#d2b48c", "#a4101c", None], 
    alphas=[1.0, 1.0, 1.0, 1.0] # Canal alpha aplicado aos componentes de madeira
)