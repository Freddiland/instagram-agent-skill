---
name: ig-carousel
description: >-
  Crea un carrusel de Instagram: la portada que se gana el deslizamiento, el
  texto de cada diapositiva y los archivos de 1080x1350 para subir. Úsala
  cuando el usuario diga «carrusel», «diapositivas», «slides», «post de
  deslizar», «convierte esto en un carrusel», o tenga una idea con forma de
  lista o de pasos que moriría como imagen única.
---

# ig-carousel

Los carruseles son el formato que más tiempo retiene en la cuadrícula, porque
deslizar es una interacción y hacer scroll no. Además tienen una segunda
oportunidad: Instagram puede volver a enseñar un carrusel empezando por una
diapositiva posterior a quien no interactuó la primera vez, así que la
diapositiva dos también tiene que sostenerse sola.

El formato premia una idea partida en pasos. Castiga un texto cortado en trozos.

**Idioma:** todo el texto de las diapositivas y del post, en español de España.

## Cuándo usarlo en lugar de un Reel

Usa un carrusel cuando la idea tenga **secuencia y haya que releerla**: pasos,
un método con partes, un antes y un después, una lista que merece una captura.
Usa un Reel cuando la idea tenga movimiento, una cara o un premio que hay que
ver suceder.

Si la idea es una sola afirmación, no es ninguna de las dos cosas. Pásala a
`/ig-reel` y dilo.

## Estructura

De 6 a 10 diapositivas. El máximo es 20, y 20 es casi siempre un libro que
nadie termina. Con menos de 5, el deslizamiento ni empieza.

```
1         PORTADA     el hook. 6 palabras o menos, a un tamaño que se lea en la
                      cuadrícula en miniatura. Una línea de promesa debajo.
2         LO EN JUEGO por qué importa, en una frase. Esta diapositiva también es una
                      segunda portada, así que no puede ser preparación.
3 a N     UNA IDEA POR DIAPOSITIVA. Un titular de 3 a 7 palabras y, como mucho,
                      25 palabras debajo. Si necesita un párrafo, son dos diapositivas.
N+1       RESUMEN     todo junto en una lista. Es la diapositiva de la captura.
ÚLTIMA    CTA         una acción. Guardar, comentar una palabra clave o seguir. Una.
```

## Reglas del texto

- **La portada es el 80 % del resultado.** Seis palabras. Grande. Nada del
  carrusel salva una portada por la que nadie desliza.
- **Diseña para el recorte de la cuadrícula.** La cuadrícula del perfil recorta
  en un rectángulo vertical, más alto que ancho, y la proporción exacta ha
  cambiado más de una vez. Trabaja a 1080x1350 y deja el texto de la portada
  bien centrado, lejos de los 120 píxeles exteriores de cada lado, y el
  recorte deja de importar.
- **Numera las diapositivas** (3/8). Se termina más cuando se ve el final.
- **Ninguna diapositiva es un párrafo.** Si no cabe en 25 palabras, pártela.
- **La diapositiva de resumen es la que se captura y se envía.** Los envíos son
  la señal más fuerte que puedes ganarte. Que se entienda sola, sin contexto.
- **El @ en cada diapositiva**, pequeño, en una esquina de abajo. Las capturas
  viajan sin ti.
- **Texto alternativo al menos en la portada.** Lo leen los lectores de
  pantalla e Instagram.
- **Ojo con la longitud en español.** Las frases en español salen un 15-25 % más
  largas que en inglés. Si un titular no cabe, recorta palabras; no bajes el
  tamaño de letra.

## Cómo hacer los archivos

Instagram pide 1080x1350 (4:5), JPEG o PNG, hasta 20 elementos. Hazlo en HTML e
imprime cada diapositiva:

```bash
# una <section> por diapositiva, 1080x1350, page-break-after: always
# y luego Chrome headless --print-to-pdf, o la conversión HTML a imagen que ya uses
```

Escribe el HTML con `width:1080px; height:1350px`, un solo color de acento y
letra de 32px como mínimo, porque se lee en un móvil a un tercio de su tamaño
real. Comprueba que las tildes y la ñ se ven bien con la fuente elegida. Si el
proyecto tiene una skill de marca o un sistema de diseño, úsalo y no te
inventes una paleta.

## Salida

Primero, el texto de cada diapositiva como lista numerada que el usuario pueda
leer en diez segundos y editar antes de generar nada. Después, el **texto del
post**, que en un carrusel es el Trabajo B de `/ig-caption`: aquí el texto
trabaja, porque la portada ya ha gastado sus seis palabras.

Pasa los dos por `/ig-human`. Genera los archivos solo cuando el usuario apruebe
el texto.

```
CARRUSEL  ·  8 diapositivas

1  PORTADA   LA CLÁUSULA DE 18.000 €
             Una línea que ahora pongo en todos mis contratos.
2  EN JUEGO  Aprobé el trabajo. Nueve días después pidieron que les devolviera el dinero.
3            QUÉ DICE
             El pago va con la entrega, no con la aprobación.
...
7  RESUMEN   Las cuatro líneas, en orden.
8  CTA       Comenta CONTRATO y te mando la cláusula completa.

Texto: Trabajo B, hook en la línea 1, una petición, 3 hashtags.
```

No se sube nada. Lo publica el usuario.
