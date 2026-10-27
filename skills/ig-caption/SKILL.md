---
name: ig-caption
description: >-
  Escribe el texto de una publicación de Instagram (la línea que sobrevive al
  corte del «... más», el cuerpo, la única petición, los términos de búsqueda
  y los hashtags) y lo revisa antes de publicarlo. Úsala cuando el usuario
  diga «escribe el texto», «ponle copy a esto», «qué pongo en la
  descripción», tenga un reel o un carrusel listo y le falte el texto, o
  pregunte por hashtags.
---

# ig-caption

En esta carpeta hay una herramienta y funciona:

```bash
python3 caption.py texto.txt
python3 caption.py texto.txt --keywords "presupuestos para clientes,precios de agencia"
```

Imprime el texto tal como lo enseña el feed: los primeros 125 caracteres en un
recuadro y todo lo demás detrás del toque. Lee ese recuadro antes que cualquier
otra cosa que hayas escrito.

**Idioma:** el texto, en español de España, salvo que el usuario pida otro.

## Primero, decide qué trabajo tiene este texto

Esta es la decisión que arruina los textos cuando se salta.

**Trabajo A: el vídeo ya los ha enganchado.** Un Reel lleva su propio hook en
los dos primeros segundos, dicho y en pantalla. El texto no es un segundo hook,
y competir con el vídeo es como se pierden los dos. Su trabajo es la petición,
el contexto que hace que la petición tenga sentido y las palabras que busca la
gente.

**Trabajo B: el texto es el contenido.** Una foto, una sola imagen, una
portada de carrusel que abre una intriga. Aquí la primera línea es el hook y
funciona exactamente igual que el de un Reel: concreta, corta y cortada en un
momento de intriga, no a mitad de una subordinada.

Pregunta cuál estás escribiendo. Si el usuario tiene un Reel con un hook fuerte,
escribe el A y di por qué.

## La estructura

```
Línea 1     125 caracteres de espacio visible. Trabajo A: la petición, sin rodeos.
            Trabajo B: el hook.
            Nunca un saludo, nunca un hashtag, nunca un emoji como primer carácter.
Cuerpo      párrafos cortos, con una línea en blanco entre cada uno. De dos a seis.
            Aquí van los términos de búsqueda.
Petición    una. Comentar una palabra clave, guardarlo o escribir por privado. Una.
Hashtags    hasta cinco, en su propia línea al final, o ninguno.
```

El límite es de 2.200 caracteres y casi nada necesita 2.200. Un texto que se
gana el toque y luego da 600 caracteres gana a uno que da 1.800.

## Hashtags, con honestidad

Los hashtags ya no son una palanca de alcance, y la plataforma lo ha dicho con
un cambio de producto. **Instagram limitó los hashtags a cinco por publicación
en diciembre de 2025**, cuando antes eran treinta, y recomendó a los creadores
usar pocos y específicos en lugar de muchos genéricos. Adam Mosseri ya había
dicho en febrero de 2025 que los hashtags no sirven para aumentar el alcance y
que son una etiqueta, no una forma de distribución.

Así que: hasta cinco, específicos, como etiquetas de tema. Si el usuario tiene
un bloque de veinte guardado en las notas del móvil, ese bloque ya es peso
muerto y la revisión lo suspenderá.

`#viral`, `#fyp`, `#parati`, `#explorar`, `#seguidores` no describen nada.
Quítalos.

## Los términos de búsqueda importan más que los hashtags

El buscador de Instagram lee el texto. Así que la frase por la que el usuario
quiere que lo encuentren va en el texto como la escribiría una persona, dentro
de una frase que se lea con normalidad. «Presupuestos para clientes» como
palabras en la tercera línea, no «#presupuestosparaclientes» en un bloque al
final.

Pide dos o tres de esos términos y pásalos a la revisión:

```bash
python3 caption.py borrador.txt --keywords "presupuestos para clientes,precios de agencia"
```

## Reglas

- **Ningún enlace en el texto.** El texto no es clicable. Una URL en el cuerpo es
  texto muerto que dice «no uso esta plataforma». A la bio o al privado.
- **Una petición.** Dos peticiones es lo mismo que ninguna. `caption.py` las
  cuenta.
- **La petición de palabra clave necesita una palabra que se pueda escribir.**
  Una palabra, sin espacios, sin emojis, en MAYÚSCULAS, y dila también en voz
  alta en el vídeo. `Comenta CONTRATO` funciona. `Comenta «la guía del
  contrato»` no. Mejor sin tilde, para que nadie dude cómo escribirla.
- **Escribe aparte el primer comentario** si hay un enlace. Dilo en el resumen.
- **Emojis como puntuación, no como decoración.** La revisión avisa a partir de
  4 por cada 100 caracteres.
- **El texto alternativo vale 20 segundos.** En carruseles y fotos, escríbelo. Lo
  leen los lectores de pantalla e Instagram.

## El proceso

1. Decide si es Trabajo A o B y dilo.
2. Escribe el borrador.
3. Pásalo por `/ig-human`. Los textos son cortos, así que el relleno se nota aquí
   más que en ningún otro sitio del paquete.
4. Pasa `caption.py` con los términos de búsqueda del usuario. Arregla cada
   FALLO. Decide cada AVISO en voz alta, no en silencio.
5. Entrega el bloque listo para copiar y luego el resumen:

```
TEXTO LISTO
trabajo:      A: el reel lleva el hook
visible:      118 de 125 caracteres antes del corte
petición:     una, comenta CONTRATO
hashtags:     3
búsqueda:     «presupuestos para clientes» en la línea 3, «precios de agencia» en la 5
revisión:     LISTO
```

No se publica nada. Lo pega el usuario.
