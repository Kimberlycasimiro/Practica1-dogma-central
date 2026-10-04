"""Simulación de la traducción (ARNm -> proteína)."""

CODON_INICIO = "AUG"
CODONES_STOP = ["UAA", "UAG", "UGA"]

# Código genético estándar: los 64 codones del ARNm (5' -> 3') y su aminoácido.
CODIGO_GENETICO = {
    "UUU": "Phe", "UUC": "Phe", "UUA": "Leu", "UUG": "Leu",
    "CUU": "Leu", "CUC": "Leu", "CUA": "Leu", "CUG": "Leu",
    "AUU": "Ile", "AUC": "Ile", "AUA": "Ile", "AUG": "Met",
    "GUU": "Val", "GUC": "Val", "GUA": "Val", "GUG": "Val",

    "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser",
    "CCU": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "GCU": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",

    "UAU": "Tyr", "UAC": "Tyr", "UAA": "STOP", "UAG": "STOP",
    "CAU": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
    "AAU": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys",
    "GAU": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",

    "UGU": "Cys", "UGC": "Cys", "UGA": "STOP", "UGG": "Trp",
    "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
    "AGU": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
    "GGU": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
}

COMPLEMENTO_ARN = {"A": "U", "U": "A", "C": "G", "G": "C"}


def obtener_anticodon(codon):
    """Devuelve el anticodón del ARNt que reconoce un codón.

    Es complementario y antiparalelo: si el codón es 5' AUG 3', el anticodón,
    escrito alineado debajo, es 3' UAC 5'.
    """
    anticodon = ""
    for base in codon:
        anticodon += COMPLEMENTO_ARN[base]
    return anticodon


def traducir_arnm(arnm):
    """Traduce el ARNm desde el primer AUG hasta el primer codón de parada.

    Devuelve un diccionario con la posición de inicio (-1 si no hay AUG), los codones
    leídos, sus aminoácidos (incluido STOP), el codón de parada (o None) y la proteína.
    """
    inicio = arnm.find(CODON_INICIO)
    codones = []
    aminoacidos = []
    codon_stop = None

    if inicio != -1:
        posicion = inicio
        # El ARNm se lee en grupos de tres nucleótidos sin solapamiento.
        while posicion + 3 <= len(arnm):
            codon = arnm[posicion:posicion + 3]
            codones.append(codon)
            aminoacidos.append(CODIGO_GENETICO[codon])
            if codon in CODONES_STOP:
                codon_stop = codon
                break
            posicion += 3

    # El codón de parada no codifica ningún aminoácido: no forma parte de la proteína.
    proteina = []
    for aminoacido in aminoacidos:
        if aminoacido != "STOP":
            proteina.append(aminoacido)

    return {
        "arnm": arnm,
        "inicio": inicio,
        "codones": codones,
        "aminoacidos": aminoacidos,
        "codon_stop": codon_stop,
        "proteina": proteina,
    }


def dibujar_ribosoma(codones, aminoacidos):
    """Dibuja el ribosoma al inicio de la traducción: el AUG en el sitio P y el
    segundo codón en el sitio A."""
    codon_p = codones[0]
    anticodon_p = obtener_anticodon(codon_p)
    aminoacido_p = aminoacidos[0]

    # Si no hay segundo codón o es de parada, ningún ARNt entra en el sitio A.
    codon_a = "···"
    anticodon_a = "   "
    aminoacido_a = "   "
    if len(codones) > 1:
        codon_a = codones[1]
        if codon_a not in CODONES_STOP:
            anticodon_a = obtener_anticodon(codon_a)
            aminoacido_a = aminoacidos[1]

    return "\n".join([
        "                    RIBOSOMA",
        "           ┌────────────────────────┐",
        "           │    " + aminoacido_p + "         " + aminoacido_a + "     │   ← aminoácidos",
        "           │     |           |      │",
        "           │    " + anticodon_p + "         " + anticodon_a + "     │   ← anticodones de los ARNt (3'→5')",
        "           │    :::         :::     │",
        "  5' ······┼─── " + codon_p + " ─────── " + codon_a + " ────┼······ 3'   ARNm",
        "           │   sitio P     sitio A  │",
        "           └────────────────────────┘",
        "              el ribosoma avanza 5' → 3', un codón cada vez →",
    ])


