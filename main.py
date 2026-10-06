import os
import tkinter as tk
from tkinter import ttk, messagebox

from secuencias import leer_fasta, limpiar_secuencia, validar_adn, buscar_caracteres_no_validos
from replicacion import simular_replicacion
from transcripcion import simular_transcripcion
from traduccion import traducir_arnm
from explicaciones import texto_replicacion, texto_transcripcion, texto_traduccion, texto_resultado
from dibujos import dibujar_replicacion, dibujar_transcripcion, dibujar_traduccion, dibujar_flujo

# Secuencia corta para la demostración: AUG, cuatro aminoácidos más y codón de parada.
SECUENCIA_EJEMPLO = "ATGAAACCCGGGTTTTAA"
RUTA_LACZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos", "lacZ.fasta")
FUENTE = ("Consolas", 10)
COLOR_FONDO = "#f5f7f8"


def crear_con_barras(marco, widget):
    """Coloca un Text o un Canvas con barras de desplazamiento vertical y horizontal."""
    barra_v = ttk.Scrollbar(marco, orient="vertical", command=widget.yview)
    barra_h = ttk.Scrollbar(marco, orient="horizontal", command=widget.xview)
    widget.configure(yscrollcommand=barra_v.set, xscrollcommand=barra_h.set)
    barra_v.pack(side="right", fill="y")
    barra_h.pack(side="bottom", fill="x")
    widget.pack(side="left", fill="both", expand=True)


