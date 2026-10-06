"""Representaciones gráficas de cada etapa con tkinter.Canvas.

Son esquemas didácticos construidos con las secuencias reales de la simulación.
Para que sigan siendo legibles, en secuencias largas solo se dibuja la primera parte
y se indica en el propio dibujo.
"""

from replicacion import TAMANO_FRAGMENTO
from traduccion import CODONES_STOP, obtener_anticodon
from explicaciones import abreviar, abreviar_proteina

ANCHO = 18            # píxeles que ocupa cada nucleótido
LIMITE_DIBUJO = 48    # nucleótidos que se dibujan como máximo (múltiplo de TAMANO_FRAGMENTO)
MAX_CODONES = 14      # codones que se dibujan como máximo en la traducción

# Tamaños negativos = píxeles: así el texto escala igual que las coordenadas del dibujo
FUENTE_BASE = ("Consolas", -15, "bold")
FUENTE_TITULO = ("Segoe UI", -16, "bold")
FUENTE_NORMAL = ("Segoe UI", -12)
FUENTE_NEGRITA = ("Segoe UI", -12, "bold")
FUENTE_NOTA = ("Segoe UI", -12, "italic")

TEXTO = "#37474f"
PARENTAL = "#455a64"
FONDO_PARENTAL = "#cfd8dc"
LIDER = "#2e7d32"
FONDO_LIDER = "#c8e6c9"
REZAGADA = "#1565c0"
FONDOS_OKAZAKI = ["#bbdefb", "#90caf9"]   # se alternan para distinguir fragmentos vecinos
CEBADOR = "#e65100"
FONDO_CEBADOR = "#ffcc80"
ARN = "#c62828"
FONDO_ARN = "#ffebee"
PROTEINA = "#6a1b9a"
FONDO_PROTEINA = "#e1bee7"

TOPOISOMERASA = "#5d4037"
HELICASA = "#f57f17"
SSB = "#8d6e63"
PRIMASA = "#ef6c00"
ADN_POLIMERASA = "#7b1fa2"
LIGASA = "#00897b"
ARN_POLIMERASA = "#ad1457"
RIBOSOMA = "#00897b"
ARNT = "#e65100"

COLOR_BASE = {"A": "#2e7d32", "T": "#c62828", "U": "#8e24aa", "C": "#1565c0", "G": "#ef6c00"}


# ---------------------------------------------------------------- utilidades


def x_columna(x0, i):
    """Coordenada x del centro del nucleótido i de una fila que empieza en x0."""
    return x0 + i * ANCHO + ANCHO / 2


def dibujar_fila(canvas, x0, y, secuencia, fondo=None, colorear_bases=False, color="black"):
    """Dibuja una secuencia letra a letra. Las minúsculas (cebadores de ARN) se resaltan."""
    if fondo is not None and len(secuencia) > 0:
        canvas.create_rectangle(x0, y - 11, x0 + len(secuencia) * ANCHO, y + 11, fill=fondo, outline="")
    for i in range(len(secuencia)):
        base = secuencia[i]
        color_letra = color
        if base.islower():
            canvas.create_rectangle(x0 + i * ANCHO, y - 11, x0 + (i + 1) * ANCHO, y + 11,
                                    fill=FONDO_CEBADOR, outline="")
            color_letra = CEBADOR
        elif colorear_bases:
            color_letra = COLOR_BASE[base]
        canvas.create_text(x_columna(x0, i), y, text=base, font=FUENTE_BASE, fill=color_letra)


def dibujar_extremos(canvas, x0, y, longitud, izquierdo, derecho, parcial=False):
    """Escribe los extremos 5'/3' a ambos lados de una fila.

    Si la fila es una representación parcial, se añaden puntos suspensivos para
    indicar que la molécula continúa.
    """
    if parcial:
        derecho = "··· " + derecho
    canvas.create_text(x0 - 4, y, text=izquierdo, anchor="e", font=FUENTE_NEGRITA, fill=TEXTO)
    canvas.create_text(x0 + longitud * ANCHO + 4, y, text=derecho, anchor="w", font=FUENTE_NEGRITA, fill=TEXTO)


def etiqueta_fila(canvas, x0, y, texto, color=TEXTO):
    canvas.create_text(x0 - 26, y, text=texto, anchor="e", font=FUENTE_NEGRITA, fill=color)


def dibujar_enzima(canvas, x, y, nombre, color):
    ancho = 7 * len(nombre) + 18
    canvas.create_oval(x - ancho / 2, y - 13, x + ancho / 2, y + 13, fill=color, outline="")
    canvas.create_text(x, y, text=nombre, font=FUENTE_NEGRITA, fill="white")


def dibujar_flecha(canvas, x1, y1, x2, y2, color=TEXTO, grosor=2, discontinua=False):
    patron = None
    if discontinua:
        patron = (4, 3)
    canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor, arrow="last",
                       arrowshape=(9, 11, 4), dash=patron)


def titulo(canvas, x, y, texto):
    canvas.create_text(x, y, text=texto, anchor="w", font=FUENTE_TITULO, fill="#263238")


def nota(canvas, x, y, texto, color=TEXTO):
    canvas.create_text(x, y, text=texto, anchor="w", font=FUENTE_NOTA, fill=color)


def dibujar_leyenda(canvas, x, y, elementos):
    """Dibuja una fila de cuadrados de color con su significado."""
    for color, texto in elementos:
        canvas.create_rectangle(x, y - 7, x + 14, y + 7, fill=color, outline=TEXTO)
        canvas.create_text(x + 20, y, text=texto, anchor="w", font=FUENTE_NORMAL, fill=TEXTO)
        x += 34 + 6 * len(texto)


def nota_parcial(canvas, x, y, dibujados, total):
    texto = "Esquema didáctico construido con la secuencia real."
    if total > dibujados:
        texto += ("  Representación parcial: se dibujan los primeros " + str(dibujados)
                  + " de " + str(total) + " nucleótidos.")
    nota(canvas, x, y, texto)


