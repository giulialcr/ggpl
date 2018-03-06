from larlib import *

# metodo per la creazione del vetro trasparente
def hex_material(color, light, trasparence):
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return map(lambda x: x / 255., list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))

    params = hex_to_rgb(color) + [.1] + \
             hex_to_rgb(light) + [trasparence] + \
             hex_to_rgb(light) + [.1] + \
             hex_to_rgb("#000000") + [.1] + \
             [100]

    return MATERIAL(params)
window = CUBOID([1, 0.1, 1])
window = hex_material("#ffffff", "#ffffff", .4)(window)

def SEMISPHERE (radius):
	def SPHERE0 (subds):
		N , M = subds
		domain = Plasm.translate( Plasm.power(INTERVALS(PI/2)(N) , INTERVALS(2*PI)(M)), Vecf(0, -PI/2,0 ) )
		fx = lambda p: radius * math.cos(p[0]) * math.sin (p[1])
		fy = lambda p: radius * math.cos(p[0]) * math.cos (p[1])
		fz = lambda p: radius * math.sin(p[0])
		ret= MAP([fx, fy, fz])(domain)
		return ret
	return SPHERE0

#############
## FINESTRE ##
#############

def finestrasporgenzasuperiore(x, y, z):

    x_sporgenza = x
    y_sporgenza = y
    z_sporgenza = z

    # vettore dei punti
    V = [[0, 0, 0],  # 1 quadrato dx
         [0, y_sporgenza, 0],  # 2 quadrato dx
         [0, y_sporgenza, z_sporgenza],  # 3 quadrato dx
         [0, 0, z_sporgenza],  # 4 quadrato dx
         [0, y_sporgenza * 1.5, z_sporgenza],  # 5 triangolo dx
         [x_sporgenza, 0, 0],  # 6 quadrato sx
         [x_sporgenza, y_sporgenza, 0],  # 7 quadrato sx
         [x_sporgenza, y_sporgenza, z_sporgenza],  # 8 quadrato sx
         [x_sporgenza, 0, z_sporgenza],  # 9 quadrato sx
         [x_sporgenza, y_sporgenza * 1.5, z_sporgenza],  # 10 triangolo sx
         [0, 0, -z_sporgenza],  # 11 sotto dx
         [0, y_sporgenza, -z_sporgenza],  # 12 sotto dx
         [x_sporgenza, 0, -z_sporgenza],  # 13 sotto sx
         [x_sporgenza, y_sporgenza, -z_sporgenza]  # 14 sotto sx
         ]

    # link vertici
    sporgenza_rect = MKPOL([V, [[1, 4, 3, 5, 2], [6, 9, 8, 10, 7]], []])
    sporgenza_cub_rect = MKPOL([V, [[1, 2, 11, 12], [6, 7, 13, 14]], []])
    sporgenza_rect = JOIN(sporgenza_rect)
    sporgenza_cub_rect = JOIN(sporgenza_cub_rect)
    sporg_result = STRUCT([sporgenza_rect, sporgenza_cub_rect])
    return sporg_result
def finestra(x, y, z, sporgenza_type, tetto_boolean):

    #type==
    # 0 sporgenza lunga
    # 1 sporgenza corta a destra
    # 2 sporgenza corta a sinistra
    # 3 sporgenza corta


    # inizializzaione varie componenti finestra
    y = y * 0.3
    z_pali = z * 0.05
    x_palo_orizzontale = x
    z_palo_orizzontale = z * 0.05

    palo_superiore = COLOR(Colore_legno)(CUBOID([x, y * 0.5, z_pali]))
    palo_inferiore = COLOR(Colore_legno)(CUBOID([x, y, z_pali]))
    palo_orizzontale = COLOR(Colore_legno)(CUBOID([x_palo_orizzontale, y, z_palo_orizzontale]))

    x_palo_verticale = x * 0.05
    z_palo_verticale = z * 2.95
    palo_verticale = COLOR(Colore_legno)(CUBOID([x_palo_verticale, y, z_palo_verticale]))

    x_vetro_sopra = x * 0.45
    z_vetro_sopra = z * 1.15
    vetro_sopra = hex_material("#ffffff", "#ffffff", .4)(CUBOID([x_vetro_sopra, y, z_vetro_sopra]))

    x_vetro_sotto = x * 0.45
    z_vetro_sotto = z * 1.7
    vetro_sotto = hex_material("#ffffff", "#ffffff", .4)(CUBOID([x_vetro_sotto, y, z_vetro_sotto]))

    x_anta = x * 0.05
    y_anta = y * 2.3
    z_anta = z * 3
    ante = COLOR(Colore_legno)(CUBOID([x_anta, y_anta, z_anta]))
    # unione per finestra
    window = STRUCT([ante, T(1)(x_anta)(palo_inferiore),
                     T([1, 3])([x_anta, z_pali])(vetro_sotto),
                     T([1, 3])([x_anta + x_vetro_sotto, z_pali])(palo_verticale),
                     T([1, 3])([x_anta + x_vetro_sotto + x_palo_verticale, z_pali])(vetro_sotto),
                     T(1)(x_anta + x_vetro_sotto + x_palo_verticale + x_vetro_sotto)(ante),
                     T([1, 3])([x_anta, z_pali + z_vetro_sotto])(palo_orizzontale),
                     T([1, 3])([x_anta, z_pali + z_vetro_sotto + z_palo_orizzontale])(vetro_sopra),
                     T([1, 3])(
                         [x_anta + x_vetro_sopra + x_palo_verticale, z_pali + z_vetro_sotto + z_palo_orizzontale])(
                         vetro_sopra),
                     T([1, 3])([x_anta, z_pali + z_vetro_sotto + z_palo_orizzontale + z_vetro_sopra])(palo_superiore)])

    # creazione contorno della finestra
    y_contorno = y_anta * 0.9
    contorno = CUBOID([x * 1.3, y_contorno, z_anta + (x * 1.3 - SIZE(1)(window)) / 2])
    contorno = DIFFERENCE([contorno, T(1)((SIZE(1)(contorno) - SIZE(1)(window)) / 2)(S(2)(y * 10)(window))])
    contorno = STRUCT([window, T(1)(-(SIZE(1)(contorno) - SIZE(1)(window)) / 2)(contorno)])
    contorno = COLOR(Colore_mattone_2)(contorno)
    window = STRUCT([window, contorno])
    x_window = SIZE(1)(window)

    # inserimento sporgenza
    z_sporgenza = z * 0.05
    if sporgenza_type == 0:
        sporgenza = COLOR(GRAY)(CUBOID([x * 4.1, y * 1.6, z_sporgenza]))
        window = BOTTOM([window, sporgenza])

    if sporgenza_type == 1:
        sporgenza = COLOR(GRAY)(CUBOID([x * 2.9, y * 1.6, z_sporgenza]))
        window = STRUCT([window, T([1, 2, 3])([-x * 0.3, (SIZE(2)(window) - y * 1.6) / 2, -z_sporgenza])(sporgenza)])

    if sporgenza_type == 2:
        sporgenza = COLOR(GRAY)(CUBOID([x * 2.9, y * 1.6, z_sporgenza]))
        window = STRUCT([window, T([1, 2, 3])([-x * 1.5, (SIZE(2)(window) - y * 1.6) / 2, -z_sporgenza])(sporgenza)])

    if sporgenza_type == 3:
        sporgenza = COLOR(GRAY)(CUBOID([x * 1.2, y * 1.6, z_sporgenza]))
        window = BOTTOM([window, sporgenza])

    # aggiungere tetto piccolo sopra finestra
    if tetto_boolean == 1:
        z_sopra = z * 0.15
        sopra = COLOR(Colore_mattone_2)(CUBOID([x * 1.4, y_contorno * 1.1, z_sopra]))
        window = STRUCT(
            [window, T([1, 3])([-(x * 1.4 - x_window) / 2 - x * 0.25 / 2, SIZE(3)(window) - z_sporgenza])(sopra)])
        pilastro = finestrasporgenzasuperiore(x * 1.8, y_contorno * 0.5, z_sopra / 2)
        pilastro = COLOR(Colore_mattone_2)(
            T([1, 2, 3])([-z_sopra - x * 0.25, y_contorno * 0.7, SIZE(3)(window) - z_sporgenza + z_sopra / 2])(
                pilastro))
        window = STRUCT([window, pilastro])

    return window
def finestrella(x, y, z):
    y = y * 0.3
    x_contorno, z_contorno = x, z * 1.5

    # creo il contorno in pietra
    contorno = CUBOID([x_contorno, y * 1.95, z_contorno])
    contorno_pietra = CUBOID([x_contorno * 1.3, y * 1.8, z_contorno * 1.3])
    contorno_pietra = DIFFERENCE([contorno_pietra,
                                  T([1, 3])([(x_contorno * 1.3 - x_contorno) / 2, (z_contorno * 1.3 - z_contorno) / 2])(
                                      contorno)])
    contorno_pietra = COLOR(Colore_mattone_2)(contorno_pietra)
    x_dif_contorno, z_dif_contorno = x_contorno - 0.1, z_contorno - 0.1
    dif_contorno = CUBOID([x_dif_contorno, y * 1.95, z_dif_contorno])

    # creo la cornice in legno
    cornice = DIFFERENCE(
        [contorno, T([1, 3])([(x_contorno - x_dif_contorno) / 2, (z_contorno - z_dif_contorno) / 2])(dif_contorno)])
    cornice = COLOR(Colore_legno)(cornice)

    # creo le varie componenti della finestra
    x_palo = x * 0.05
    palo = CUBOID([x_palo, y, z_dif_contorno])
    x_vetro, z_vetro = (x_dif_contorno - x_palo) / 2, z_dif_contorno
    vetro = CUBOID([x_vetro, y, z_vetro])
    palo = COLOR(Colore_legno)(palo)
    vetro = hex_material("#ffffff", "#ffffff", .4)(vetro)
    vetro = STRUCT([vetro, T(1)(x_vetro)(palo), T(1)(x_vetro + x_palo)(vetro)])

    # assemblo il tutto
    finestra_result = STRUCT(
        [cornice, T([1, 3])([(x_contorno - x_dif_contorno) / 2, (z_contorno - z_dif_contorno) / 2])(vetro),
         T([1, 2, 3])([-(x_contorno * 1.3 - x_contorno) / 2, y * 0.2, -(z_contorno * 1.3 - z_contorno) / 2])(
             contorno_pietra)])
    return finestra_result
def finestrella2(x, y, z, aperta, con_maniglia):
    #conmaniglia=1 se ha maniglia 0 altrimenti
    #aperta=1 se finestra aperta 0 se chiusa

    bordo_x, bordo_z = x, z * 1.2

    # creazione bordo finestra
    contorno = CUBOID([bordo_x, y * 0.6, bordo_z])
    bordo_x_diff, bordo_z_diff = bordo_x - (x * 0.1), bordo_z - (z * 0.1)
    app_z = bordo_z / 3.0
    app_y = y * 0.4

    # creazione bordo con materiale
    grandezza_piccola = COLOR(Colore_mattone)(mattoncino([x * 0.2, app_y, app_z], 0))
    grandezza_media = COLOR(Colore_mattone)(mattoncino([x * 0.4, app_y, app_z], 0))
    grandezza_estesa = muro_mattoncini([x * 1.8, app_y, z * 0.3], 5, 1)

    y2 = y * 0.2
    p1 = T([1, 2])([bordo_x, y2])(grandezza_piccola)
    p2 = T([1, 2, 3])([bordo_x, y2, app_z])(grandezza_media)
    p3 = T([1, 2, 3])([bordo_x, y2, app_z * 2])(grandezza_piccola)
    p4 = T([1, 2, 3])([-x * 0.4, y2, app_z * 3])(grandezza_estesa)
    p5 = T([1, 2])([-x * 0.2, y2])(grandezza_piccola)
    p6 = T([1, 2, 3])([-x * 0.4, y2, app_z])(grandezza_media)
    p7 = T([1, 2, 3])([-x * 0.2, y2, app_z * 2])(grandezza_piccola)
    piastrelle = STRUCT([p1, p2, p3, p4, p5, p6, p7])

    if aperta == 0:
        bordo_diff = CUBOID([bordo_x_diff, y * 0.6, bordo_z_diff])
        cornice = DIFFERENCE(
            [contorno, T([1, 3])([(bordo_x - bordo_x_diff) / 2, (bordo_z - bordo_z_diff) / 2])(bordo_diff)])
        cornice = COLOR(Colore_legno)(cornice)
        vetro = hex_material("#ffffff", "#ffffff", .4)(CUBOID([bordo_x_diff, y * 0.3, bordo_z_diff]))
        piastrella = T([1, 2, 3])([-x * 0.4, y2, -z * 0.3])(grandezza_estesa)
        piastrelle = STRUCT([piastrella, piastrelle])

        finestra_result = STRUCT([cornice, piastrelle,
                           T([1, 3])([(bordo_x - bordo_x_diff) / 2, (bordo_z - bordo_z_diff) / 2])(vetro)])

    #finestra aperta
    else:
        y = y * 0.5

        #porta
        p_sopra = COLOR(Colore_legno)(CUBOID([x, y, z * 0.05]))
        zp = z * 0.15
        p_inferiore = COLOR(Colore_legno)(CUBOID([x, y, zp]))

        p_verticale_x = x * 0.05
        p_verticale_z = z * 1.3
        palo_verticale = COLOR(Colore_legno)(mattoncino([p_verticale_x, y * 1.01, p_verticale_z], 0))
        p_verticale_x = x * 0.1

        if x < z:
            antax = x * 0.1
            antaxz = z * 0.1
        else:
            antax = z * 0.1
            antaxz = x * 0.1

        vetrox = x * 0.35 + antaxz - antax
        vetroz = p_verticale_z
        vetro = hex_material("#ffffff", "#ffffff", .4)(CUBOID([vetrox, y, vetroz]))

        antaz = vetroz
        ante = COLOR(Colore_legno)(CUBOID([antax, y, antaz]))

        # assemblo la porta
        finestra_result = STRUCT([p_inferiore, T(3)(zp)(ante),
                           T([1, 3])([antax, zp])(vetro),
                           T([1, 3])([antax + vetrox, zp])(palo_verticale),
                           T([1, 3])([antax + vetrox + x * 0.05, zp])(palo_verticale),
                           T([1, 3])([antax + vetrox + p_verticale_x, zp])(vetro),
                           T([1, 3])([antax + vetrox + p_verticale_x + vetrox, zp])(ante),
                           T(3)([zp + antaz])(p_sopra)])
        grandezza_media = COLOR(Colore_mattone)(mattoncino([x * 0.4, app_y, z * 0.3], 0))
        piastrelle = T(3)(z * 0.3)(piastrelle)
        piastrella = STRUCT(
            [T([1, 2, 3])([bordo_x, y2])(grandezza_media), T([1, 2, 3])([-x * 0.4, y2])(grandezza_media)])
        piastrelle = STRUCT([piastrella, piastrelle])

        # assemblo la finestra con le piastrelle e con la maniglia
        finestra_result = STRUCT([piastrelle, finestra_result])
        if con_maniglia == 1:
            man = maniglia(x / 14.0, y / 8, z / 14.0)
            man2 = R([1, 2])(PI)(man)
            finestra_result = STRUCT([finestra_result,
                               T([1, 2, 3])([vetrox + antax + x * 0.02, y, z * 0.6])(man),
                               T([1, 2, 3])([vetrox + x * 0.08 + antax, y, z * 0.6])(man),
                               T([1, 3])([vetrox + antax + x * 0.02, z * 0.6])(man2),
                               T([1, 3])([vetrox + x * 0.08 + antax, z * 0.6])(man2)
                               ])
    return finestra_result
