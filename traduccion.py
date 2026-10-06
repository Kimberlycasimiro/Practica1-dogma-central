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