def ajustar_scroll(canvas):
    """Ajusta la zona desplazable del Canvas a lo que se ha dibujado."""
    caja = canvas.bbox("all")
    if caja is not None:
        canvas.configure(scrollregion=(0, 0, caja[2] + 30, caja[3] + 30))


# ---------------------------------------------------------------- replicación

def dibujar_replicacion(canvas, resultado):
    canvas.delete("all")
    superior = resultado["hebra_superior"]
    inferior = resultado["hebra_inferior"]
    fragmentos = resultado["fragmentos"]
    n = min(len(superior), LIMITE_DIBUJO)
    parcial = len(superior) > n
    x0 = 200

    titulo(canvas, 20, 20, "1. Horquilla de replicación (un instante intermedio del proceso)")
    nota_parcial(canvas, 20, 42, n, len(superior))
    dibujar_leyenda(canvas, 20, 64, [
        (FONDO_PARENTAL, "hebra parental (molde)"),
        (FONDO_LIDER, "cadena líder (nueva)"),
        (FONDOS_OKAZAKI[0], "fragmentos de Okazaki (cadena rezagada nueva)"),
        (FONDO_CEBADOR, "cebador de ARN (minúsculas)"),
    ])

    # Se dibuja la horquilla cuando la helicasa ha abierto unos 2/3 del tramo,
    # justo al final de un fragmento de Okazaki.
    p = (n * 2 // 3) // TAMANO_FRAGMENTO * TAMANO_FRAGMENTO
    if p == 0:
        p = n
    resto = n - p

    y_superior = 125
    y_rezagada = 149
    y_okazaki = 172
    y_cerrada_1 = 215
    y_cerrada_2 = 245
    y_lider = 290
    y_inferior = 314
    x_fin = x0 + p * ANCHO          # hasta aquí llega la zona abierta
    x_cerrada = x_fin + 110         # aquí empieza la doble hélice sin abrir

    # Origen de replicación y sentido de avance de la horquilla.
    canvas.create_line(x0, 92, x0, y_inferior + 16, fill="#90a4ae", dash=(3, 3))
    canvas.create_text(x0, 86, text="origen", font=FUENTE_NEGRITA, fill=TEXTO)
    dibujar_flecha(canvas, x_cerrada - 40, 100, x_cerrada + 80, 100, HELICASA, 3)
    canvas.create_text(x_cerrada + 20, 86, text="avance de la horquilla", font=FUENTE_NEGRITA, fill=HELICASA)

    # Hebras parentales: separadas a la izquierda y todavía unidas a la derecha.
    canvas.create_line(x0, y_superior - 13, x_fin, y_superior - 13, x_cerrada, y_cerrada_1 - 13,
                       x_cerrada + resto * ANCHO, y_cerrada_1 - 13, fill=PARENTAL, width=3)
    canvas.create_line(x0, y_inferior + 13, x_fin, y_inferior + 13, x_cerrada, y_cerrada_2 + 13,
                       x_cerrada + resto * ANCHO, y_cerrada_2 + 13, fill=PARENTAL, width=3)
    dibujar_fila(canvas, x0, y_superior, superior[:p], fondo=FONDO_PARENTAL)
    dibujar_fila(canvas, x0, y_inferior, inferior[:p], fondo=FONDO_PARENTAL)
    dibujar_extremos(canvas, x0, y_superior, 0, "5'", "")
    dibujar_extremos(canvas, x0, y_inferior, 0, "3'", "")
    etiqueta_fila(canvas, x0, y_superior, "Hebra parental", PARENTAL)
    etiqueta_fila(canvas, x0, y_inferior, "Hebra parental", PARENTAL)

    if resto > 0:
        dibujar_fila(canvas, x_cerrada, y_cerrada_1, superior[p:n], fondo=FONDO_PARENTAL)
        dibujar_fila(canvas, x_cerrada, y_cerrada_2, inferior[p:n], fondo=FONDO_PARENTAL)
        for i in range(resto):
            x = x_columna(x_cerrada, i)
            canvas.create_line(x, y_cerrada_1 + 11, x, y_cerrada_2 - 11, fill=PARENTAL)
        dibujar_extremos(canvas, x_cerrada, y_cerrada_1, resto, "", "3'", parcial)
        dibujar_extremos(canvas, x_cerrada, y_cerrada_2, resto, "", "5'", parcial)
        canvas.create_text(x_cerrada, y_cerrada_2 + 32, anchor="w", font=FUENTE_NORMAL, fill=TEXTO,
                           text="doble hélice todavía sin abrir")

    # La helicasa está en el punto donde se separan las dos hebras.
    dibujar_enzima(canvas, x_cerrada - 40, (y_cerrada_1 + y_cerrada_2) / 2, "Helicasa", HELICASA)

    # La topoisomerasa actúa por delante de la horquilla, sobre el ADN aún sin abrir.
    x_topo = x_cerrada + resto * ANCHO + 100
    dibujar_enzima(canvas, x_topo, (y_cerrada_1 + y_cerrada_2) / 2, "Topoisomerasa", TOPOISOMERASA)
    canvas.create_text(x_topo, y_cerrada_2 + 13, font=FUENTE_NORMAL, fill=TOPOISOMERASA,
                       text="evita el superenrollamiento")

    # Proteínas SSB sobre las hebras sencillas recién separadas (tramo diagonal).
    for fraccion in [0.3, 0.6]:
        x = x_fin + fraccion * (x_cerrada - x_fin)
        y_arriba = (y_superior - 13) + fraccion * (y_cerrada_1 - y_superior)
        y_abajo = (y_inferior + 13) + fraccion * (y_cerrada_2 - y_inferior)
        canvas.create_oval(x - 7, y_arriba - 7, x + 7, y_arriba + 7, fill=SSB, outline="")
        canvas.create_oval(x - 7, y_abajo - 7, x + 7, y_abajo + 7, fill=SSB, outline="")
    x_etiqueta = x_fin + 0.6 * (x_cerrada - x_fin) + 12
    canvas.create_text(x_etiqueta, (y_superior - 13) + 0.6 * (y_cerrada_1 - y_superior) - 8,
                       anchor="w", font=FUENTE_NEGRITA, fill=SSB, text="SSB")

    # Cadena líder: un cebador en el origen y síntesis continua hasta la horquilla.
    lider = resultado["lider_con_cebador"][:p]
    dibujar_fila(canvas, x0, y_lider, lider, fondo=FONDO_LIDER)
    dibujar_extremos(canvas, x0, y_lider, p, "5'", "3'")
    etiqueta_fila(canvas, x0, y_lider, "Cadena líder", LIDER)
    dibujar_flecha(canvas, x0 + 2, y_lider - 20, x_fin + 4, y_lider - 20, LIDER)
    dibujar_enzima(canvas, x_fin - 20, 248, "ADN pol III", ADN_POLIMERASA)
    canvas.create_line(x_fin - 10, 261, x_fin - ANCHO / 2, y_lider - 11, fill=ADN_POLIMERASA, width=2)

    # Cadena rezagada: fragmentos de Okazaki ya abiertos por la horquilla.
    en_horquilla = []
    for fragmento in fragmentos:
        if fragmento["inicio"] < p:
            en_horquilla.append(fragmento)

    for fragmento in en_horquilla:
        texto = fragmento["alineado_con_cebador"]
        desplazamiento = 0
        etiqueta = "Okazaki " + str(fragmento["numero"])
        if fragmento is en_horquilla[-1]:
            # El fragmento más reciente todavía se está alargando hacia su extremo 3' (izquierda).
            desplazamiento = (len(texto) - len(fragmento["cebador"])) // 2
            texto = texto[desplazamiento:]
        x_inicio = x0 + (fragmento["inicio"] + desplazamiento) * ANCHO
        x_final = x_inicio + len(texto) * ANCHO
        fondo = FONDOS_OKAZAKI[(fragmento["numero"] - 1) % 2]
        dibujar_fila(canvas, x_inicio, y_rezagada, texto, fondo=fondo)
        dibujar_flecha(canvas, x_final - 3, y_okazaki, x_inicio + 3, y_okazaki, REZAGADA)
        canvas.create_text((x_inicio + x_final) / 2, y_okazaki + 13, text=etiqueta,
                           font=FUENTE_NORMAL, fill=REZAGADA)

    dibujar_extremos(canvas, x0, y_rezagada, p, "3'", "5'")
    etiqueta_fila(canvas, x0, y_rezagada, "Cadena rezagada", REZAGADA)

    # Primasa sobre el último cebador y ADN polimerasa en el hueco que aún falta por rellenar.
    ultimo = en_horquilla[-1]
    longitud_ultimo = len(ultimo["alineado_con_cebador"])
    hueco = (longitud_ultimo - len(ultimo["cebador"])) // 2
    x_cebador = x0 + (ultimo["fin"] - len(ultimo["cebador"]) / 2) * ANCHO
    x_polimerasa = x0 + (ultimo["inicio"] + hueco / 2) * ANCHO
    dibujar_enzima(canvas, x_cebador + 45, 200, "Primasa", PRIMASA)
    canvas.create_line(x_cebador + 30, 188, x_cebador + 4, y_rezagada + 11, fill=PRIMASA, width=2)
    x_ovalo = max(x_polimerasa - 30, x0 + 50)   # que no se salga a la izquierda del origen
    dibujar_enzima(canvas, x_ovalo, 222, "ADN pol III", ADN_POLIMERASA)
    canvas.create_line(x_ovalo, 209, x_polimerasa, y_rezagada + 11, fill=ADN_POLIMERASA, width=2)

    nota(canvas, 20, 350, "Cadena líder: su molde es la hebra 3'→5'. Crece 5'→3' en el mismo sentido en que "
                          "avanza la horquilla, así que la síntesis es continua con un solo cebador.", LIDER)
    nota(canvas, 20, 370, "Cadena rezagada: su molde es la hebra 5'→3'. Para crecer 5'→3' debe avanzar en "
                          "sentido contrario a la horquilla, así que se sintetiza a trozos (Okazaki), "
                          "cada uno con su cebador.", REZAGADA)
    nota(canvas, 20, 390, "El último fragmento aún se está sintetizando: la primasa acaba de colocar su cebador "
                          "y la ADN polimerasa III lo alarga hacia su extremo 3' (izquierda).", REZAGADA)

    # ---- 2. Maduración de la cadena rezagada ----
    y = 430
    titulo(canvas, 20, y, "2. Cadena rezagada: la ADN polimerasa I sustituye los cebadores y la ADN ligasa une los fragmentos")
    separacion = 18
    dibujados = []
    for fragmento in fragmentos:
        if fragmento["inicio"] < n:
            dibujados.append(fragmento)
    ancho_separado = n * ANCHO + (len(dibujados) - 1) * separacion

    y_con = y + 42
    y_sin = y + 92
    y_ligasa = y + 132
    y_unida = y + 172
    for fragmento in dibujados:
        x_inicio = x0 + fragmento["inicio"] * ANCHO + (fragmento["numero"] - 1) * separacion
        fondo = FONDOS_OKAZAKI[(fragmento["numero"] - 1) % 2]
        dibujar_fila(canvas, x_inicio, y_con, fragmento["alineado_con_cebador"], fondo=fondo)
        dibujar_fila(canvas, x_inicio, y_sin, fragmento["alineado_sin_cebador"], fondo=fondo)
        if fragmento["numero"] > 1:
            # Entre dos fragmentos queda una mella que sella la ligasa.
            x_mella = x_inicio - separacion / 2
            dibujar_enzima(canvas, x_mella, y_ligasa, "Ligasa", LIGASA)
            canvas.create_line(x_mella, y_sin + 11, x_mella, y_ligasa - 13, fill=LIGASA, width=2)
            dibujar_flecha(canvas, x_mella, y_ligasa + 13, x_mella, y_unida - 13, LIGASA)

    dibujar_extremos(canvas, x0, y_con, ancho_separado / ANCHO, "3'", "5'", parcial)
    dibujar_extremos(canvas, x0, y_sin, ancho_separado / ANCHO, "3'", "5'", parcial)
    etiqueta_fila(canvas, x0, y_con, "Fragmentos con cebador", REZAGADA)
    etiqueta_fila(canvas, x0, y_sin, "Cebadores → ADN", REZAGADA)
    dibujar_enzima(canvas, x0 + ancho_separado + 95, y_sin, "ADN pol I", ADN_POLIMERASA)
    canvas.create_text(x0 + ancho_separado + 152, y_sin, anchor="w", font=FUENTE_NORMAL, fill=TEXTO,
                       text="elimina el ARN de los cebadores y lo sustituye por ADN")

    dibujar_fila(canvas, x0, y_unida, resultado["rezagada"][:n], fondo=FONDOS_OKAZAKI[0])
    dibujar_extremos(canvas, x0, y_unida, n, "3'", "5'", parcial)
    etiqueta_fila(canvas, x0, y_unida, "Rezagada completa", REZAGADA)
    if len(dibujados) == 1:
        canvas.create_text(x0 + n * ANCHO + 40, y_ligasa, anchor="w", font=FUENTE_NORMAL, fill=TEXTO,
                           text="(con un solo fragmento no hay mellas que unir)")

    # ---- 3. Replicación semiconservativa ----
    y = y_unida + 50
    titulo(canvas, 20, y, "3. Resultado: replicación semiconservativa (dos moléculas hijas)")
    hijo_1 = resultado["hijo_1"]
    hijo_2 = resultado["hijo_2"]
    filas = [
        (y + 40, "ADN hijo 1", hijo_1["hebra_5_3"], FONDO_PARENTAL, "5'", "3'", "parental"),
        (y + 64, "", hijo_1["hebra_3_5"], FONDOS_OKAZAKI[0], "3'", "5'", "nueva (rezagada)"),
        (y + 110, "ADN hijo 2", hijo_2["hebra_5_3"], FONDO_LIDER, "5'", "3'", "nueva (líder)"),
        (y + 134, "", hijo_2["hebra_3_5"], FONDO_PARENTAL, "3'", "5'", "parental"),
    ]
    for y_fila, nombre, secuencia, fondo, izquierdo, derecho, tipo in filas:
        dibujar_fila(canvas, x0, y_fila, secuencia[:n], fondo=fondo)
        dibujar_extremos(canvas, x0, y_fila, n, izquierdo, derecho, parcial)
        etiqueta_fila(canvas, x0, y_fila, nombre)
        canvas.create_text(x0 + n * ANCHO + 30, y_fila, anchor="w", font=FUENTE_NORMAL, fill=TEXTO,
                           text="hebra " + tipo)

    if hijo_1["hebra_5_3"] == hijo_2["hebra_5_3"] == superior:
        nota(canvas, 20, y + 168, "Cada molécula hija conserva una hebra parental y tiene una nueva. "
                                  "Las dos son idénticas a la molécula inicial.", LIDER)
    ajustar_scroll(canvas)


# ---------------------------------------------------------------- transcripción

def dibujar_transcripcion(canvas, resultado):
    canvas.delete("all")
    codificante = resultado["codificante"]
    molde = resultado["molde"]
    arnm = resultado["arnm"]
    n = min(len(arnm), LIMITE_DIBUJO)
    parcial = len(arnm) > n
    x0 = 200
    x_final = x0 + n * ANCHO

    titulo(canvas, 20, 20, "Transcripción: la ARN polimerasa sintetiza el ARNm usando la cadena molde")
    nota_parcial(canvas, 20, 42, n, len(arnm))

    y_codificante = 105
    y_molde = 135
    y_arnm = 200

    dibujar_flecha(canvas, x0, 75, x_final, 75, ARN_POLIMERASA, 3)
    canvas.create_text(x0, 62, anchor="w", font=FUENTE_NEGRITA, fill=ARN_POLIMERASA,
                       text="avance de la ARN polimerasa: lee la cadena molde 3' → 5'")
    # La región dibujada se considera la región transcrita: entre el promotor y el terminador.
    canvas.create_text(x0 - 8, 75, anchor="e", font=FUENTE_NEGRITA, fill=TEXTO, text="promotor ▸")
    texto_terminador = "◂ terminador"
    if parcial:
        texto_terminador = "···  ◂ terminador"
    canvas.create_text(x_final + 8, 75, anchor="w", font=FUENTE_NEGRITA, fill=TEXTO, text=texto_terminador)

    dibujar_fila(canvas, x0, y_codificante, codificante[:n], fondo="#eceff1", colorear_bases=True)
    dibujar_extremos(canvas, x0, y_codificante, n, "5'", "3'", parcial)
    etiqueta_fila(canvas, x0, y_codificante, "Cadena codificante")

    dibujar_fila(canvas, x0, y_molde, molde[:n], fondo=FONDO_PARENTAL, colorear_bases=True)
    dibujar_extremos(canvas, x0, y_molde, n, "3'", "5'", parcial)
    etiqueta_fila(canvas, x0, y_molde, "Cadena MOLDE", PARENTAL)

    # Cada base del ARNm es la complementaria de la base de la molde que tiene encima.
    for i in range(n):
        x = x_columna(x0, i)
        canvas.create_line(x, y_codificante + 11, x, y_molde - 11, fill=PARENTAL)
        dibujar_flecha(canvas, x, y_molde + 13, x, y_arnm - 13, "#b0bec5", 1)

    dibujar_fila(canvas, x0, y_arnm, arnm[:n], fondo=FONDO_ARN, colorear_bases=True)
    dibujar_extremos(canvas, x0, y_arnm, n, "5'", "3'", parcial)
    etiqueta_fila(canvas, x0, y_arnm, "ARNm (nuevo)", ARN)
    dibujar_flecha(canvas, x0, y_arnm + 24, x_final, y_arnm + 24, ARN)
    canvas.create_text(x_final + 12, y_arnm + 24, anchor="w", font=FUENTE_NEGRITA, fill=ARN,
                       text="el ARNm crece 5' → 3'")

    # La ARN polimerasa se dibuja en su posición final, sobre las últimas bases transcritas.
    columnas = min(5, n)
    x_izquierda = x_final - columnas * ANCHO
    canvas.create_oval(x_izquierda - 8, y_molde - 18, x_final + 8, y_arnm + 14,
                       outline=ARN_POLIMERASA, width=3, dash=(6, 3))
    dibujar_enzima(canvas, x_final + 110, (y_molde + y_arnm) / 2, "ARN polimerasa", ARN_POLIMERASA)
    canvas.create_line(x_final + 8, (y_molde + y_arnm) / 2, x_final + 52, (y_molde + y_arnm) / 2,
                       fill=ARN_POLIMERASA, width=2)

    # Reglas de complementariedad.
    y = 270
    canvas.create_rectangle(20, y, 520, y + 70, outline=TEXTO, fill="#fafafa")
    canvas.create_text(35, y + 18, anchor="w", font=FUENTE_NEGRITA, fill=TEXTO,
                       text="Complementariedad: base de la cadena molde (ADN) → base del ARNm")
    parejas = [("A", "U"), ("T", "A"), ("C", "G"), ("G", "C")]
    x = 55
    for base_adn, base_arn in parejas:
        canvas.create_text(x, y + 47, text=base_adn, font=("Consolas", -21, "bold"), fill=COLOR_BASE[base_adn])
        dibujar_flecha(canvas, x + 14, y + 47, x + 46, y + 47)
        canvas.create_text(x + 60, y + 47, text=base_arn, font=("Consolas", -21, "bold"), fill=COLOR_BASE[base_arn])
        x += 120

    # Comparación de la cadena codificante con el ARNm.
    y = 380
    canvas.create_text(20, y, anchor="w", font=FUENTE_TITULO, fill="#263238",
                       text="El ARNm tiene la misma secuencia que la cadena codificante, cambiando T por U")
    y_fila_1 = y + 40
    y_fila_2 = y + 64
    for i in range(n):
        if codificante[i] == "T":
            canvas.create_rectangle(x0 + i * ANCHO, y_fila_1 - 12, x0 + (i + 1) * ANCHO, y_fila_2 + 12,
                                    fill="#fff59d", outline="")
    dibujar_fila(canvas, x0, y_fila_1, codificante[:n], colorear_bases=True)
    dibujar_fila(canvas, x0, y_fila_2, arnm[:n], colorear_bases=True)
    dibujar_extremos(canvas, x0, y_fila_1, n, "5'", "3'", parcial)
    dibujar_extremos(canvas, x0, y_fila_2, n, "5'", "3'", parcial)
    etiqueta_fila(canvas, x0, y_fila_1, "Cadena codificante")
    etiqueta_fila(canvas, x0, y_fila_2, "ARNm", ARN)
    if resultado["coincide_con_codificante"]:
        nota(canvas, 20, y_fila_2 + 34, "Comprobación: coinciden en todas las posiciones "
                                        "(en amarillo, las T que pasan a ser U).", LIDER)
    else:
        nota(canvas, 20, y_fila_2 + 34, "ERROR: el ARNm no coincide con la cadena codificante.", ARN)
    ajustar_scroll(canvas)


# ---------------------------------------------------------------- traducción

def dibujar_codon(canvas, x, y, codon, relleno):
    """Dibuja un codón como una caja de tres nucleótidos con su esquina izquierda en x."""
    canvas.create_rectangle(x, y - 13, x + 3 * ANCHO, y + 13, fill=relleno, outline=TEXTO)
    dibujar_fila(canvas, x, y, codon)


def color_codon(codon, numero):
    if numero == 0:
        return FONDO_LIDER              # el AUG de inicio
    if codon in CODONES_STOP:
        return "#ffcdd2"
    return "#e3f2fd"


def dibujar_aminoacido(canvas, x, y, nombre):
    canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill=FONDO_PROTEINA, outline=PROTEINA, width=2)
    canvas.create_text(x, y, text=nombre, font=FUENTE_NEGRITA, fill=PROTEINA)


