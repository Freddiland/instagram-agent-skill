---
name: ig-human
description: >-
  Quita la huella de máquina de cualquier borrador en español (rayas,
  muletillas de IA, calcos del inglés, caracteres invisibles) y lo puntúa con
  un panel de cinco comprobaciones antes de publicarlo. Úsala siempre que un
  texto tenga que sonar humano, cuando el usuario diga «humaniza esto»,
  «¿esto suena a IA?», «quita las rayas», «suena a ChatGPT», «límpialo», y
  antes de enseñarle cualquier texto, guion, comentario, respuesta o mensaje
  privado.
---

# ig-human

En esta carpeta hay dos herramientas y las dos funcionan de verdad. Úsalas. No
lo hagas a ojo.

```bash
python3 humanize.py borrador.txt --report        # lo limpia y enseña qué ha cambiado
python3 detect.py borrador.txt                    # lo puntúa, cinco comprobaciones
python3 detect.py antes.txt despues.txt           # demuestra la diferencia
```

Las dos leen `slop.json`: 300 palabras y frases de relleno con sustituciones en
español de España, 18 clases de caracteres invisibles, 11 sustituciones
tipográficas y 18 señales estructurales. La búsqueda ignora tildes y
mayúsculas, así que «Adentrémonos» y «adentremonos» caen igual. El último
bloque de cada lista es específico de Instagram: el vocabulario que solo sale
en textos de publicaciones y voces en off. Está hecho para editarlo. Si el
usuario tiene una palabra que usa siempre y el diccionario la quita, sácala del
archivo.

**Idioma:** todo lo que entregues, en español de España, salvo que el usuario
pida otro. Tú o vosotros, no usted, salvo que su público lo pida.

## Por qué en Instagram importa más de lo que parece

Los textos son cortos y los guiones se dicen en voz alta. Una frase que suena
escrita en un texto de 600 caracteres pesa mucho más que la misma frase en un
artículo, y una voz en off que nadie diría con naturalidad se nota en la
primera toma. La señal aquí no es que un detector marque el post. La señal es
una persona que pasa de largo porque aquello suena a marca, o un creador que
se traba con su propio guion.

## Qué se arregla solo

**1. Caracteres invisibles.** Espacios y unidores de ancho cero, unidores de
palabra, guiones blandos, marcas de orden de bytes, caracteres de etiqueta
Unicode, separadores invisibles, espacios duros y estrechos. Un teclado no los
produce. Sobreviven al copiar y pegar, son invisibles en cualquier editor y son
lo más mecánico de un texto generado. `humanize.py` los borra todos, incluido
cualquier carácter de formato Unicode que no tenga en su lista.

**2. Tipografía.** Raya a coma, semirraya a guion, comillas curvas a rectas,
el carácter único de puntos suspensivos a tres puntos, viñeta a guion. La
pasada de la raya es la importante: convierte el inciso en coma y luego limpia
la puntuación doble y los puntos huérfanos que deja. La raya de diálogo a
principio de línea se quita sin más. Las comillas latinas «» y los signos ¿ ¡
**no se tocan**: son español correcto, no huella.

**3. Las muletillas.** Potenciar, crucial, robusto, sin fisuras, adentrémonos,
«en el mundo actual», «juega un papel fundamental», «cabe destacar que», los
calcos del inglés («al final del día», «mover la aguja», «un cambio de
juego») y el bloque de Instagram: «deja de hacer scroll», «en el vídeo de
hoy», «sígueme para más», «etiqueta a alguien que necesite esto», «el
algoritmo ama». Cada una se cambia por una palabra normal o se borra,
respetando las mayúsculas, la concordancia de género y número, y sin tocar los
enlaces.

## Qué NO se arregla solo

Las señales estructurales se **marcan, no se reescriben**, porque cambiar la
forma de una frase necesita criterio:

- «No es solo X, es Y», «No se trata de X, se trata de Y» y «No solo X, sino también Y»
- Tríadas de tres elementos
- Preguntas retóricas de una línea: «¿El resultado?»
- El preámbulo de vídeo: «En este vídeo te voy a enseñar»
- Listas con emojis como viñetas
- Tres o más palabras seguidas en mayúsculas
- Muros de hashtags
- Cebos reflejos: «sígueme para más», «etiqueta a alguien que», «dale doble tap si»
- **Mayúscula en cada palabra de un título** («Cómo Crecer En Instagram»): calco del inglés
- **Conectores de redacción al inicio de frase** («Además,», «Asimismo,», «Por otro lado,»)

Esa lista es tu trabajo. Reescribe a mano cada línea marcada, conservando el
sentido, y vuelve a pasar `detect.py`. Esto es lo que lleva la nota de REVISAR
a PASA, y es justo lo que un script no puede hacer.

## Las cinco comprobaciones

`detect.py` puntúa cinco señales de 0 a 100, y más es más humano:

| comprobación | qué mide | cómo se ve la máquina |
| --- | --- | --- |
| VARIACIÓN | variación en la longitud de las frases | todas las frases igual de largas |
| CONCRECIÓN | cifras (también con letra), días, meses y nombres por cada 100 palabras | sustantivos abstractos, ninguna cifra |
| MULETILLAS | coincidencias del diccionario por cada 100 palabras | vocabulario de relleno |
| HUELLA | invisibles, rayas, comillas curvas por cada 1.000 caracteres | tipográficamente perfecto |
| VOZ | registro coloquial, 1.ª y 2.ª persona, adverbios en -mente, señales estructurales | impersonal, lleno de «-mente», revelaciones montadas |

En español no hay contracciones como en inglés, así que la VOZ se mide con
marcas de registro hablado («vale», «mira», «o sea», «un montón»), con los
pronombres de primera y segunda persona, y con la densidad de adverbios en
«-mente», que es una de las huellas más claras del texto generado en español.

El veredicto pondera la media al 60 % y la **comprobación más floja** al 40 %,
porque basta una señal. PASA necesita una nota global de 70 o más sin ninguna
comprobación por debajo de 55. Los demás veredictos son REVISAR y SOSPECHOSO.

## Dilo con honestidad

Son cinco heurísticas locales inspiradas en las señales en las que se fijan los
detectores públicos. Funcionan enteras en el equipo y no se sube nada. **No**
son GPTZero, Originality, Copyleaks, Winston ni Turnitin, no llaman a esas API
y no pueden prometer sus veredictos. Arreglar lo que miden suele mover esos
números, porque miden las mismas cosas de fondo. Esa es la afirmación. No hagas
una más grande en nombre del usuario y no le digas nunca que su texto es
indetectable.

Los umbrales de las cinco comprobaciones vienen de la versión original en
inglés y no se han recalibrado con un corpus en español. Un texto humano puede
salir en REVISAR, sobre todo en VARIACIÓN. Si pasa, dilo, no fuerces la
reescritura de algo que ya suena bien.

## Orden de trabajo

1. `humanize.py borrador.txt -o limpio.txt --report`
2. Lee las señales estructurales. Reescribe tú esas líneas.
3. `detect.py borrador.txt limpio.txt` para enseñar el antes y el después.
4. Si el veredicto no es PASA, arregla la comprobación más floja que indica la
   salida y repite. Dos rondas es lo normal. Cinco significa que el borrador
   está escrito con plantilla, y la solución es otro borrador, no más pasadas.
5. Enséñale al usuario el texto limpio y la nota. Nunca la nota sola.
