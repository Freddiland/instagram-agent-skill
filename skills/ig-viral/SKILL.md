---
name: ig-viral
description: >-
  Busca los reels que de verdad están funcionando ahora en el nicho del
  usuario, los ordena por cuánto superaron a su propia cuenta, nombra la
  fórmula de hook de cada uno y lo convierte en un archivo de referencias del
  que se puede grabar. Úsala cuando el usuario diga «busca vídeos virales»,
  «qué está funcionando ahora», «qué publica la gente de mi nicho», «analiza
  esta cuenta», «hazme un swipe file», «por qué este reel está petándolo», o
  pregunte qué hacer a continuación sin datos con los que responder.
---

# ig-viral

La skill de investigación. Todo lo demás del paquete escribe; esta sale a
mirar. Úsala una vez al mes, no a diario. Las fórmulas duran una temporada.

**Idioma:** el informe y las versiones para el usuario, en español de España.
Copia los hooks de otras cuentas tal como los dicen, en su idioma.

En esta carpeta hay una herramienta y funciona:

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

## La idea que hace que merezca la pena

**Las visitas a secas no son una prueba.** Una cuenta con dos millones de
seguidores que hace 400.000 visitas ha tenido un martes flojo. Una cuenta con
cuatro mil seguidores que hace 400.000 visitas ha dado con algo, y ese algo se
puede copiar.

Por eso aquí todo se ordena por el **múltiplo sobre lo normal**: visitas
divididas entre la mediana reciente de esa misma cuenta. Por encima de 3x es
una señal. Por debajo de 1,5x es un día normal de esa cuenta y no te enseña
nada, por grande que parezca el número.

Recoge cuentas **de hasta unas 10 veces el tamaño del usuario**. Una fórmula
que funciona con 2 millones de seguidores muchas veces funciona porque tiene 2
millones de seguidores.

## Paso 1: elige las cuentas

Pide al usuario entre 6 y 12 cuentas, o propónselas y que te dé el visto bueno:

- **4 directas**: mismo nicho, misma oferta, un poco por delante.
- **4 cercanas**: otro nicho, mismo público. Es de donde se toman prestados
  los formatos antes de que nadie del nicho los tenga.
- **De 2 a 4 enormes**: cuentas mucho más grandes, solo para el formato, nunca
  para la frecuencia ni el tono.

Pídele también que abra su propia **colección de Guardados**. Es el corpus más
rápido y más relevante que existe, y ya viene filtrado por su gusto.

Si trabaja en el mercado español, prioriza cuentas en español: los hooks se
dicen distinto y las fórmulas que funcionan en inglés no siempre se traducen.

## Paso 2: ve a mirar

Usa la herramienta de navegación que tenga de verdad esta sesión: un navegador
integrado, una extensión conectada al Chrome del propio usuario o una
herramienta de control del ordenador. No hay API para esto y no hace falta,
porque el volumen es lo bastante pequeño como para leerlo.

**Reglas no negociables:**

- **Nunca inicies sesión en Instagram en nombre del usuario y nunca le pidas
  la contraseña.** Si una página pide iniciar sesión, quien ya la tiene
  iniciada es el usuario. Maneja su navegador con él delante, o pídele que
  pegue la información.
- **Esto es leer, no hacer scraping.** Diez cuentas, una docena de reels por
  cuenta, a velocidad humana. La recogida automática a volumen incumple las
  Condiciones de uso de Instagram y provoca bloqueos de acciones. No construyas
  un rastreador, no uses un servicio de scraping y no lo pongas en bucle en
  segundo plano.
- **Copia la fórmula, nunca el vídeo.** La forma del hook, la estructura, la
  duración, el patrón de cortes. No su guion, ni su voz, ni su edición.
  Atribuye cada fila del archivo de referencias a la cuenta de la que sale.

**Qué apuntar de cada reel**, con las palabras del creador:

| campo | notas |
| --- | --- |
| cuenta | el @ |
| seguidores | del perfil |
| mediana | mira los 12 últimos reels y quédate con el número de visitas del medio |
| visitas | las de este reel |
| hook | la primera frase, dicha o en pantalla, literal, faltas incluidas |
| en pantalla | la primera tarjeta de texto, si es distinta |
| duración | segundos |
| cta | qué pidió al final |

