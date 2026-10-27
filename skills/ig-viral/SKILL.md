---
name: ig-viral
description: >-
  Busca los reels que de verdad están funcionando ahora en el nicho del
  usuario, los ordena por cuánto superó cada uno a su propia cuenta, nombra la
  fórmula de hook que usó cada uno y lo convierte en un swipe file del que
  pueda grabar. Úsalo cuando el usuario diga "busca vídeos virales", "qué está
  funcionando ahora", "qué publica la gente en mi nicho", "analiza esta
  cuenta", "hazme un swipe file", "por qué este reel está petándolo", o
  pregunte qué hacer a continuación sin pruebas con las que responder.
---

# ig-viral

La skill de investigación. Todo lo demás de este pack escribe; esta va y mira.
Ejecútala una vez al mes, no a diario. Las fórmulas duran una temporada.

En esta carpeta hay una herramienta y se ejecuta:

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

## La única idea que hace que esto merezca la pena

**Las visualizaciones en bruto no son una prueba.** Una cuenta con dos millones
de seguidores que hace 400.000 vistas ha tenido un martes flojo. Una cuenta con
cuatro mil seguidores que hace 400.000 vistas ha dado con algo, y ese algo se
puede copiar.

Así que aquí todo se ordena por el **múltiplo sobre la referencia**: las vistas
divididas entre la mediana reciente de esa misma cuenta. Lo que pasa de 3x es
una señal. Lo que queda por debajo de 1,5x es un día normal de esa cuenta y no
te enseña nada, por muy grande que parezca la cifra.

Recoge cuentas **como mucho unas 10 veces más grandes que la del usuario**. Una
fórmula que funciona con 2 millones de seguidores a menudo funciona porque
tiene 2 millones de seguidores.

## Paso 1: elegir las cuentas

Pídele al usuario entre 6 y 12 cuentas, o propónselas y que las apruebe:

- **4 directas**: mismo nicho, misma oferta, un poco por delante.
- **4 adyacentes**: otro nicho, misma audiencia. De aquí se toman prestados
  los formatos antes de que nadie del nicho los tenga.
- **De 2 a 4 enormes**: cuentas mucho más grandes, solo para el formato, nunca
  para la frecuencia ni el tono.

Pídele también que abra su **colección de Guardados**. Es el corpus más rápido
y más relevante que existe, y ya está filtrado por su gusto.

## Paso 2: ir a mirar

Usa la herramienta de navegación que tenga de verdad esta sesión: un navegador
integrado, una extensión conectada al Chrome del propio usuario o una
herramienta de uso del ordenador. No hay API para esto y no hace falta, porque
el volumen es lo bastante pequeño como para leerlo.

**Reglas no negociables:**

- **Nunca inicies sesión en Instagram en nombre del usuario y nunca le pidas la
  contraseña.** Si una página pide iniciar sesión, el que ya tiene la sesión
  abierta es el usuario. Maneja su navegador con él delante, o pídele que pegue
  lo que haga falta.
- **Esto es leer, no hacer scraping.** Diez cuentas, una docena de reels cada
  una, a velocidad humana. La recogida automatizada a gran escala incumple las
  Condiciones de uso de Instagram y hace que bloqueen acciones de la cuenta. No
  construyas un rastreador, no uses un servicio de scraping y no lo ejecutes en
  bucle en segundo plano.
- **Copia la fórmula, nunca el vídeo.** La forma del hook, la estructura, la
  duración, el patrón de cortes. No su guion, no su voz, no su edición.
  Atribuye cada fila del swipe file a la cuenta de la que salió.

**Qué recoger de cada reel**, con las palabras del creador:

| campo | notas |
| --- | --- |
| cuenta | el @usuario |
| seguidores | del perfil |
| mediana | mira los últimos 12 reels y quédate con el número de vistas del medio |
| vistas | las de este reel |
| hook | la primera frase, hablada o en pantalla, literal, faltas incluidas |
| en pantalla | el primer rótulo de texto, si es distinto |
| duración | segundos |
| cta | lo que pidieron al final |

La mediana es la importante. Sin ella vuelves a ordenar por número de
seguidores, que es justo lo que esta skill existe para evitar.