def finestrarco(x, y, z):
    curva_esterna=BEZIER(S1)([[x*0,z*0],[x*0.5,z*2],[x*2.5,z*4],[x*4.5,z*2],[x*5,z*0]])
    curva_interna=BEZIER(S1)([[x*0.2,z*0],[x*0.5,z*1.8],[x*2.5,z*3.6],[x*4.5,z*1.8],[x*4.8,z*0]])
    curva_2D=BEZIER(S2)([curva_esterna,curva_interna])
    dominio=PROD([INTERVALS(1)(32),INTERVALS(1)(1)])
    curva_2D=MAP(curva_2D)(dominio)
    return PROD([curva_2D,QUOTE([y*0.5])])
def finestralaterale(x, y, z):
    curva_esterna=BEZIER(S1)([[x*0,z*0],[x*0.42,z*1.24],[x*1.4,z*2.08]])
    curva_interna=BEZIER(S1)([[x*1.4,z*0],[x*1.4,z*2.08]])
    curva_2D=BEZIER(S2)([curva_esterna,curva_interna])
    dominio=PROD([INTERVALS(1)(32),INTERVALS(1)(1)])
    curva_2D=MAP(curva_2D)(dominio)
    return PROD([curva_2D,QUOTE([y*0.5])])
def finestracentrale(x, y, z):
    curva_esterna=BEZIER(S1)([[x*0,z*2.2],[x*0.8,z*2.4],[x*1.6,z*2.2]])
    curva_interna=BEZIER(S1)([[x*0,z*0],[x*1.6,z*0]])
    curva_2D=BEZIER(S2)([curva_esterna,curva_interna])
    dominio=PROD([INTERVALS(1)(32),INTERVALS(1)(1)])
    curva_2D=MAP(curva_2D)(dominio)
    return PROD([curva_2D,QUOTE([y*0.5])])
def finestra2(x, y, z):
    finestra_curva_laterale_sx=hex_material("#ffffff", "#ffffff", .4)(JOIN(finestralaterale(x, y * 0.95, z)))
    finestra_curva_laterale_dx=COMP([T([1,3])([x*4.9,y*0.485]),R([1,3])(PI)])(finestra_curva_laterale_sx)
    aste=COLOR(Colore_legno)(CUBOID([x * 0.2, z * 2.2, y * 0.5]))
    finestra_centrale=finestracentrale(x, y * 0.95, z)
    finestra_centrale=hex_material("#ffffff", "#ffffff", .4)(JOIN(finestra_centrale))
    arc=COLOR(Colore_legno)(finestrarco(x, y, z))
    finestra_senza_asta_sotto=STRUCT([T([1,3])([0.1*x,y*0.013])(finestra_curva_laterale_sx),arc,finestra_curva_laterale_dx,T(1)(x*1.5)(aste),T(1)(x*3.3)(aste),T([1,3])([x*1.7,y*0.013])(finestra_centrale)])
    asta_sotto=COLOR(Colore_legno)(CUBOID([x * 5, z * 0.2, y * 0.5]))
    return DOWN([finestra_senza_asta_sotto,asta_sotto])


#############
## TETTO ##
#############


def vertici(x, y, z, add1, add2):
    #vertici per la creazione del tetto

    x_pilastro = x
    y_pilastro = y
    z_pilastro = z * 0.4
    x_pilastro2 = x_pilastro / 2
    z_pilastro2 = (x_pilastro2 / 4.1) / COS(PI / 6) * 2.2
    V = [[0, 0, 0],  # 1 quadrato dx
         [0, y_pilastro, 0],  # 2 quadrato dx
         [0, y_pilastro, z_pilastro],  # 3 quadrato dx
         [0, 0, z_pilastro],  # 4 quadrato dx
         [-y_pilastro + add1, y_pilastro * 2, z_pilastro],  # 5 triangolo dx
         [x_pilastro, 0, 0],  # 6 quadrato sx
         [x_pilastro, y_pilastro, 0],  # 7 quadrato sx
         [x_pilastro, y_pilastro, z_pilastro],  # 8 quadrato sx
         [x_pilastro, 0, z_pilastro],  # 9 quadrato sx
         [x_pilastro + y_pilastro - add2, y_pilastro * 2, z_pilastro],  # 10 triangolo sx
         [0, 0, -z_pilastro],  # 11 sotto dx
         [0, y_pilastro, -z_pilastro],  # 12 sotto dx
         [x_pilastro, 0, -z_pilastro],  # 13 sotto sx
         [x_pilastro, y_pilastro, -z_pilastro],  # 14 sotto sx
         [x_pilastro2, -(x_pilastro2 - (y_pilastro)), z_pilastro2 + z_pilastro],  # 15 tetto
         ]
    return V
def tettoia(x, y, z, murox, muroy):
    V = vertici(murox * 1.02, muroy * 1.1, z * 0.5, 0, 0)
    # base del tetto
    asserect = MKPOL([V, [[1, 4, 3, 5, 2], [6, 9, 8, 10, 7]], []])
    assecub = MKPOL([V, [[1, 2, 11, 12], [6, 7, 13, 14]], []])
    # tetto
    su = MKPOL([V, [[15, 10, 5]], []])
    asserect = COLOR(Colore_tegola)(JOIN(asserect))
    su = COLOR(Colore_tegola)(su)
    assecub = JOIN(assecub)
    tettoia_result = STRUCT([assecub, asserect, su])
    tetto_dx = COMP([T([1, 2])([muroy * 1.1, -murox * 1.02 + muroy * 1.1]), R([1, 2])(PI / 2)])(tettoia_result)
    tetto_su = COMP([T([1, 2])([murox * 1.02, -murox * 1.02 + muroy * 1.1 * 2]), R([1, 2])(PI)])(tettoia_result)
    tetto_sx = COMP([T([1, 2])([murox * 1.02 - muroy * 1.1, muroy * 1.1]), R([1, 2])(-PI / 2)])(tettoia_result)
    tettoia_result = STRUCT([tettoia_result, tetto_dx, tetto_su, tetto_sx])

    return tettoia_result
def tetto_ingresso(x, y, z, tetto_bool):

    x1 = x * 1.01
    x2 = x1 / 2
    y1 = y * 1.05
    z1 = z * 0.4
    z2 = (x2 / 4.1) / COS(PI / 6)

    V = [[0, 0, 0],  # 1 quadrato dx
         [0, y1, 0],  # 2 quadrato dx
         [0, y1, z1],  # 3 quadrato dx
         [0, 0, z1],  # 4 quadrato dx
         [0, y1 * 2, z1],  # 5 triangolo dx
         [x1, 0, 0],  # 6 quadrato sx
         [x1, y1, 0],  # 7 quadrato sx
         [x1, y1, z1],  # 8 quadrato sx
         [x1, 0, z1],  # 9 quadrato sx
         [x1, y1 * 2, z1],  # 10 triangolo sx
         [x2, 0, z2],  # 11 quadrato su
         [x2, y1, z2],  # 12 quadrato su
         [x2, y1, z2 + z1],  # 13 quadrato su
         [x2, 0, z2 + z1],  # 14 quadrato su
         [x2, y1 * 2, z2 + z1],  # 15 triangolo su
         [0, 0, -z1],  # 16 sotto dx
         [0, y1, -z1],  # 17 sotto dx
         [x1, 0, -z1],  # 18 sotto sx
         [x1, y1, -z1],  # 19 sotto sx
         [x2, 0, z2 - z1],  # 20 sotto su
         [x2, y1, z2 - z1],  # 21 sotto su
         [x2, -(x / (1.3 * 3.6)), z2 - (z1 * 1.5)],  # 22 tetto
         [y1, -(x / (1.3 * 3.6)), z2 - (z1 * 1.5)],  # 23 tetto
         [x1 - y1, -(x / (1.3 * 3.6)), z2 - (z1 * 1.5)],  # 24 tetto
         [y1, 0, z1],  # 25 tetto
         [x1 - y1, 0, z1]  # 26 tetto
         ]

    angolosx = MKPOL([V, [[6, 9, 8, 10, 7], [11, 14, 13, 15, 12]], []])
    angolosx2 = MKPOL([V, [[6, 7, 18, 19], [11, 12, 20, 21]], []])
    angolodx = MKPOL([V, [[1, 4, 3, 5, 2], [11, 14, 13, 15, 12]], []])
    angolodx2 = MKPOL([V, [[1, 2, 16, 17], [11, 12, 20, 21]], []])
    asse1 = MKPOL([V, [[1, 4, 3, 5, 2], [6, 9, 8, 10, 7]], []])
    asse2 = MKPOL([V, [[1, 2, 16, 17], [6, 7, 18, 19]], []])
    sfondo = MKPOL([V, [[4, 9, 11]], []])

    angolosx = JOIN(angolosx)
    angolosx2 = JOIN(angolosx2)
    angolodx = JOIN(angolodx)
    angolodx2 = JOIN(angolodx2)
    asse1 = JOIN(asse1)
    asse2 = JOIN(asse2)
    sfondo = COMP([T(1)(x1), R([1, 2])(PI)])(TEXTURE('./immagini/stemma.png')(JOIN(sfondo)))
    tetto_result = STRUCT([sfondo, angolosx, angolosx2, angolodx,
                       angolodx2, asse1, asse2])
    # tetto
    if tetto_bool == 1:
        angolosx = COLOR(Colore_tegola)(angolosx)
        angolodx = COLOR(Colore_tegola)(angolodx)
        tetto = COLOR(Colore_tegola)(STRUCT([JOIN(MKPOL([V, [[14, 22, 26]], []])), MKPOL([V, [[14, 25, 22]], []]),
                                             JOIN(MKPOL([V, [[22, 23, 25]], []])), JOIN(MKPOL([V, [[26, 24, 22]], []]))]))
        tetto = STRUCT(
            [tetto, angolosx, angolosx2, angolodx, angolodx2])
        tetto = T(3)(SIZE(3)(asse1) + SIZE(3)(asse2))(tetto)
        tetto_result = STRUCT([tetto_result, tetto])
    #VIEW(tetto_result)
    return tetto_result


#############
## SCALE ##
#############

