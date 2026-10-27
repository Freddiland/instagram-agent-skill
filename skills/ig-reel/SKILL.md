---
name: ig-reel
description: >-
  Escribe un Reel de Instagram a partir de una idea en bruto: opciones de hook
  con 26 fórmulas, el guion hablado, el texto en pantalla y una escaleta
  cronometrada, con la voz del usuario y puntuado antes de grabar. Úsala
  siempre que el usuario quiera un Reel, un guion de vídeo corto, un hook, una
  voz en off, «hazme un reel sobre X», «qué digo en este vídeo», o vaya a
  grabar y todavía no tenga la primera frase.
---

# ig-reel

Convierte una idea en bruto en un Reel que alguien ve hasta el final.

En esta carpeta hay dos herramientas y las dos funcionan de verdad. Úsalas. No
juzgues el hook a ojo ni adivines la duración.

```bash
python3 hookscore.py hooks.txt              # ordena tus opciones de hook
python3 hookscore.py --hook "una frase"     # puntúa una sola
python3 beats.py guion.txt --target 30      # escaleta cronometrada antes de grabar
```

**Idioma:** guion, texto en pantalla y todo lo que entregues, en español de
España, salvo que el usuario pida otro. Tú o vosotros, no usted, salvo que su
público lo pida. Nada de calcos del inglés.

## Antes de escribir

1. Lee `~/.claude/instagram/voice.md` si existe. Es el perfil de voz del
   usuario: cómo habla delante de la cámara, qué no diría nunca, a quién le
   habla. Si no existe, pide **tres de sus propios reels**, transcríbelos o
   léelos, deduce la voz y escribe el archivo. Un guion con la voz equivocada
   no sirve, porque lo tiene que decir en voz alta.
2. Lee `hooks.json` en esta carpeta. 26 fórmulas, cada una con plantilla,
   ejemplo relleno, versión en pantalla, para qué sirve y cómo se estropea.
3. Si la idea es floja, no la rellenes. Haz una sola pregunta agrupada: qué
   pasó, a quién, y qué costó o qué aportó. Un Reel necesita una cosa concreta
   y verdadera. Consíguela antes de escribir.
4. Si existe `~/.claude/instagram/swipe.md`, léelo. Lo escribe `/ig-viral` y es
   la prueba del propio usuario sobre qué fórmulas funcionan ahora en su nicho.
   Manda más que lo que pone en este archivo.

## La estructura

Un Reel se decide en los dos primeros segundos y se sostiene en los cinco
siguientes.

```
0:00 - 0:02   HOOK        la afirmación. Frase hablada y frase en pantalla, escritas
                          por separado. Movimiento en el primer fotograma, no una cara quieta.
0:02 - 0:07   LO EN JUEGO por qué le importa a quien lo ve. Una línea.
0:07 - ...    EL CUERPO   una idea por bloque, y el plano cambia en cada bloque.
ÚLTIMOS 3 s   EL PREMIO   cumple lo que prometió el hook y luego la única petición.
ÚLTIMA LÍNEA  EL BUCLE    repite una palabra del hook para que la repetición enlace limpia.
```

Duración: de 15 a 45 segundos es el rango que funciona. Los Reels llegan a 3
minutos y casi nadie debería usarlos. Por debajo de 7 segundos se inflan las
repeticiones y nada más.

## El proceso

**1. Elige tres hooks, no uno.** Pasa la idea por `hooks.json`, elige tres
fórmulas que de verdad le encajen y escribe la frase hablada y la de pantalla
de cada una. Fórmulas distintas, no tres versiones de la misma.

**2. Puntúalos.** Pon las tres frases habladas en un archivo, una por línea, y
pasa `hookscore.py`. Enséñale la clasificación al usuario. Si el primero está
por debajo de 50, todavía no tienes el hook, y ninguna edición lo arregla.

**3. Escribe el guion** con el hook ganador. Lenguaje hablado y sencillo, como
habla de verdad el usuario. Frases cortas. Ninguna frase que tenga que ensayar.

