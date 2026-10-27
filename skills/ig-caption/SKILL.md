---
name: ig-caption
description: >-
  Escribe la descripción (pie de foto) de Instagram: la línea que sobrevive al
  corte del "... más", el cuerpo, la única petición, los términos de búsqueda
  y los hashtags, y la revisa antes de que salga. Úsalo cuando el usuario diga
  "escribe la descripción", "hazme el copy", "el caption de este reel", "qué
  pongo en el pie de foto", tenga un reel o un carrusel listo y le falte el
  texto, o pregunte por hashtags.
---

# ig-caption

En esta carpeta hay una herramienta y se ejecuta:

```bash
python3 caption.py descripcion.txt
python3 caption.py descripcion.txt --keywords "presupuestos para clientes,precios de agencia"
```

Imprime la descripción como la imprime el feed: los primeros 125 caracteres en
una caja y todo lo demás detrás del toque. Lee esa caja antes que cualquier
otra cosa que hayas escrito. Funciona en español y en inglés.

## Primero, decide qué trabajo tiene esta descripción

Esta es la decisión que arruina las descripciones cuando se salta.

**Trabajo A: el vídeo ya los ha enganchado.** Un Reel lleva su propio hook en
los dos primeros segundos, hablado y en pantalla. La descripción no es un
segundo hook, y competir con el vídeo es la forma de perder los dos. Su trabajo
es la petición, el contexto que le da sentido y las palabras que la gente busca.

**Trabajo B: la descripción es el contenido.** Una foto, una imagen suelta, una
portada de carrusel que abre una intriga. Aquí la primera línea es el hook y
funciona igual que el de un Reel: concreto, corto y cortado en un punto de
intriga, no en mitad de una subordinada.

Pregúntate cuál estás escribiendo. Si el usuario tiene un Reel con un hook
fuerte, escribe la A y explica por qué.

## La estructura

```
Línea 1     125 caracteres de espacio visible. Trabajo A: la petición, sin
            rodeos. Trabajo B: el hook.
            Nunca un saludo, nunca un hashtag, nunca un emoji como primer
            carácter.
Cuerpo      párrafos cortos, con una línea en blanco entre cada uno. De dos a
            seis. Aquí viven los términos de búsqueda.
La petición una. Comentar una palabra clave, guardarlo o escribir por DM. Una.
Hashtags    hasta cinco, en su propia línea al final, o ninguno.
```

El límite es de 2.200 caracteres y casi nada los necesita. Una descripción que
se gana el toque y luego entrega 600 caracteres gana a una que entrega 1.800.

## Hashtags, con honestidad

Los hashtags ya no son una palanca de alcance, y la plataforma lo ha dicho con
un cambio de producto. **Instagram limitó los hashtags a cinco por publicación
el 18 de diciembre de 2025**, antes eran treinta, y les dijo a los creadores
que usar menos (hasta cinco), más específicos, en vez de muchos genéricos,
funciona mejor. Adam Mosseri ya había dicho en febrero de 2025 que los hashtags
no sirven para aumentar el alcance y que son una etiqueta, no una vía de
distribución.

Así que: hasta cinco, específicos, como etiquetas de tema. Si el usuario tiene
un bloque de veinte guardado en las notas del móvil, ese bloque ya es peso
muerto y el revisor lo marcará como fallo.

`#viral`, `#fyp`, `#parati`, `#explorar` no describen nada. Fuera.

## Los términos de búsqueda importan más que los hashtags

El buscador de Instagram lee el texto de la descripción. Así que la frase por la
que el usuario quiere que le encuentren va en la descripción tal como la
escribiría una persona, dentro de una frase que se lea con normalidad.
"Presupuestos para clientes" como palabras en la tercera línea, no
"#presupuestosparaclientes" en un bloque al final.

Pide dos o tres de esos términos y pásaselos al revisor:

```bash
python3 caption.py borrador.txt --keywords "presupuestos para clientes,precios de agencia"
```

## Reglas

- **Ningún enlace en la descripción.** No es clicable. Una URL en el texto es
  texto muerto que dice "no uso esta plataforma". Bio o DM.
- **Una petición.** Dos peticiones es lo mismo que ninguna. `caption.py` las
  cuenta.
- **La petición de palabra clave necesita una palabra que se pueda escribir.**
  Una palabra, sin espacios, sin emoji, sin tildes si se puede, y dila también
  en voz alta en el vídeo. `Comenta CONTRATO` funciona. `Comenta "la guía del
  contrato"` no.
- **Escribe aparte el primer comentario** si hay enlace. Dilo en el resumen.
- **Emoji como puntuación, no como decoración.** El revisor marca cualquier
  cosa por encima de 4 por cada 100 caracteres.
- **El texto alternativo vale 20 segundos.** En carruseles y fotos, escríbelo.
  Lo leen los lectores de pantalla y lo lee Instagram.

## El proceso

1. Decide si es Trabajo A o B y dilo.
2. Haz el borrador.
3. Pásalo por `/ig-human`. Las descripciones son cortas, así que el relleno se
   nota más aquí que en cualquier otra parte del pack.
4. Ejecuta `caption.py` con los términos de búsqueda del usuario. Arregla cada
   FALLO. Decide en voz alta, no en silencio, sobre cada AVISO.
5. Imprime el bloque listo para copiar y luego el resumen:

```
DESCRIPCIÓN LISTA
trabajo:     A - el reel lleva el hook
visible:     118 de 125 caracteres usados antes del corte
petición:    una, comentar CONTRATO
hashtags:    3
búsqueda:    "presupuestos para clientes" en la línea 3, "precios de agencia" en la 5
revisor:     LISTA
```

No se publica nada. El usuario lo pega.