def dibujar_arnt(canvas, x, y_anticodon, y_aminoacido, codon, etiqueta_derecha=False):
    """Dibuja un ARNt: su anticodón (3' -> 5') sobre el codón y el brazo que lleva el aminoácido."""
    canvas.create_line(x, y_anticodon - 13, x, y_aminoacido + 18, fill=ARNT, width=3)
    canvas.create_rectangle(x - 1.5 * ANCHO, y_anticodon - 12, x + 1.5 * ANCHO, y_anticodon + 12,
                            fill="#fff3e0", outline=ARNT, width=2)
    dibujar_fila(canvas, x - 1.5 * ANCHO, y_anticodon, obtener_anticodon(codon))
    if etiqueta_derecha:
        canvas.create_text(x + 1.5 * ANCHO + 4, y_anticodon, text="ARNt", anchor="w",
                           font=FUENTE_NORMAL, fill=ARNT)
    else:
        canvas.create_text(x - 1.5 * ANCHO - 4, y_anticodon, text="ARNt", anchor="e",
                           font=FUENTE_NORMAL, fill=ARNT)


def dibujar_traduccion(canvas, resultado):
    canvas.delete("all")
    arnm = resultado["arnm"]
    inicio = resultado["inicio"]
    codones = resultado["codones"]
    aminoacidos = resultado["aminoacidos"]
    proteina = resultado["proteina"]

    titulo(canvas, 20, 20, "Traducción: el ribosoma lee el ARNm en codones y los ARNt aportan los aminoácidos")

    if inicio == -1:
        n = min(len(arnm), LIMITE_DIBUJO)
        parcial = len(arnm) > n
        nota_parcial(canvas, 20, 42, n, len(arnm))
        dibujar_fila(canvas, 200, 90, arnm[:n], fondo=FONDO_ARN, colorear_bases=True)
        dibujar_extremos(canvas, 200, 90, n, "5'", "3'", parcial)
        etiqueta_fila(canvas, 200, 90, "ARNm", ARN)
        canvas.create_rectangle(20, 130, 720, 200, fill="#ffebee", outline=ARN, width=2)
        canvas.create_text(40, 152, anchor="w", font=FUENTE_TITULO, fill=ARN,
                           text="No se ha encontrado un codón de inicio AUG.")
        canvas.create_text(40, 178, anchor="w", font=FUENTE_NORMAL, fill=ARN,
                           text="El ribosoma no puede iniciar la traducción, así que no se sintetiza ninguna proteína.")
        ajustar_scroll(canvas)
        return

    dibujados = min(len(codones), MAX_CODONES)

    # ---- 1. Lectura en codones ----
    canvas.create_text(20, 52, anchor="w", font=FUENTE_NEGRITA, fill=TEXTO,
                       text="1. Lectura del ARNm en codones a partir del primer AUG (posición "
                            + str(inicio + 1) + ")")
    y = 95
    x = 60
    canvas.create_text(x, y, text="5'", anchor="e", font=FUENTE_NEGRITA, fill=TEXTO)
    previa = arnm[:inicio]
    if len(previa) > 6:
        previa = "···" + previa[-5:]
    if len(previa) > 0:
        dibujar_fila(canvas, x + 4, y, previa, color="#90a4ae")
        canvas.create_text(x + 4, y - 24, anchor="w", text="no se traduce",
                           font=FUENTE_NORMAL, fill="#90a4ae")
        x += len(previa) * ANCHO + 8
    else:
        x += 8
    for k in range(dibujados):
        dibujar_codon(canvas, x, y, codones[k], color_codon(codones[k], k))
        debajo = str(k + 1)
        color_debajo = TEXTO
        if k == 0:
            debajo = "INICIO"
            color_debajo = LIDER
        elif codones[k] == resultado["codon_stop"]:
            debajo = "STOP"
            color_debajo = ARN
        canvas.create_text(x + 1.5 * ANCHO, y + 26, text=debajo, font=FUENTE_NEGRITA, fill=color_debajo)
        x += 3 * ANCHO + 6
    if len(codones) > dibujados:
        canvas.create_text(x, y, anchor="w", font=FUENTE_NEGRITA, fill=TEXTO,
                           text="···  (" + str(len(codones)) + " codones leídos en total)")
        x += 210
    else:
        final = inicio + 3 * len(codones)
        posterior = arnm[final:final + 5]
        if len(arnm) > final + 5:
            posterior += "···"
        dibujar_fila(canvas, x, y, posterior, color="#90a4ae")
        x += len(posterior) * ANCHO + 4
    canvas.create_text(x, y, text="3'", anchor="w", font=FUENTE_NEGRITA, fill=TEXTO)

    # ---- 2. El ribosoma en un instante de la elongación ----
    canvas.create_text(20, 160, anchor="w", font=FUENTE_NEGRITA, fill=TEXTO,
                       text="2. El ribosoma durante la elongación: el ARNt del sitio P lleva la cadena "
                            "en crecimiento y al sitio A llega el siguiente ARNt")
    if len(proteina) >= 2:
        i = min(2, len(proteina) - 2)
    else:
        i = 0
    # Se dibujan unos pocos codones alrededor de los sitios P (codón i) y A (codón i + 1).
    primero = max(0, i - 2)
    ultimo = min(len(codones), i + 4)
    paso = 3 * ANCHO + 6
    x_primero = 140
    x_ultimo = x_primero + (ultimo - primero) * paso
    y_arnm = 390
    y_anticodon = 348
    y_aminoacido = 300
    x_p = x_primero + (i - primero) * paso + 1.5 * ANCHO
    x_a = x_p + paso

    canvas.create_oval(x_p - 85, 225, x_a + 85, y_arnm + 4, fill="#e0f2f1", outline=RIBOSOMA, width=2)
    canvas.create_oval(x_p - 75, y_arnm - 6, x_a + 75, y_arnm + 44, fill="#b2dfdb", outline=RIBOSOMA, width=2)
    canvas.create_text((x_p + x_a) / 2, 240, text="RIBOSOMA", font=FUENTE_TITULO, fill=RIBOSOMA)
    canvas.create_text(x_p - 90, 262, anchor="e", font=FUENTE_NORMAL, fill=RIBOSOMA, text="subunidad mayor")
    canvas.create_text(x_p - 80, y_arnm + 34, anchor="e", font=FUENTE_NORMAL, fill=RIBOSOMA,
                       text="subunidad menor")
    canvas.create_text(x_p, y_arnm + 28, text="sitio P", font=FUENTE_NEGRITA, fill=RIBOSOMA)
    canvas.create_text(x_a, y_arnm + 28, text="sitio A", font=FUENTE_NEGRITA, fill=RIBOSOMA)

    canvas.create_line(x_primero - 30, y_arnm, x_ultimo + 20, y_arnm, fill=ARN, width=3)
    canvas.create_text(x_primero - 36, y_arnm, text="5'", anchor="e", font=FUENTE_NEGRITA, fill=TEXTO)
    canvas.create_text(x_ultimo + 26, y_arnm, text="3'  ARNm", anchor="w", font=FUENTE_NEGRITA, fill=ARN)
    for j in range(primero, ultimo):
        x_codon = x_primero + (j - primero) * paso
        dibujar_codon(canvas, x_codon, y_arnm, codones[j], color_codon(codones[j], j))

    # Sitio P: ARNt con la cadena de aminoácidos ya formada.
    dibujar_arnt(canvas, x_p, y_anticodon, y_aminoacido, codones[i])
    for k in range(i, -1, -1):
        distancia = i - k
        x_aa = x_p - distancia * 34
        y_aa = y_aminoacido - distancia * 36
        if k < i:
            canvas.create_line(x_aa, y_aa, x_aa + 34, y_aa + 36, fill=PROTEINA, width=3)
        dibujar_aminoacido(canvas, x_aa, y_aa, aminoacidos[k])

    # Sitio A: llega el siguiente ARNt, salvo que sea un STOP o se acabe el ARNm.
    if i + 1 >= len(codones):
        canvas.create_text(x_a, y_anticodon, text="fin del\nARNm", justify="center",
                           font=FUENTE_NEGRITA, fill=ARN)
    elif codones[i + 1] in CODONES_STOP:
        canvas.create_text(x_a, y_anticodon - 10, text="STOP: factor\nde liberación", justify="center",
                           font=FUENTE_NEGRITA, fill=ARN)
    else:
        dibujar_arnt(canvas, x_a, y_anticodon, y_aminoacido, codones[i + 1], etiqueta_derecha=True)
        dibujar_aminoacido(canvas, x_a, y_aminoacido, aminoacidos[i + 1])
        dibujar_flecha(canvas, x_a - 20, y_aminoacido, x_p + 20, y_aminoacido, PROTEINA, 2, True)
    dibujar_flecha(canvas, x_p - 70, y_arnm + 60, x_a + 70, y_arnm + 60, RIBOSOMA, 2)
    canvas.create_text(x_a + 80, y_arnm + 60, anchor="w", font=FUENTE_NORMAL, fill=RIBOSOMA,
                       text="el ribosoma avanza 5' → 3', un codón cada vez")

    x_texto = x_a + 140
    explicaciones = [
        "INICIACIÓN: la subunidad menor se une al ARNm y localiza el primer AUG;",
        "el ARNt iniciador (Met) ocupa el sitio P y se une la subunidad mayor.",
        "",
        "ELONGACIÓN (lo que muestra el dibujo): al sitio A llega el ARNt cuyo",
        "anticodón (3' → 5') empareja con el codón. Su aminoácido se une a la",
        "cadena con un enlace peptídico (flecha discontinua) y el ribosoma",
        "avanza un codón.",
        "",
        "TERMINACIÓN: los codones de parada (UAA, UAG, UGA) no tienen ARNt;",
        "los reconoce un factor de liberación, se libera la proteína y las",
        "subunidades se separan.",
    ]
    for linea in range(len(explicaciones)):
        canvas.create_text(x_texto, 190 + linea * 17, anchor="w", font=FUENTE_NORMAL, fill=TEXTO,
                           text=explicaciones[linea])

    # ---- 3. Correspondencia codón → ARNt → aminoácido → proteína ----
    y = 500
    canvas.create_text(20, y, anchor="w", font=FUENTE_NEGRITA, fill=TEXTO,
                       text="3. Codón → anticodón del ARNt → aminoácido → proteína")
    x0 = 190
    paso = 64
    y_codon = y + 40
    y_anti = y + 82
    y_aa = y + 132
    etiqueta_fila(canvas, x0 + 20, y_codon, "Codón ARNm (5'→3')", ARN)
    etiqueta_fila(canvas, x0 + 20, y_anti, "Anticodón ARNt (3'→5')", ARNT)
    etiqueta_fila(canvas, x0 + 20, y_aa, "Aminoácido", PROTEINA)

    # Primero la línea de la cadena para que quede detrás de los círculos.
    ultimo_aminoacido = -1
    for k in range(dibujados):
        if aminoacidos[k] != "STOP":
            ultimo_aminoacido = k
    if ultimo_aminoacido > 0:
        canvas.create_line(x0 + 1.5 * ANCHO, y_aa, x0 + ultimo_aminoacido * paso + 1.5 * ANCHO, y_aa,
                           fill=PROTEINA, width=3)

    for k in range(dibujados):
        x = x0 + k * paso
        centro = x + 1.5 * ANCHO
        dibujar_codon(canvas, x, y_codon, codones[k], color_codon(codones[k], k))
        if aminoacidos[k] == "STOP":
            canvas.create_text(centro, y_anti, text="factor de\nliberación", justify="center",
                               font=FUENTE_NORMAL, fill=ARN)
            canvas.create_rectangle(centro - 22, y_aa - 14, centro + 22, y_aa + 14, fill="#ffcdd2", outline=ARN)
            canvas.create_text(centro, y_aa, text="STOP", font=FUENTE_NEGRITA, fill=ARN)
        else:
            canvas.create_line(centro, y_codon + 13, centro, y_anti - 12, fill=TEXTO)
            canvas.create_rectangle(x, y_anti - 12, x + 3 * ANCHO, y_anti + 12, fill="#fff3e0", outline=ARNT)
            dibujar_fila(canvas, x, y_anti, obtener_anticodon(codones[k]))
            canvas.create_line(centro, y_anti + 12, centro, y_aa - 18, fill=ARNT)
            dibujar_aminoacido(canvas, centro, y_aa, aminoacidos[k])
    if len(codones) > dibujados:
        canvas.create_text(x0 + dibujados * paso, y_aa, anchor="w", font=FUENTE_NEGRITA, fill=PROTEINA,
                           text="··· (se dibujan " + str(dibujados) + " de " + str(len(codones)) + " codones)")

    y_texto = y_aa + 45
    canvas.create_text(20, y_texto, anchor="w", font=FUENTE_TITULO, fill=PROTEINA,
                       text="Proteína (" + str(len(proteina)) + " aminoácidos):  " + abreviar_proteina(proteina))
    if resultado["codon_stop"] is not None:
        nota(canvas, 20, y_texto + 24, "Termina en el codón " + resultado["codon_stop"]
             + ". STOP no es un aminoácido y no forma parte de la proteína.")
    else:
        nota(canvas, 20, y_texto + 24, "No hay codón de parada después del AUG: la traducción llega al final "
                                       "del ARNm y la proteína estaría incompleta.", ARN)
    ajustar_scroll(canvas)