def texto_traduccion(resultado):
    """Genera el texto que se muestra en la pestaña de traducción."""
    arnm = resultado["arnm"]
    inicio = resultado["inicio"]
    codones = resultado["codones"]
    aminoacidos = resultado["aminoacidos"]
    lineas = []

    lineas.append("TRADUCCIÓN  (ARNm → proteína)")
    lineas.append("=" * 70)
    lineas.append("La traducción ocurre en el RIBOSOMA, que recorre el ARNm 5' → 3' leyendo")
    lineas.append("un codón (3 nucleótidos) cada vez. Cada ARNt reconoce el codón mediante su")
    lineas.append("anticodón y transporta el aminoácido correspondiente. El ribosoma une los")
    lineas.append("aminoácidos formando la cadena polipeptídica.")
    lineas.append("")
    lineas.append("  - Inicio: el primer codón AUG (Met).")
    lineas.append("  - Parada: UAA, UAG o UGA. Ningún ARNt los reconoce; la traducción termina")
    lineas.append("    y la proteína se libera. STOP no es un aminoácido.")
    lineas.append("")
    lineas.append("ARNm 5' " + arnm + " 3'")
    lineas.append("")

    if inicio == -1:
        lineas.append("No se ha encontrado un codón de inicio AUG.")
        lineas.append("No se puede sintetizar ninguna proteína.")
        return "\n".join(lineas)

    lineas.append("Primer AUG en la posición " + str(inicio + 1) + " del ARNm.")
    if inicio > 0:
        lineas.append("Los " + str(inicio) + " nucleótidos anteriores (" + arnm[:inicio]
                      + ") no se traducen.")
    lineas.append("")

    lineas.append("LECTURA EN CODONES:")
    fila_codones = ""
    fila_aminoacidos = ""
    for i in range(len(codones)):
        if i > 0:
            fila_codones += " | "
            fila_aminoacidos += " | "
        fila_codones += codones[i].ljust(4)
        fila_aminoacidos += aminoacidos[i].ljust(4)
    lineas.append("  " + fila_codones)
    lineas.append("  " + fila_aminoacidos)
    lineas.append("")

    lineas.append(dibujar_ribosoma(codones, aminoacidos))
    lineas.append("")

    lineas.append("CORRESPONDENCIA CODÓN - ARNt - AMINOÁCIDO:")
    lineas.append("  Nº     Codón ARNm (5'→3')   Anticodón ARNt (3'→5')   Aminoácido")
    for i in range(len(codones)):
        codon = codones[i]
        if codon in CODONES_STOP:
            anticodon = "ninguno"
            aminoacido = "STOP (fin de la traducción)"
        else:
            anticodon = obtener_anticodon(codon)
            aminoacido = aminoacidos[i]
        lineas.append("  " + str(i + 1).ljust(7) + codon.ljust(21) + anticodon.ljust(25) + aminoacido)
    lineas.append("")

    if resultado["codon_stop"] is not None:
        lineas.append("Codón de parada encontrado: " + resultado["codon_stop"] + ". Termina la traducción.")
    else:
        lineas.append("No se ha encontrado codón de parada después del AUG: la traducción llega")
        lineas.append("al final del ARNm y la proteína obtenida estaría incompleta.")
    lineas.append("")
    lineas.append("PROTEÍNA (" + str(len(resultado["proteina"])) + " aminoácidos):")
    lineas.append("  " + "-".join(resultado["proteina"]))
    return "\n".join(lineas)
