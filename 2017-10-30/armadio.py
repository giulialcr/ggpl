from pyplasm import *

def tavolo(width, depth, height):
    plane=CUBOID([width,depth*1.5,height*.1])
    legs=CUBOID([width*.1,depth*.1,height*.8])
    return STRUCT([legs,T(3)(height*.8)(plane),T([1,2])([width*.9,depth*1.4])(legs),T(1)(width*.9)(legs),T(2)(depth*1.4)(legs)])

def desk(width,depth,height):

    tabl=tavolo(width, depth, height)
    chair=tavolo(width * 0.5, depth * 0.333, height * 0.5)
    cubo=CUBOID([width*.05,depth*1.5*0.333,height*0.5])
    chair=STRUCT([chair,T([1,3])([width*0.45,height*0.4])(cubo)])
    return STRUCT([tabl,T([1,2])([width*0.7,depth*0.6])(chair)])

def HEX(color, alpha = 1):

	def hex_to_rgb(value):
		value = value.lstrip('#')
		lv = len(value)
		return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

	rgb = hex_to_rgb(color)

	return COLOR(Color4f([rgb[0]/255., rgb[1]/255., rgb[2]/255., alpha]))

def hex_material(color, light, trasparence):

    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return map(lambda x: x/255., list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))

    # ambientRGBA, diffuseRGBA specularRGBA emissionRGBA shininess
    params = hex_to_rgb(color) + [.1] + \
             hex_to_rgb(light) + [trasparence] +\
             hex_to_rgb(light) + [.1] +\
             hex_to_rgb("#000000") + [.1] +\
             [100]

    return MATERIAL(params)


def armadio(larghezza_armadio,altezza_armadio,profondita_armadio,spessore_cornice,numero_ante,numero_ripiani,color):


    def anta(larghezza_anta):

        cornice = CUBOID([larghezza_anta, altezza_armadio, spessore_cornice])
        vetro = T([1, 2])([spessore_cornice, spessore_cornice])(
            CUBOID([larghezza_anta - spessore_cornice * 2, altezza_armadio - spessore_cornice * 2, spessore_cornice]))
        vetro = hex_material("#00EAFF", "#00EAFF", .4)(vetro)
        cornice = STRUCT([
            HEX("#ffc4ff")(T([1, 2])([spessore_cornice/2, altezza_armadio/3])(DIFFERENCE([
                T([1, 2, 3])([larghezza_anta - spessore_cornice, spessore_cornice, spessore_cornice])(
                    CUBOID([spessore_cornice/2, spessore_cornice * 2, spessore_cornice])),
                T([1, 2, 3])([larghezza_anta - spessore_cornice, spessore_cornice-(spessore_cornice/3), spessore_cornice-(spessore_cornice/3)])(
                    CUBOID([spessore_cornice/2, spessore_cornice * 2, spessore_cornice])),
            ]))),
            HEX(color)(DIFFERENCE([cornice, vetro]))
        ])

        return STRUCT([cornice, vetro])

    def ante(N):

        if(N == 0):
            return CUBOID([0])
        return STRUCT(map(lambda i: T([1, 3])([float(larghezza_armadio)/N*i, profondita_armadio])(
            anta(float(larghezza_armadio)/N)), range(0, N)))

    def ripiani(N):


        if (N == 0):
            return CUBOID([0])
        return STRUCT(map(lambda i: T([1, 2])([spessore_cornice, (float(altezza_armadio)/(N+1))*(i+1)])(ripiano()), range(0, N)))

    def ripiano():
        return HEX(color)(CUBOID([larghezza_armadio - (spessore_cornice * 2), spessore_cornice, profondita_armadio]))

    def struttura():
        return HEX(color)(DIFFERENCE([
            CUBOID([larghezza_armadio, altezza_armadio, profondita_armadio]),
            T([1, 2, 3])([spessore_cornice, spessore_cornice, spessore_cornice])(CUBOID([
                larghezza_armadio-(spessore_cornice*2),
                altezza_armadio-(spessore_cornice*2),
                profondita_armadio
            ]))
        ]))

    return STRUCT([
        ante(numero_ante),
        ripiani(numero_ripiani),
        struttura()
    ])


def composizione_armadio():
    armadio1 = T([1, 2, 3])([0, 0, 0])(armadio(
        larghezza_armadio=1.2,
        altezza_armadio=2.8,
        profondita_armadio=1.2,
        spessore_cornice=.04,
        numero_ante=0,
        numero_ripiani=6,
        color="#2c3e50",
    ))

    armadio2 = T([1, 2, 3])([1.2, 1.6, 0])(armadio(
        larghezza_armadio=2,
        altezza_armadio=1.2,
        profondita_armadio=.7,
        spessore_cornice=.04,
        numero_ante=4,
        numero_ripiani=2,
        color="#34495e",
    ))

    armadio3 = T([1, 2, 3])([3.2, 1.6, 0])(armadio(
        larghezza_armadio=1,
        altezza_armadio=.6,
        profondita_armadio=.7,
        spessore_cornice=.04,
        numero_ante=0,
        numero_ripiani=0,
        color="#2c3e50",
    ))

    pavimento = HEX("fffff4")(CUBOID([6, 0, 4]))

    parete = HEX("ffff33")(CUBOID([6, 3.5]))



    return STRUCT([parete, pavimento,T([1,3])([3,4])((R([2,3])(-PI/2)(desk(1.5,1.5,1.5)))), T(1)(1)(STRUCT([armadio1, armadio2, armadio3]))])

VIEW(composizione_armadio())