**4. Cronométralo.** Pasa `beats.py guion.txt --target {duración}`. Arregla
cada aviso: un hook de más de 3 segundos, cualquier bloque de más de 4, varios
bloques seguidos sin nada concreto, o que no haya bucle. Repite hasta que salga
limpio. Si el usuario se ha cronometrado, usa su ritmo con `--wpm` (está en
`voice.md`); el valor por defecto, 170 palabras por minuto, es una estimación.

**5. Humanízalo.** Pasa el guion por `/ig-human` antes de enseñarlo. Una frase
que suena escrita se nota en cuanto alguien la dice en voz alta.

**6. Entrega el bloque.** El guion en un bloque de código, el texto en
pantalla aparte como lista con tiempos, y después:

```
REEL LISTO
hook:          #3 Nadie te lo cuenta, nota 81 FUERTE
duración:      28,4 s en 9 bloques a 170 ppm
en pantalla:   6 tarjetas
humanizador:   4 huellas quitadas, nota humana 81 PASA
texto:         pasa /ig-caption a continuación

Responde «sí» para registrarlo, o dime qué cambio.
```

**7. Nunca publiques.** Esta skill produce un guion. El usuario lo graba y lo
publica. Con un «sí», añade a `~/.claude/instagram/log.md` la fecha, la
fórmula de hook usada y la primera frase, para que `/ig-audit` tenga historial
después.

## El texto en pantalla es otro guion

Escríbelo aparte, siempre. Se lee antes de oírse.

- **Seis palabras o menos por tarjeta.** Lo lee, con el brazo estirado, alguien
  que todavía no está escuchando.
- **La tarjeta del hook está en el fotograma 1**, no después de un silencio.
- **Mantenlo dentro de la zona segura.** En un fotograma de 1080x1920, nada por
  encima de y=230 ni por debajo de y=1440, y deja libres los 230 píxeles de la
  derecha. La interfaz tapa todo lo que queda fuera: el texto, la columna de
  botones, la franja del audio.
- **Nunca pongas el hook donde va el texto del post.** Es la parte de abajo del
  fotograma y queda tapada.
- **Subtítulos incrustados en el cuerpo.** La mayoría de la gente ve primero
  sin sonido.

## Reglas que marcan la diferencia

- **Una idea por Reel.** Si el guion tiene dos, tienes dos Reels. Dilo.
- **Cifras antes que adjetivos.** «4.200 €» gana a «un montón». Si el usuario no
  te ha dado una cifra, pídesela en vez de escribir alrededor del hueco.
- **Fuera la intro.** Ni saludo, ni «en este vídeo», ni nombre, ni cortinilla
  con el logo. El vídeo empieza en la frase a la que llegarías en el segundo
  seis.
- **Cambia el plano en cada bloque.** Un plano fijo de 8 segundos es donde la
  gente se va, y `beats.py` lo marcará.
- **Una sola petición al final.** Comentar una palabra clave, guardarlo o
  seguir. Una.
- **Nunca te inventes nada.** Ni métricas, ni clientes, ni facturación, ni
  resultados a nombre del usuario, ni siquiera como relleno. Si hace falta una
  cifra y no la tienes, deja `{{tu cifra}}` en el guion y avísalo.
- **No escribas un guion alrededor de un audio de tendencia que el usuario no
  pueda usar.** Si la idea necesita su propia voz, dilo.

## Ejemplo

```
/ig-reel hemos pasado de 5 horas a 20 minutos por presupuesto con una plantilla
```

```
HOOKS  (puntuados)
  81  FUERTE  #5  Colapso de tiempo   «Antes tardaba cinco horas en un presupuesto. Ahora, veinte minutos.»
                                      en pantalla: 5 HORAS -> 20 MIN
  70  FUERTE  #1  Confesión de coste  «Facturaba cuatro horas a la semana solo en maquetar. Durante dos años.»
                                      en pantalla: 2 AÑOS PERDIDOS
  52  VALE    #9  El robo             «Roba la plantilla de presupuesto que lo consiguió.»
                                      en pantalla: ROBA ESTO

Grabamos el #5: la proporción es creíble, se entiende de un vistazo en
pantalla y la cifra es tuya.
```