def gradini(x, y, z, n):

    # crea una scalinata
    # n numero gradini

    gradinoy = y * 0.5
    gradinoz = z * 1.9
    gradinoz2 = gradinoz / n

    #si riducono le dimensioni singolari in funzione del numero dei gradini
    #si passa da gradino a scala

    def gradini2(i, diff_y, scale):
        if i >= n:
            return scale
        else:
            if scale == 1:
                gradinoy2 = gradinoy * 5

                # spiazzo prima della discesa
                gradino = CUBOID([x * 7, gradinoy2, gradinoz])
                lato = CUBOID([x * 0.5, gradinoy2, gradinoz * 1.05])
                gradino = RIGHT([lato, RIGHT([gradino, lato])])

                return gradini2(i + 1, gradinoy2, gradino)
            else:
                # struttura laterale
                discesalaterale = MKPOL([[[0, 0], [gradinoy, 0], [0, gradinoz2]], [[1, 2, 3]], [[]]])
                discesalaterale = PROD([discesalaterale, QUOTE([x * 0.5])])
                discesalaterale = COMP([R([1, 3])(-PI / 2), R([1, 2])(PI / 2)])(discesalaterale)
                colscala = TOP(
                    [CUBOID([x * 0.5, gradinoy, (gradinoz - (gradinoz2 * i)) * 1.05]), discesalaterale])

                gradino = CUBOID([x * 7, gradinoy, gradinoz - (gradinoz2 * i)])
                gradino = RIGHT([colscala, RIGHT([gradino, colscala])])
                scale = STRUCT([scale, T(2)(diff_y)(gradino)])

                return gradini2(i + 1, diff_y + gradinoy, scale)

    return gradini2
def scala(x, y, z, numgradini, dimgradino):
    #scala interna

    scalinoy = y
    scalinoz = z * 1.0
    scalinoz2 = scalinoz / numgradini

    def gradini1(i, diff_y, scala):
        if i >= numgradini:
            return scala
        else:
            if scala == 1:
                gradino = CUBOID([x, dimgradino, scalinoz])
                return gradini1(i + 1, dimgradino, gradino)
            else:

                gradino = CUBOID([x, scalinoy, scalinoz - (scalinoz2 * i)])
                scala = STRUCT([scala, T(2)(diff_y)(gradino)])
                return gradini1(i + 1, diff_y + scalinoy, scala)

    return gradini1
def semicirconferenza(x, y, z):
    x1 = lambda (u, v): v * cos(u)
    y1 = lambda (u, v): v * sin(u)

    dom = PROD([INTERVALS(PI)(32), INTERVALS(1)(32)])
    mapp = MAP([x1, y1])(dom)

    return JOIN(S([1, 2])([(x / 1.3), y])(PROD([mapp, QUOTE([z * 2.0 / 6.0])])))
def scale_cilindriche(x, y, z):
    # n numero gradini
    # i serve per mettere gli gradini uno sopra l'altro
    def scalini(n, scala, i):
        if n < 1:
            return scala
        else:
            scalino = semicirconferenza(x * (n + 2), y * (n + 2), z)
            if scala == 1:
                return scalini(n - 1, scalino, i + 2.0 / 6.0)
            else:
                scala = STRUCT([scala, T(3)(i)(scalino)])
                return scalini(n - 1, scala, i + 2.0 / 6.0)

    return scalini

#############
## PORTE ##
#############

def maniglia(x, y, z):
    x = x / 1.3
    curva_sx = BEZIER(S1)(
        [[x * 0, y * 0, z * 0], [x * 0, y * 2.4, z * 1], [x * 0, y * 2.4, z * 2], [x * 0, y * 2.4, z * 3],
         [x * 0, y * 0, z * 4.4]])
    curva_up = BEZIER(S1)(
        [[x * 0.2, y * 0, z * 0.2], [x * 0.2, y * 2.2, z * 1], [x * 0.2, y * 2.2, z * 2], [x * 0.2, y * 2.2, z * 3],
         [x * 0.2, y * 0, z * 4.2]])
    curva_2D = BEZIER(S2)([curva_sx, curva_up])

    curva_dx = BEZIER(S1)(
        [[-x * 0.2, y * 0, z * 0.2], [-x * 0.2, y * 2.2, z * 1], [-x * 0.2, y * 2.2, z * 2], [-x * 0.2, y * 2, z * 3],
         [-x * 0.2, y * 0, z * 4.2]])
    curva_down = BEZIER(S1)(
        [[x * 0, y * 0, z * 0.4], [x * 0, y * 2, z * 1], [x * 0, y * 2, z * 2], [x * 0, y * 2, z * 3],
         [x * 0, y * 0, z * 4]])
    curva_2D1 = BEZIER(S2)([curva_dx, curva_down])

    dominio1 = PROD([INTERVALS(1)(32), INTERVALS(1)(1)])

    curva_3D = BEZIER(S3)([curva_2D, curva_2D1])
    dominio3d = PROD([dominio1, QUOTE([1])])
    curva_3D = MAP(curva_3D)(dominio3d)
    return COLOR(Colore_legno_2)(curva_3D)
def porta_vetrata(x, y, z, bordo_bool, maniglia_bool):

    y = y * 0.5
    asse_inferiore_z = z * 0.15
    asse_laterale_x = x * 0.05
    asse_laterale_z = z * 2.8
    asse_superiore = COLOR(Colore_legno)(CUBOID([x, y, z * 0.05]))
    asse_inferiore = COLOR(Colore_legno)(CUBOID([x, y, asse_inferiore_z]))
    asse_laterale = COLOR(Colore_legno)(mattoncino([asse_laterale_x, y * 1.01, asse_laterale_z], 0))
    asse_laterale_x = x * 0.1


    if x < z:
        antax = x * 0.1
        antax_h = z * 0.1
    else:
        antax = z * 0.1
        antax_h = x * 0.1

    vetrata_x = x * 0.35 + antax_h - antax
    vetrata_z = asse_laterale_z
    vetro = hex_material("#ffffff", "#ffffff", .4)(CUBOID([vetrata_x, y, vetrata_z]))

    antaz = vetrata_z
    anta = COLOR(Colore_legno)(CUBOID([antax, y, antaz]))

    porta_vetrata_result = STRUCT([asse_inferiore, T(3)(asse_inferiore_z)(anta),
                   T([1, 3])([antax, asse_inferiore_z])(vetro),
                   T([1, 3])([antax + vetrata_x, asse_inferiore_z])(asse_laterale),
                   T([1, 3])([antax + vetrata_x + x * 0.05, asse_inferiore_z])(asse_laterale),
                   T([1, 3])([antax + vetrata_x + asse_laterale_x, asse_inferiore_z])(vetro),
                   T([1, 3])([antax + vetrata_x + asse_laterale_x + vetrata_x, asse_inferiore_z])(anta),
                   T(3)([asse_inferiore_z + antaz])(asse_superiore)])

    # bordo
    if x > 4:
        bordox = x * 1.15
    else:
        bordox = x * 1.5
    bordoy = y * 0.9
    portaz = SIZE(3)(porta_vetrata_result)
    portay = SIZE(2)(porta_vetrata_result)
    pietrax = (bordox - SIZE(1)(porta_vetrata_result)) / 2
    bordo = CUBOID([bordox, bordoy, portaz + pietrax])
    bordo = DIFFERENCE([bordo, T(1)((SIZE(1)(bordo) - SIZE(1)(porta_vetrata_result)) / 2)(S(2)(y * 10)(porta_vetrata_result))])
    bordo = STRUCT([porta_vetrata_result, T([1, 2])([-(SIZE(1)(bordo) - SIZE(1)(porta_vetrata_result)) / 2, portay - bordoy])(bordo)])
    bordo = COLOR(Colore_mattone_2)(bordo)


    porta_vetrata_result = STRUCT([porta_vetrata_result, bordo])

    if bordo_bool == 1:
        # inserimento tetto sulla finestra
        z2 = z * 0.15
        portax = SIZE(1)(porta_vetrata_result)
        x2 = x * 1.6
        sopra = COLOR(Colore_mattone_2)(CUBOID([x2, bordoy * 1.1, z2]))
        porta_vetrata_result = STRUCT(
            [porta_vetrata_result, T([1, 2, 3])([-pietrax - (x2 - portax) / 2, portay - bordoy, SIZE(3)(porta_vetrata_result)])(sopra)])
        assex = x * 2
        asse = finestrasporgenzasuperiore(assex, bordoy * 0.5, z2 / 2)
        asse = COLOR(Colore_mattone_2)(T([1, 2, 3])(
            [-pietrax - (assex - portax) / 2, bordoy * 0.7 + portay - bordoy,
             SIZE(3)(porta_vetrata_result) + z2 / 2])(asse))

        # unione
        porta_vetrata_result = STRUCT([porta_vetrata_result, asse])

    if maniglia_bool == 1:
        maniglie = maniglia(x / 14.0, y / 8, z / 14.0)
        maniglie2 = R([1, 2])(PI)(maniglie)
        porta_vetrata_result = STRUCT([porta_vetrata_result,
                       T([1, 2, 3])([vetrata_x + antax + x * 0.02, y, z * 1.8])(maniglie),
                       T([1, 2, 3])([vetrata_x + x * 0.08 + antax, y, z * 1.8])(maniglie),
                       T([1, 3])([vetrata_x + antax + x * 0.02, z * 1.8])(maniglie2),
                       T([1, 3])([vetrata_x + x * 0.08 + antax, z * 1.8])(maniglie2)
                       ])

    return porta_vetrata_result
def porta_legno(x, y, z, maniglia_bool, bordo_bool):
    # inizializzazione componenti porta

    texturelegno = './immagini/legno.jpg'
    assiz = z * 0.05
    y = y * 0.3
    asse_orizzontalex = x * 0.455
    asse_orizzontalez = z * 0.05
    asse_verticalex = x * 0.05
    asse_verticalez = z * 2.95
    superiorex = x * 0.45
    superiorez = z * 1.15
    inferiorex = x * 0.45
    inferiorez = z * 1.7
    antax = x * 0.05
    antaz = z * 3


    asse_superiore = COLOR(Colore_legno)(CUBOID([x, y, assiz]))
    asse_inferiore = COLOR(Colore_legno)(CUBOID([x, y, assiz]))
    asse_orizzontale = COLOR(Colore_legno)(CUBOID([asse_orizzontalex, y, asse_orizzontalez]))
    asse_verticale = COLOR(Colore_legno)(mattoncino([asse_verticalex, y, asse_verticalez], 0))
    superiore = TEXTURE(texturelegno)(mattoncino([superiorex, y, superiorez], 0))
    inferiore = TEXTURE(texturelegno)(mattoncino([inferiorex, y, inferiorez], 0))
    anta = COLOR(Colore_legno)(CUBOID([antax, y, antaz]))
    maniglie = maniglia(x / 14.0, y / 8, z / 14.0)

    # creazione struttura
    porta_legno_result = STRUCT([anta, T(1)(antax)(asse_inferiore),
                    T([1, 3])([antax, assiz])(inferiore),
                    T([1, 3])([antax + inferiorex, assiz])(asse_verticale),
                    T([1, 3])([antax + inferiorex + asse_verticalex, assiz])(asse_verticale),
                    T([1, 3])([antax + inferiorex + asse_verticalex * 2, assiz])(inferiore),
                    T(1)(antax + inferiorex + asse_verticalex * 2 + inferiorex)(anta),
                    T([1, 3])([antax, assiz + inferiorez])(asse_orizzontale),
                    T([1, 3])([antax + superiorex + asse_verticalex * 2 - x * 0.005, assiz + inferiorez])(
                        asse_orizzontale),
                    T([1, 3])([antax, assiz + inferiorez + asse_orizzontalez])(superiore),
                    T([1, 3])(
                        [antax + superiorex + asse_verticalex * 2, assiz + inferiorez + asse_orizzontalez])(
                        superiore),
                    T([1, 3])([antax, assiz + inferiorez + asse_orizzontalez + superiorez])(asse_superiore)])

    if bordo_bool == 1:
        # creo il bordo
        bordoy = y * 0.9
        portaz = SIZE(3)(porta_legno_result)
        portay = SIZE(2)(porta_legno_result)
        x2pietra = (x * 1.5 - SIZE(1)(porta_legno_result)) / 2
        bordo = CUBOID([x * 1.5, bordoy, portaz + x2pietra])
        bordo = DIFFERENCE(
            [bordo, T([1, 2])([(SIZE(1)(bordo) - SIZE(1)(porta_legno_result)) / 2, -y])(S(2)(y * 10)(porta_legno_result))])
        bordo = STRUCT(
            [porta_legno_result, T([1, 2])([-(SIZE(1)(bordo) - SIZE(1)(porta_legno_result)) / 2, portay - bordoy])(bordo)])
        bordo = COLOR(Colore_mattone_2)(bordo)
        porta_legno_result = STRUCT([porta_legno_result, bordo])

        # aggiunta tetto
        sup_z = z * 0.15
        portax = SIZE(1)(porta_legno_result)
        sup_x = x * 1.6
        sup = COLOR(Colore_mattone_2)(CUBOID([sup_x, bordoy * 1.1, sup_z]))
        porta_legno_result = STRUCT(
            [porta_legno_result, T([1, 2, 3])([-x2pietra - (sup_x - portax) / 2, portay - bordoy, SIZE(3)(porta_legno_result)])(sup)])
        assex = x * 2
        asse = finestrasporgenzasuperiore(assex, bordoy * 0.5, sup_z / 2)
        asse = COLOR(Colore_mattone_2)(T([1, 2, 3])(
            [-x2pietra - (assex - portax) / 2, bordoy * 0.7 + portay - bordoy,
             SIZE(3)(porta_legno_result) + sup_z / 2])(asse))

        # assemblo
        porta_legno_result = STRUCT([porta_legno_result, asse])

    if maniglia_bool == 1:
        maniglia2 = R([1, 2])(PI)(maniglie)
        porta_legno_result = STRUCT([porta_legno_result,
                        T([1, 2, 3])([antax + superiorex + asse_verticalex - x * 0.03, y,
                                      assiz + inferiorez + asse_orizzontalez])(maniglie),
                        T([1, 2, 3])([antax + superiorex + asse_verticalex + x * 0.03, y,
                                      assiz + inferiorez + asse_orizzontalez])(maniglie),
                        T([1, 3])([antax + superiorex + asse_verticalex - x * 0.03,
                                   assiz + inferiorez + asse_orizzontalez])(maniglia2),
                        T([1, 3])([antax + superiorex + asse_verticalex + x * 0.03,
                                   assiz + inferiorez + asse_orizzontalez])(maniglia2)])

    return porta_legno_result

