# Práctica 1 - Simulación del dogma central de la biología molecular

**Asignatura:** Bioinformática. Escuela de Ingeniería Informática, ULPGC
**Autoras:** Kimberly Casimiro Torres y Leonoor Antje Barton

## Descripción

Simulador con interfaz gráfica (tkinter) que, a partir de una molécula de ADN, representa el flujo de la información genética:

```text
ADN  →  ADN  →  ARN  →  proteína
   replicación  transcripción  traducción
```

Cada etapa tiene su propia pestaña con dos partes:

- **Esquema gráfico** (dibujado con `tkinter.Canvas`) construido con las secuencias reales de la simulación.
- **Explicación en texto**, paso a paso, con las enzimas, las moléculas y la orientación 5'/3' de todas las cadenas.

## Objetivos

- Comprender de forma integrada la replicación, la transcripción y la traducción.
- Representar con un programa el flujo de información desde el ADN hasta la proteína.
- Identificar el papel de las principales moléculas y enzimas de cada proceso.
- Diferenciar la formación de la cadena líder y de la cadena rezagada, incluidos los fragmentos de Okazaki.

## Convenio de orientación

La secuencia introducida es la **cadena codificante**, escrita 5' → 3' de izquierda a derecha. La hebra complementaria se escribe alineada debajo, es decir, 3' → 5'. En la replicación el origen está en el extremo izquierdo y la horquilla avanza hacia la derecha.

## Replicación (ADN → ADN)

- **Helicasa:** separa las dos cadenas de ADN al abrir la doble hélice, rompiendo los puentes de hidrógeno entre las bases.
- **Primasa:** coloca los cebadores que permiten iniciar la síntesis.
- **Cebadores:** fragmentos cortos de ARN que aportan el extremo 3' libre que necesita la ADN polimerasa. En el programa aparecen en minúsculas, con U en lugar de T y en color naranja.
- **ADN polimerasa:** añade nucleótidos complementarios (A-T, C-G) y sintetiza la nueva cadena, siempre 5' → 3'. También sustituye el ARN de los cebadores por ADN.
- **Cadena líder:** su molde es la hebra 3' → 5'. Como crece 5' → 3' en el mismo sentido en que avanza la horquilla, se sintetiza de forma **continua** con un único cebador en el origen.
- **Cadena rezagada:** su molde es la hebra 5' → 3'. Para crecer 5' → 3' tiene que avanzar en sentido contrario a la horquilla, así que se sintetiza de forma **discontinua**.
- **Fragmentos de Okazaki:** son los trozos de la cadena rezagada. Cada uno empieza con su propio cebador en el extremo 5'. El fragmento 1 es el más cercano al origen.
- **ADN ligasa:** una vez sustituidos los cebadores por ADN, sella las mellas entre fragmentos y deja la cadena rezagada continua.
- **Semiconservatividad:** se obtienen dos moléculas hijas. Cada una tiene una hebra parental y una hebra nueva. El programa comprueba que ambas son idénticas a la molécula original.

**Esquema de la pestaña Replicación:**

1. La horquilla en un instante intermedio:
   - las hebras parentales separadas y, a la derecha, la doble hélice todavía sin abrir;
   - la helicasa en el punto de apertura;
   - la cadena líder completa hasta la horquilla, con su ADN polimerasa;
   - los fragmentos de Okazaki con sus flechas de síntesis (←);
   - el último fragmento a medio sintetizar, con la primasa sobre su cebador y la ADN polimerasa en el hueco.
2. La maduración de la rezagada: fragmentos con cebador, cebadores sustituidos por ADN, ligasa en cada mella y cadena completa.
3. Las dos moléculas hijas, coloreadas según si cada hebra es parental o nueva.

Los fragmentos tienen 6 nucleótidos y los cebadores 2. Son tamaños didácticos, porque los reales son mucho mayores.

## Transcripción (ADN → ARNm)

Se transcribe una de las moléculas hijas obtenidas en la replicación.

- **Cadena codificante:** la hebra 5' → 3'. Tiene la misma secuencia que el ARNm, salvo que lleva T donde el ARN lleva U.
- **Cadena molde:** la hebra complementaria (3' → 5'). Es la que lee la enzima.
- **ARN polimerasa:** lee la cadena molde 3' → 5' y sintetiza el ARNm 5' → 3'. El ARNm es antiparalelo a la molde y paralelo a la codificante.
- **Complementariedad molde → ARN:** A → U, T → A, C → G, G → C.

**Esquema de la pestaña Transcripción:**
- las tres cadenas alineadas, con las bases coloreadas;
- una flecha de complementariedad por cada base;
- la ARN polimerasa y los sentidos de lectura y de síntesis;
- un cuadro con las reglas de complementariedad;
- una comparación entre la cadena codificante y el ARNm, que resalta las posiciones en las que la T pasa a ser U.

## Traducción (ARNm → proteína)

