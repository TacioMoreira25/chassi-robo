from build123d import *
import math
import config as cfg
import medidas as med

from pecas_madeira import chapa_base, paredes, travessas
from pecas_mecanicas import motor_johnson, catraca_18t, eixos

def montar_chassi() -> Compound:
    """
    Realiza a montagem global do Creative Home Tank perfeitamente alinhada.
    """
    # --- CHAPAS DE MADEIRA ---
    espessura = cfg.CONFIG["ESPESSURA_MADEIRA"]
    z_teto = cfg.CONFIG["ALT_PAREDE"]
    
    # A base do robô (que na verdade é o teto) vai para o topo!
    base = chapa_base.criar_chapa_base().moved(Location((0, 0, z_teto)))
    
    # As paredes laterais ficam apoiadas no chão (Z=0)
    parede_conj = paredes.criar_paredes()
    
    # As travessas são coladas por baixo do teto (Z = z_teto - altura_delas)
    z_travessas = z_teto - cfg.CONFIG["ALT_TRAVESSA"]
    travessas_conj = travessas.criar_travessas().moved(Location((0, 0, z_travessas)))
    
    # --- CATRACAS ---
    catraca_livre = catraca_18t.criar_catraca_com_bucha()
    catraca_motriz = catraca_18t.criar_catraca_motriz()
    
    y_parede_dir = -cfg.CONFIG["LARG_EXTERNA"] / 2
    y_parede_esq = cfg.CONFIG["LARG_EXTERNA"] / 2
    
    catracas_lista = []
    
    for i, (x_centro, z_centro_rel) in enumerate(med.FUROS_RODAS):
        z_centro = z_centro_rel
        
        # Se for o furo 0, é a motriz. Se não, é a livre.
        if i == 0:
            modelo = catraca_motriz
        else:
            modelo = catraca_livre
            
        # A catraca livre fica "de costas", com a bucha (em +Z no modelo) voltada para a madeira.
        # Parede Direita (-Y): Queremos que o +Z da catraca aponte para +Y (Inwards). Rotation(-90,0,0)
        c_dir = modelo.moved(Rotation(-90, 0, 0))
        y_pos_dir = y_parede_dir - med.DIST_CATRACA_PAREDE - med.ESPESSURA_CATRACA / 2
        c_dir = c_dir.moved(Location((x_centro, y_pos_dir, z_centro)))
        
        # Parede Esquerda (+Y): Queremos que o +Z da catraca aponte para -Y (Inwards). Rotation(90,0,0)
        c_esq = modelo.moved(Rotation(90, 0, 0))
        y_pos_esq = y_parede_esq + med.DIST_CATRACA_PAREDE + med.ESPESSURA_CATRACA / 2
        c_esq = c_esq.moved(Location((x_centro, y_pos_esq, z_centro)))
        
        catracas_lista.extend([c_dir, c_esq])
        
    conjunto_catracas = Compound(label="Catracas 18T (x8)", children=catracas_lista)
    
    # --- MOTORES JOHNSON ---
    motor_modelo = motor_johnson.criar_motor_johnson()
    # O motor fica do lado de dentro.
    # Lado Direito (-Y): Corpo(-Z) aponta para dentro (+Y). Eixo(+Z) aponta para fora (-Y). -> Rotation(90, 0, 0)
    motor_dir = motor_modelo.moved(Rotation(90, 0, 0)) 
    # Lado Esquerdo (+Y): Corpo(-Z) aponta para dentro (-Y). Eixo(+Z) aponta para fora (+Y). -> Rotation(-90, 0, 0)
    motor_esq = motor_modelo.moved(Rotation(-90, 0, 0))
    
    y_int_dir = -cfg.CONFIG["LARG_INTERNA"] / 2
    y_int_esq = cfg.CONFIG["LARG_INTERNA"] / 2
    
    x_motriz = med.FUROS_RODAS[0][0]
    z_motriz = med.FUROS_RODAS[0][1]
    
    m_dir = motor_dir.moved(Location((x_motriz, y_int_dir, z_motriz)))
    m_esq = motor_esq.moved(Location((x_motriz, y_int_esq, z_motriz)))
    conjunto_motores = Compound(label="Motores Johnson (x2)", children=[m_esq, m_dir])
    
    # --- EIXOS E PORCAS (M8x75mm independentes) ---
    eixo_modelo = eixos.criar_eixo_m8()
    porca_modelo = eixos.criar_arruela_e_porca()
    
    # O eixo entra de fora para dentro. 
    # Lado Direito (-Y): Cabeça na catraca, corpo (+Z) entra para +Y. -> Rotation(-90, 0, 0)
    eixo_dir = eixo_modelo.moved(Rotation(-90, 0, 0))
    # A porca fica do lado de dentro (-Y) e face (+Z) aponta para +Y -> Rotation(-90, 0, 0)
    porca_dir = porca_modelo.moved(Rotation(-90, 0, 0))
    
    # Lado Esquerdo (+Y): Cabeça na catraca, corpo (+Z) entra para -Y. -> Rotation(90, 0, 0)
    eixo_esq = eixo_modelo.moved(Rotation(90, 0, 0))
    # Porca fica do lado de dentro (+Y) e face (+Z) aponta para -Y -> Rotation(90, 0, 0)
    porca_esq = porca_modelo.moved(Rotation(90, 0, 0))
    
    eixos_lista = []
    # Eixos nas 3 rodas livres (índices 1, 2, 3)
    for (x_centro, z_centro_rel) in med.FUROS_RODAS[1:]:
        z_centro = z_centro_rel
        # O parafuso M8 encosta a cabeça do lado de fora da catraca
        y_cabeca_dir = y_parede_dir - med.DIST_CATRACA_PAREDE - med.ESPESSURA_CATRACA
        e_d = eixo_dir.moved(Location((x_centro, y_cabeca_dir, z_centro)))
        p_d = porca_dir.moved(Location((x_centro, y_int_dir, z_centro)))
        
        y_cabeca_esq = y_parede_esq + med.DIST_CATRACA_PAREDE + med.ESPESSURA_CATRACA
        e_e = eixo_esq.moved(Location((x_centro, y_cabeca_esq, z_centro)))
        p_e = porca_esq.moved(Location((x_centro, y_int_esq, z_centro)))
        
        eixos_lista.extend([e_d, p_d, e_e, p_e])
        
    conjunto_eixos = Compound(label="Parafusos M8 e Porcas", children=eixos_lista)

    chassi_global = Compound(label="Creative Home Tank", children=[
        base, 
        travessas_conj,
        parede_conj, 
        conjunto_catracas,
        conjunto_motores,
        conjunto_eixos
    ])
    
    return chassi_global
