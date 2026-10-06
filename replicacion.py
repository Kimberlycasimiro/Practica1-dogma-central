"""Simulación didáctica de la replicación del ADN (ADN -> ADN).

Convenio usado en todo el programa:
- La secuencia introducida es la hebra superior, escrita 5' -> 3' de izquierda a derecha.
- La hebra inferior se guarda alineada debajo, es decir, escrita 3' -> 5' de izquierda a derecha.
- El origen de replicación está en el extremo izquierdo y la horquilla avanza hacia la derecha.
"""

# Tamaños didácticos (no son los biológicos reales, que son mucho mayores).
TAMANO_FRAGMENTO = 6   # nucleótidos por fragmento de Okazaki
TAMANO_CEBADOR = 2     # nucleótidos de ARN de cada cebador

COMPLEMENTO_ADN = {"A": "T", "T": "A", "C": "G", "G": "C"}


def complementaria_adn(secuencia):
    """Devuelve la secuencia complementaria base a base (A-T, C-G), alineada con la original."""
    complementaria = ""
    for base in secuencia:
        complementaria += COMPLEMENTO_ADN[base]
    return complementaria


def crear_cebador(secuencia_adn):
    """Convierte un trozo de ADN en el cebador de ARN equivalente (T -> U).

    Se escribe en minúsculas para distinguirlo del ADN en la visualización.
    """
    return secuencia_adn.replace("T", "U").lower()


def invertir(secuencia):
    """Invierte una secuencia. Sirve para escribir en 5' -> 3' una cadena guardada 3' -> 5'."""
    return secuencia[::-1]


def crear_fragmentos_okazaki(molde_5_3):
    """Genera los fragmentos de Okazaki de la cadena rezagada.

    El molde de la rezagada es la hebra 5' -> 3'. La nueva cadena tiene que ser
    antiparalela (3' -> 5' de izquierda a derecha) y la ADN polimerasa solo sintetiza
    5' -> 3', es decir, de derecha a izquierda, en sentido contrario al avance de la
    horquilla. Por eso se sintetiza a trozos a medida que la helicasa abre la hélice.
    """
    fragmentos = []
    for inicio in range(0, len(molde_5_3), TAMANO_FRAGMENTO):
        trozo_molde = molde_5_3[inicio:inicio + TAMANO_FRAGMENTO]
        nuevo_adn = complementaria_adn(trozo_molde)   # alineado 3' -> 5'

        # El extremo 5' del fragmento está a la derecha: ahí la primasa coloca el cebador
        # y desde ahí la ADN polimerasa sintetiza hacia la izquierda.
        longitud_cebador = min(TAMANO_CEBADOR, len(nuevo_adn))
        corte = len(nuevo_adn) - longitud_cebador
        cebador = crear_cebador(nuevo_adn[corte:])
        con_cebador = nuevo_adn[:corte] + cebador     # alineado 3' -> 5'

        fragmento = {
            "numero": len(fragmentos) + 1,
            "inicio": inicio,
            "fin": inicio + len(trozo_molde),
            "cebador": cebador,
            "alineado_con_cebador": con_cebador,
            "alineado_sin_cebador": nuevo_adn,
            "secuencia_5_3": invertir(con_cebador),
        }
        fragmentos.append(fragmento)
    return fragmentos


def simular_replicacion(adn):
    """Simula la horquilla de replicación y devuelve todas las cadenas implicadas."""
    hebra_superior = adn                              # parental 5' -> 3'
    hebra_inferior = complementaria_adn(adn)          # parental 3' -> 5'

    # Cadena líder: su molde es la hebra inferior (3' -> 5'). La nueva cadena crece
    # 5' -> 3' en el mismo sentido en que avanza la horquilla, así que basta un único
    # cebador en el origen y la síntesis es continua.
    lider = complementaria_adn(hebra_inferior)        # nueva 5' -> 3'
    longitud_cebador = min(TAMANO_CEBADOR, len(lider))
    cebador_lider = crear_cebador(lider[:longitud_cebador])
    lider_con_cebador = cebador_lider + lider[longitud_cebador:]

    # Cadena rezagada: síntesis discontinua mediante fragmentos de Okazaki.
    fragmentos = crear_fragmentos_okazaki(hebra_superior)

    # Los cebadores se sustituyen por ADN y la ADN ligasa une los fragmentos.
    rezagada = ""
    rezagada_con_huecos = ""
    for fragmento in fragmentos:
        rezagada += fragmento["alineado_sin_cebador"]
        if rezagada_con_huecos != "":
            rezagada_con_huecos += "|"
        rezagada_con_huecos += fragmento["alineado_sin_cebador"]

    # Replicación semiconservativa: cada molécula hija conserva una hebra parental.
    hijo_1 = {"hebra_5_3": hebra_superior, "hebra_3_5": rezagada}   # parental + nueva
    hijo_2 = {"hebra_5_3": lider, "hebra_3_5": hebra_inferior}      # nueva + parental

    return {
        "hebra_superior": hebra_superior,
        "hebra_inferior": hebra_inferior,
        "cebador_lider": cebador_lider,
        "lider_con_cebador": lider_con_cebador,
        "lider": lider,
        "fragmentos": fragmentos,
        "rezagada_con_huecos": rezagada_con_huecos,
        "rezagada": rezagada,
        "hijo_1": hijo_1,
        "hijo_2": hijo_2,
    }
