---
name: ig-comment
description: >-
  Escribe comentarios en posts y reels de otras personas que suenen a alguien
  con opinión, no a un bot. Úsala cuando el usuario pegue un post o un reel y
  quiera un comentario, diga «comenta esto», «interactúa con esto», «qué le
  digo aquí», o quiera un lote para su ronda diaria de interacción.
---

# ig-comment

Comentar son los veinte minutos con más efecto de Instagram y los más fáciles
de hacer mal. Un comentario arriba del todo en un reel con 40.000 visitas lo ve
más gente que la mayoría de los posts de la mayoría de las cuentas, y es el
único sitio donde un desconocido puede tocar y llegar directo a un perfil.

Un comentario genérico es peor que ninguno. Cuesta un toque que no lleva a
nada y marca la cuenta como de grupo de interacción ante la única persona cuya
opinión importaba: el creador.

**Idioma:** el comentario, en el idioma del post. Si el post está en español,
en español de España y en el registro del creador.

## Lo que necesitas

El usuario pega el texto del post o del reel, o una captura, con el nombre de
la cuenta. Si te da una URL que no puedes abrir, pídele que lo pegue. No uses
un navegador para rastrear el feed y no publiques nada.

## Los nueve tipos de comentario

Elige según lo que sea de verdad el post. Nunca uses el tipo 1 por defecto.

| # | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | **Aporta un dato** | el post afirma algo que puedes respaldar con una cifra | «A nosotros igual: el 40 % de...» |
| 2 | **El caso que falta** | el post tiene razón pero está incompleto | «Esto vale hasta que {condición}.» |
| 3 | **Discrepar con respeto** | de verdad crees que se equivoca | primero en qué estás de acuerdo, luego dónde te separas |
| 4 | **Amplía una frase** | una frase del post es la buena | cítala y construye sobre ella |
| 5 | **La pregunta de verdad** | el post se saltó la parte difícil | una pregunta, concreta |
| 6 | **El recibo** | has hecho lo que describe | qué pasó, en dos frases |
| 7 | **La corrección** | hay un error de hecho | ten razón, sé breve, sé amable, asegúrate |
| 8 | **Otra lectura** | los hechos bien, el enfoque mal | «Otra forma de verlo:» |
| 9 | **La frase corta** | el post no necesita nada y quieres estar | menos de 10 palabras, tiene que tener gracia o ser verdad |

## Reglas

- **De una a tres frases.** Los comentarios de Instagram se leen en una columna
  estrecha debajo de un vídeo. Un párrafo queda escondido detrás de «más» y
  nadie lo toca.
- **Nunca empieces con** «Qué buen post», «Me encanta», «Qué gran verdad»,
  «Esto 👏», «Lo necesitaba hoy», «Totalmente de acuerdo» ni con el nombre del
  creador seguido de exclamación. Todos son invisibles.
- **Nada de comentarios solo con emojis** y ningún emoji como primer carácter.
- **No repitas el reel.** Todos los que lo están viendo lo acaban de ver.
- **Una idea.** Un comentario con dos puntos suena a querer secuestrar el hilo.
- **Di lo concreto.** Si el comentario podría ir debajo de cualquier post del
  tema, no es un comentario, es ruido.
- **Nunca vendas.** Ni la oferta, ni el enlace, ni «pásate por mi perfil». Es la
  forma más rápida de que te bloquee justo la persona a la que querías llegar.
- **Aquí llegar pronto importa más que en ningún sitio.** Un comentario en la
  primera hora de un reel que luego viaja viaja con él.

## Salida

Da **dos opciones de tipos distintos**, con etiqueta, y una línea sobre cuál
publicarías y por qué. Pasa las dos por `/ig-human` antes: los comentarios son
cortos, así que una raya o una muletilla se nota proporcionalmente más que en un
texto largo.

```
OPCIONES DE COMENTARIO  (en el reel de @cuenta sobre precios)

[6 · Recibo]
Nosotros subimos un 40 % en marzo del año pasado y perdimos un solo cliente,
justo el que nos ocupaba media bandeja de entrada. Tardamos ocho meses en dejar
de tenerle miedo.

[3 · Discrepar con respeto]
De acuerdo con lo del ancla. Donde no lo veo es en hacerlo a mitad de proyecto.
Lo probamos así y nos costó una renovación que iba bien.

Publica el primero. Concede algo y lleva una cifra.
```

## Modo lote

Para una ronda de interacción, pide los 5 a 10 posts como texto pegado en un
solo mensaje, devuelve un comentario para cada uno en un único bloque y lleva
una nota en `~/.claude/instagram/log.md` de a quién se ha comentado esta
semana. Comentar a las mismas tres cuentas todos los días se nota y parece
exactamente lo que es.

## Nunca

No publiques automáticamente, no automatices comentarios y no uses un
navegador para publicar en nombre del usuario. La interacción automatizada
incumple las Condiciones de uso de Instagram y provoca bloqueos de acciones.
Esta skill escribe el comentario. Lo publica el usuario.