############################
## MURATURA  ARCHI COLONNE##
############################

def mattoncino(parametri, mattoncino_type):
    x, y, z = parametri
    if z < x:
        mattoncino_x = z * 0.2
        mattoncino_z = z * 0.2
    else:
        mattoncino_x = x * 0.2
        mattoncino_z = x * 0.2
    if mattoncino_type == 1:
        mattoncino_x = 0
    if mattoncino_type == 2:
        mattoncino_z = 0

    mattoncino = CUBOID([x, y * 0.8, z])
    matttoncino2 = CUBOID([x - mattoncino_x, y, z - mattoncino_z])
    mattoncino = DIFFERENCE(
        [T(2)((y - y * 0.9) / 2)(mattoncino), T([1, 3])([(mattoncino_x) / 2, (mattoncino_z) / 2])(matttoncino2)])
    mattoncino_result = STRUCT(
        [T(2)((y - y * 0.9) / 2)(mattoncino), T([1, 3])([(mattoncino_x) / 2, (mattoncino_z) / 2])(matttoncino2)])
    return mattoncino_result
def muro_mattoncini(parametri, n_larghezza, n_altezza):
    # n_larghezza = mattoni H
    # n_altezza =mattoni V
    x,y,z=parametri
    x= x / n_larghezza
    z= z / n_altezza
    mattone=COLOR(Colore_mattone)(mattoncino([x, y, z], 0))
    muro=STRUCT(NN(n_larghezza)([mattone, T(1)(x)]))
    muro=STRUCT(NN(n_altezza)([muro, T(3)(z)]))
    return muro
def muro_con_porta(x, y, z, altezza, portasopra_bool, tipologia, bordo_bool, portagrande_bool):


    # tipologia==1 se porta con finestra
    # tipologia==0 se porta di legno
    murox, muroz = x * 1.5, altezza

    muro = CUBOID([murox, y * 0.5, muroz])

    if tipologia == 1:
        porta = porta_vetrata(x, y, z, 0, 1)
        portaz = SIZE(3)(porta) - z * 0.375
    else:
        porta = porta_legno(x * 0.91, y * 1.77, z, 1, 0)
        portaz = SIZE(3)(porta)
    if bordo_bool == 1:
        porta = COMP([T([1, 2])([x, y * 0.5]), R([1, 2])(PI)])(porta_legno(x * 0.91, y * 1.77, z, 1, 1))
        portaz = SIZE(3)(porta) - z * 0.525

    if portasopra_bool == 1:
        porta2x, porta2z = x * 1, z * 4.8 - portaz
        porta2 = CUBOID([porta2x, y * 0.5, porta2z])
        muroz = muroz - portaz * 2 - porta2z
        muro = CUBOID([porta2x, y * 0.5, muroz])
        porta2 = STRUCT([porta2, T(3)(porta2z)(porta),
                             T(3)(portaz + porta2z)(muro)])

    else:
        porta2x, porta2z = x * 1, muroz - portaz
        porta2 = CUBOID([porta2x, y * 0.5, porta2z])
    if portagrande_bool == 1:
        porta = porta_vetrata(x, y, z, 0, 1)
        x2 = SIZE(1)(porta)
        porta = porta_vetrata(x * 0.5, y, z, 0, 1)
        x3 = SIZE(1)(porta)
        x4 = x2 - x3
        murox, muroz = (x * 1.5) + x4 / 4, altezza
        muro = CUBOID([murox, y * 0.5, muroz])
        porta2x, porta2z = x3, muroz - portaz
        porta2 = CUBOID([porta2x, y * 0.5, porta2z])
        porta = T(1)(x * 0.125)(porta)

    muro_result = STRUCT(
        [muro, T([1, 3])([murox, portaz])(porta2), T(1)(murox + porta2x)(muro), T(1)(murox)(porta)])

    return muro_result
def arco(x, y, z, dmax, dmin, nmattoni):

    #distanza archi

    dimmattone = 180.0 / nmattoni
    dimbordo = dimmattone * 0.1

    def arco1(cont, arcoinit):
        # passo iniziale
        if arcoinit == 1:
            arcoinit = MKPOL(([[x * dmin * COS(radians(dimmattone * (cont - 1))),
                                z * dmin * SIN(radians(dimmattone * (cont - 1)))],
                               [x * dmax * COS(radians(dimmattone * (cont - 1))),
                                 z * dmax * SIN(radians(dimmattone * (cont - 1)))],
                               [x * dmin * COS(radians(dimmattone * cont - dimbordo)),
                                 z * dmin * SIN(radians(dimmattone * cont - dimbordo))],
                               [x * dmax * COS(radians(dimmattone * cont - dimbordo)),
                                 z * dmax * SIN(radians(dimmattone * cont - dimbordo))]],
                              [[1, 2, 4, 3]], []))

            bordo = MKPOL(([[x * dmin * COS(radians(dimmattone * cont - dimbordo)),
                                z * dmin * SIN(radians(dimmattone * cont - dimbordo))],
                               [x * dmax * COS(radians(dimmattone * cont - dimbordo)),
                                z * dmax * SIN(radians(dimmattone * cont - dimbordo))],
                               [x * dmin * COS(radians(dimmattone * cont)),
                                z * dmin * SIN(radians(dimmattone * cont))],
                               [x * dmax * COS(radians(dimmattone * cont)),
                                z * dmax * SIN(radians(dimmattone * cont))]],
                              [[1, 2, 4, 3]], []))

            arcoinit = PROD([arcoinit, QUOTE([y])])
            bordo = PROD([bordo, QUOTE([y * 0.9])])
            arcoinit = STRUCT([arcoinit, bordo])
            return arco1(cont + 1, arcoinit)
        else:
            # passo base
            if cont == nmattoni:
                arcobase = MKPOL(([[x * dmin * COS(radians(dimmattone * (cont - 1))),
                                      z * dmin * SIN(radians(dimmattone * (cont - 1)))],
                                     [x * dmax * COS(radians(dimmattone * (cont - 1))),
                                      z * dmax * SIN(radians(dimmattone * (cont - 1)))],
                                     [x * dmin * COS(radians(dimmattone * cont)),
                                      z * dmin * SIN(radians(dimmattone * cont))],
                                     [x * dmax * COS(radians(dimmattone * cont)),
                                      z * dmax * SIN(radians(dimmattone * cont))]],
                                    [[1, 2, 4, 3]], []))

                arcobase = PROD([arcobase, QUOTE([y])])
                arcoinit = STRUCT([arcoinit, arcobase])
                return COLOR(Colore_mattone)(arcoinit)
            # passo induttivo
            else:
                arcobase = MKPOL(([[x * dmin * COS(radians(dimmattone * (cont - 1))),
                                      z * dmin * SIN(radians(dimmattone * (cont - 1)))],
                                     [x * dmax * COS(radians(dimmattone * (cont - 1))),
                                      z * dmax * SIN(radians(dimmattone * (cont - 1)))],
                                     [x * dmin * COS(
                                         radians(dimmattone * cont - dimbordo)),
                                      z * dmin * SIN(
                                          radians(dimmattone * cont - dimbordo))],
                                     [x * dmax * COS(radians(dimmattone * cont - dimbordo)),
                                      z * dmax * SIN(
                                          radians(dimmattone * cont - dimbordo))]],
                                    [[1, 2, 4, 3]], []))

                bordo2 = MKPOL(([[x * dmin * COS(radians(dimmattone * cont - dimbordo)),
                                     z * dmin * SIN(
                                         radians(dimmattone * cont - dimbordo))],
                                    [x * dmax * COS(radians(dimmattone * cont - dimbordo)),
                                     z * dmax * SIN(radians(dimmattone * cont - dimbordo))],
                                    [x * dmin * COS(radians(dimmattone * cont)),
                                     z * dmin * SIN(radians(dimmattone * cont))],
                                    [x * dmax * COS(radians(dimmattone * cont)),
                                     z * dmax * SIN(radians(dimmattone * cont))]],
                                   [[1, 2, 4, 3]], []))

                arcobase = PROD([arcobase, QUOTE([y])])
                bordo2 = PROD([bordo2, QUOTE([y * 0.9])])
                arcobase = STRUCT([arcobase, bordo2])
                arcoinit = STRUCT([arcoinit, arcobase])
                return arco1(cont + 1, arcoinit)

    return arco1
def colonna(x, y, z):
    x = x / 1.3
    strato1 = COLOR(Colore_mattone)(CUBOID([x, y, z * 0.025]))
    strato2 = T([1, 2])([x * 0.1, y * 0.1])(COLOR(Colore_mattone)(CUBOID([x * 0.8, y * 0.8, z * 0.015])))
    strato3 = T([1, 2])([x * 0.05, y * 0.05])(COLOR(Colore_mattone)(CUBOID([x * 0.9, y * 0.9, z * 0.02])))
    strato4 = T([1, 2, 3])([x * 0.1, y * 0.1])(COLOR(Colore_mattone)(CUBOID([x * 0.8, y * 0.8, z * 0.04])))
    strato5 = T([1, 2, 3])([x * 0.115, y * 0.115, z * 0.10])(CUBOID([x * 0.77, y * 0.77, z * 0.8]))
    return STRUCT([strato1, T(3)(z * 0.025)(strato2), T(3)(z * 0.04)(strato3), T(3)(z * 0.06)(strato4), strato5,
                   T(3)(z * 0.9)(strato4), T(3)(z * 0.94)(strato3), T(3)(z * 0.96)(strato2), T(3)(z * 0.975)(strato1)])
def bottomArc(d):
    return BEZIER(S1)([[0, 0], [0, 2 * d / 3], [d, 2 * d / 3], [d, 0]])
def topArc(d):
    return BEZIER(S1)([[0, 2 * d / 3], [d, 2 * d / 3]])
def arc2D(d):
    return BEZIER(S2)([bottomArc(d), topArc(d)])
def arc3D(d):
    def arc3D1(w):
        arco = arc2D(3.2)
        dominio = PROD([INTERVALS(1)(16), INTERVALS(1)(1)])
        ar = MAP(arco)(dominio)
        domin = PROD([ar, QUOTE([1.5])])
        return COMP([T(2)(w), R([2, 3])(PI / 2)])(domin)

    return arc3D1
def Interarc(d1, d2):
    def Interarc1(w):
        return CUBOID([d1, w, 2 * d2 / 3])

    return Interarc1
def arco_mattonato(d1, d2):
    def arco_mattonato_app(w, destra, lunghezza_lato):

        if destra == 1:
            muro = RIGHT([TEXTURE('./immagini/mattone.jpg')(Interarc(lunghezza_lato, d2)(w)),
                          TEXTURE('./immagini/mattone.jpg')(
                              RIGHT([RIGHT([Interarc(d1, d2)(w), arc3D(d2)(w)]), Interarc(d1, d2)(w)]))])
        else:
            #destra=0 quindi sinistra
            muro = LEFT([TEXTURE('./immagini/mattone.jpg')(Interarc(lunghezza_lato, d2)(w)),
                         TEXTURE('./immagini/mattone.jpg')(
                             RIGHT([RIGHT([Interarc(d1, d2)(w), arc3D(d2)(w)]), Interarc(d1, d2)(w)]))])

        return muro

    return arco_mattonato_app