La mediana es la importante. Sin ella vuelves a ordenar por número de
seguidores, que es justo lo que esta skill existe para evitar.

**Cuando Instagram no te deja ver lo suficiente:** la misma gramática de hooks
funciona en YouTube Shorts, donde las visitas y las transcripciones son
públicas y no hace falta iniciar sesión. Es un segundo corpus legítimo, y el
hook hablado es más fácil de sacar:

```bash
# visitas de los shorts de un canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# la primera frase hablada de un short, de sus subtítulos automáticos
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "es.*" \
  --sub-format json3 -o hook "https://www.youtube.com/watch?v=ID_DEL_VIDEO"
```

Quédate con cada palabra de los subtítulos con marca de tiempo por debajo de
3,0 segundos. Ese es el hook, tal como se dijo y no como se escribió. Si el
canal no tiene subtítulos automáticos en español, usa `--sub-langs "es.*,en.*"`.

## Paso 3: ordénalo

Rellena un archivo separado por tabuladores con una fila de cabecera (sirven
los nombres en español o en inglés) y pasa el script:

```
cuenta	seguidores	mediana	visitas	hook
@alguien	48000	11000	412000	nadie te cuenta que tus primeros 30 reels están para fracasar
```

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

Calcula el múltiplo, nombra la fórmula de hook con las mismas 26 fórmulas con
las que escribe `/ig-reel` (la comparación ignora tildes, porque en las
transcripciones y los comentarios casi nadie las pone), puntúa cada hook con
`hookscore.py` e imprime lo que separa el tercio de arriba del de abajo.

## Paso 4: di qué significa, con cuidado

Informa de tres cosas y nada más:

1. **Qué fórmulas destacan** en el tercio de arriba, con recuentos. Dos
   fórmulas que salen cuatro veces cada una en seis cuentas son un hallazgo.
   Una que sale dos veces, no.
2. **Qué tienen en común en estructura** los de arriba que no tengan los de
   abajo: longitud del hook, si el premio es visual, si el primer fotograma se
   mueve, dónde va la petición.
3. **Las filas sin clasificar.** Cada hook que el clasificador no sabe nombrar
   es ruido o una fórmula que todavía no está en `hooks.json`. Léelos a mano. Es
   la columna más valiosa de la salida y es la razón por la que el script
   imprime el recuento. Las fórmulas de esta versión están escritas en español
   pero no se han validado con un corpus de reels en español, así que espera
   más filas sin clasificar que en la versión original y trátalas como pistas.

Después di el tamaño de la muestra y la confianza con palabras normales.
Cuarenta reels de seis cuentas sostienen una afirmación. Doce no, y decirlo es
la diferencia entre investigar y leer el horóscopo.

## Paso 5: conviértelo en algo que grabar

Para las tres fórmulas de arriba, escribe **la versión del usuario**: su propia
historia, su propia cifra, con la forma que está funcionando. Pásale cada una a
`/ig-reel` con el número de fórmula ya elegido.

No devuelvas nunca «haz un reel como este». Devuelve una frase de hook que
podría decir mañana.

## Salida

```
REFERENCIAS  ·  38 reels  ·  7 cuentas  ·  referencia: mediana de la cuenta

POR ENCIMA DE 3x
  38,4x  hook 81  #3  Nadie te lo cuenta  @cuenta_a   412.000  (mediana 10.700)
  11,2x  hook 74  #9  El robo             @cuenta_c   180.000  (mediana 16.100)
  ...

QUÉ ESTÁ DESTACANDO
  #3 Nadie te lo cuenta   x5 en el tercio de arriba, 0 en el de abajo
  #2 Orden negativa       x4
  longitud mediana        8 palabras arriba, 19 abajo

SIN CLASIFICAR (6)
  Dos tienen la misma forma y no está en hooks.json: un hook que empieza
  leyendo en voz alta el comentario de otra persona. Merece la pena añadirlo.

TU VERSIÓN
  #3  «Nadie te cuenta que los primeros 20 presupuestos están para perderlos.»
  ...
```

Escribe el archivo de referencias en `~/.claude/instagram/swipe.md`. Lo leen
`/ig-reel` y `/ig-plan`, y esa es la gracia: después de usarla una vez, el
resto del paquete trabaja con las pruebas del propio usuario y no con valores
por defecto.

Esta skill no publica, no sigue, no da me gusta ni envía mensajes. Lee.
