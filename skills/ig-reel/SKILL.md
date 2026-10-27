---
name: ig-reel
description: >-
  Escribe un Reel de Instagram a partir de una idea en bruto: opciones de hook
  sacadas de 26 fórmulas, el guion hablado, el texto en pantalla y una escaleta
  cronometrada, con la voz del usuario y puntuado antes de grabar. Úsalo cuando
  el usuario quiera un Reel, un guion de vídeo corto, un hook, una locución,
  "hazme un reel sobre X", "qué digo en este vídeo", "escríbeme el guion", o
  esté a punto de grabar y todavía no tenga la primera frase.
---

# ig-reel

Convierte una idea en bruto en un Reel que alguien vea hasta el final.

En esta carpeta hay dos herramientas y las dos se ejecutan de verdad. Úsalas.
No juzgues el hook a ojo y no adivines la duración.

```bash
python3 hookscore.py hooks.txt              # ordena tus opciones de hook
python3 hookscore.py --hook "una frase"     # puntúa uno solo
python3 beats.py guion.txt --target 30      # escaleta cronometrada antes de grabar
```

Las dos funcionan en español y en inglés, y las tildes no afectan.

## Antes de escribir

1. Lee `~/.claude/instagram/voice.md` si existe. Es el perfil de voz del
   usuario: cómo habla a cámara, qué no dice nunca y a quién le habla. Si no
   existe, pídele **tres de sus propios reels**, transcríbelos o léelos, deduce
   la voz y escribe el archivo. Un guion con la voz equivocada no sirve, porque
   lo tiene que decir en voz alta.
2. Lee `hooks.json` en esta carpeta. 26 fórmulas, cada una con plantilla,
   ejemplo relleno, versión en pantalla, para qué sirve y cómo se estropea.
   Cuatro están ahí porque aparecían una y otra vez en hooks reales, no para
   completar un patrón. Las cifras de los ejemplos son ilustrativas.
3. Si la idea es floja, no la rellenes. Haz una sola pregunta agrupada: qué
   pasó, a quién, y qué costó o qué devolvió. Un Reel necesita una cosa
   concreta y verdadera. Consíguela antes de escribir.
4. Si existe `~/.claude/instagram/swipe.md`, léelo. Lo escribe `/ig-viral`, y
   son las pruebas del propio usuario sobre qué fórmulas funcionan ahora mismo
   en su nicho. Tienen prioridad sobre lo que dice este archivo.

## La estructura

Un Reel se decide en los dos primeros segundos y se retiene en los cinco
siguientes.

```
0:00 - 0:02   HOOK        la afirmación. Frase hablada y frase en pantalla, escritas
                          por separado. Movimiento en el primer fotograma, no una
                          cara estática.
0:02 - 0:07   LO EN JUEGO por qué le importa a quien lo está viendo. Una frase.
0:07 - ...    EL CUERPO   una idea por beat, y el plano cambia en cada beat.
ÚLTIMOS 3 s   LA RECOMPENSA cumple lo que prometió el hook, y luego la única petición.
ÚLTIMA FRASE  EL BUCLE    repite una palabra del hook para que la repetición encaje.
```

Duración: de 15 a 45 segundos es el rango que funciona. Los Reels pueden durar
hasta 3 minutos y casi nadie debería usarlos. Por debajo de 7 segundos se
inflan las repeticiones y nada más.

## El proceso

**1. Elige tres hooks, no uno.** Pasa la idea por `hooks.json`, elige tres
fórmulas que de verdad encajen y escribe para cada una la frase hablada y la de
pantalla. Fórmulas distintas, no tres versiones de la misma.

**2. Puntúalos.** Pon las tres frases habladas en un archivo, una por línea, y
ejecuta `hookscore.py`. Enséñale el ranking al usuario. Si el primero está por
debajo de 50, todavía no tienes el hook y ninguna edición lo arregla.

**3. Escribe el guion** sobre el hook ganador. Lenguaje hablado y llano, como
habla de verdad el usuario. Frases cortas. Ninguna frase que tenga que ensayar.
Tutea al espectador salvo que su `voice.md` diga lo contrario.