def arcata_ingresso(x, y, z):
    y2 = y * 0.5
    mattonex = x * 0.8
    mattonez = z * 0.3625
    n = 11

    # creazione colonna
    mattone2x = x * 0.8
    mattone2y = y * 0.52
    mattone2 = COLOR(Colore_mattone)(mattoncino([mattone2x, mattone2y, mattonez], 0))
    msuperiorex = mattone2x / 2
    msuperiore = COLOR(Colore_mattone)(mattoncino([msuperiorex, mattone2y, mattonez], 0))
    colonna = STRUCT(NN(16)([mattone2, T(3)(mattonez)]))
    colonnacentrale = STRUCT([T([1, 3])([mattone2x, mattonez * 15])(msuperiore),
                             T([1, 3])([mattone2x * 1.5, mattonez * 15])(msuperiore), colonna,
                             T([1, 3])([-msuperiorex, mattonez * 15])(msuperiore),
                             T([1, 3])([-msuperiorex * 2, mattonez * 15])(msuperiore)])

    # creazione arco
    mattone = COLOR(Colore_mattone)(mattoncino([mattonex, y2, mattonez], 0))
    colonna2 = STRUCT(NN(n)([mattone, T(3)(z * 0.3625)]))
    lunghezza_arco = 1.3 * 0.75 * 3.75
    w = 1.3 * 0.75
    arch = arco(x, y2, z, 1.85, 0.85, 13)(1, 1)
    arch = STRUCT([T(1)(-(1.3 / (lunghezza_arco + w)))(colonna2),
                   T(1)(lunghezza_arco + (1.3 / (lunghezza_arco + w)) - mattonex)(colonna2),
                   COMP([T([1, 3])([x * 1.41, mattonez * n]), R([1, 2])(PI), R([2, 3])(PI / 2)])(arch)])

    # l'ingresso ha tre archi individuo le tre fasi con destra centro e sinistra
    # centro
    arcocc = DIFFERENCE([T(1)(mattone2x * 0.5)(arch), S(2)(y * 1.5)(T(2)(-y * 0.1)(colonnacentrale)),
                              S(2)(y * 1.5)(T([1, 2])([(x / 1.3) * lunghezza_arco, -y * 0.1])(colonnacentrale))])
    arcocc = COLOR(Colore_mattone)(STRUCT([arcocc, T(2)(z * -0.01)(colonnacentrale),
                                                T([1, 2])([(x / 1.3) * lunghezza_arco, z * -0.01])(colonnacentrale)]))

    # sinistra
    colonnasxsx = STRUCT([T([1, 3])([-msuperiorex, mattonez * 15])(msuperiore),
                          T([1, 3])([-msuperiorex * 2, mattonez * 15])(msuperiore), colonna])
    colonnasxdx = LEFT([colonna, colonnasxsx])
    arcosx = DIFFERENCE(
        [arch, S(2)(y * 1.5)(T([1, 2])([(x / 1.3) * lunghezza_arco + mattone2x * 0.5, y * 0.1])(colonnasxdx)),
         S(2)(y * 1.5)(T([1, 2])([-x * 0.4, y * 0.1])(colonnacentrale))])
    arcosx = COLOR(Colore_mattone)(
        STRUCT([arcosx, T([1, 2])([(x / 1.3) * lunghezza_arco + mattone2x * 0.5, z * -0.01])(colonnasxdx)]))

    # destra
    colonnadxsx = STRUCT([T([1, 3])([mattone2x, mattonez * 15])(msuperiore),
                          T([1, 3])([mattone2x * 1.5, mattonez * 15])(msuperiore), colonna])
    colonnadxdx = RIGHT([colonna, colonnadxsx])
    arcodx = DIFFERENCE([T(1)(mattone2x + mattone2x * 0.5)(arch), S(2)(y * 1.5)(T(2)(-y * 0.1)(colonnadxdx)),
                         S(2)(y * 1.5)(T([1, 2])([(x / 1.3) * lunghezza_arco + mattone2x, y * 0.1])(colonnacentrale))])
    arcodx = COLOR(Colore_mattone)(STRUCT([arcodx, T(2)(z * -0.01)(colonnadxdx)]))

    #realizzazione della strattura

    arcata_result = STRUCT([arcodx, T(1)((x / 1.3) * lunghezza_arco + mattone2x)(arcocc),
                    T(1)((x / 1.3) * lunghezza_arco * 2 + mattone2x + mattone2x * 0.5)(arcosx)])
    assesuperiore = cornice([SIZE(1)(arcata_result), mattone2y, z * 0.5], 22)
    arcata_result = STRUCT([arcata_result, T([2, 3])([y * 0.05, mattonez * 16])(COLOR(Colore_mattone)(assesuperiore))])
    x1 = x / 1.3
    muro_colonnine = S([1, 2, 3])([x1 * 0.12, y * 0.36, z * 0.2])(muro_colonne(x, y, z))
    arcata_result = STRUCT([arcata_result, T(1)(mattone2x * 2 + mattone2x * 0.18)(muro_colonnine),
                    T(1)(SIZE(1)(arcata_result) - (mattone2x * 2 + mattone2x * 0.18) - SIZE(1)(muro_colonnine))(
                        muro_colonnine)])
    arcata_result = S([1, 3])([(x / 1.2975) * 1.41, z * 0.9])(arcata_result)
    return arcata_result
def colonnina(x, y, z):
    x = x / 1.3
    curva_sx = BEZIER(S1)([[x * 1, y * 0, z * 0], [-x * 2, y * 0, z * 1], [x * 5, y * 0, z * 2], [-x * 2, y * 0, z * 3],
                           [x * 1, y * 0, z * 4]])
    curva_up = BEZIER(S1)([[x * 0, -y * 1, z * 0], [x * 0, y * 2, z * 1], [x * 0, -y * 5, z * 2], [x * 0, y * 2, z * 3],
                           [x * 0, -y * 1, z * 4]])
    curva_2D = BEZIER(S2)([curva_sx, curva_up])

    curva_dx = BEZIER(S1)([[-x * 1, y * 0, z * 0], [x * 2, y * 0, z * 1], [-x * 5, y * 0, z * 2], [x * 2, y * 0, z * 3],
                           [-x * 1, y * 0, z * 4]])
    curva_down = BEZIER(S1)(
        [[x * 0, y * 1, z * 0], [x * 0, -y * 2, z * 1], [x * 0, y * 5, z * 2], [x * 0, -y * 2, z * 3],
         [x * 0, y * 1, z * 4]])
    curva_2D1 = BEZIER(S2)([curva_dx, curva_down])

    dominio1 = PROD([INTERVALS(1)(32), INTERVALS(1)(1)])

    curva_3D = BEZIER(S3)([curva_2D, curva_2D1])
    dominio3d = PROD([dominio1, QUOTE([1])])
    curva_3D = MAP(curva_3D)(dominio3d)
    return COLOR(Colore_mattone)(curva_3D)
def muro_colonne(x, y, z):
    # muretto fatto di colonnine situato nella facciata principale

    colonna1 = R([1, 2])(PI / 4)(colonnina(x, y, z))
    colonnax, colonnay = SIZE(1)(colonna1), SIZE(2)(colonna1)
    muro_result = STRUCT(NN(5)([colonna1, T(1)((colonnax) + (colonnax) / 10)]))
    murocentrale = T([1, 2])([-colonnax / 2, -colonnay / 2])(CUBOID([colonnax, colonnay, SIZE(3)(colonna1)]))
    muro_result = STRUCT([muro_result, T(1)(SIZE(1)(muro_result) + (colonnax) / 10)(murocentrale),
                      T(1)(SIZE(1)(murocentrale) + SIZE(1)(muro_result) + (colonnax) * 2 / 10)(muro_result)])
    astax = SIZE(1)(muro_result) * 1.1
    astaz = SIZE(3)(muro_result) / 10
    asta = CUBOID([astax, SIZE(2)(muro_result), astaz])
    muro_result = T([1, 2, 3])([(colonnax / 2) + (astax - (astax / 1.1)) / 2, colonnay / 2, astaz])(
        TOP([BOTTOM([muro_result, asta]), asta]))

    return COLOR(Colore_mattone)(muro_result)
def muro_archi(x, y, z, tetto_bool):
    x = x / 1.3
    colonna1 = colonna(x * 1.2, y * 0.5, z * 5)
    colonna1x = SIZE(1)(colonna1)
    muro_result = CUBOID([x * 0.4, z * 1.5, 2 * y * 3.2 / 3])
    muro_result = RIGHT([RIGHT([muro_result, arc3D(y * 3.2)(z * 1.5)]), muro_result])
    colonna1z = SIZE(3)(colonna1) - SIZE(3)(muro_result) * 0.6
    muro_result = T([1, 3])([x * 0.7, colonna1z])(S([1, 2, 3])([x * 1.245, y * 0.2, z * 0.6])(muro_result))
    arcox = SIZE(1)(muro_result)
    #colonna piu piccola
    colonna2 = T(1)(x * 0.7)(colonna(x * 0.64, y * 0.4, colonna1z))
    colonna2x = SIZE(1)(colonna2)
    colonna2z = SIZE(3)(colonna2)
    y2 = SIZE(2)(muro_result)
    sporgenza = T(1)(-x * 1.2)(COLOR(Colore_mattone)(CUBOID([x * 20, y * 0.5, z * 0.2])))
    sporgenza = T(3)(SIZE(3)(colonna1))(
        STRUCT([T(2)(-y * 0.2)(sporgenza), T([2, 3])([-y * 0.125, z * 0.2])(sporgenza)]))

    # tetto
    if tetto_bool == 1:
        tetto = T(3)(SIZE(3)(colonna1))(T(1)(-x * 1.2)(CUBOID([x * 20, y * 4.7, z * 0.2])))
        sporgenza = STRUCT([sporgenza, T([2, 3])([y * 0.05, z * 0.4])(tetto)])

    sporgenza_archi = COLOR(Colore_mattone)(T([1, 2, 3])([x * 0.2, y * 0.1, colonna2z - colonna1z * 0.1])(
        CUBOID([x * 17, y * 0.2, colonna1z * 0.1])))
    colonna1 = STRUCT(
        [colonna1, T(1)(arcox + x * 0.55)(colonna1), T(1)((arcox + x * 0.57) * 2)(colonna1),
         T(1)((arcox + x * 0.57) * 3)(colonna1)])
    colonna2 = STRUCT([colonna2, T(1)(arcox - x * 0.5)(colonna2),
                              T(1)(arcox - x * 0.3 + colonna1x)(colonna2),
                              T(1)(arcox * 2 + x * 0.1)(colonna2),
                              T(1)(arcox * 2 + colonna1x + x * 0.28)(colonna2),
                              T(1)(arcox * 3 + x * 0.7)(colonna2)])
    muro_result = STRUCT([muro_result, T(1)(arcox + x * 0.6)(muro_result), T(1)((arcox + x * 0.6) * 2)(muro_result)])

    return STRUCT([colonna1, muro_result, colonna2, sporgenza, sporgenza_archi])
def cornice(param, ncolonne):
    x,y,z=param
    x= x / ncolonne
    mattone = mattoncino([x * 0.1, y * 0.7, z * 0.8], 2)
    base=CUBOID([x * ncolonne, y * 0.8, z * 0.8])
    sporgenza=CUBOID([x * ncolonne, y, z * 0.1])
    colonnine=T([1,2])([x*0.35,y*0.2])(STRUCT(NN(3)([mattone,T(1)(x*0.1)])))
    cornice_res=STRUCT([base, STRUCT(NN(ncolonne)([colonnine, T(1)(x)]))])
    return COLOR(Colore_mattone)(STRUCT([sporgenza, T(3)(z * 0.1)(cornice_res), T(3)(z * 0.9)(sporgenza)]))


##########################
## STRUTTURA PRINCIPALE ##
##########################
def cupoletta(c,max):
    i=1
    Colore_prato = [0.2, 0.4, 0.05]
    base = CYLINDER([c, 0.01])(40)
    base2=  CYLINDER([c-0.01, 0.01])(40)
    base2=T(3)(0.01*i)(base2)
    base3=STRUCT([base,base2])
    c=c-0.01
    i=2
    while(c>max):
        base_c = CYLINDER([c, 0.01])(40)
        base_c=T(3)(0.01*i)(base_c)
        base3 = STRUCT([base3, base_c])
        c=c-0.01
        i=i+1
    base3=COLOR(Colore_prato)(base3)
    return base3

