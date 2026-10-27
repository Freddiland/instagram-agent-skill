---
name: ig-comment
description: >-
  Escribe comentarios en posts y reels de otras personas en Instagram que
  suenen a alguien con opinión, no a un bot. Úsalo cuando el usuario pegue un
  post o un reel y quiera un comentario, diga "comenta esto", "interactúa con
  esto", "qué pongo aquí", o quiera un lote para su ronda diaria de
  interacción.
---

# ig-comment

Comentar son los veinte minutos con más palanca de Instagram y los más fáciles
de hacer mal. Un comentario arriba del todo en un reel con 40.000 vistas lo ve
más gente que la mayoría de los posts de la mayoría de las cuentas, y es el
único sitio donde un desconocido puede saltar directamente a un perfil.

Un comentario genérico es peor que ninguno. Cuesta un toque que no lleva a
ninguna parte y marca la cuenta como de "grupo de interacción" ante la única
persona cuya opinión importaba, que es el creador.

## Entrada

El usuario pega el texto del post o del reel, o una captura, con el nombre de la
cuenta. Si te da una URL que no puedes abrir, pídele que lo pegue. No uses una
herramienta de navegador para rascar el feed y no publiques nada.

## Los nueve tipos de comentario

Elige según lo que sea de verdad el post. Nunca por defecto el tipo 1.

| # | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | **Aportar un dato** | el post afirma algo que puedes respaldar con una cifra | "A nosotros igual: el 40 % de..." |
| 2 | **Aportar el caso que falta** | el post tiene razón pero está incompleto | "Esto se cumple hasta que {condición}." |
| 3 | **Discrepar con respeto** | de verdad crees que se equivoca | primero en qué estás de acuerdo, luego dónde te separas |
| 4 | **Estirar una frase** | hay una frase buena | cítala y construye sobre ella |
| 5 | **Hacer la pregunta de verdad** | el post se saltó la parte difícil | una pregunta, concreta |
| 6 | **El recibo** | has hecho lo que describen | qué pasó, en dos frases |
| 7 | **La corrección** | hay un error de hecho | ten razón, sé breve, sé amable, asegúrate |
| 8 | **El reencuadre** | datos correctos, marco equivocado | "Otra forma de leerlo:" |
| 9 | **La frase corta** | el post no necesita nada y quieres estar | menos de 10 palabras, y tiene que ser graciosa o verdad |

## Reglas

- **De una a tres frases.** Los comentarios de Instagram se leen en una columna
  estrecha bajo un vídeo. Un párrafo se pliega detrás de "más" y nadie lo toca.
- **Nunca empieces con** "Qué buen post", "Me encanta", "Totalmente", "Esto 👏",
  "Lo necesitaba hoy", ni con el nombre del creador seguido de una
  exclamación. Todos son invisibles.
- **Nada de comentarios solo de emoji** ni un emoji como primer carácter.
- **Nunca repitas el reel.** Todo el que lo ve lo acaba de ver.
- **Una idea.** Un comentario con dos puntos parece un secuestro del hilo.
- **Di lo concreto.** Si el comentario serviría bajo cualquier post del tema, no
  es un comentario, es ruido.
- **Nunca vendas.** Ni la oferta, ni el enlace, ni "pásate por mi perfil". Es la
  forma más rápida de que te bloquee justo la persona a la que querías llegar.
- **Aquí llegar pronto importa más que en ningún otro sitio.** Un comentario en
  la primera hora de un reel que luego despega viaja con él.

## Salida

Da **dos opciones de tipos distintos**, etiquetadas, más una línea sobre cuál
publicarías y por qué. Pásalas antes las dos por `/ig-human`: los comentarios son
cortos, así que una raya o una frase hecha pesan proporcionalmente más que en
una descripción.

```
OPCIONES DE COMENTARIO  (en el reel de @cuenta sobre precios)

[6 · Recibo]
Subimos un 40 % en marzo del año pasado y perdimos exactamente un cliente, el
que se comía medio buzón. Tardamos ocho meses en dejar de tenerle miedo.

[3 · Discrepar con respeto]
De acuerdo con lo del anclaje. Lo que no haría es subirlo a mitad de proyecto.
Lo probamos y nos costó una renovación que por lo demás iba bien.

Publicaría el primero. Concede algo y lleva una cifra.
```

## Modo lote

Para una ronda de interacción, pide los 5 a 10 posts pegados en un solo mensaje,
devuelve un comentario por post en un único bloque y lleva una nota en
`~/.claude/instagram/log.md` de a quién se ha comentado esta semana. Comentar a
las mismas tres cuentas todos los días se nota, y parece justo lo que es.

## Nunca

No publiques automáticamente, no automatices comentarios y no uses una
herramienta de navegador para publicar en nombre del usuario. La interacción
automatizada incumple las Condiciones de uso de Instagram y hace que bloqueen
acciones de la cuenta. Esta skill escribe el comentario. El usuario lo publica.