- **Codones:** el ARNm se lee 5' → 3' en grupos de tres nucleótidos, sin solapamiento.
- **Código genético:** diccionario con los 64 codones, escrito en `traduccion.py`.
- **Inicio (AUG):** la traducción empieza en el primer AUG (metionina). Los nucleótidos anteriores no se traducen. Si no hay AUG, se indica que no puede iniciarse la traducción.
- **Parada (UAA, UAG, UGA):** la traducción termina en el primer codón de parada. Se muestra, pero no se añade a la proteína. Si no aparece ninguno, se avisa de que la proteína estaría incompleta.
- **ARNt:** cada ARNt reconoce un codón mediante su anticodón, complementario y antiparalelo (codón 5' AUG 3' ↔ anticodón 3' UAC 5'), y transporta el aminoácido correspondiente.
- **Ribosoma:** recorre el ARNm 5' → 3' y une los aminoácidos mediante enlaces peptídicos.

**Esquema de la pestaña Traducción:**
1. El ARNm dividido en codones, con el inicio y el STOP marcados.
2. Un ribosoma en plena elongación, con los sitios P y A. El ARNt del sitio P lleva la cadena ya formada y al sitio A llega el siguiente ARNt.
3. Una tabla gráfica codón → anticodón → aminoácido, en la que los aminoácidos aparecen unidos formando la proteína.

## Resultado

Diagrama de flujo con los datos de la ejecución:

```text
ADN inicial → replicación → ADN hijo (x2) → transcripción → ARNm → traducción → proteína
```

Incluye la longitud del ADN y del ARNm, el número de fragmentos de Okazaki y de cebadores, la posición del AUG, los codones leídos, el codón de parada y la proteína con su longitud.

## Ejemplos

- **Secuencia corta de prueba:** `ATGAAACCCGGGTTTTAA`, la que usamos para la demostración.
  - 3 fragmentos de Okazaki;
  - codón de inicio AUG;
  - proteína Met-Lys-Pro-Gly-Phe;
  - codón de parada UAA.
- **Secuencia real:** gen *lacZ* de *Escherichia coli* K-12 MG1655 (`datos/lacZ.fasta`, NC_000913.3:c366305-363231, 3075 nt). Se traduce a la β-galactosidasa, de 1024 aminoácidos.

Se puede escribir cualquier otra secuencia. Solo se admiten A, T, C y G, y se ignoran espacios y saltos de línea. Si aparece otro carácter, se muestra un mensaje de error.

## Lectura FASTA

`fasta.py` incluye un lector propio:
1. ignora la línea de cabecera, que empieza por `>`;
2. une las líneas de secuencia;
3. elimina espacios y saltos de línea;
4. devuelve la secuencia en mayúsculas.

Después la secuencia pasa por la misma validación que una secuencia escrita a mano.

## Decisiones técnicas

- **Python + tkinter.** tkinter viene con Python, y su `Canvas` basta para dibujar esquemas con rectángulos, óvalos, líneas, flechas y texto. No hacen falta OpenCV, NumPy ni otras librerías.
- **Biopython.** Se podría utilizar Biopython para el manejo de secuencias, ya que está permitido en la práctica. Sin embargo, para esta implementación se han programado directamente las operaciones básicas utilizadas en la simulación, de forma que la lógica de complementariedad, transcripción y traducción quede explícita.
- **Separación por procesos.** Cada proceso biológico tiene su módulo. La interfaz (`main.py`) y los dibujos (`dibujos.py`) solo muestran los resultados que calculan esos módulos.
- **Esquemas didácticos.** Los dibujos no son modelos moleculares realistas, sino esquemas simplificados construidos con los datos de la simulación. Para que las secuencias largas se puedan leer, solo se dibujan los primeros 48 nucleótidos o 14 codones. En el propio dibujo se indica que la representación es parcial y aparecen puntos suspensivos (`···`) al final de las cadenas. La explicación en texto incluye las secuencias completas.

## Instalación

No hacen falta librerías externas. Solo se necesita Python 3 con tkinter, que viene incluido en la instalación estándar de Python para Windows. Por eso el proyecto no incluye fichero `requirements.txt`.

## Ejecución

```bash
python main.py
```

1. En la pestaña **Entrada**, pulsar **Cargar ejemplo corto** (o **Cargar lacZ (FASTA)**, o escribir una secuencia).
2. Pulsar **Ejecutar simulación**.
3. Recorrer las pestañas **Replicación**, **Transcripción**, **Traducción** y **Resultado**. En cada pestaña, la barra que separa el esquema de la explicación se puede arrastrar. El esquema se desplaza con la rueda del ratón, o con Mayús + rueda en horizontal.

## Estructura

```text
Practica1_Dogma_Central/
├── main.py            Interfaz tkinter: pestañas, botones y texto del resumen final
├── replicacion.py     Complementariedad, cadena líder, fragmentos de Okazaki, ligasa y moléculas hijas
├── transcripcion.py   Transcripción de la cadena molde a ARNm
├── traduccion.py      Código genético, búsqueda de AUG, codones, anticodones y STOP
├── fasta.py           Lectura del fichero FASTA y validación de la secuencia de ADN
├── dibujos.py         Esquemas gráficos (tkinter.Canvas) de cada etapa y del flujo completo
├── datos/
│   └── lacZ.fasta     Gen lacZ de E. coli K-12 MG1655
└── README.md
```
