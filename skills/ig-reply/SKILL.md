---
name: ig-reply
description: >-
  Gestiona los comentarios bajo los reels y posts del propio usuario: redacta
  respuestas para los que merecen respuesta, ordenados por cuáles la merecen.
  Úsalo cuando el usuario pegue sus comentarios, diga "responde a estos",
  "gestiona mis comentarios", "alguien ha dicho X en mi reel", o esté lidiando
  con un crítico, un hater o un posible cliente en los comentarios.
---

# ig-reply

El hilo de comentarios bajo tu propio post es donde se decide el alcance. Cada
respuesta es otra interacción en el post, las respuestas de la primera hora
hacen casi todo el trabajo, y en Instagram una respuesta también puede ser un
Reel, que es el movimiento menos aprovechado de la plataforma.

Pero no todos los comentarios valen lo mismo, así que esta skill ordena antes de
escribir.

## Entrada

El usuario pega los comentarios, a ser posible con los @usuarios. Las capturas
valen. No rasques el hilo con una herramienta de navegador.

## Primero, clasificar

Mete cada comentario en uno de seis grupos y di los recuentos en voz alta:

| grupo | qué es | qué recibe |
| --- | --- | --- |
| **PALABRA CLAVE** | la palabra que les pediste comentar | lo prometido, enviado a mano o con tu herramienta aprobada |
| **CLIENTE POTENCIAL** | alguien que describe el problema que resuelves | una respuesta de verdad en público, y luego una puerta |
| **SUSTANCIA** | aporta datos, discrepa, amplía | la respuesta más larga del hilo |
| **PREGUNTA** | una pregunta que tiene mucha gente | se convierte en un Reel, no solo en una respuesta |
| **APOYO** | "🔥", "qué buen post", una etiqueta | un me gusta, y de 3 a 8 palabras como mucho |
| **RUIDO** | venta, spam, mala fe, provocación | nada, o una frase y fuera |

Escribe en ese orden y para cuando deje de aportar.

## El movimiento que casi todo el mundo se salta

Si una pregunta de los comentarios es una que tienen otras treinta personas,
**respóndela con un Reel**. Instagram engancha el comentario al vídeo nuevo como
sticker, a quien preguntó le llega una notificación, y una pregunta con demanda
real detrás se convierte en un post con el hook ya escrito. Señala cada PREGUNTA
que cumpla esto y pásasela a `/ig-reel` como fórmula #16.

## Cómo responder

- **Responde a la pregunta de verdad.** Si alguien pregunta cómo, dile cómo, en
  la respuesta. No le mandes al DM para oír una respuesta que podía tener ahí.
- **Usa su nombre una vez**, al principio, sin exclamación.
- **Iguala su longitud.** Un comentario de cuatro palabras no recibe una
  respuesta de cuatro líneas.
- **A un crítico:** primero concede la parte verdadera, con sus palabras, y
  luego mantén tu postura. Nunca borres, nunca te pongas a la defensiva, nunca
  respondas dos veces en el mismo hilo.
- **A un hater:** nada. Una respuesta es alcance, y el alcance es a lo que vino.
  Oculta el comentario si es ofensivo. Los controles de comentarios de
  Instagram existen y usarlos no es perder.
- **A un cliente potencial:** responde del todo en público. La puerta es una
  frase al final y es un ofrecimiento de ayuda, no una venta. La respuesta
  pública es lo que hace que la siguiente persona te escriba por DM.

## Comentarios con palabra clave

Si el post usó una petición de palabra clave, esos comentarios son la razón de
ser del post. Cada uno es alguien que ha levantado la mano. Responde a cada uno
y luego envía lo prometido. Si el usuario tiene automatización configurada con
las herramientas de Instagram o un socio aprobado, dilo y deja que funcione; si
no, las respuestas son manuales y a este volumen no pasa nada. Nunca envíes DMs
masivos a gente que no ha comentado.

## Salida

Un bloque, agrupado por grupo, con cada respuesta lista para copiar y ya
humanizada:

```
RESPUESTAS  ·  84 comentarios  ·  41 PALABRA CLAVE, 2 CLIENTE POTENCIAL, 3 SUSTANCIA, 2 PREGUNTA, 34 APOYO, 2 RUIDO

PALABRA CLAVE  (41)  envía la cláusula. Una frase cada uno, mismo cariño, sin copiar y pegar.

CLIENTE POTENCIAL
@usuario - "a nosotros nos pasó exactamente esto en junio"
> Lo que nos lo arregló fue sacar el pago de la aprobación del todo.
> Si te sirve, te paso la redacción.

PREGUNTA -> REEL
@usuario - "¿y qué haces si se niegan a firmarlo?"
  34 me gusta en este comentario. Eso es un Reel, no una respuesta. Fórmula #16.

RUIDO  (2)  ignorados. Responder les da alcance.
```

Y luego la puerta: no se publica nada hasta que el usuario diga que sí. Él pega
las respuestas.
