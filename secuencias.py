"""Lectura de ficheros FASTA y validación de la secuencia de ADN de entrada."""

BASES_ADN = "ATCG"


def leer_fasta(ruta):
    """Lee un fichero FASTA con una sola secuencia y devuelve la secuencia sin cabecera."""
    secuencia = ""
    with open(ruta, "r", encoding="utf-8") as fichero:
        for linea in fichero:
            linea = linea.strip()
            # La línea que empieza por '>' es la cabecera (nombre del gen) y no forma parte de la secuencia.
            if linea.startswith(">"):
                continue
            secuencia += linea
    return limpiar_secuencia(secuencia)


def limpiar_secuencia(texto):
    """Elimina espacios y saltos de línea y pasa la secuencia a mayúsculas."""
    secuencia = ""
    for caracter in texto:
        if not caracter.isspace():
            secuencia += caracter.upper()
    return secuencia


def buscar_caracteres_no_validos(secuencia):
    """Devuelve los caracteres de la secuencia que no son A, T, C ni G (sin repetir)."""
    no_validos = []
    for caracter in secuencia:
        if caracter not in BASES_ADN and caracter not in no_validos:
            no_validos.append(caracter)
    return no_validos


def validar_adn(secuencia):
    """Indica si la secuencia contiene solo A, T, C y G y no está vacía."""
    return len(secuencia) > 0 and len(buscar_caracteres_no_validos(secuencia)) == 0
