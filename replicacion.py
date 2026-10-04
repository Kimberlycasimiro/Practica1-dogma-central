"""Simulación didáctica de la replicación del ADN (ADN -> ADN).

Convenio usado en todo el programa:
- La secuencia introducida es la hebra superior, escrita 5' -> 3' de izquierda a derecha.
- La hebra inferior se guarda alineada debajo, es decir, escrita 3' -> 5' de izquierda a derecha.
- El origen de replicación está en el extremo izquierdo y la horquilla avanza hacia la derecha.
"""

# Tamaños didácticos (no son los biológicos reales, que son mucho mayores).
TAMANO_FRAGMENTO = 6   # nucleótidos por fragmento de Okazaki
TAMANO_CEBADOR = 2     # nucleótidos de ARN de cada cebador
LIMITE_DIBUJO = 48     # nucleótidos que se dibujan como máximo (múltiplo de TAMANO_FRAGMENTO)

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


def dibujar_horquilla(resultado):
    """Dibuja en texto la horquilla con la cadena líder y la rezagada alineadas con sus moldes."""
    superior = resultado["hebra_superior"][:LIMITE_DIBUJO]
    inferior = resultado["hebra_inferior"][:LIMITE_DIBUJO]
    lider = resultado["lider_con_cebador"][:LIMITE_DIBUJO]

    rezagada = ""
    flechas_rezagada = ""
    etiquetas = ""
    for fragmento in resultado["fragmentos"]:
        if fragmento["inicio"] >= LIMITE_DIBUJO:
            break
        ancho = len(fragmento["alineado_con_cebador"])
        rezagada += fragmento["alineado_con_cebador"]
        # Cada fragmento crece hacia la izquierda (hacia su extremo 3').
        flechas_rezagada += "←" + "─" * (ancho - 1)
        etiquetas += ("F" + str(fragmento["numero"])).ljust(ancho)

    flecha_lider = "─" * (len(lider) - 1) + "→"
    sangria = " " * 22

    lineas = [
        "                    HORQUILLA DE REPLICACIÓN",
        "",
        sangria + "origen ──────> la horquilla (helicasa) avanza →",
        "",
        "Hebra parental     5' " + superior + " 3'",
        "Nueva (rezagada)   3' " + rezagada + " 5'",
        sangria + flechas_rezagada + "   síntesis discontinua, cada fragmento 5'→3'",
        sangria + etiquetas + "   fragmentos de Okazaki",
        "",
        "Hebra parental     3' " + inferior + " 5'",
        "Nueva (líder)      5' " + lider + " 3'",
        sangria + flecha_lider + "   síntesis continua 5'→3'",
        "",
        "Letras minúsculas = cebador de ARN colocado por la primasa.",
    ]
    if len(resultado["hebra_superior"]) > LIMITE_DIBUJO:
        lineas.append("(Solo se dibujan los primeros " + str(LIMITE_DIBUJO)
                      + " nucleótidos; los fragmentos se listan completos más abajo.)")
    return "\n".join(lineas)