def crear_pestana_visual(pestana, alto_dibujo, alto_texto=8):
    """Divide la pestaña en un esquema gráfico (arriba) y la explicación en texto (abajo)."""
    panel = ttk.PanedWindow(pestana, orient="vertical")
    panel.pack(fill="both", expand=True, padx=8, pady=8)

    marco_dibujo = ttk.LabelFrame(panel, text=" Esquema ")
    lienzo = tk.Canvas(marco_dibujo, background="white", height=alto_dibujo, highlightthickness=0)
    crear_con_barras(marco_dibujo, lienzo)
    # La rueda del ratón desplaza el dibujo (con Mayús, en horizontal).
    lienzo.bind("<MouseWheel>", lambda evento: lienzo.yview_scroll(-evento.delta // 120, "units"))
    lienzo.bind("<Shift-MouseWheel>", lambda evento: lienzo.xview_scroll(-evento.delta // 120, "units"))

    marco_texto = ttk.LabelFrame(panel, text=" Explicación ")
    area = tk.Text(marco_texto, font=FUENTE, wrap="none", state="disabled", height=alto_texto)
    crear_con_barras(marco_texto, area)

    panel.add(marco_dibujo, weight=3)
    panel.add(marco_texto, weight=2)
    return lienzo, area


def mostrar_texto(area, texto):
    area.configure(state="normal")
    area.delete("1.0", "end")
    area.insert("1.0", texto)
    area.configure(state="disabled")


def main():
    ventana = tk.Tk()
    ventana.title("Práctica 1 - Dogma central: ADN → ADN → ARN → proteína")
    ventana.geometry("1200x800")
    ventana.configure(background=COLOR_FONDO)

    estilo = ttk.Style()
    estilo.configure("TNotebook.Tab", padding=(14, 5), font=("Segoe UI", 10, "bold"))
    estilo.configure("TLabelframe.Label", font=("Segoe UI", 9, "bold"), foreground="#37474f")
    estilo.configure("Principal.TButton", font=("Segoe UI", 10, "bold"))

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=6, pady=6)

    pestana_entrada = ttk.Frame(pestanas)
    pestana_replicacion = ttk.Frame(pestanas)
    pestana_transcripcion = ttk.Frame(pestanas)
    pestana_traduccion = ttk.Frame(pestanas)
    pestana_resultado = ttk.Frame(pestanas)
    pestanas.add(pestana_entrada, text="1. Entrada")
    pestanas.add(pestana_replicacion, text="2. Replicación")
    pestanas.add(pestana_transcripcion, text="3. Transcripción")
    pestanas.add(pestana_traduccion, text="4. Traducción")
    pestanas.add(pestana_resultado, text="5. Resultado")

    lienzo_replicacion, area_replicacion = crear_pestana_visual(pestana_replicacion, 430)
    lienzo_transcripcion, area_transcripcion = crear_pestana_visual(pestana_transcripcion, 430)
    lienzo_traduccion, area_traduccion = crear_pestana_visual(pestana_traduccion, 430)
    lienzo_resultado, area_resultado = crear_pestana_visual(pestana_resultado, 560, 4)

    # ---- Pestaña de entrada ----
    cabecera = tk.Frame(pestana_entrada, background="#37474f")
    cabecera.pack(fill="x")
    tk.Label(cabecera, text="Simulación del dogma central de la biología molecular",
             font=("Segoe UI", 16, "bold"), foreground="white", background="#37474f"
             ).pack(anchor="w", padx=14, pady=(12, 0))
    tk.Label(cabecera, text="ADN  →  ADN  →  ARN  →  proteína        (replicación · transcripción · traducción)",
             font=("Segoe UI", 11), foreground="#cfd8dc", background="#37474f"
             ).pack(anchor="w", padx=14, pady=(0, 12))

    marco_secuencia = ttk.LabelFrame(pestana_entrada, text=" Secuencia de ADN: cadena codificante, 5' → 3' ")
    marco_secuencia.pack(fill="both", expand=True, padx=12, pady=(12, 6))
    ttk.Label(marco_secuencia, justify="left", text=(
        "Solo se admiten las bases A, T, C y G. Los espacios y saltos de línea se ignoran.\n"
        "Se puede escribir una secuencia o cargar uno de los dos ejemplos."
    )).pack(anchor="w", padx=8, pady=(6, 0))
    entrada = tk.Text(marco_secuencia, font=("Consolas", 11), height=10, wrap="char")
    entrada.pack(fill="both", expand=True, padx=8, pady=8)

    botones = ttk.Frame(pestana_entrada)
    botones.pack(anchor="w", padx=12, pady=(0, 4))
    etiqueta_estado = ttk.Label(pestana_entrada, text="", foreground="#2e7d32")
    etiqueta_estado.pack(anchor="w", padx=12, pady=(2, 0))

    marco_ayuda = ttk.LabelFrame(pestana_entrada, text=" Qué muestra cada pestaña ")
    marco_ayuda.pack(fill="x", padx=12, pady=(6, 12))
    ttk.Label(marco_ayuda, justify="left", font=("Segoe UI", 9), text=(
        "2. Replicación: topoisomerasa, helicasa, proteínas SSB, primasa y cebadores, ADN polimerasa III y I,\n"
        "    cadena líder, cadena rezagada con fragmentos de Okazaki, ADN ligasa y las dos moléculas hijas.\n"
        "3. Transcripción: promotor y terminador, cadena molde y cadena codificante, ARN polimerasa,\n"
        "    complementariedad y orientación de las cadenas.\n"
        "4. Traducción: iniciación, elongación y terminación; codones desde AUG, ribosoma (subunidades\n"
        "    y sitios P y A), ARNt con su anticodón, aminoácidos y factor de liberación en el STOP.\n"
        "5. Resultado: el flujo completo con los datos de esta ejecución.\n"
        "Los dibujos son esquemas didácticos; en secuencias largas solo se dibuja la primera parte."
    )).pack(anchor="w", padx=8, pady=6)

    def cargar_ejemplo():
        entrada.delete("1.0", "end")
        entrada.insert("1.0", SECUENCIA_EJEMPLO)
        etiqueta_estado.configure(text="Cargada la secuencia corta de ejemplo.")

    def cargar_lacz():
        try:
            secuencia = leer_fasta(RUTA_LACZ)
        except OSError:
            messagebox.showerror("Error", "No se ha podido leer el fichero:\n" + RUTA_LACZ)
            return
        entrada.delete("1.0", "end")
        entrada.insert("1.0", secuencia)
        etiqueta_estado.configure(text="Cargado el gen lacZ de E. coli K-12 MG1655 ("
                                  + str(len(secuencia)) + " nt) desde datos/lacZ.fasta.")

    def ejecutar_simulacion():
        adn = limpiar_secuencia(entrada.get("1.0", "end"))
        if not validar_adn(adn):
            if len(adn) == 0:
                mensaje = "No se ha introducido ninguna secuencia."
            else:
                mensaje = ("La secuencia no es válida. Solo se admiten A, T, C y G.\n"
                           "Caracteres no válidos: " + ", ".join(buscar_caracteres_no_validos(adn)))
            messagebox.showerror("Secuencia no válida", mensaje)
            return

        replicacion = simular_replicacion(adn)
        # Se transcribe una de las moléculas hijas producidas en la replicación.
        hijo = replicacion["hijo_1"]
        transcripcion = simular_transcripcion(hijo["hebra_5_3"], hijo["hebra_3_5"])
        traduccion = traducir_arnm(transcripcion["arnm"])

        dibujar_replicacion(lienzo_replicacion, replicacion)
        dibujar_transcripcion(lienzo_transcripcion, transcripcion)
        dibujar_traduccion(lienzo_traduccion, traduccion)
        dibujar_flujo(lienzo_resultado, adn, replicacion, transcripcion, traduccion)

        mostrar_texto(area_replicacion, texto_replicacion(replicacion))
        mostrar_texto(area_transcripcion, texto_transcripcion(transcripcion))
        mostrar_texto(area_traduccion, texto_traduccion(traduccion))
        mostrar_texto(area_resultado, texto_resultado(adn, replicacion, transcripcion, traduccion))
        etiqueta_estado.configure(text="Simulación completada (" + str(len(adn))
                                  + " nt). Revisa las pestañas 2 a 5.")
        pestanas.select(pestana_replicacion)

    ttk.Button(botones, text="Cargar ejemplo corto", command=cargar_ejemplo).pack(side="left", padx=(0, 6))
    ttk.Button(botones, text="Cargar lacZ (FASTA)", command=cargar_lacz).pack(side="left", padx=(0, 6))
    ttk.Button(botones, text="▶  Ejecutar simulación", style="Principal.TButton",
               command=ejecutar_simulacion).pack(side="left", padx=(12, 0))

    ventana.mainloop()


if __name__ == "__main__":
    main()