#VIEW(cupoletta(3,2))
def muro_nord(x, y, z, tetto_bool):

    # muro
    murox = x * 4
    muro = CUBOID([murox, y * 0.5, z * 10])
    #muro = COLOR(Colore_main)(muro)
    finestra1 = finestra(x, y * (0.5 / 0.3), z, 0, 1)
    finestra_superiore = T([1, 3])([x * 1.5, z * 0.7])(finestra(x, y * (0.5 / 0.3), z, 3, 0))
    finestra1 = T([1, 3])([x * 1.5, z * 0.7])(finestra1)
    muro = DIFFERENCE([muro, finestra1, T(3)(z * 5.8)(finestra_superiore)])
    #muro = COLOR(Colore_main)(muro)
    finestra1 = finestra(x, y, z, 0, 1)
    finestra1 = T([1, 3])([x * 1.5, z * 0.7])(finestra1)
    finestra_superiore = T([1, 3])([x * 1.5, z * 0.7])(finestra(x, y, z, 3, 0))
    muro = STRUCT([muro, finestra1, T(3)(z * 5.8)(finestra_superiore)])
    #muro = COLOR(Colore_main)(muro)
    x_sporgenza = (murox + 0.2)
    sporgenza = COLOR(GRAY)(CUBOID([x_sporgenza, y * 0.6, z * 0.2]))
    muro = STRUCT([T([1, 3])([x * 0.1, z * 0.2])(muro), sporgenza])
    #muro = COLOR(Colore_main)(muro)
    #muro inferiore
    muro2z = z * 1.8
    muro2 = CUBOID([murox, y * 0.5, muro2z])
    finestra2 = T([1, 3])([x * 1.5, z * 0.3])(finestrella2(x, y * (0.5 / 0.3), z, 0, 0))
    muro2 = DIFFERENCE([muro2, finestra2])
    finestra2 = T([1, 3])([x * 1.5, z * 0.3])(finestrella2(x, y, z, 0, 0))
    muro2 = STRUCT([muro2, finestra2])
    muro = STRUCT([T(1)(x * 0.1)(muro2), T(3)(muro2z + (z * 0.2))(muro)])
    arch = S(1)((x / 1.3) * 1.05)(arcata_ingresso(x, y, z))

    # tetto
    asse = tetto_ingresso(19.7764624023, 0.519999980927, z, tetto_bool)
    arco = STRUCT([S(2)(y * 1.1)(arch),
                   T([1, 3])([0.5, SIZE(3)(arch) + z * 0.4])(asse)])

    arco2 = COLOR(Colore_mattone)(muro_mattoncini([SIZE(1)(arco), y * 0.5, muro2z], 10, 4))
    arco = STRUCT([arco2, T(3)(muro2z + (z * 0.2))(arco)])
    muro3 = T([1, 3])([x * 0.1, -z * 1.8])(CUBOID([x * 24, y * 0.5, z * 1.8]))

    # scala
    scale = COLOR(Colore_mattone_2)(scale_cilindriche(x / 1.87, y / 1.87, z)(6, 1, 0))
    mattonez = z * 1.8 / 5.0
    scala2 = T([1, 3])([-mattonez * 0.28, mattonez * 0.1])(
        COLOR(Colore_mattone)(CUBOID([x * 0.1, y * 0.1, mattonez * 0.8])))
    mattonep = COLOR(Colore_mattone)(mattoncino([x * 0.25, y * 0.5, mattonez], 1))
    mattoneg = COLOR(Colore_mattone)(mattoncino([x * 0.5, y * 0.5, mattonez], 1))
    mattoni = STRUCT([mattoneg, T(3)(mattonez)(mattonep), T(3)(mattonez * 2)(mattoneg),
                      T(3)(mattonez * 3)(mattonep), T(3)(mattonez * 4)(mattoneg)])
    mattonesx = STRUCT([mattoni, STRUCT(NN(5)([scala2, T(3)(mattonez)])),
                         COMP([T([1, 2])([y * 0.4, y * 0.05]), R([1, 2])(PI / 2)])(mattoni)])
    mattonedx = STRUCT(
        [mattoni, T([1, 2])([x * 0.1 - mattonez * 0.22, y * 0.4])(STRUCT(NN(5)([scala2, T(3)(mattonez)]))),
         COMP([T([1, 2])([-y * 0.05, y * 0.4]), R([1, 2])(-PI / 2)])(mattoni)])

    return STRUCT([muro, T(1)(murox)(arco), T(1)(murox + SIZE(1)(arch) - x * 0.1)(muro),
                   T([1, 2])([murox + SIZE(1)(arch) / 2, z * 0.5])(scale), muro3,
                   COMP([T([1, 2])([x * 24.1, y * 0.6]), R([1, 2])(PI)])(mattonesx),
                   T([1, 2])([-x * 0, y * 0.1])(mattonedx)])
def muro_sud(x, y, z):

    murox = x * 24
    muro = CUBOID([murox, y * 0.5, z * 8.5])
    finestra1 = finestra(x, y * (0.5 / 0.3), z, 0, 1)
    finestrasx = T([1, 3])([x * 13.5, z * 0.7])(finestra(x, y * (0.5 / 0.3), z, 1, 1))
    finestradx = T([1, 3])([x * 9.5, z * 0.7])(finestra(x, y * (0.5 / 0.3), z, 2, 1))
    finestra1 = T([1, 3])([x * 1.5, z * 0.7])(finestra1)
    finestrella1 = T([1, 3])([x * 1.5, z * 6.5])(finestrella(x, y * (0.5 / 0.3), z))
    finestrelladx = STRUCT(NN(2)([finestrella1, T(1)(x * 4)]))
    finestrellasx = T(1)(x * 16)(finestrelladx)
    finestra_centrale = finestra2(x * (1 / 1.3), y * 2, z)
    porta1 = porta_vetrata(x * 0.97, y * 1.6, z, 1, 0)
    finestrecoppia = STRUCT(NN(2)([finestra1, T(1)(x * 4)]))
    muro = DIFFERENCE([muro, finestradx, finestrasx, finestrecoppia, T(1)(x * 16)(finestrecoppia), finestrelladx,
                       finestrellasx,
                       COMP([T([1, 2, 3])([(x * 10.15384), y * 0.5 * (0.5 / 0.3), z * 5.5]), R([2, 3])(PI / 2)])(
                           finestra_centrale),
                       T([1, 2, 3])([x * 11.5, -y * 0.1, -z * 0.2])(porta1)
                       ])
    finestra1 = finestra(x, y, z, 0, 1)
    finestrasx = T([1, 3])([x * 13.5, z * 0.7])(finestra(x, y, z, 1, 1))
    finestradx = T([1, 3])([x * 9.5, z * 0.7])(finestra(x, y, z, 2, 1))
    finestra1 = T([1, 3])([x * 1.5, z * 0.7])(finestra1)
    finestrella1 = T([1, 3])([x * 1.5, z * 6.5])(finestrella(x, y, z))
    finestrelladx = STRUCT(NN(2)([finestrella1, T(1)(x * 4)]))
    finestrellasx = T(1)(x * 16)(finestrelladx)
    finestrecoppia = STRUCT(NN(2)([finestra1, T(1)(x * 4)]))

    muro = STRUCT([muro, finestrecoppia, finestradx, finestrasx, T(1)(x * 16)(finestrecoppia), finestrelladx,
                   finestrellasx])
    finestra_centrale = finestra2(x * (1 / 1.3), y, z)
    porta1 = porta_vetrata(x * 0.97, y, z, 1, 1)

    muro = STRUCT([muro, COMP([T([1, 2, 3])([(x * 10.15384), y * 0.5, z * 5.5]), R([2, 3])(PI / 2)])(finestra_centrale),
                   T([1, 3])([x * 11.5, -z * 0.2])(porta1)])

    x_sporgenza = ((murox + 0.2) / 2) - (x * 1.4 / 2)
    sporgenza = COLOR(GRAY)(CUBOID([x_sporgenza, y * 0.6, z * 0.2]))
    muro = STRUCT([T([1, 3])([x * 0.1, z * 0.2])(muro), T(1)((x / 1.3) * 0.05)(S(1)((x / 1.3) * 0.995)(sporgenza)),
                   T(1)(x_sporgenza + (x * 1.43))(sporgenza)])

    muro2 = CUBOID([murox, y * 0.5, z * 1.8])
    muro2 = STRUCT([muro2, T(3)(-z * 1.8)(CUBOID([murox, y * 0.5, z * 1.8]))])
    finestrellasotto = finestrella2(x, y * (0.5 / 0.3), z, 0, 0)
    finestrellasotto2 = finestrella2(x, y * (0.6 / 0.3), z, 1, 0)
    muro2 = DIFFERENCE(
        [muro2, T([1, 3])([x * 5.5, z * 0.3])(finestrellasotto), T([1, 3])([x * 17.5, z * 0.3])(finestrellasotto),
         T([1, 2])([x * 1.5, -y * 0.2])(finestrellasotto2), T([1, 2])([x * 21.5, -y * 0.2])(finestrellasotto2)])
    finestrellasotto = finestrella2(x, y, z, 0, 0)
    finestrellasotto2 = finestrella2(x, y, z, 1, 1)
    scale = COLOR(Colore_mattone_2)(gradini(x, y, z, 10)(0, 0, 1))
    mattonez = z * 1.8 / 5.0
    scala = T([1, 3])([-mattonez * 0.28, mattonez * 0.1])(
        COLOR(Colore_mattone)(CUBOID([x * 0.1, y * 0.1, mattonez * 0.8])))
    mattonepic = COLOR(Colore_mattone)(mattoncino([x * 0.25, y * 0.5, mattonez], 1))
    mattonegr = COLOR(Colore_mattone)(mattoncino([x * 0.5, y * 0.5, mattonez], 1))
    mattoni = STRUCT([mattonegr, T(3)(mattonez)(mattonepic), T(3)(mattonez * 2)(mattonegr),
                      T(3)(mattonez * 3)(mattonepic), T(3)(mattonez * 4)(mattonegr)])
    mattonesx = STRUCT([mattoni, STRUCT(NN(5)([scala, T(3)(mattonez)])),
                         COMP([T([1, 2])([y * 0.4, y * 0.05]), R([1, 2])(PI / 2)])(mattoni)])
    mattonedx = STRUCT(
        [mattoni, T([1, 2])([x * 0.1 - mattonez * 0.22, y * 0.4])(STRUCT(NN(5)([scala, T(3)(mattonez)]))),
         COMP([T([1, 2])([-y * 0.05, y * 0.4]), R([1, 2])(-PI / 2)])(mattoni)])
    muro2 = STRUCT(
        [muro2, T([1, 3])([x * 5.5, z * 0.3])(finestrellasotto), T([1, 3])([x * 17.5, z * 0.3])(finestrellasotto),
         T(1)(x * 1.5)(finestrellasotto2), T(1)(x * 21.5)(finestrellasotto2), T([1, 2])([x * 8, y * 0.5])(scale),
         COMP([T([1, 2])([x * 24.05, y * 0.6]), R([1, 2])(PI)])(mattonesx),
         T([1, 2])([-x * 0.02, y * 0.1])(mattonedx)])

    return STRUCT([T(1)(x * 0.1)(muro2), T(3)(z * 2)(muro)])
def murolaterale(x, y, z, orientazione):
    # muro ovest
    if orientazione == 0:

        murox = x * 12
        muro = CUBOID([murox, y * 0.5, z * 8.5])
        murox2 = x * 4
        muro2 = CUBOID([murox2, y * 0.5, z * 10])
        muro = STRUCT([muro, T(1)(murox)(muro2)])
        finestra1 = finestra(x, y * (0.5 / 0.3), z, 0, 1)
        finestrasuperiore = finestra(x, y * (0.5 / 0.3), z, 3, 0)
        finestrainferiore = T([1, 3])([x * 1.5, z * 0.7])(finestra1)
        finestrasuperiore = T([1, 3])([x * 13.5, z * 6.5])(finestrasuperiore)
        finestrella1 = T([1, 3])([x * 1.5, z * 6.5])(finestrella(x, y * (0.5 / 0.3), z))
        muro = DIFFERENCE([muro, finestrasuperiore, STRUCT(NN(4)([finestrainferiore, T(1)(x * 4)])),
                           STRUCT(NN(3)([finestrella1, T(1)(x * 4)]))])

        # inserimento oggetti nella parete del muro
        finestra1 = finestra(x, y, z, 0, 1)
        finestrasuperiore = finestra(x, y, z, 3, 0)
        finestrainferiore = T([1, 3])([x * 1.5, z * 0.7])(finestra1)
        finestrasuperiore = T([1, 3])([x * 13.5, z * 6.5])(finestrasuperiore)
        finestrella1 = T([1, 3])([x * 1.5, z * 6.5])(finestrella(x, y, z))
        muro = STRUCT([muro, finestrasuperiore, STRUCT(NN(4)([finestrainferiore, T(1)(x * 4)])),
                       STRUCT(NN(3)([finestrella1, T(1)(x * 4)]))])
        sporgenzax = (murox + murox2 + 0.2)
        sporgenza = COLOR(GRAY)(CUBOID([sporgenzax, y * 0.6, z * 0.2]))
        muro = STRUCT([T([1, 3])([x * 0.1, z * 0.2])(muro), sporgenza])

        # muro inferiore e spazi finestre
        muroinferiore = CUBOID([murox + murox2, y * 0.5, z * 1.8])
        muroinferiore = STRUCT([muroinferiore, T(3)(-z * 1.8)(CUBOID([x * 16, y * 0.5, z * 1.8]))])
        finestrainferiore = T([1, 3])([x * 1.5, z * 0.3])(finestrella2(x, y * (0.5 / 0.3), z, 0, 0))
        muroinferiore = DIFFERENCE([muroinferiore, STRUCT(NN(3)([finestrainferiore, T(1)(x * 4)]))])
        finestrainferiore = T([1, 3])([x * 1.5, z * 0.3])(finestrella2(x, y, z, 0, 0))
        muroinferiore = STRUCT([muroinferiore, STRUCT(NN(4)([finestrainferiore, T(1)(x * 4)]))])
        muro = STRUCT([T(1)(x * 0.1)(muroinferiore), T(3)(z * 2)(muro)])


    else:
        # muro est
        murox = x * 12
        muro = CUBOID([murox, y * 0.5, z * 8.5])
        murox2 = x * 4
        muro2 = CUBOID([murox2, y * 0.5, z * 10])
        muro = STRUCT([muro2, T(1)(murox2)(muro)])
        finestra1 = finestra(x, y * (0.5 / 0.3), z, 0, 1)
        finestrasuperiore = finestra(x, y * (0.5 / 0.3), z, 3, 0)

        finestrainferiore = T([1, 3])([x * 1.5, z * 0.7])(finestra1)
        finestrasuperiore = T([1, 3])([x * 1.5, z * 6.5])(finestrasuperiore)
        finestrella1 = T([1, 3])([x * 5.5, z * 6.5])(finestrella(x, y * (0.5 / 0.3), z))
        muro = DIFFERENCE([muro, finestrasuperiore, STRUCT(NN(4)([finestrainferiore, T(1)(x * 4)])),
                           STRUCT(NN(3)([finestrella1, T(1)(x * 4)]))])

        finestra1 = finestra(x, y, z, 0, 1)
        finestrasuperiore = finestra(x, y, z, 3, 0)
        finestrainferiore = T([1, 3])([x * 1.5, z * 0.7])(finestra1)
        finestrasuperiore = T([1, 3])([x * 1.5, z * 6.5])(finestrasuperiore)
        finestrella1 = T([1, 3])([x * 5.5, z * 6.5])(finestrella(x, y, z))

        muro = STRUCT([muro, finestrasuperiore, STRUCT(NN(4)([finestrainferiore, T(1)(x * 4)])),
                       STRUCT(NN(3)([finestrella1, T(1)(x * 4)]))])


        sporgenzax = (murox + murox2 + 0.2)
        sporgenza = COLOR(GRAY)(CUBOID([sporgenzax, y * 0.6, z * 0.2]))
        muro = STRUCT([T([1, 3])([x * 0.1, z * 0.2])(muro), sporgenza])


        muroinferiore = CUBOID([murox + murox2, y * 0.5, z * 1.8])
        muroinferiore = STRUCT([muroinferiore, T(3)(-z * 1.8)(CUBOID([x * 16, y * 0.5, z * 1.8]))])
        finestrainferiore = T([1, 3])([x * 5.5, z * 0.3])(finestrella2(x, y * (0.5 / 0.3), z, 0, 0))
        muroinferiore = DIFFERENCE([muroinferiore, STRUCT(NN(3)([finestrainferiore, T(1)(x * 4)]))])


        finestrainferiore = T([1, 3])([x * 1.5, z * 0.3])(finestrella2(x, y, z, 0, 0))
        muroinferiore = STRUCT([muroinferiore, STRUCT(NN(4)([finestrainferiore, T(1)(x * 4)]))])
        muro = STRUCT([T(1)(x * 0.1)(muroinferiore), T(3)(z * 2)(muro)])

    return muro