def texto_replicacion(resultado):
    """Genera el texto que se muestra en la pestaña de replicación."""
    superior = resultado["hebra_superior"]
    inferior = resultado["hebra_inferior"]
    lineas = []

    lineas.append("REPLICACIÓN DEL ADN  (ADN → ADN)")
    lineas.append("=" * 70)
    lineas.append("Enzimas que intervienen:")
    lineas.append("  Helicasa       Separa las dos cadenas de ADN al abrir la doble hélice.")
    lineas.append("  Primasa        Coloca los cebadores que permiten iniciar la síntesis.")
    lineas.append("  ADN polimerasa Añade nucleótidos complementarios y sintetiza la nueva")
    lineas.append("                 cadena de ADN, siempre en dirección 5' → 3'.")
    lineas.append("  ADN ligasa     Une los fragmentos de Okazaki de la cadena rezagada.")
    lineas.append("")

    lineas.append("0) MOLÉCULA DE ADN INICIAL (doble hélice cerrada)")
    lineas.append("   5' " + superior + " 3'")
    lineas.append("      " + "|" * len(superior))
    lineas.append("   3' " + inferior + " 5'")
    lineas.append("")

    lineas.append("1) HELICASA: apertura de la doble hélice")
    lineas.append("   La helicasa rompe los puentes de hidrógeno entre las bases y separa")
    lineas.append("   las dos hebras parentales, que pasan a actuar como molde:")
    lineas.append("   5' " + superior + " 3'   → molde de la cadena rezagada")
    lineas.append("")
    lineas.append("   3' " + inferior + " 5'   → molde de la cadena líder")
    lineas.append("")

    lineas.append("2) PRIMASA: colocación de cebadores")
    lineas.append("   La ADN polimerasa no puede empezar una cadena desde cero; necesita un")
    lineas.append("   cebador corto de ARN con un extremo 3' libre.")
    lineas.append("")
    lineas.append("        Primasa")
    lineas.append("           ↓")
    lineas.append("        Cebador (ARN)")
    lineas.append("           ↓")
    lineas.append("        ADN polimerasa")
    lineas.append("           ↓")
    lineas.append("        Síntesis 5' → 3'")
    lineas.append("")
    lineas.append("   Cadena líder:    1 cebador en el origen: 5' " + resultado["cebador_lider"] + " 3'")
    lineas.append("   Cadena rezagada: 1 cebador por cada fragmento de Okazaki ("
                  + str(len(resultado["fragmentos"])) + " cebadores)")
    lineas.append("")

    lineas.append("3) ADN POLIMERASA: síntesis de las nuevas cadenas")
    lineas.append("")
    lineas.append(dibujar_horquilla(resultado))
    lineas.append("")
    lineas.append("   Cadena líder (continua), escrita 5' → 3':")
    lineas.append("     5' " + resultado["lider_con_cebador"] + " 3'")
    lineas.append("")
    lineas.append("   Cadena rezagada (discontinua): fragmentos de Okazaki, cada uno escrito 5' → 3'.")
    lineas.append("   Cada fragmento empieza en su cebador (extremo 5') y se sintetiza en")
    lineas.append("   sentido contrario al avance de la horquilla:")
    for fragmento in resultado["fragmentos"]:
        posiciones = "(posiciones " + str(fragmento["inicio"] + 1) + "-" + str(fragmento["fin"]) + ")"
        lineas.append("     Fragmento " + str(fragmento["numero"]).ljust(4) + posiciones.ljust(24)
                      + "5' " + fragmento["secuencia_5_3"] + " 3'   cebador: " + fragmento["cebador"])
    lineas.append("")

    lineas.append("4) SUSTITUCIÓN DE CEBADORES Y ADN LIGASA")
    lineas.append("   Los cebadores de ARN (el de la cadena líder y el de cada fragmento) se eliminan")
    lineas.append("   y la ADN polimerasa rellena el hueco con ADN. En la cadena rezagada quedan")
    lineas.append("   fragmentos separados por mellas (marcadas con |):")
    lineas.append("     3' " + resultado["rezagada_con_huecos"] + " 5'")
    lineas.append("                ↓")
    lineas.append("            ADN ligasa")
    lineas.append("                ↓")
    lineas.append("   Cadena rezagada completa:")
    lineas.append("     3' " + resultado["rezagada"] + " 5'")
    lineas.append("")

    lineas.append("5) RESULTADO: REPLICACIÓN SEMICONSERVATIVA")
    lineas.append("   Se obtienen dos moléculas hijas. Cada una tiene 1 hebra parental + 1 hebra nueva.")
    hijo_1 = resultado["hijo_1"]
    hijo_2 = resultado["hijo_2"]
    lineas.append("")
    lineas.append("   ADN HIJO 1:  hebra parental superior + nueva cadena rezagada")
    lineas.append("     5' " + hijo_1["hebra_5_3"] + " 3'  (parental)")
    lineas.append("        " + "|" * len(hijo_1["hebra_5_3"]))
    lineas.append("     3' " + hijo_1["hebra_3_5"] + " 5'  (nueva)")
    lineas.append("")
    lineas.append("   ADN HIJO 2:  nueva cadena líder + hebra parental inferior")
    lineas.append("     5' " + hijo_2["hebra_5_3"] + " 3'  (nueva)")
    lineas.append("        " + "|" * len(hijo_2["hebra_5_3"]))
    lineas.append("     3' " + hijo_2["hebra_3_5"] + " 5'  (parental)")

    identicas = (resultado["hijo_1"]["hebra_5_3"] == resultado["hijo_2"]["hebra_5_3"] == superior
                 and resultado["hijo_1"]["hebra_3_5"] == resultado["hijo_2"]["hebra_3_5"] == inferior)
    lineas.append("")
    if identicas:
        lineas.append("   Comprobación: las dos moléculas hijas son idénticas a la molécula inicial.")
    else:
        lineas.append("   ERROR: las moléculas hijas no coinciden con la molécula inicial.")
    return "\n".join(lineas)
