---
name: ig-human
description: >-
  Quita la huella de máquina de cualquier borrador (rayas, palabras de relleno
  típicas de IA, caracteres invisibles de marca de agua) y lo puntúa con un
  panel de detección de cinco comprobaciones antes de que salga. Úsalo cuando
  un texto tenga que sonar humano, cuando el usuario diga "humaniza esto",
  "¿esto suena a IA?", "quita las rayas", "esto suena a ChatGPT", "límpialo", o
  antes de enseñarle al usuario cualquier descripción, guion, comentario,
  respuesta o DM.
---

# ig-human

En esta carpeta hay dos herramientas y las dos se ejecutan de verdad. Úsalas.
Esto no se hace a ojo.

```bash
python3 humanize.py borrador.txt --report        # lo limpia y enseña qué cambió
python3 detect.py borrador.txt                    # lo puntúa, cinco comprobaciones
python3 detect.py antes.txt despues.txt           # demuestra la diferencia
```

Las dos leen `slop.json`: 220 palabras y frases de relleno en español y 154 en
inglés, cada una con su sustitución llana, 18 clases de caracteres invisibles,
13 sustituciones tipográficas y 27 señales estructurales. Detectan solas el
idioma del texto y aplican solo las entradas de ese idioma (se puede forzar con
`--lang es`). Al comparar ignoran las tildes, así que "sígueme" y "sigueme"
cuentan igual. El último bloque de cada lista es específico de Instagram: el
vocabulario que solo aparece en descripciones y locuciones. Está pensado para
editarlo. Si el usuario tiene una palabra que usa siempre y el léxico se la
quita, sácala del archivo.

## Por qué en Instagram importa más de lo que parece

Las descripciones son cortas y los guiones se dicen en voz alta. Una frase que
suena a escrita pesa más en una descripción de 600 caracteres que en un ensayo,
y una locución que nadie diría con naturalidad se nota en la primera toma. La
señal aquí no es que un detector marque el post. Es que alguien pase de largo
ante algo que suena a marca, o que un creador se trabe con su propio guion.

## Qué se arregla solo

**1. Caracteres invisibles.** Espacios y uniones de ancho cero, word joiners,
guiones blandos, marcas de orden de bytes, caracteres de etiqueta Unicode,
separadores invisibles, espacios de no separación y estrechos. Un teclado no
los produce. Sobreviven al copiar y pegar, no se ven en ningún editor y son lo
más mecánico de un texto generado. `humanize.py` los borra todos, incluido
cualquier otro carácter de formato Unicode para el que no tenga nombre.

**2. Tipografía.** Raya a coma, guion medio a guion, comillas curvas y
angulares («») a rectas, puntos suspensivos de un solo carácter a tres puntos,
viñeta a guion. Los signos de apertura `¿` y `¡` no se tocan nunca. La pasada
importante es la de la raya: la convierte en coma y luego limpia la doble
puntuación y los puntos huérfanos que deja.

**3. El léxico de relleno.** potenciar, desbloquear, robusto, sin fisuras,
crucial, cabe destacar que, "en el mundo acelerado de hoy", "es un testimonio
de", más el bloque de Instagram: "deja de hacer scroll", "en el vídeo de hoy",
"sígueme para más", "etiqueta a alguien que lo necesite", "al algoritmo le
encanta". Cada uno se cambia por una palabra normal o se borra, respetando
mayúsculas, género y número, y sin tocar los enlaces.

## Qué NO se arregla solo

Las señales estructurales se **señalan, no se reescriben**, porque cambiar la
forma de una frase necesita criterio:

- "No es solo X, es Y" y "no solo X sino también Y"
- "No se trata de X. Se trata de Y."
- Tríadas de tres elementos
- Líneas de pregunta retórica de una palabra: "¿El resultado?"
- El preámbulo de vídeo: "en este vídeo te voy a enseñar"
- Listas con emoji como viñetas
- Tres o más palabras gritadas seguidas
- Muros de hashtags
- Cebos reflejos: "sígueme para más", "etiqueta a alguien que", "dale like si"

Esa lista es trabajo tuyo. Reescribe a mano cada línea señalada manteniendo el
sentido y vuelve a ejecutar `detect.py`. Esto es lo que lleva la nota de
REVISAR a APTO, y es lo que un script no puede hacer.

## Las cinco comprobaciones

`detect.py` puntúa cinco señales de 0 a 100; más alto es más humano:

| comprobación | qué mide | cómo se ve una máquina |
| --- | --- | --- |
| RITMO | variación en la longitud de las frases | todas las frases igual de largas |
| CONCRECIÓN | cifras, nombres y datos concretos por cada 100 palabras | sustantivos abstractos, ni una cifra |
| RELLENO | términos del léxico por cada 100 palabras | vocabulario de plantilla |
| HUELLA | invisibles, rayas y comillas curvas por cada 1.000 caracteres | tipografía perfecta |
| VOZ | registro, persona y señales estructurales | registro neutro, revelaciones montadas |

En la VOZ, el inglés mide contracciones ("don't", "I'm"). El español no tiene
contracciones equivalentes, así que mide marcadores coloquiales ("vale",
"pues", "o sea", "en plan", "tío", "mola"). Ese umbral en español es una
estimación razonada, no una calibración: si el usuario escribe en un registro
neutro a propósito, la VOZ le saldrá más baja sin que eso sea un problema.

El veredicto pondera la media al 60 % y la **comprobación más débil** al 40 %,
porque basta una señal. APTO necesita una nota de 70 o más sin ninguna
comprobación por debajo de 55.

## Dilo con honestidad

Son cinco heurísticas locales basadas en las señales en las que se fijan los
detectores públicos. Se ejecutan enteras en la máquina del usuario y no se
sube nada. **No** son GPTZero, Originality, Copyleaks, Winston ni Turnitin, no
llaman a esas APIs y no pueden prometer esos veredictos. Arreglar lo que miden
suele mover esos números, porque miden las mismas cosas de fondo. Esa es la
afirmación. No hagas una mayor en nombre del usuario y no le digas nunca que su
texto es indetectable.

## Orden de trabajo

1. `humanize.py borrador.txt -o limpio.txt --report`
2. Lee las señales estructurales. Reescribe tú esas líneas.
3. `detect.py borrador.txt limpio.txt` para enseñar el antes y el después.
4. Si el veredicto no es APTO, arregla la comprobación más débil que indique la
   salida y repite. Dos rondas es lo normal. Cinco significa que el borrador
   se escribió por fórmula, y la solución es otro borrador, no más pasadas.
5. Enséñale al usuario el texto limpio y la nota. Nunca la nota sola.
