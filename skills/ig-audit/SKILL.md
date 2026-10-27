---
name: ig-audit
description: >-
  Autopsia de lo que el usuario ya ha publicado: qué reels funcionaron de
  verdad, por qué, y qué dejar de hacer. Úsala cuando el usuario pegue sus
  estadísticas de Instagram o sus posts antiguos y pregunte «qué me está
  funcionando», «por qué ha fracasado esto», «léeme las estadísticas»,
  «audita mi contenido», o quiera saber de qué hacer más.
---

# ig-audit

La única fuente honesta de lo que funciona para una cuenta es esa cuenta. Cada
regla de cada guía de Instagram, incluidas las de este paquete, es una
suposición previa. Los últimos 30 posts del usuario son la prueba.

**Idioma:** el informe, en español de España. Si el usuario tiene Instagram en
español, sus capturas traerán las etiquetas en español (visualizaciones,
alcance, interacciones, compartidos, guardados...) y los nombres exactos
cambian con las versiones de la app; trátalas igual que sus equivalentes en
inglés y, si una no está clara, pregunta.

## Lo que necesitas

Pide lo que tenga el usuario:

- Estadísticas por post: visualizaciones, alcance, interacciones, tiempo de
  reproducción, guardados, veces compartido, seguidores ganados y el porcentaje
  de alcance que viene de quien no te sigue. Las capturas valen.
- O la gráfica de retención de sus mejores y peores reels recientes. Esa
  captura vale más que todo lo demás junto.
- O solo los posts y sus visualizaciones, que basta para una primera pasada.

Lee también `~/.claude/instagram/log.md` si existe, porque apunta qué fórmula
de hook usó cada post.

## Qué medir de verdad

Las visualizaciones a secas son el número menos útil de la pantalla, porque
dependen sobre todo de cuánta gente sigue ya la cuenta. Calcula esto en su
lugar y enseña las cuentas:

| métrica | cómo | qué te dice |
| --- | --- | --- |
| **Múltiplo sobre lo normal** | visualizaciones / la mediana de visualizaciones de la cuenta | si fue un acierto real o un día normal |
| **Alcance fuera de seguidores** | % del alcance que viene de quien no te sigue | si viajó o no |
| **Retención a los 3 s** | espectadores que siguen a los 3 s / espectadores que empezaron | si funcionó el hook. Es la nota del hook. |
| **Tiempo medio de reproducción** | directo de las estadísticas | si funcionó la parte central |
| **Envíos por alcance** | veces compartido / alcance | la señal más fuerte que puedes ganarte. Un envío es alguien poniendo su nombre detrás. |
| **Seguidores por alcance** | seguidores ganados / alcance | si el perfil convirtió la atención |

Ordena por múltiplo y por envíos por alcance, no por visualizaciones. Un reel
con 4.000 visualizaciones y 90 envíos gana al de 60.000 visualizaciones y 11.

## Luego busca el patrón

Con los cinco de arriba y los cinco de abajo uno al lado del otro, busca qué
los separa, y atrévete a concluir algo que al usuario no le va a gustar:

- **Retención a los 3 segundos.** Si arriba y abajo se diferencian aquí, es el
  hook y nada más, y todo lo demás es una distracción.
- **Fórmula de hook.** ¿Qué números de `ig-reel/hooks.json` están entre los cinco
  de arriba?
- **Formato.** Reel, carrusel, imagen única.
- **Duración.** En grupos: menos de 15 s, de 15 a 30 s, de 30 a 60 s, más de 60 s.
- **Tema.**
- **Si el usuario contestó los comentarios en la primera hora.**
- **Día y hora.** Esto **lo último**, y solo si lo demás no enseña nada. Casi
  nunca es la causa y es donde la gente quiere que esté.

Expón el hallazgo como una afirmación con la prueba al lado, y di cuánta
confianza tiene. Con 30 posts se puede ver un patrón. Con 6 no, y decirlo es
mejor que inventárselo.

## La distinción que ahorra meses

**Un reel que tiene visitas y no gana seguidores no es un reel fallido, es un
problema del perfil.** Un reel sin visitas es un problema del hook. Separa los
dos antes de recomendar nada. Si el alcance fuera de seguidores es alto y los
seguidores por alcance son bajos, deja de reescribir hooks y pasa a
`/ig-profile`.

## Salida

```
AUDITORÍA  ·  31 posts  ·  12 jun - 5 sep  ·  mediana de visualizaciones 4.100

LOS 5 DE ARRIBA POR MÚLTIPLO
  18,2x  #3  Nadie te lo cuenta  74.600 visualiz.  62 % fuera seg.  ret@3s 71 %  128 envíos
   6,4x  #1  Confesión de coste  26.300 visualiz.  48 % fuera seg.  ret@3s 64 %   71 envíos
  ...

LOS 5 DE ABAJO
   0,3x  #11 Lista con favorita   1.200 visualiz.   9 % fuera seg.  ret@3s 31 %    2 envíos
  ...

QUÉ DICEN LOS DATOS
1. La retención a los 3 segundos lo explica todo. Los cinco de arriba tienen un
   66 % de media; los de abajo, un 33 %. Todo lo demás que te preocupa depende
   de los dos primeros segundos.
2. Los posts en los que el que queda mal eres tú: media de 8,1x frente a 0,9x
   del resto. n=5. La señal más fuerte de aquí, y por mucho.
3. Las listas de herramientas tienen visitas y nada más. Mucho alcance, ni
   envíos ni seguidores. Tres de tus cinco de abajo.
4. El día de la semana no enseña nada. Tus medias del martes y del viernes
   están dentro del ruido. Deja de optimizarlo.

DEJA DE HACER: listas.
HAZ MÁS: los que llevan un coste que pagaste tú y una cifra.
```

Después pásale las conclusiones a `/ig-plan` para que la semana que viene se
construya con las pruebas del propio usuario y no con valores por defecto, y a
`/ig-viral` para que el archivo de referencias se filtre a las fórmulas que
funcionan en esta cuenta en concreto.