**Cuando Instagram no te enseña lo suficiente:** la misma gramática de hook
funciona en YouTube Shorts, donde las vistas y las transcripciones son públicas
y no hace falta iniciar sesión. Es un segundo corpus legítimo, y el hook
hablado es más fácil de sacar:

```bash
# vistas de los shorts de un canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# la primera frase hablada de un short, desde sus subtítulos automáticos
# ("es.*" para canales en español, "en.*" para canales en inglés)
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "es.*" \
  --sub-format json3 -o hook "https://www.youtube.com/watch?v=ID_DEL_VIDEO"
```

Quédate con cada palabra de los subtítulos con marca de tiempo por debajo de
3,0 segundos. Ese es el hook, tal como se dijo, no como se escribió.

## Paso 3: ordenarlo

Rellena un archivo separado por tabuladores con una fila de cabecera (vale en
español o en inglés) y ejecuta el script:

```
cuenta	seguidores	mediana	vistas	hook
@alguien	48000	11000	412000	nadie te cuenta que tus primeros 30 reels están para fracasar
```

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

Calcula el múltiplo, nombra la fórmula de hook con las mismas 26 fórmulas con
las que escribe `/ig-reel`, puntúa cada hook con `hookscore.py` e imprime qué
separa el tercio superior del inferior. Las fórmulas reconocen hooks en
español y en inglés, con o sin tildes.

## Paso 4: decir qué significa, con cuidado

Informa de tres cosas y no más:

1. **Qué fórmulas están sobrerrepresentadas** en el tercio superior, con
   recuentos. Dos fórmulas que aparecen cuatro veces cada una en seis cuentas
   es un hallazgo. Una que aparece dos veces no lo es.
2. **Qué tiene en común el tercio superior en estructura** que no tenga el
   inferior: longitud del hook, si la recompensa es visual, si el primer
   fotograma se mueve, dónde va la petición.
3. **Las filas sin clasificar.** Cada hook que el clasificador no ha podido
   nombrar es ruido o una fórmula que todavía no está en `hooks.json`. Léelos a
   mano. Es la columna más valiosa de la salida y es la razón por la que el
   script imprime el recuento.

Después di el tamaño de la muestra y la confianza con palabras normales.
Cuarenta reels de seis cuentas sostienen una afirmación. Doce no, y decirlo es
la diferencia entre investigar y leer el horóscopo.

## Paso 5: convertirlo en algo que grabar

Para las tres fórmulas principales, escribe **la versión del usuario**: su
propia historia, su propia cifra, con la forma que está funcionando. Pásale
cada una a `/ig-reel` con el id de fórmula ya elegido.

Nunca devuelvas "haz un reel como este". Devuelve una frase de hook que pueda
decir mañana.

## Salida

```
SWIPE  ·  38 reels  ·  7 cuentas  ·  referencia: mediana de la cuenta

ATÍPICOS (por encima de 3x)
  38.4x  hook 86  #3  Nadie te lo cuenta  @cuenta_a    412.000  (mediana 10.700)
  11.2x  hook 79  #9  Róbalo              @cuenta_c    180.000  (mediana 16.100)
  ...

QUÉ ESTÁ SOBRERREPRESENTADO
  #3 Nadie te lo cuenta   x5 en el tercio superior, 0 en el inferior
  #2 Orden negativa       x4
  longitud mediana del hook   8 palabras arriba, 19 abajo

SIN CLASIFICAR (6)
  Dos tienen la misma forma y no está en hooks.json: un hook que empieza
  leyendo en voz alta el comentario de otra persona. Merece la pena añadirlo.

TU VERSIÓN
  #3  "Nadie te cuenta que los primeros 20 presupuestos están para perderlos."
  ...
```

Escribe el swipe file en `~/.claude/instagram/swipe.md`. Lo leen `/ig-reel` y
`/ig-plan`, que es la gracia: después de ejecutarlo una vez, el resto del pack
trabaja con las pruebas del propio usuario en vez de con valores por defecto.

Esta skill no publica, no sigue, no da me gusta ni envía mensajes. Lee.
