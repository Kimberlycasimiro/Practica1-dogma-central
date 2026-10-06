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
