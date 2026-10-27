---
name: ig-reply
description: >-
  Gestiona los comentarios de los reels y posts del propio usuario: redacta
  respuestas para los que merecen respuesta, ordenados por cuáles la merecen.
  Úsala cuando el usuario pegue sus comentarios, diga «responde a estos»,
  «gestiona mis comentarios», «alguien ha puesto X en mi reel», o esté
  lidiando con un crítico, un hater o un posible cliente en los comentarios.
---

# ig-reply

El hilo de comentarios de tu propio post es donde se decide el alcance. Cada
respuesta es otra interacción en el post, las respuestas de la primera hora
hacen la mayor parte del trabajo, y en Instagram una respuesta también puede
ser un Reel, que es el movimiento menos aprovechado de toda la plataforma.

Pero no todos los comentarios valen lo mismo, así que esta skill ordena antes
de escribir.

**Idioma:** responde en el idioma del comentario. En español, de España, y en el
registro de la persona: si escribe de tú, de tú.

## Lo que necesitas

El usuario pega los comentarios, a ser posible con los @. Las capturas valen.
No rastrees el hilo con un navegador.

## Primero, clasificar

Mete cada comentario en uno de estos seis grupos y di los recuentos en voz alta:

| grupo | qué es | qué recibe |
| --- | --- | --- |
| **PALABRA CLAVE** | la palabra que les pediste que comentaran | lo prometido, enviado a mano o con tu herramienta aprobada |
| **CLIENTE** | alguien que describe el problema que tú resuelves | una respuesta de verdad en público, y luego una puerta |
| **FONDO** | aporta datos, discrepa, amplía | la respuesta más larga del hilo |
| **PREGUNTA** | una pregunta que tiene mucha gente | esta se convierte en un Reel, no solo en una respuesta |
| **APOYO** | «🔥», «qué buen post», una etiqueta | un me gusta y de 3 a 8 palabras como mucho |
| **RUIDO** | venta, spam, mala fe, provocación | nada, o una línea y fuera |

Escribe en ese orden y para cuando deje de merecer la pena.

## El movimiento que casi nadie hace

Si una pregunta de los comentarios la tienen otras treinta personas,
**respóndela con un Reel**. Instagram adjunta el comentario al vídeo nuevo como
sticker, la persona que preguntó recibe un aviso, y una pregunta con demanda
real detrás se convierte en un post con el hook ya escrito. Marca cada PREGUNTA
que cumpla esto y pásasela a `/ig-reel` como fórmula #16.

## Cómo responder

- **Contesta la pregunta de verdad.** Si alguien pregunta cómo, dile cómo, en
  la respuesta. No lo mandes al privado para oír algo que podía tener ahí.
- **Usa su nombre una vez**, al principio, sin exclamación.
- **Iguala su longitud.** Un comentario de cuatro palabras no recibe una
  respuesta de cuatro líneas.
- **A un crítico:** primero concede lo que tiene de verdad, con sus palabras,
  y luego mantén tu postura. Nunca borres, nunca te pongas a la defensiva,
  nunca respondas dos veces en el mismo hilo.
- **A un hater:** nada. Una respuesta es alcance, y el alcance es lo que ha
  venido a buscar. Oculta el comentario si es ofensivo. Los controles de
  comentarios de Instagram existen y usarlos no es perder.
- **A un posible cliente:** responde completo en público. La puerta es una
  frase al final y es un ofrecimiento de ayuda, no una venta. La respuesta
  pública es lo que hace que la siguiente persona te escriba por privado.

## Comentarios con palabra clave

Si el post usaba una petición de palabra clave, esos comentarios son toda la
razón de ser del post. Cada uno es una persona que ha levantado la mano.
Responde a cada uno y luego envía lo prometido. Si el usuario tiene la
automatización configurada con las herramientas de Instagram o un partner
aprobado, dilo y déjala funcionar; si no, las respuestas son a mano y con este
volumen está bien. Nunca mandes mensajes masivos a gente que no comentó.

Ten en cuenta que la gente escribirá la palabra clave con y sin tilde, en
minúsculas o con faltas («contrato», «Contrato», «CONTARTO»). Cuéntalas todas
como PALABRA CLAVE.

## Salida

Un bloque, agrupado por grupo, cada respuesta lista para copiar y ya
humanizada:

```
RESPUESTAS  ·  84 comentarios  ·  41 PALABRA CLAVE, 2 CLIENTE, 3 FONDO, 2 PREGUNTA, 34 APOYO, 2 RUIDO

PALABRA CLAVE  (41)  envía la cláusula. Una línea a cada uno, mismo calor, sin copiar y pegar.

CLIENTE
@usuario - «a nosotros nos pasó esto mismo en junio»
> Lo que nos lo arregló fue quitar el pago de la aprobación del todo. Si te
> sirve, te paso el texto.

PREGUNTA -> REEL
@usuario - «¿y qué haces si se niegan a firmarla?»
  34 me gusta en este comentario. Eso es un Reel, no una respuesta. Fórmula #16.

RUIDO  (2)  ignorados. Responder les da alcance.
```

Y luego el filtro: no se publica nada hasta que el usuario diga que sí. Él
pega las respuestas.
