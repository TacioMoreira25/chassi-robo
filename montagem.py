from build123d import *
import math
import config as cfg
import medidas as med

from pecas_madeira import chapa_base, paredes, travessas
from pecas_mecanicas import motor_johnson, catraca_18t, eixos
from pecas_impressas import suportes

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
    
    # --- SUPORTES E ROLAMENTOS ---
    suporte_rol = suportes.criar_suporte_rolamento()
    suporte_mot = suportes.criar_suporte_motor()
    rolamento_608 = eixos.criar_rolamento_608zz()
    
    # --- CATRACAS E MOTORES ---
    catraca_livre = catraca_18t.criar_catraca_com_bucha()
    catraca_motriz = catraca_18t.criar_catraca_motriz()
    motor_modelo = motor_johnson.criar_motor_johnson()
    eixo_modelo = eixos.criar_eixo_m8()
    porca_modelo = eixos.criar_arruela_e_porca()
    
    # Coordenadas internas e externas das paredes laterais de madeira
    y_int_dir = -cfg.CONFIG["LARG_INTERNA"] / 2   # -99.0 mm
    y_ext_dir = -cfg.CONFIG["LARG_EXTERNA"] / 2   # -111.0 mm
    y_int_esq = cfg.CONFIG["LARG_INTERNA"] / 2    # 99.0 mm
    y_ext_esq = cfg.CONFIG["LARG_EXTERNA"] / 2    # 111.0 mm
    
    # Coordenadas do centro das catracas no eixo Y (afastamento nominal)
    y_pos_dir = y_ext_dir - med.DIST_CATRACA_PAREDE - med.ESPESSURA_CATRACA / 2  # -131.5 mm
    y_pos_esq = y_ext_esq + med.DIST_CATRACA_PAREDE + med.ESPESSURA_CATRACA / 2  # 131.5 mm
    
    catracas_lista = []
    motores_lista = []
    suportes_lista = []
    rolamentos_lista = []
    eixos_lista = []
    
    for i, (x_centro, z_centro) in enumerate(med.FUROS_RODAS):
        if i == 0:
            # Roda Motriz (Johnson)
            # Lado Direito (-Y)
            s_d = suporte_mot.moved(Rotation(90, 0, 0)).moved(Location((x_centro, y_int_dir, z_centro)))
            m_d = motor_modelo.moved(Rotation(90, 0, 0)).moved(Location((x_centro, y_int_dir + 2.0, z_centro)))
            c_d = catraca_motriz.moved(Rotation(-90, 0, 0)).moved(Location((x_centro, y_pos_dir, z_centro)))
            
            # Lado Esquerdo (+Y)
            s_e = suporte_mot.moved(Rotation(-90, 0, 0)).moved(Location((x_centro, y_int_esq, z_centro)))
            m_e = motor_modelo.moved(Rotation(-90, 0, 0)).moved(Location((x_centro, y_int_esq - 2.0, z_centro)))
            c_e = catraca_motriz.moved(Rotation(90, 0, 0)).moved(Location((x_centro, y_pos_esq, z_centro)))
            
            suportes_lista.extend([s_d, s_e])
            motores_lista.extend([m_d, m_e])
            catracas_lista.extend([c_d, c_e])
        else:
            # Rodas Livres (Eixos Parafusados M8)
            # Lado Direito (-Y)
            s_d = suporte_rol.moved(Rotation(90, 0, 0)).moved(Location((x_centro, y_int_dir, z_centro)))
            r_d = rolamento_608.moved(Rotation(-90, 0, 0)).moved(Location((x_centro, y_ext_dir, z_centro)))
            
            y_cabeca_dir = y_pos_dir - med.ESPESSURA_CATRACA / 2
            e_d = eixo_modelo.moved(Rotation(-90, 0, 0)).moved(Location((x_centro, y_cabeca_dir, z_centro)))
            p_d = porca_modelo.moved(Rotation(-90, 0, 0)).moved(Location((x_centro, y_int_dir, z_centro)))
            c_d = catraca_livre.moved(Rotation(-90, 0, 0)).moved(Location((x_centro, y_pos_dir, z_centro)))
            
            # Lado Esquerdo (+Y)
            s_e = suporte_rol.moved(Rotation(-90, 0, 0)).moved(Location((x_centro, y_int_esq, z_centro)))
            r_e = rolamento_608.moved(Rotation(90, 0, 0)).moved(Location((x_centro, y_ext_esq, z_centro)))
            
            y_cabeca_esq = y_pos_esq + med.ESPESSURA_CATRACA / 2
            e_e = eixo_modelo.moved(Rotation(90, 0, 0)).moved(Location((x_centro, y_cabeca_esq, z_centro)))
            p_e = porca_modelo.moved(Rotation(90, 0, 0)).moved(Location((x_centro, y_int_esq, z_centro)))
            c_e = catraca_livre.moved(Rotation(90, 0, 0)).moved(Location((x_centro, y_pos_esq, z_centro)))
            
            suportes_lista.extend([s_d, s_e])
            rolamentos_lista.extend([r_d, r_e])
            eixos_lista.extend([e_d, p_d, e_e, p_e])
            catracas_lista.extend([c_d, c_e])
            
    conjunto_catracas = Compound(label="Catracas 18T (x8)", children=catracas_lista)
    conjunto_motores = Compound(label="Motores Johnson (x2)", children=motores_lista)
    conjunto_suportes = Compound(label="Suportes Impressos 3D (x8)", children=suportes_lista)
    conjunto_rolamentos = Compound(label="Rolamentos 608Z (x6)", children=rolamentos_lista)
    conjunto_eixos = Compound(label="Parafusos M8 e Porcas", children=eixos_lista)
    
    chassi_global = Compound(label="Creative Home Tank", children=[
        base, 
        travessas_conj,
        parede_conj, 
        conjunto_catracas,
        conjunto_motores,
        conjunto_suportes,
        conjunto_rolamentos,
        conjunto_eixos
    ])
    
    return chassi_global
