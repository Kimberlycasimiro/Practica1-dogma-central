"""Simulación de la transcripción (ADN -> ARNm)."""

# Complementariedad entre la base de la cadena molde y la base que se añade al ARN.
COMPLEMENTO_ARN = {"A": "U", "T": "A", "C": "G", "G": "C"}


def transcribir_adn(cadena_molde):
    """Sintetiza el ARNm a partir de la cadena molde, guardada 3' -> 5' de izquierda a derecha.

    La ARN polimerasa lee la cadena molde 3' -> 5' y el ARNm se sintetiza 5' -> 3'.
    Como la molde está escrita empezando por su extremo 3', recorrerla de izquierda a
    derecha equivale a leerla 3' -> 5', y cada base nueva se añade al extremo 3' del ARNm.
    """
    arnm = ""
    for base in cadena_molde:
        arnm += COMPLEMENTO_ARN[base]
    return arnm


def simular_transcripcion(cadena_codificante, cadena_molde):
    """Transcribe una molécula de ADN y comprueba la relación molde/codificante/ARNm."""
    arnm = transcribir_adn(cadena_molde)
    # El ARNm debe ser igual que la cadena codificante cambiando T por U.
    coincide = arnm == cadena_codificante.replace("T", "U")
    return {
        "codificante": cadena_codificante,
        "molde": cadena_molde,
        "arnm": arnm,
        "coincide_con_codificante": coincide,
    }


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