def muro_ovest(x, y, z, tetto_bool, secondop_bool):

    # analogo che per est

    muro1 = T(3)(z * 2.2)(muro_con_porta(x, y, z, z * 10.2, 0, 0, 1, 0))
    murox = SIZE(1)(muro1)
    muroy = SIZE(2)(muro1)
    tetto = tettoia(x, y, z, murox, muroy)
    scale = scala(x * 1.2, y * 0.5, z * 5, 12, y * 0.5 * 3)(0, 0, 1)
    scale = COMP([T(3)(z * 2.2), R([1, 2])(-PI / 2)])(scale)
    pavimento = T(3)(z * 2.2)(COLOR(GRAY)(CUBOID([x * 15.9, y * 5, z * 0.2])))
    pavimento2 = T(3)(z * 2.2)(COLOR(GRAY)(CUBOID([x * 16 / 4.1, y * 5, z * 0.2])))
    scalax = SIZE(1)(scale)
    muro_laterale = murolaterale(x, y, z, 0)
    finestra1 = finestra2(x * (1 / 1.3), y * 2, z)
    finestra1 = COMP([T([1, 3])([(x * 8 - SIZE(1)(finestra1)) / 2, z * 1]), R([2, 3])(PI / 2)])(
        finestra1)
    muro3 = CUBOID([x * 8, y * 0.5, z * 3.7])
    murofinestra = DIFFERENCE([muro3, T(2)(y * 0.75)(finestra1)])
    finestra1 = finestra2(x * (1 / 1.3), y, z)
    finestra1 = COMP([T([1, 3])([(x * 8 - SIZE(1)(finestra1)) / 2, z * 1]), R([2, 3])(PI / 2)])(
        finestra1)
    murofinestra = STRUCT([murofinestra, T(2)(y * 0.5)(finestra1)])
    muro4 = muro_con_porta(x, y, z, z * 5, 0, 0, 0, 0)
    muro4 = STRUCT([T(1)(SIZE(1)(muro4))(muro4), CUBOID([x * 4, y * 0.5, z * 5])])
    murofinestra = STRUCT([muro4, T(3)(z * 5)(murofinestra)])
    muro4 = STRUCT([muro4, T(3)(z * 5)(muro3)])
    muro4 = T(3)(z * 2.2)(muro4)
    murofinestra = T(3)(z * 2.2)(murofinestra)
    muro4x = SIZE(1)(muro4)
    muro2 = T(3)(z * 2.2)(muro_con_porta(x, y, z, z * 10.2, 1, 0, 0, 0))
    muro2 = COMP([T([1, 2])([murox + x * 0.1 + y * 0.5 + muro4x, -murox]), R([1, 2])(PI / 2)])(muro2)
    muro5 = T(3)(z * 2.2)(muro_con_porta(x, y, z, z * 8.7, 1, 0, 0, 0))
    muro5 = COMP([T([1, 2])([murox + x * 0.1, -murox]), R([1, 2])(PI / 2)])(muro5)
    muro6 = T(3)(z * 2.2)(muro_con_porta(x, y, z, z * 8.7, 0, 0, 0, 0))
    muro7x = x * 4
    porta1 = porta_legno(x * 0.91, y * 3, z, 0, 0)
    porta1x = x
    muro7 = T(3)(z * 2.2)(CUBOID([muro7x, y * 0.5, z * 8.7]))
    muro7 = DIFFERENCE([muro7, T([1, 2, 3])([muro7x - y * 0.1 - porta1x, -y * 0.25, z * 7.2])(porta1)])
    porta1 = porta_legno(x * 0.91, y * 1.77, z, 1, 0)
    muro7 = STRUCT([muro7, T([1, 3])([muro7x - y * 0.1 - porta1x, z * 7.2])(porta1)])
    muro7 = COMP([T([1, 2])([murox + x * 0.1, -murox * 2]), R([1, 2])(PI / 2)])(muro7)
    murovest_result = STRUCT([T([1, 2])([x * 0.08 + murox + muro4x, -y * murox])(muro1),
                     T([1, 2])([murox + x * 0.1, -scalax - y * 0.3])(murofinestra),
                     T([1, 2])([murox + x * 0.1, -murox])(scale),
                     muro2, T([1, 2])([murox + x * 0.1, -y * murox])(muro4), muro5,
                     T([1, 2])([x * 0.1, -y * murox - muro7x])(muro6),
                     muro7])
    murovest_result = STRUCT([muro_laterale, T(3)(-z * 0.2)(murovest_result)])
    if secondop_bool == 1:
        murovest_result = STRUCT([murovest_result, T([1, 2, 3])([x * 0.1, -SIZE(2)(pavimento), z * 4.6])(pavimento),
                         T([1, 2, 3])([x * 0.1, -SIZE(2)(pavimento) * 2, z * 4.6])(pavimento2)])

    if tetto_bool == 1:

        x3 = (x * 0.08 + murox + muro4x) - (((murox * 1.02) - murox) / 2)
        y3 = muroy * 1.1
        z3 = SIZE(3)(murovest_result) + z * 0.5 * 0.4 - z * 1.8
        murovest_result = STRUCT([murovest_result,
                         T([1, 2, 3])([x3, -y3 * 0.3, z3])
                         (S([1, 2])([(x / 1.3) * 1.04, (murox + muroy) / murox * 1.02])(tetto))])
    return murovest_result
def muro_est(x, y, z, tetto_bool, secondop_bool):
    #tettobol== 1 se ha tetto
    #secondop==1 se ha secondo piano

    muro1 = T(3)(z * 2.2)(muro_con_porta(x, y, z, z * 10.2, 0, 0, 1, 0))
    murox = SIZE(1)(muro1)
    muroy = SIZE(2)(muro1)
    tetto = tettoia(x, y, z, murox, muroy)
    scale = scala(x * 1.2, y * 0.5, z * 5, 12, y * 0.5 * 3)(0, 0, 1)
    scalax = SIZE(1)(scale)
    scale = COMP([T(3)(z * 2.2), R([1, 2])(PI / 2)])(scale)
    pavimento = T(3)(z * 2.2)(COLOR(GRAY)(CUBOID([x * 16, y * 5, z * 0.2])))
    pavimento2 = T(3)(z * 2.2)(COLOR(GRAY)(CUBOID([x * 16 / 4.1, y * 5, z * 0.2])))

    # Qua creo i muri interni e li collego su uno dei due muri laterali
    muro_laterale = murolaterale(x, y, z, 1)

    muro2 = T(3)(z * 2.2)(muro_con_porta(x, y, z, z * 10.2, 1, 0, 0, 0))
    muro2 = COMP([T([1, 2])([murox + x * 0.1, -murox]), R([1, 2])(PI / 2)])(muro2)
    finestra1 = finestra2(x * (1 / 1.3), y * 2, z)
    finestra1 = COMP([T([1, 3])([(x * 8 - SIZE(1)(finestra1)) / 2, z * 1]), R([2, 3])(PI / 2)])(
        finestra1)
    muro3 = CUBOID([x * 8, y * 0.5, z * 3.7])
    murofinestra = DIFFERENCE([muro3, T(2)(y * 0.75)(finestra1)])
    finestra1 = finestra2(x * (1 / 1.3), y, z)
    finestra1 = COMP([T([1, 3])([(x * 8 - SIZE(1)(finestra1)) / 2, z * 1]), R([2, 3])(PI / 2)])(
        finestra1)
    murofinestra = STRUCT([murofinestra, T(2)(y * 0.5)(finestra1)])
    muro4 = muro_con_porta(x, y, z, z * 5, 0, 0, 0, 0)
    muro4 = STRUCT([T(1)(SIZE(1)(muro4))(CUBOID([x * 4, y * 0.5, z * 5])), muro4])
    murofinestra = STRUCT([muro4, T(3)(z * 5)(murofinestra)])
    muro4 = STRUCT([muro4, T(3)(z * 5)(muro3)])
    muro4 = T(3)(z * 2.2)(muro4)
    murofinestra = T(3)(z * 2.2)(murofinestra)
    muro4x = SIZE(1)(muro4)

    muro5 = T(3)(z * 2.2)(muro_con_porta(x, y, z, z * 8.7, 1, 0, 0, 0))
    muro5 = COMP([T([1, 2])([murox + x * 0.4 + muro4x, -murox]), R([1, 2])(PI / 2)])(muro5)

    muro6 = T(3)(z * 2.2)(muro_con_porta(x, y, z, z * 8.7, 0, 0, 0, 0))

    muro7x = x * 4
    porta1 = porta_legno(x * 0.91, y * 3, z, 0, 0)
    porta1x = x
    muro7 = T(3)(z * 2.2)(CUBOID([muro7x, y * 0.5, z * 8.7]))
    muro7 = DIFFERENCE([muro7, T([1, 2, 3])([muro7x - y * 0.1 - porta1x, -y * 0.25, z * 7.2])(porta1)])
    porta1 = porta_legno(x * 0.91, y * 1.77, z, 1, 0)
    muro7 = STRUCT([muro7, T([1, 3])([muro7x - y * 0.1 - porta1x, z * 7.2])(porta1)])
    muro7 = COMP([T([1, 2])([murox + x * 0.4 + muro4x, -murox * 2]), R([1, 2])(PI / 2)])(muro7)

    muro8 = T(3)(z * 2.2)(muro_con_porta(x * 3.9, y, z, z * 8.7, 0, 1, 0, 1))
    muro8 = COMP([T([1, 2])([murox + x * 0.1, -murox - SIZE(1)(muro8)]), R([1, 2])(PI / 2)])(muro8)

    muroest_result = STRUCT([T([1, 2])([x * 0.1, -y * murox])(muro1),
                     muro2, T([1, 2])([murox + x * 0.1, -y * murox])(muro4),
                     T([1, 2])(
                         [murox + x * 0.1 + SIZE(1)(scale) - SIZE(1)(scale) + muro4x, -y * murox - SIZE(2)(scale)])(
                         scale),
                     T([1, 2])([murox + x * 0.1, -y * murox - scalax - y * 0.5])(murofinestra), muro5,
                     T([1, 2])([murox + x * 0.1 + muro4x, -y * murox - muro7x])(muro6),
                     muro7, muro8])
    muroest_result = STRUCT([muro_laterale, T(3)(-z * 0.2)(muroest_result)])

    # aggiungere piano 2
    if secondop_bool == 1:
        muroest_result = STRUCT([muroest_result, T([1, 2, 3])([x * 0.1, -SIZE(2)(pavimento), z * 4.6])(pavimento),
                         T([1, 2, 3])(
                             [x * 0.1 + SIZE(1)(pavimento) - SIZE(1)(pavimento2), -SIZE(2)(pavimento) * 2, z * 4.6])(
                             pavimento2)])
    #tetto aggiuntivo
    if tetto_bool == 1:

        V = vertici((murox * 3) + SIZE(2)(muro1), muroy * 1.1, z * 0.5, 0.6, 0)


        asserect = MKPOL([V, [[1, 4, 3, 5, 2], [6, 9, 8, 10, 7]], []])
        assecub = MKPOL([V, [[1, 2, 11, 12], [6, 7, 13, 14]], []])
        su = MKPOL([V, [[15, 10, 5]], []])
        asserect = COLOR(Colore_tegola)(JOIN(asserect))
        su = COLOR(Colore_tegola)(su)
        assecub = JOIN(assecub)

        # sistemazione
        x_sposta_tetto, z_sposta_tetto = muro4x / 2, SIZE(3)(muro4) + z * 2.2 + SIZE(3)(assecub)
        assecub = T([1, 3])([x_sposta_tetto, z_sposta_tetto])(assecub)
        asserect = T([1, 3])([x_sposta_tetto, z_sposta_tetto])(asserect)
        su = T([1, 3])([x_sposta_tetto, z_sposta_tetto])(su)
        V2 = vertici((murox * 3) + SIZE(2)(muro1), muroy * 1.1, z * 0.5, 0, 0.6)
        asserect2 = MKPOL([V2, [[1, 4, 3, 5, 2], [6, 9, 8, 10, 7]], []])
        assecub2 = MKPOL([V2, [[1, 2, 11, 12], [6, 7, 13, 14]], []])
        su2 = MKPOL([V2, [[15, 10, 5]], []])
        asserect2 = COLOR(Colore_tegola)(JOIN(asserect2))
        su2 = COLOR(Colore_tegola)(su2)
        assecub2 = JOIN(assecub2)

        tetto2x, tetto2z = muro4x / 2, SIZE(3)(muro4) + z * 2.2 + SIZE(3)(
            assecub2)
        assecub2 = T([1, 3])([tetto2x, tetto2z])(
            assecub2)
        asserect2 = T([1, 3])([tetto2x, tetto2z])(
            asserect2)
        su2 = T([1, 3])([tetto2x, tetto2z])(su2)

        x2, y2 = SIZE(1)(assecub) + SIZE(1)(muro1) * 2, -SIZE(1)(muro1) * 6 + SIZE(2)(
            assecub) + SIZE(2)(assecub) / 2
        assecub2 = COMP([T([1, 2])([x2, y2]), R([1, 2])(PI)])(
            assecub2)
        asserect2 = COMP([T([1, 2])([x2, y2]), R([1, 2])(PI)])(
            asserect2)
        su2 = COMP([T([1, 2])([x2, y2]), R([1, 2])(PI)])(su2)
        assecub = JOIN([assecub, assecub2])
        asserect = COLOR(Colore_tegola)(JOIN([asserect2, asserect]))
        su = COLOR(Colore_tegola)(JOIN([su, su2]))
        tetto_grande = STRUCT([assecub, asserect, su])
        x3 = (x * 0.08 + murox + muro4x) - (((murox * 1.02) - murox) / 2)
        y3 = muroy * 1.1
        z3 = z * 14 + z * 0.5 * 0.4 - z * 1.8
        muroest_result = STRUCT([muroest_result, T([2, 3])([-y * 0.2, -z * 0.2])(tetto_grande), T([2, 3])([-y * 0.3, z3])(
            S([1, 2])([(x / 1.3) * 1.04, (murox + muroy) / murox * 1.02])(tetto))])

    return muroest_result

