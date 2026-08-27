from build123d import *
import medidas as med
from pecas_mecanicas.flange_coupling import criar_flange_coupling

def _gerar_base_catraca():
    raio_externo = med.DIAM_CATRACA / 2
    raio_interno = med.DIAM_FURO_CATRACA / 2
    espessura = med.ESPESSURA_CATRACA
    raio_base = raio_externo - 4.5 
    
    # 1. Anel Interno (Prata)
    with BuildPart() as anel_interno:
        with BuildSketch(Plane.XY):
            Circle(raio_interno + 2.0)
            Circle(raio_interno, mode=Mode.SUBTRACT)
            with PolarLocations(raio_interno + 1.0, 2):
                Circle(1.5, mode=Mode.SUBTRACT)
        extrude(amount=espessura - 2.0)
    
    anel_interno.part.color = Color("silver")
    
    # 2. Corpo Externo da Catraca (Dourado/Bronze/Preto)
    with BuildPart() as anel_externo:
        with BuildSketch(Plane.XY):
            Circle(raio_base)
            Circle(raio_interno + 2.5, mode=Mode.SUBTRACT)
        extrude(amount=espessura)
        
    with BuildPart() as dentes:
        with BuildSketch(Plane.XY):
            with PolarLocations(raio_base, med.DENTES_CATRACA):
                Polygon((0, -3.5), (4.5, -1.0), (4.5, 1.0), (2.0, 3.5), (0, 4.0))
        extrude(amount=espessura - 1.0)
        
    catraca_externa = anel_externo.part + dentes.part
    catraca_externa.color = Color("#222222")
    
    return anel_interno.part, catraca_externa

def criar_catraca_com_bucha() -> Compound:
    """Catraca Livre (com rolamento 608zz e bucha)"""
    anel_interno, catraca_externa = _gerar_base_catraca()
    espessura = med.ESPESSURA_CATRACA
    
    with BuildPart() as bucha:
        with BuildSketch(Plane.XY):
            Circle(med.OD_BUCHA / 2)
            Circle(med.ID_ROLAMENTO_608 / 2, mode=Mode.SUBTRACT)
        extrude(amount=med.ESPESSURA_BUCHA)
        with BuildSketch(Plane.XY.offset(med.ESPESSURA_BUCHA - med.PROF_REBAIXO_BUCHA)):
            Circle(med.DIAM_REBAIXO_BUCHA / 2)
        extrude(amount=med.PROF_REBAIXO_BUCHA, mode=Mode.SUBTRACT)
        
    bucha.part.color = Color("#111111")
    conj = Compound(label="Catraca Livre 18T", children=[anel_interno, catraca_externa, bucha.part])
    return conj.moved(Location((0, 0, -espessura / 2)))

def criar_catraca_motriz() -> Compound:
    """Catraca Motriz (com flange coupling de 6mm montado internamente)"""
    anel_interno, catraca_externa = _gerar_base_catraca()
    espessura = med.ESPESSURA_CATRACA
    
    # Adicionando o Flange Coupling no centro
    flange = criar_flange_coupling()
    
    # Criar uma chapa/disco de montagem interna (a que o usuario mostrou na foto)
    with BuildPart() as disco_montagem:
        with BuildSketch(Plane.XY):
            Circle(med.OD_BUCHA / 2) # Mesmo diametro externo pra caber na catraca
            Circle(3.2) # Furo central de 6.4mm pro eixo do motor passar folgado
            # 4 furos para parafusos cruzados
            with PolarLocations(10.0, 4, start_angle=45):
                Circle(1.6, mode=Mode.SUBTRACT)
        extrude(amount=2.0)
    disco_montagem.part.color = Color("silver")
    
    # O Flange fica colado no disco de montagem
    flange_posicionado = flange.moved(Location((0, 0, 2.0)))
    
    conj = Compound(label="Catraca Motriz 18T", children=[anel_interno, catraca_externa, disco_montagem.part, flange_posicionado])
    return conj.moved(Location((0, 0, -espessura / 2)))

if __name__ == "__main__":
    from ocp_vscode import show
    c_livre = criar_catraca_com_bucha()
    c_motriz = criar_catraca_motriz().moved(Location((100, 0, 0)))
    show(c_livre, c_motriz)
