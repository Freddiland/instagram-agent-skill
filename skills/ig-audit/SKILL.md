---
name: ig-audit
description: >-
  Autopsia de lo que el usuario ya ha publicado: qué reels funcionaron de
  verdad, por qué y qué dejar de hacer. Úsalo cuando el usuario pegue sus
  estadísticas de Instagram o sus posts anteriores y pregunte "qué está
  funcionando", "por qué ha flopado esto", "lee mis estadísticas", "audita mi
  contenido", o quiera saber de qué hacer más.
---

# ig-audit

La única fuente honesta de lo que funciona en una cuenta es esa cuenta. Cada
regla de cada guía de Instagram, incluidas las de este pack, es un punto de
partida. Los últimos 30 posts del usuario son la prueba.

## Entrada

Pide lo que tenga el usuario:

- Estadísticas por post: visualizaciones, alcance, interacciones, tiempo de
  reproducción, guardados, compartidos, seguidores ganados y el porcentaje del
  alcance que viene de no seguidores. Las capturas valen.
- O la gráfica de retención de sus mejores y peores reels recientes. Esta
  captura vale más que todo lo demás junto.
- O solo los posts y sus visualizaciones, que basta para una primera pasada.

Lee también `~/.claude/instagram/log.md` si existe, porque registra qué fórmula
de hook usó cada post.

## Qué medir de verdad

Las visualizaciones en bruto son la cifra menos útil de la pantalla, porque
dependen sobre todo de cuánta gente sigue ya la cuenta. Calcula esto en su lugar
y enseña las cuentas:

| métrica | cómo | qué te dice |
| --- | --- | --- |
| **Múltiplo** | vistas / mediana de vistas de la propia cuenta | si fue un éxito real o un día normal |
| **Alcance a no seguidores** | % del alcance que viene de gente que no sigue | si ha viajado algo |
| **Retención a 3 s** | espectadores que siguen a los 3 s / los que empezaron | si el hook funcionó. Es la nota del hook. |
| **Tiempo medio de reproducción** | directo de las estadísticas | si funcionó la mitad |
| **Envíos por alcance** | compartidos / alcance | la señal más fuerte que te puedes ganar. Un envío es alguien poniendo su nombre detrás. |
| **Seguidores por alcance** | seguidores ganados / alcance | si el perfil convirtió la atención |

Ordena por múltiplo y por envíos por alcance, no por vistas. Un reel con 4.000
vistas y 90 envíos le ganó al de 60.000 vistas y 11.

## Después, busca el patrón

Con los cinco mejores y los cinco peores uno al lado del otro, busca qué los
separa, y atrévete a concluir algo que al usuario no le va a gustar:

- **Retención a 3 segundos.** Si los mejores y los peores se diferencian aquí,
  es el hook y nada más, y todo lo que viene después es una distracción.
- **Fórmula de hook.** ¿Qué ids de `ig-reel/hooks.json` están en los cinco
  mejores?
- **Formato.** Reel, carrusel, imagen suelta.
- **Duración.** Agrupa en menos de 15 s, de 15 a 30 s, de 30 a 60 s y más de
  60 s.
- **Tema.**
- **Si el usuario respondió a los comentarios en la primera hora.**
- **Día y hora.** Compruébalo **lo último** y solo si lo demás no enseña nada.
  Casi nunca es la causa y es donde la gente quiere que esté.

Plantea el hallazgo como una afirmación con la prueba al lado, y di cuánta
confianza tiene. Con 30 posts se ve un patrón. Con 6 no, y decirlo es mejor que
inventárselo.

## La distinción que ahorra meses

**Un reel que tiene vistas y no gana seguidores no es un reel fallido, es un
problema del perfil.** Un reel que no tiene vistas es un problema del hook.
Separa las dos cosas antes de recomendar nada. Si el alcance a no seguidores es
alto y los seguidores por alcance son bajos, deja de reescribir hooks y ve a
`/ig-profile`.

## Salida

```
AUDITORÍA  ·  31 posts  ·  12 jun - 5 sep  ·  mediana de vistas 4.100

5 MEJORES POR MÚLTIPLO
  18.2x  #3  Nadie te lo cuenta   74.600 vistas  62 % no seguidores  ret@3s 71 %  128 envíos
   6.4x  #1  Confesión de coste   26.300 vistas  48 % no seguidores  ret@3s 64 %   71 envíos
  ...

5 PEORES
   0.3x  #11 Lista con favorito    1.200 vistas   9 % no seguidores  ret@3s 31 %    2 envíos
  ...

QUÉ DICEN LOS DATOS
1. La retención a 3 segundos lo explica todo. Los cinco mejores tienen un 66 % de
   media, los cinco peores un 33 %. Todo lo demás que te preocupa depende de los
   dos primeros segundos.
2. Los posts en los que el que quedaba mal eras tú: media de 8,1x frente a 0,9x
   para todo lo demás. n=5. Es la señal más fuerte y no hay color.
3. Las listas de herramientas tienen vistas y nada más. Mucho alcance, ni envíos
   ni seguidores. Tres de tus cinco peores.
4. El día de la semana no enseña nada. Tus medias del martes y del viernes están
   dentro del ruido. Deja de optimizarlo.

DEJA DE HACER: listas.
HAZ MÁS: los que tienen un coste que pagaste y una cifra.
```

Después pásale las conclusiones a `/ig-plan` para que la semana siguiente se
construya con las pruebas del propio usuario y no con valores por defecto, y a
`/ig-viral` para que el swipe file se filtre por las fórmulas que funcionan en
esta cuenta en concreto.