# ---------------------------------------------------------------- resultado

def dibujar_flujo(canvas, adn, replicacion, transcripcion, traduccion):
    """Diagrama del flujo completo ADN → ADN → ARN → proteína con los datos de la ejecución."""
    canvas.delete("all")

    # Cabecera con el dogma central.
    # Debajo de cada flecha se escribe el proceso que representa.
    x = 40
    partes = [("ADN", PARENTAL, ""), ("  →  ", TEXTO, "replicación"), ("ADN", PARENTAL, ""),
              ("  →  ", TEXTO, "transcripción"), ("ARN", ARN, ""), ("  →  ", TEXTO, "traducción"),
              ("PROTEÍNA", PROTEINA, "")]
    for texto, color, proceso in partes:
        elemento = canvas.create_text(x, 35, text=texto, anchor="w", font=("Segoe UI", -27, "bold"), fill=color)
        caja = canvas.bbox(elemento)
        if proceso != "":
            canvas.create_text((caja[0] + caja[2]) / 2, 66, text=proceso, font=FUENTE_NOTA, fill=TEXTO)
        x = caja[2]

    respuesta_identicas = "NO"
    if replicacion["hijo_1"]["hebra_5_3"] == replicacion["hijo_2"]["hebra_5_3"] == adn:
        respuesta_identicas = "sí"

    # Cada fragmento de Okazaki empieza con su propio cebador.
    numero_fragmentos = len(replicacion["fragmentos"])
    if numero_fragmentos == 1:
        texto_okazaki = "1 fragmento de Okazaki, 1 cebador"
    else:
        texto_okazaki = (str(numero_fragmentos) + " fragmentos de Okazaki, "
                         + str(numero_fragmentos) + " cebadores (uno por fragmento)")

    if traduccion["inicio"] == -1:
        datos_traduccion = ["No se ha encontrado un codón de inicio AUG: no hay traducción."]
        datos_proteina = ["No se sintetiza proteína."]
    else:
        if traduccion["codon_stop"] is not None:
            parada = "en " + traduccion["codon_stop"] + " (factor de liberación)"
        else:
            parada = "no hay codón de parada (proteína incompleta)"
        datos_traduccion = [
            "Ribosoma + ARNt · iniciación en el AUG de la posición " + str(traduccion["inicio"] + 1),
            "elongación: " + str(len(traduccion["codones"])) + " codones leídos · terminación: " + parada,
        ]
        datos_proteina = [
            str(len(traduccion["proteina"])) + " aminoácidos",
            abreviar_proteina(traduccion["proteina"]),
        ]

    pasos = [
        ("ADN INICIAL", "molécula", FONDO_PARENTAL, PARENTAL,
         [str(len(adn)) + " nucleótidos", "5' " + abreviar(adn) + " 3'"]),
        ("REPLICACIÓN", "ADN → ADN", "white", HELICASA,
         ["Topoisomerasa, helicasa, SSB, primasa, ADN polimerasa III y I, ADN ligasa",
          "Líder: síntesis continua, 1 cebador  ·  Rezagada: " + texto_okazaki]),
        ("ADN HIJO (x2)", "molécula", FONDO_PARENTAL, PARENTAL,
         ["Semiconservativa: 1 hebra parental + 1 hebra nueva",
          "Idénticas a la molécula inicial: " + respuesta_identicas]),
        ("TRANSCRIPCIÓN", "ADN → ARN", "white", ARN_POLIMERASA,
         ["ARN polimerasa · del promotor al terminador", "lee la cadena molde 3' → 5' y sintetiza el ARNm 5' → 3'"]),
        ("ARNm", "molécula", FONDO_ARN, ARN,
         [str(len(transcripcion["arnm"])) + " nucleótidos", "5' " + abreviar(transcripcion["arnm"]) + " 3'"]),
        ("TRADUCCIÓN", "ARN → PROTEÍNA", "white", RIBOSOMA, datos_traduccion),
        ("PROTEÍNA", "molécula", FONDO_PROTEINA, PROTEINA, datos_proteina),
    ]

    y = 90
    alto = 48
    for numero in range(len(pasos)):
        nombre, subtitulo, relleno, color, detalles = pasos[numero]
        es_proceso = relleno == "white"
        grosor = 2
        if es_proceso:
            grosor = 3
        canvas.create_rectangle(40, y, 300, y + alto, fill=relleno, outline=color, width=grosor)
        canvas.create_text(170, y + 17, text=nombre, font=("Segoe UI", -16, "bold"), fill=color)
        canvas.create_text(170, y + 35, text=subtitulo, font=FUENTE_NORMAL, fill=TEXTO)
        for linea in range(len(detalles)):
            canvas.create_text(325, y + 15 + linea * 19, text=detalles[linea], anchor="w",
                               font=FUENTE_NORMAL, fill=TEXTO)
        if numero < len(pasos) - 1:
            dibujar_flecha(canvas, 170, y + alto, 170, y + alto + 22, TEXTO, 3)
        y += alto + 22
    ajustar_scroll(canvas)
