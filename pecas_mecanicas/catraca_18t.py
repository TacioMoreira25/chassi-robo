from build123d import *
import medidas as med

def criar_catraca_com_bucha() -> Compound:
    """
    Modelagem procedural da catraca 18T super detalhada e colorida!
    """
    raio_externo = med.DIAM_CATRACA / 2
    raio_interno = med.DIAM_FURO_CATRACA / 2
    espessura = med.ESPESSURA_CATRACA
    raio_base = raio_externo - 4.5 
    
    # 1. Anel Interno (Prata)
    with BuildPart() as anel_interno:
        with BuildSketch(Plane.XY):
            Circle(raio_interno + 2.0)
            Circle(raio_interno, mode=Mode.SUBTRACT)
            # 2 furos para ferramenta de remoção
            with PolarLocations(raio_interno + 1.0, 2):
                Circle(1.5, mode=Mode.SUBTRACT)
        extrude(amount=espessura - 2.0)
    
    anel_interno.part.color = Color("silver")
    
    # 2. Corpo Externo da Catraca (Dourado/Bronze)
    with BuildPart() as anel_externo:
        with BuildSketch(Plane.XY):
            Circle(raio_base)
            # Espaço para o anel interno e esferas
            Circle(raio_interno + 2.5, mode=Mode.SUBTRACT)
        extrude(amount=espessura)
        
    with BuildPart() as dentes:
        with BuildSketch(Plane.XY):
            with PolarLocations(raio_base, med.DENTES_CATRACA):
                # Dente curvo (tipo Shark fin)
                Polygon(
                    (0, -3.5),   # Base inferior
                    (4.5, -1.0), # Ponta inferior (mais fina)
                    (4.5, 1.0),  # Ponta superior
                    (2.0, 3.5),  # Curva de transição
                    (0, 4.0)     # Base superior
                )
        extrude(amount=espessura - 1.0) # Dentes levemente mais finos
        
    catraca_externa = anel_externo.part + dentes.part
    # --- Atribuição de Cores Realistas ---
    catraca_externa.color = Color("#222222")
    
    # 3. Bucha de Madeira Interna
    with BuildPart() as bucha:
        with BuildSketch(Plane.XY):
            Circle(med.OD_BUCHA / 2)
            Circle(med.ID_ROLAMENTO_608 / 2, mode=Mode.SUBTRACT)
        extrude(amount=med.ESPESSURA_BUCHA)
        
        with BuildSketch(Plane.XY.offset(med.ESPESSURA_BUCHA - med.PROF_REBAIXO_BUCHA)):
            Circle(med.DIAM_REBAIXO_BUCHA / 2)
        extrude(amount=med.PROF_REBAIXO_BUCHA, mode=Mode.SUBTRACT)
        
    bucha.part.color = Color("#111111") # Preto
        
    # Centralizando Z=0 no meio da espessura
    conj = Compound(label="Catraca 18T", children=[anel_interno.part, catraca_externa, bucha.part])
    return conj.moved(Location((0, 0, -espessura / 2)))

if __name__ == "__main__":
    from ocp_vscode import show
    c = criar_catraca_com_bucha()
    show(c)