#colori utilizzati
Colore_legno = [0.3, 0.2, 0.1]
Colore_legno_2 = [0.627455, 0.321569, 0.176471]
Colore_mattone = [0.8696, 0.8486, 0.73058]
Colore_mattone_2 = [0.97, 0.94, 0.9]
Colore_prato = [0.2, 0.4, 0.05]
Colore_tegola = [0.553, 0.349, 0.306]
Colore_main = [0.9356,0.94431373,0.93137]


# ornamento interno
def affresco(x, y, z):
    x = x / 1.3
    # definiso punto al centro della cupola e dominio
    curva_up = BEZIER(S1)([[x * 2.6, y * 2, z * 1]])
    dominio1 = PROD([INTERVALS(1)(32), INTERVALS(1)(1)])

    # allungamento dietro
    curva_sx = BEZIER(S1)([[x * 0, y * 0, z * 0], [x * 2.6, y * 0, z * 2], [x * 5.2, y * 0, z * 0]])
    curva_sx_1 = BEZIER(S1)([[x * 0, -y * 1.35, z * 0], [x * 2.6, -y * 1.35, z * 2], [x * 5.2, -y * 1.35, z * 0]])
    curva_2D = BEZIER(S2)([curva_sx, curva_sx_1])
    curva_2D = MAP(curva_2D)(dominio1)
    curva_2D = TEXTURE('./immagini/bordo.jpeg')(curva_2D)

    # le curve della cupola
    curva_sx2 = BEZIER(S1)([[x * 0, y * 0, z * 0], [x * 0, y * 2, z * 2], [x * 0, y * 4, z * 0]])
    curva_2D2 = BEZIER(S2)([curva_sx2, curva_up])
    curva_2D2 = MAP(curva_2D2)(dominio1)

    curva_sx3 = BEZIER(S1)([[x * 0, y * 4, z * 0], [x * 2.6, y * 4, z * 2], [x * 5.2, y * 4, z * 0]])
    curva_2D3 = BEZIER(S2)([curva_sx3, curva_up])
    curva_2D3 = MAP(curva_2D3)(dominio1)

    # allungamneto a sinistra
    curva_sx4 = BEZIER(S1)([[x * 5.2, y * 0, z * 0], [x * 5.2, y * 2, z * 2], [x * 5.2, y * 4, z * 0]])
    curva_sx5 = BEZIER(S1)([[x * 8, y * 0, z * 0], [x * 8, y * 2, z * 2], [x * 8, y * 4, z * 0]])
    curva_2D5 = BEZIER(S2)([curva_sx4, curva_sx5])
    curva_2D5 = MAP(curva_2D5)(dominio1)
    curva_2D5 = TEXTURE('./immagini/affresco.jpeg')(curva_2D5)

    # assemblo il tutto
    cupola = TEXTURE('./immagini/affresco2.jpg')(
        STRUCT([curva_2D2, curva_2D3, T([1, 2])([x * 5.2, y * 4])(R([1, 2])(-PI)(curva_2D2)),
                T([1, 2])([x * 5.2, y * 4])(R([1, 2])(PI)(curva_2D3))]))
    return STRUCT([cupola, curva_2D5, curva_2D, T(2)(y * 5.35)(curva_2D)])

def villaPisani(tetto_bool, piano2_bool, chiusa_sotto):
    x = 1.3
    y = 1.0
    z = 1.0
    sud = muro_sud(x, y, z)
    sud = COLOR(Colore_main)(sud)
    muroovest = muro_ovest(x, y, z, 1, 1)

    muroest = muro_est(x, y, z, tetto_bool, piano2_bool)
    muroest = COLOR(Colore_main)(muroest)
    muroy = y * 0.6
    sudx = SIZE(1)(sud)
    muroovestx = SIZE(1)(muroovest)
    muroovest = muro_ovest(x, y, z, tetto_bool, piano2_bool)
    muroovest = COLOR(Colore_main)(muroovest)
    sud = S(1)(x / 1.3 * 1.003)(COMP([T([1, 2])([sudx - x * 0.03, z * 0.5]), R([1, 2])(PI)])(sud))
    ovest = COMP([T([1, 2])([muroy - 0.025 * x, -y * 0.23 + muroy]), R([1, 2])(PI / 2)])(muroovest)
    est = COMP([T([1, 2])([x * 23.75, y * 21.41]), R([1, 2])(-PI / 2)])(muroest)
    nord = T(2)(y * 20.78)(muro_nord(x, y, z, tetto_bool))
    nord = COLOR(Colore_main)(nord)

    # erba
    pavimento2 = T([1, 2, 3])([-x * 0.15 + x * 0.2, -y * 0.3 + x * 0.2, z * 1.8])(
        CUBOID([x * 24.1, muroovestx - x * 0.67, z * 0.2]))
    erba = T([1, 2, 3])([-x * 5, -y * 10, z * 1.8])(CUBOID([x * 35, y * 40, z * 0.2]))
    erba = T(3)(-z * 2)(COLOR(Colore_prato)(DIFFERENCE([erba, pavimento2])))

    # pavimento
    pavimento = T([1, 2, 3])([-x * 0.15, -y * 0.2, z * 1.8])(CUBOID([x * 24.4, x * 16.7, z * 0.2]))

    # scale interne
    scale = scala(x * 1.2, y * 0.3, z * 3.7, 10, y * 0.5 * 3)(0, 0, 1)
    scale = T([1, 2, 3])([x * 20 - SIZE(1)(scale) - y * 0.35, y * 12.7, -z * 1.7])(scale)
    scale2 = T(1)(-x * 14.1)(scale)
    pavimento = COLOR(GRAY)(DIFFERENCE([pavimento, T(3)(z * 2.8)(scale), T(3)(z * 2.8)(scale2)]))

    # fondamenta
    murox = x * 7.818
    arcofond = arco_mattonato(x * 0.4, y * 3.2)(z * 1.5, 0, murox)
    arcofond2z = SIZE(3)(arcofond)
    arcofond = S(3)(z * 3.85 - arcofond2z)(arcofond)
    arcofondx, arcofondy, arcofondz = SIZE(1)(arcofond), SIZE(2)(arcofond), SIZE(
        3)(arcofond)
    murofondx = x * 7.81
    murofond = TEXTURE('./immagini/mattone.jpg')(
        CUBOID([murofondx, arcofondy, arcofondz]))
    murofond = COMP([T([1, 2])([murox + arcofondy, -y * 3.5]), R([1, 2])(PI / 2)])(murofond)
    arcofondsx = arco_mattonato(x * 0.4, y * 3.2)(z * 1.5, 1, murox)
    arcofondsx = T(1)(murox + arcofondy)(S(3)(z * 3.85 - arcofond2z)(arcofondsx))
    scalefond = T([1, 2])([-x * 2.15, -y * 3.8])(scala(x, y * 0.3, z * 1.8, 6, y * 0.3)(0, 0, 1))
    fondamenta = STRUCT(
        [arcofond, T(2)(y * 8)(arcofond), murofond, T(2)(murofondx)(murofond),
         arcofondsx, T(2)(y * 8)(arcofondsx), scalefond, T(1)(x * 20.1)(scalefond)])
    fondamenta = T([1, 2, 3])([x * 3.7, y * 4, -z * 1.8])(fondamenta)

    # salone
    affresco1 = affresco(x * 2, y * 2.38, z)
    affresco1 = COMP([T([1, 2, 3])([x * 10.96 / 1.3, y * 16.1, z * 9.5]), R([1, 2])(-PI / 2)])(affresco1)
    colonne = T(3)(z * 2)(colonna(x * 0.5, y * 0.5, z * 7.5))
    colonnesx = STRUCT([T([1, 2])([x * 15.69, y * 0.2])(colonne), T([1, 2])([x * 15.6, y * 0.1])(colonne)])
    colonnedx = STRUCT([T([1, 2])([x * 8.11, y * 0.2])(colonne), T([1, 2])([x * 8.2, y * 0.1])(colonne)])
    colonne = STRUCT([T([1, 2])([x * 8, y * 16])(colonne), T([1, 2])([x * 15.8, y * 16])(colonne),
                      T([1, 2])([x * 8.1, y * 5.4])(colonne), T([1, 2])([x * 15.7, y * 5.5])(colonne),
                      colonnedx, T([1, 2])([-x * 2.3, y * 5.3])(colonnedx),
                      colonnesx, T([1, 2])([x * 2.3, y * 5.4])(colonnesx),
                      T([1, 2])([x * 5.9, y * 16])(colonne), T([1, 2])([x * 17.9, y * 16])(colonne),
                      T([1, 2])([x * 5.8, y * 15.9])(colonne), T([1, 2])([x * 18, y * 15.9])(colonne)])

    # muro archi
    muro_arco = T([1, 2, 3])([x * 5.3, y * 16.4, z * 2])(muro_archi(x, y, z, tetto_bool))

    # tetto
    if tetto_bool == 1:
        fondamenta = STRUCT([fondamenta, affresco1])

    # con fondamenta
    if chiusa_sotto == 1:
        y_scale = SIZE(2)(scale)
        fondamenta = STRUCT([fondamenta, T(3)(-y_scale + y * 0.5)(COLOR(GRAY)(pavimento2))])

    # assemblo il tutto
    villa= STRUCT([sud, pavimento, est, erba, ovest, nord, scale, scale2, fondamenta, colonne, muro_arco])
    return villa

VIEW(villaPisani(1, 1, 1))