**4. Cronométralo.** Ejecuta `beats.py guion.txt --target {duración}`. Arregla
todos los avisos: un hook que pasa de 3 segundos, cualquier beat de más de 4
segundos, una racha de beats sin nada concreto, la falta de bucle. Repite hasta
que salga limpio. Si el usuario se ha cronometrado, usa su ritmo con `--wpm`:
en español las palabras son más largas que en inglés y el valor por defecto
(165) es solo un punto de partida.

**5. Humanízalo.** Pasa el guion por `/ig-human` antes de enseñarlo. Una frase
que suena a escrita se nota en cuanto alguien la dice en voz alta.

**6. Imprime el bloque.** El guion en un bloque de código, el texto en pantalla
como lista aparte con sus tiempos, y después:

```
REEL LISTO
hook:        #3 Nadie te lo cuenta, nota 86 FUERTE
duración:    28,4 s en 9 beats a 165 ppm
en pantalla: 6 rótulos
humanizador: 4 restos eliminados, nota humana 81 APTO
descripción: ejecuta /ig-caption después

Responde "sí" para guardarlo en el registro, o dime qué cambio.
```

**7. Nunca publiques.** Esta skill produce un guion. El usuario lo graba y lo
publica. Con un "sí", añade a `~/.claude/instagram/log.md` la fecha, la fórmula
de hook usada y la primera frase, para que `/ig-audit` tenga historial después.

## El texto en pantalla es otro guion

Escríbelo aparte, siempre. Se lee antes de oírse.

- **Seis palabras o menos por rótulo.** Lo lee, con el móvil a un brazo de
  distancia, alguien que todavía no está escuchando.
- **El rótulo del hook aparece en el fotograma 1**, no tras un silencio.
- **Mantenlo dentro de la zona segura.** En un fotograma de 1080x1920, nada por
  encima de y=230 ni por debajo de y=1440, y deja libres los 230 píxeles de la
  derecha. Fuera de esa caja la interfaz lo tapa todo: la descripción, la barra
  de acciones y la tira del audio.
- **Nunca pongas el hook donde va la descripción.** Es la parte de abajo del
  fotograma y queda tapada.
- **Subtitula el cuerpo.** Casi todo el mundo lo ve primero sin sonido.

## Reglas que marcan la diferencia

- **Una idea por Reel.** Si el guion tiene dos, tienes dos Reels. Dilo.
- **Cifras mejor que adjetivos.** "4.200 €" gana a "un montón". Si el usuario
  no ha dado una cifra, pídela en vez de escribir alrededor del hueco.
- **Fuera la intro.** Ni saludo, ni "en este vídeo", ni nombre, ni cortinilla
  con el logo. El vídeo empieza en la frase a la que normalmente llegarías en
  el segundo seis.
- **Cambia el plano en cada beat.** Un plano fijo durante 8 segundos es donde
  la gente se va, y `beats.py` lo marcará.
- **Una petición al final.** Comentar una palabra clave, guardarlo o seguir.
  Una.
- **Nunca inventes.** Ni métricas, ni clientes, ni facturación, ni resultados
  inventados a nombre del usuario, ni siquiera de relleno. Si hace falta una
  cifra que no sabes, deja `{{tu cifra}}` en el guion y señálalo.
- **No escribas un guion alrededor de un audio en tendencia que el usuario no
  puede usar.** Si la idea necesita su propia voz, dilo.

## Ejemplo

```
/ig-reel hemos pasado de 5 horas a 20 minutos por presupuesto con una plantilla
```

```
HOOKS  (puntuados)
  79  FUERTE  #5  Colapso de tiempo   "Antes tardaba cinco horas en un presupuesto. Ahora, veinte minutos."
                                      en pantalla: 5 HORAS -> 20 MIN
  79  FUERTE  #1  Confesión de coste  "Cobré cuatro horas a la semana por maquetar. Durante dos años."
                                      en pantalla: 2 AÑOS PERDIDOS
  37  DÉBIL   #9  Róbalo              "Róbame la plantilla de presupuesto que lo hizo."
                                      en pantalla: RÓBAME ESTO
              más débil: CONCRECIÓN. Ni una cifra; sin el "5 horas -> 20 min" no hay nada que robar.

Empate entre #5 y #1. Grabaría el #5: la proporción es creíble, se lee de un
vistazo en pantalla y la cifra es tuya. El script no desempata; eso lo decides tú.
```
