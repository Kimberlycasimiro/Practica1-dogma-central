"""Explicaciones en texto de cada etapa (parte inferior de cada pestaña).

Estas funciones no calculan nada: reciben los resultados de replicacion.py,
transcripcion.py y traduccion.py y los convierten en texto para mostrarlos.
"""

from traduccion import CODONES_STOP, obtener_anticodon

LIMITE_HORQUILLA = 48   # nucleótidos que se muestran en la horquilla de texto

# ---------------------------------------------------------------- utilidades


def abreviar(secuencia, maximo=60):
    """Acorta una secuencia larga dejando el principio y el final."""
    if len(secuencia) <= maximo:
        return secuencia
    return secuencia[:30] + "..." + secuencia[-27:]


def abreviar_proteina(aminoacidos, maximo=20):
    if len(aminoacidos) <= maximo:
        return "-".join(aminoacidos)
    return "-".join(aminoacidos[:10]) + "-...-" + "-".join(aminoacidos[-5:])

# ---------------------------------------------------------------- replicación


def texto_horquilla(resultado):
    """Dibuja en texto la horquilla con la cadena líder y la rezagada alineadas con sus moldes."""
    superior = resultado["hebra_superior"][:LIMITE_HORQUILLA]
    inferior = resultado["hebra_inferior"][:LIMITE_HORQUILLA]
    lider = resultado["lider_con_cebador"][:LIMITE_HORQUILLA]

    rezagada = ""
    flechas_rezagada = ""
    etiquetas = ""
    for fragmento in resultado["fragmentos"]:
        if fragmento["inicio"] >= LIMITE_HORQUILLA:
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
    if len(resultado["hebra_superior"]) > LIMITE_HORQUILLA:
        lineas.append("(Solo se dibujan los primeros " + str(LIMITE_HORQUILLA)
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
    lineas.append(texto_horquilla(resultado))
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

# ---------------------------------------------------------------- transcripción


def texto_transcripcion(resultado):
    """Genera el texto que se muestra en la pestaña de transcripción."""
    codificante = resultado["codificante"]
    molde = resultado["molde"]
    arnm = resultado["arnm"]
    lineas = []

    lineas.append("TRANSCRIPCIÓN  (ADN → ARNm)")
    lineas.append("=" * 70)
    lineas.append("Se transcribe el ADN hijo 1 obtenido en la replicación.")
    lineas.append("")
    lineas.append("ARN polimerasa: se une al ADN, separa localmente las dos hebras y usa una")
    lineas.append("de ellas (la cadena molde) para sintetizar el ARN mensajero.")
    lineas.append("")
    lineas.append("  - La ARN polimerasa lee la cadena molde en dirección 3' → 5'.")
    lineas.append("  - El ARNm se sintetiza en dirección 5' → 3'.")
    lineas.append("  - El ARNm tiene la misma secuencia que la cadena codificante,")
    lineas.append("    salvo que sustituye T por U.")
    lineas.append("")
    lineas.append("Complementariedad ADN (molde) → ARN:")
    lineas.append("    A → U     T → A     C → G     G → C")
    lineas.append("")
    lineas.append("CADENA CODIFICANTE   5' " + codificante + " 3'")
    lineas.append("CADENA MOLDE         3' " + molde + " 5'")
    lineas.append("                        " + "|" * len(molde) + "   (complementariedad)")
    lineas.append("ARNm                 5' " + arnm + " 3'")
    lineas.append("                        " + "─" * (len(arnm) - 1) + "→   la ARN polimerasa avanza")
    lineas.append("")
    lineas.append("Las cadenas son antiparalelas: el ARNm (5' → 3') es antiparalelo a la")
    lineas.append("cadena molde (3' → 5') y paralelo a la cadena codificante (5' → 3').")
    lineas.append("")
    if resultado["coincide_con_codificante"]:
        lineas.append("Comprobación: el ARNm coincide con la cadena codificante cambiando T por U.")
    else:
        lineas.append("ERROR: el ARNm no coincide con la cadena codificante.")
    return "\n".join(lineas)

# ---------------------------------------------------------------- traducción


def texto_ribosoma(codones, aminoacidos):
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

    lineas.append(texto_ribosoma(codones, aminoacidos))
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

# ---------------------------------------------------------------- resultado


def texto_resultado(adn, replicacion, transcripcion, traduccion):
    """Resumen del flujo completo ADN -> ADN -> ARN -> proteína."""
    hijo = replicacion["hijo_1"]
    if traduccion["inicio"] == -1:
        proteina = "No se ha encontrado un codón de inicio AUG."
    else:
        proteina = abreviar_proteina(traduccion["proteina"])
        if len(traduccion["proteina"]) > 20:
            proteina += "   (completa en la pestaña Traducción)"
        if traduccion["codon_stop"] is None:
            proteina += "   (sin codón de parada: proteína incompleta)"

    lineas = [
        "RESULTADO: FLUJO DE LA INFORMACIÓN GENÉTICA",
        "=" * 70,
        "",
        "ADN INICIAL  (" + str(len(adn)) + " nucleótidos)",
        "   5' " + abreviar(adn) + " 3'",
        "      ↓",
        "REPLICACIÓN  (helicasa, primasa, ADN polimerasa, ADN ligasa)",
        "      ↓",
        "ADN HIJO  (1 hebra parental + 1 hebra nueva; se obtienen dos moléculas iguales)",
        "   5' " + abreviar(hijo["hebra_5_3"]) + " 3'",
        "   3' " + abreviar(hijo["hebra_3_5"]) + " 5'",
        "      ↓",
        "TRANSCRIPCIÓN  (ARN polimerasa; lee la cadena molde 3'→5')",
        "      ↓",
        "ARNm",
        "   5' " + abreviar(transcripcion["arnm"]) + " 3'",
        "      ↓",
        "TRADUCCIÓN  (ribosoma y ARNt; desde AUG hasta el codón de parada)",
        "      ↓",
        "PROTEÍNA",
        "   " + proteina,
    ]
    if traduccion["inicio"] != -1:
        lineas.append("   Longitud: " + str(len(traduccion["proteina"])) + " aminoácidos")
    return "\n".join(lineas)
