---
name: ig-repurpose
description: >-
  Convierte un contenido largo (un vídeo de YouTube, un pódcast, un directo,
  una newsletter, un artículo o una llamada con un cliente) en una semana de
  reels y carruseles. Úsala cuando el usuario diga «reaprovecha esto», «sácale
  reels a esto», «tengo un vídeo/pódcast/transcripción», «trocéalo», o pegue
  algo largo y lo quiera en Instagram.
---

# ig-repurpose

Un buen contenido largo tiene dentro de cuatro a seis posts. La mayoría de la
gente saca uno y tira el resto.

**Idioma:** los posts, en español de España, aunque la fuente esté en otro
idioma. Si traduces una frase citable, dilo: una cita traducida ya no es literal.

## Lo que necesitas

Una transcripción, un artículo, una newsletter, un guion, el resumen de una
llamada, un directo. Si el usuario da una URL y esta sesión tiene una
herramienta de transcripción, úsala; si no, pídele que lo pegue. Léelo entero
antes de sacar nada.

Si la fuente es un vídeo del propio usuario, pide también el archivo. Un Reel
hecho con su propio metraje gana a uno hecho con sus propias palabras leídas de
nuevo.

## Extrae, no resumas

Un resumen de un vídeo no es un Reel. Nadie quiere el resumen. Recorre el
contenido y saca lo que se sostiene solo:

| qué sacar | qué es |
| --- | --- |
| **Afirmaciones** | cada frase que empezaría una discusión |
| **Cifras** | cada número, coste, duración, porcentaje |
| **Historias** | cada momento con una persona, una escena y un coste |
| **Mecanismos** | cada «esto funciona de verdad así...» |
| **Errores** | cada reconocimiento de algo que salió mal |
| **Frases** | cada frase que ya se puede citar tal cual |

Lista lo que has encontrado, con recuentos, antes de escribir nada. Si salen
menos de cuatro elementos, el contenido es flojo, y cuatro posts exprimidos de
ahí también lo serán. Dilo.

## Luego elige el formato de cada extracto

No todo es un Reel.

- **Afirmación, error, historia**: a Reel. Necesitan una voz y una cara.
- **Mecanismo, lista numerada**: a carrusel. Hay que releerlos.
- **Una frase citable**: a una pantalla de historia, no a un post.

## Luego monta la semana

Cada extracto se convierte en un post y cada post se sostiene completamente
solo. El espectador no ha visto la fuente y no la va a ver. Nunca escribas «como
dije en mi último vídeo». El post es la cosa.

Asigna a cada uno una fórmula de hook de `ig-reel/hooks.json` y varíalas. Cinco
posts de una misma fuente con la misma forma de hook suenan a fábrica de
contenido, porque lo son.

Si la fuente es un vídeo del usuario, **usa el metraje real**. El clip en el
que dijo la cosa, con la reacción real, gana siempre a volver a grabarlo. Corta
en la frase, no en la respiración.

Ordena la semana para que la afirmación más fuerte vaya primero, la historia a
mitad de semana y el mecanismo al final, cuando quienes vieron los anteriores
lo están esperando.

## Salida

```
FUENTE: «Por qué eliminamos las llamadas de descubrimiento» (pódcast de 42 min, 8.900 palabras)

ENCONTRADO  5 afirmaciones, 9 cifras, 3 historias, 4 mecanismos, 2 errores, 7 frases citables

SEMANA
MAR  REEL      #2  Orden negativa       Deja de hacer llamadas de descubrimiento
                                        usa el clip del 14:20, se ríe al final
MIÉ  CARRUSEL  texto Trabajo B          El formulario de 4 preguntas que sustituyó a la llamada
VIE  REEL      #21 A mitad de frase     «...y nueve días después pidió que le devolviéramos el dinero»
DOM  REEL      #5  Colapso de tiempo    Seis horas a la semana recuperadas, un enlace borrado

Di «escribe el martes» y lo redacto.
```

Después, redacta bajo petición, de uno en uno, cada uno con `/ig-reel` y
`/ig-human`. No sueltes cuatro guiones terminados de golpe. Sonarán todos igual
y el usuario no grabará ninguno.
