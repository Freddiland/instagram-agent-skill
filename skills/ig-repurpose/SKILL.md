---
name: ig-repurpose
description: >-
  Convierte un contenido largo (un vídeo de YouTube, un pódcast, un directo,
  una newsletter, un artículo del blog o una llamada con un cliente) en una
  semana de reels y carruseles. Úsalo cuando el usuario diga "reaprovecha
  esto", "sácame reels de aquí", "tengo un vídeo/pódcast/transcripción",
  "trocea esto", o pegue algo largo y lo quiera en Instagram.
---

# ig-repurpose

Un buen contenido largo tiene dentro de cuatro a seis posts. La mayoría de la
gente saca uno y tira el resto.

## Entrada

Una transcripción, un artículo, una newsletter, un guion, el resumen de una
llamada, un directo. Si el usuario da una URL y esta sesión tiene una
herramienta de transcripción, úsala; si no, pídele que lo pegue. Lee el
contenido entero antes de extraer nada.

Si la fuente es un vídeo del propio usuario, pídele también el archivo. Un Reel
hecho con su propia grabación gana a uno hecho con sus propias palabras leídas
otra vez.

## Extrae, no resumas

El resumen de un vídeo no es un Reel. Nadie quiere el resumen. Recorre el
contenido y saca lo que se sostiene solo:

| qué sacar | qué es |
| --- | --- |
| **Afirmaciones** | cada frase que empezaría una discusión |
| **Cifras** | cada número, coste, duración, porcentaje |
| **Historias** | cada momento con una persona, una escena y un coste |
| **Mecanismos** | cada "la forma en que esto funciona de verdad es..." |
| **Errores** | cada reconocimiento de algo que salió mal |
| **Frases** | cada frase que ya se puede citar tal cual |

Enumera lo que has encontrado, con recuentos, antes de escribir nada. Si el
contenido da menos de cuatro elementos, es flojo, y cuatro posts exprimidos de
ahí también lo serán. Dilo.

## Después, elige el formato de cada extracto

No todo es un Reel.

- **Afirmación, error, historia** a Reel. Necesitan una voz y una cara.
- **Mecanismo, lista numerada** a carrusel. Hay que releerlos.
- **Una frase citable** a una pantalla de historia, no a un post.

## Después, monta la semana

Cada extracto se convierte en un post y cada post se sostiene completamente
solo. El espectador no ha visto la fuente y no la verá nunca. Nunca escribas
"como dije en mi último vídeo". El post es la cosa.

Asigna a cada uno una fórmula de hook de `ig-reel/hooks.json` y varíalas. Cinco
posts de una misma fuente con la misma forma de hook parecen una fábrica de
contenido, porque lo son.

Si la fuente es un vídeo del propio usuario, **usa la grabación real**. El clip
en el que dijo la cosa, con la reacción de verdad, gana siempre a volver a
grabarlo. Corta en la frase, no en la respiración.

Ordena la semana para que la afirmación más fuerte vaya primero, la historia
caiga a mitad de semana y el mecanismo vaya al final, cuando la gente a la que
le gustaron los anteriores esté esperándolo.

## Salida

```
FUENTE: "Por qué eliminamos las llamadas de descubrimiento" (pódcast de 42 min, 8.900 palabras)

ENCONTRADO  5 afirmaciones, 9 cifras, 3 historias, 4 mecanismos, 2 errores, 7 frases citables

SEMANA
MAR  REEL      #2  Orden negativa       Deja de hacer llamadas de descubrimiento
                                        usa el clip del 14:20, se ríe al final
MIÉ  CARRUSEL  descripción Trabajo B    El formulario de 4 preguntas que sustituyó a la llamada
VIE  REEL      #21 Media frase          "...y nueve días después pidió que le devolviéramos el dinero"
DOM  REEL      #5  Colapso de tiempo    Seis horas a la semana recuperadas, un enlace borrado

Dime "escribe el martes" y te lo redacto.
```

Luego redacta cuando te lo pidan, de uno en uno, cada uno pasado por `/ig-reel` y
`/ig-human`. No sueltes cuatro guiones terminados de golpe. Sonarán todos igual
y el usuario no grabará ninguno.
