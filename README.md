# La skill de agente para Instagram (en español)

Trece skills de Claude que llevan una cuenta de Instagram. Gratis, MIT, sin
registro, sin API key, sin nada que conectar.

> Adaptación al español de
> [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill),
> de Jake Schincariol. Las instrucciones, los ejemplos y toda la salida de las
> herramientas están en español de España. Las herramientas Python son
> bilingües: detectan si el texto está en español o en inglés y aplican las
> reglas de ese idioma.

Una de ellas te escribe los Reels a partir de 26 fórmulas de hook y puntúa el
hook antes de que malgastes una toma. Otra va y busca los reels que de verdad
están funcionando en tu nicho y los ordena por cuánto superó cada uno a su
propia cuenta. Otra escribe la descripción y te enseña exactamente lo que
muestra el feed antes del "... más". Otra puntúa tu perfil sobre 100 y
reescribe lo que pierde puntos. Otra planifica la semana.

Y una es el humanizador, que es la razón de que el resto sea usable. Quita las
rayas, el vocabulario de relleno y los caracteres invisibles de marca de agua de
un borrador, y luego puntúa lo que queda con un panel de cinco comprobaciones
antes de que lo veas.

**No se publica nada hasta que tú digas que sí.** Estas skills escriben. Tú
publicas.

## Instalación

Pega esto en Claude:

```
https://github.com/Freddiland/instagram-agent-skill

Instala esta skill y luego comprueba que /ig-reel funciona.
```

O hazlo tú, en Claude Code:

```bash
git clone https://github.com/Freddiland/instagram-agent-skill.git
cp -r instagram-agent-skill/skills/ig-* ~/.claude/skills/
```

O como plugin:

```
/plugin marketplace add Freddiland/instagram-agent-skill
/plugin install instagram-agent-es
```

Para un proyecto concreto en vez de global: copia esas mismas carpetas en el
`.claude/skills/` de tu repo. ¿Sin Claude Code? Pega cualquier `SKILL.md` al
principio de un chat y funciona como un modo. Pierdes las cinco herramientas de
Python, que son casi todo el sentido de `/ig-reel` y `/ig-human`, pero el resto
funciona.

Después dedica diez minutos a `templates/voice.md`. Cópialo en
`~/.claude/instagram/voice.md` y rellénalo, o mándale a Claude tres de tus
propios reels y dile "escríbeme el voice.md a partir de estos". Todas las skills
leen ese archivo. Aquí importa más que en otras plataformas, porque las palabras
las tienes que decir en voz alta.

## Las trece

| comando | qué hace |
| --- | --- |
| `/ig-reel` | Una idea convertida en Reel. Tres hooks de [26 fórmulas](skills/ig-reel/hooks.json), puntuados, y luego el guion, el texto en pantalla y una escaleta cronometrada. |
| `/ig-viral` | Busca qué está funcionando en tu nicho, lo ordena por múltiplo sobre la mediana de cada cuenta, nombra la fórmula y escribe el swipe file. |
| `/ig-caption` | La descripción, revisada. Te enseña los 125 caracteres que muestra el feed antes del toque. |
| `/ig-carousel` | Posts para deslizar. La portada que se gana el deslizamiento, el texto de cada diapositiva y los archivos de 1080x1350. |
| `/ig-story` | La secuencia diaria de historias, qué sticker hace qué trabajo y el embudo de DMs que empieza cuando ellos se mueven primero. |
| `/ig-profile` | Puntúa tu perfil con una [rúbrica de 12 apartados](skills/ig-profile/rubric.json) sobre 100 y reescribe por orden de prioridad. |
| `/ig-plan` | La semana. Qué publicar, en qué formato, cuándo, y las 10 cuentas con las que interactuar. |
| `/ig-human` | El humanizador. Dos scripts que se ejecutan de verdad. Más abajo. |
| `/ig-comment` | Comentarios en posts de otros. Nueve tipos, elegidos según lo que sea de verdad el post. Nunca "🔥🔥🔥". |
| `/ig-reply` | El hilo bajo tu propio post. Clasifica en palabra clave / cliente potencial / sustancia / pregunta / apoyo / ruido, y escribe en ese orden. |
| `/ig-dm` | La entrega por palabra clave, el primer mensaje, la propuesta de colaboración y los dos seguimientos. Dos. |
| `/ig-repurpose` | Un vídeo, pódcast o newsletter convertido en una semana de reels y carruseles que se sostienen solos. |
| `/ig-audit` | Autopsia de lo que ya has publicado. Ordena por múltiplo y por envíos por alcance, no por vistas. |

## Las cinco herramientas que se ejecutan de verdad

Sin dependencias, sin red, sin subir nada. Se ejecutan en tu máquina, sobre tu
texto. Funcionan en español y en inglés, y las tildes no les afectan.

### Hooks

```bash
python3 hookscore.py hooks.txt              # ordena tus opciones
python3 beats.py guion.txt --target 30      # cronométralo antes de grabarlo
```

```
RANKING DE HOOKS
==============================================================================
->  85.6 FUERTE  Nadie te cuenta que tus primeros 30 reels están para fracasar.
        más débil: CONCRECIÓN (75)
    81.4 FUERTE  Perdí 18.000 € por un contrato que no firmé.
        más débil: DESTINATARIO (70)
    53.0 OK      Deja de hacer scroll si quieres crecer en Instagram en 2026 🔥
        más débil: TENSIÓN (70)
        descalificante: Empieza con "deja de hacer scroll". Pedir atención
                        demuestra que no te la has ganado.
     5.4 DÉBIL   Hola chicos, hoy quería hablaros de estrategia de contenido
        más débil: ARRANQUE (0)
        descalificante: Saludo. Nadie ha entrado al feed para que le saluden.
```

El español omite el pronombre ("Perdí" ya es primera persona, "¿Cobras por
horas?" ya le habla al espectador), así que el script también lee la persona en
el verbo, no solo en "yo" y "tú".

`beats.py` estima cuánto se tarda en decir cada línea, las apila en códigos de
tiempo y marca las cuatro cosas que matan un Reel en la edición: un hook que
pasa de tres segundos, un beat tan largo que da tiempo a irse, una racha de
líneas sin nada concreto y que no haya un bucle de vuelta a la primera frase.

```
ESCALETA  ·  72 palabras  ·  ~26.2 s a 165 ppm  ·  objetivo 30 s
========================================================================
  0:00.0   4.0s  HOOK    Perdí 18.000 € por una cláusula que faltaba en un contrato.
                         ^ el hook dura 4.0 s, pasa de los 3 s
  0:04.0  11.6s  MITAD   Esta es la cláusula exacta que ahora pongo en todos y...
                         ^ 11.6 s en un solo beat
  0:15.6   3.6s          Apartado 4. Pago a la entrega, no a la aprobación.
  0:19.3   3.6s          La aprobación es una sensación. La entrega es una fecha.
  0:22.9   3.3s  CTA     Ese cambio de una palabra me vale 18.000 €.
------------------------------------------------------------------------
  - El beat 1 tarda 4.0 s en decirse. Déjalo en 8 palabras o menos, o el
    hook llega cuando la decisión ya está tomada.
  - Beat(s) 2 pasan de 4 s. Parte la línea o cambia lo que se ve en pantalla
    dentro de ella. Un plano estático es donde la gente se va.
  - Bucle: el último beat repite "18.000" del hook. Las segundas
    reproducciones son alcance gratis.
  - 3.8 s por debajo del objetivo. Añade 10 palabras o grábalo corto. Corto
    suele ser lo correcto.
```

El ritmo por defecto es de 165 palabras por minuto. En español las palabras son
más largas de media que en inglés, así que cronométrate leyendo un guion en voz
alta y usa tu cifra con `--wpm`.

### La descripción

```bash
python3 caption.py descripcion.txt --keywords "contratos con clientes,precios freelance"
```

Instagram le da a la descripción unos 125 caracteres en el feed y esconde el
resto detrás de un toque. Casi todas las descripciones que fallan, fallan ahí.
Así que lo primero que imprime es esa ventana, en una caja, tal como la lee un
desconocido haciendo scroll:

```
  LO QUE ENSEÑA EL FEED
  +------------------------------------------------------+
  | Perdí 18.000 € por una cláusula que faltaba en un    |
  | contrato, y lo peor es que me lo había leído dos     |
  | veces antes de firmarlo.                             |
  +--------------------------------------------- ... más +

  OK    LONGITUD        422 / 2200 caracteres
  OK    PRIMERA LÍNEA   123 caracteres, se ve entera
  OK    HOOK CONCRETO   1 cifra(s) o nombre(s) en la ventana visible
  OK    HASHTAGS        3 hashtag(s): #freelance #contratos #autonomos
  OK    UNA PETICIÓN    una llamada a la acción: comentar una palabra clave
  AVISO BÚSQUEDA        1/2 presentes. Faltan: precios freelance
```

Aplica el tope actual de hashtags, que es de **cinco por publicación**, no
treinta. Instagram lo cambió el 18 de diciembre de 2025. Reconoce las peticiones
en español ("comenta CONTRATO", "guárdalo", "link en la bio", "escríbeme por
DM") y marca como genéricos `#parati`, `#explorar` y compañía.

### El humanizador

```bash
python3 humanize.py borrador.txt --report      # lo limpia y enseña cada cambio
python3 detect.py borrador.txt                  # lo puntúa, cinco comprobaciones
python3 detect.py antes.txt despues.txt         # demuestra la diferencia
```

**Lo que se quita solo:**

- **Caracteres invisibles.** Espacios y uniones de ancho cero, word joiners,
  guiones blandos, marcas de orden de bytes, caracteres de etiqueta Unicode,
  separadores invisibles, espacios de no separación y estrechos. Tu teclado no
  los produce. Sobreviven al copiar y pegar y no se ven en ningún editor.
- **Tipografía.** Raya a coma, guion medio a guion, comillas curvas y angulares
  a rectas, puntos suspensivos de un carácter a tres puntos, y la puntuación
  huérfana que queda. Los signos `¿` y `¡` no se tocan.
- **El léxico.** 220 palabras y frases de relleno en español (y las 154
  originales en inglés), con sustituciones llanas que respetan género y número.
  El último bloque es específico de Instagram: "deja de hacer scroll", "en el
  vídeo de hoy", "sígueme para más", "etiqueta a alguien que lo necesite", "al
  algoritmo le encanta", "corre, no camines". Está en
  [`slop.json`](skills/ig-human/slop.json) y está pensado para editarlo.

**Lo que se señala en vez de arreglarse:** "no es solo X, es Y", "no se trata de
X, se trata de Y", tríadas de tres, el preámbulo de vídeo, listas con emoji como
viñetas, tres palabras gritadas seguidas, muros de hashtags, cebos reflejos para
seguir, longitud de frase uniforme. Cambiar la forma de una frase necesita
criterio, así que vuelven para reescribirse en vez de destrozarse con una regex.

Con una descripción escrita para ser lo peor posible:

```
  RITMO         ############............  51.3
  CONCRECIÓN    ##......................   9.8    1 dato concreto por 100 palabras
  RELLENO       ........................   0.0    20 términos de relleno, 20.8 por 100 palabras
  HUELLA        ........................   0.0    1 invisible, 1 raya, 2 comillas
  VOZ           ######..................  26.2    11 señales estructurales
  ------------------------------------------------------------
  NOTA HUMANA   ###.....................  10.5   MARCADO
```

Después de `humanize.py`, con las estructuras señaladas todavía sin reescribir:

```
  NOTA HUMANA   ###########.............  44.3   MARCADO   (+33.8)
```

La segunda mitad del salto la da reescribir a mano lo que el script ha señalado.

En inglés la VOZ se mide con contracciones ("don't", "I'm"); en español, que no
las tiene, con marcadores coloquiales ("vale", "pues", "o sea", "en plan"). Ese
umbral en español es una estimación, no una calibración.

### El swipe file

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

Las visualizaciones en bruto no son una prueba. Una cuenta de 2.000.000 de
seguidores con 400.000 vistas ha tenido un martes flojo. Una cuenta de 4.000
seguidores con 400.000 vistas ha dado con algo. `swipe.py` ordena por múltiplo
sobre la mediana de la propia cuenta, nombra la fórmula del hook e imprime qué
separa el tercio superior del inferior. Acepta cabeceras en español (`cuenta`,
`seguidores`, `mediana`, `vistas`, `hook`).

```
SWIPE FILE  ·  4 reels  ·  4 cuentas  ·  referencia: mediana de la cuenta
==============================================================================
    60.0x  hook  80  #9  Róbalo                 @c                 180.000
           "Róbame este seguimiento de cuatro líneas, me costó dos años"
    37.5x  hook  86  #3  Nadie te lo cuenta     @a                 412.000
           "Nadie te cuenta que tus primeros 30 reels están para fracasar"
     1.3x  hook  13  -   sin clasificar         @b               1.200.000
           "En este vídeo te voy a enseñar mi rutina de mañana"
```

## Lo que se midió de verdad, que es la parte que merece la pena leer

El autor original no quiso publicar un puntuador de hooks con el argumento de
que "parece que funciona", así que lo probó. El corpus son **74 hooks reales de
vídeo corto**: los tres primeros segundos de los subtítulos automáticos de los
ocho mejores y los ocho peores shorts de cinco canales, con visualizaciones de
931 a 550.000.

Son YouTube Shorts y no Reels, porque Instagram no da cifras de visualización
que se puedan recoger sin iniciar sesión en la cuenta de otra persona, y hacer
scraping incumpliría las Condiciones que este repo te dice que no incumplas. La
gramática del hook es la misma y las fuentes son públicas. Es una limitación
real y se dice aquí en vez de esconderla.

**Una limitación más, de esta adaptación:** ese corpus estaba **en inglés**. Las
listas de palabras y las regex en español se han escrito a mano y se han
probado con ejemplos, no con un corpus de hooks reales en español. La lógica de
puntuación es la misma, pero las cifras de abajo no están medidas en español.

**Tres resultados, dos de ellos incómodos:**

**1. Detecta bien los hooks malos.** Con diez hooks escritos mal a propósito,
AUC 0,83, y nueve de los diez quedaron por debajo de la mediana del corpus real.
Si tu hook empieza con un saludo, un preámbulo o nada concreto, esto te lo dice.

**2. No elige ganadores.** Para separar los éxitos de un buen creador de los
fracasos de ese mismo creador: **AUC 0,56, donde 0,50 es tirar una moneda.** De
las cinco comprobaciones, solo la CONCRECIÓN separó los grupos de forma
apreciable, por 60 puntos de mediana. TENSIÓN y DESTINATARIO tuvieron la misma
mediana en los dos grupos, o sea, que en este corpus no medían nada.

Así que el uso honesto es: mata los hooks claramente flojos antes de grabarlos y
luego fíate de tu propia gráfica de retención. Nada que lea texto puede decirte
cuál de dos hooks decentes va a viajar, porque eso lo deciden tu cara, tu
edición, tu audio y a quién se lo enseña Instagram.

**3. El clasificador de fórmulas estaba roto y fue la prueba la que lo pilló.**
Las regex `match` de `hooks.json` se escribieron a partir de las propias
plantillas, y nombraban solo el **8 %** de los hooks reales. La gente no habla
en plantillas. Reescribirlas contra habla transcrita de verdad lo subió al
**49 %**, y entraron cinco fórmulas porque aparecían una y otra vez y no estaban:
Giro a la contra, La estadística, La revelación, El resultado de otro y El
superlativo. En el otro 51 % no se pronuncia, que es lo correcto: mucho vídeo
corto son clips de pódcast que no tienen ninguna fórmula de hook.

Un fallo corregido que merece la pena nombrar: la CONCRECIÓN solo contaba
dígitos, así que "cero euros" y "tres libros de marketing" puntuaban como si no
tuvieran nada concreto. Los hooks hablados dicen los números en voz alta. En
esta adaptación eso también vale para los números dichos en español.

Si vuelves a ejecutar esto con un corpus más grande o más limpio, y sobre todo
con uno en español, y sale otra cosa, mejor saberlo. El script de medición no
está en el repo porque depende de `yt-dlp`, pero el método son cuatro líneas y
está explicado en [`/ig-viral`](skills/ig-viral/SKILL.md).

## La letra pequeña, que es la parte honesta

**Estas skills no publican en Instagram.** Existe una API real de publicación
de contenido para cuentas profesionales, y necesita una app de desarrollador de
Meta, una página vinculada, un token de larga duración y una revisión de la app,
que no es algo que una skill te pueda dar. Todo lo demás que usa la gente para
automatizar publicaciones, comentarios, follows o DMs es automatización del
navegador o una herramienta de terceros, y las dos incumplen las [Condiciones de
uso de Instagram](https://help.instagram.com/581066165581870) y hacen que
bloqueen acciones de las cuentas. Así que todas las skills de aquí acaban igual:
un bloque listo para copiar, y tú lo publicas. No es una limitación añadida
después, es el diseño, y por eso la puerta de aprobación es real y no un ajuste.

La única excepción son las respuestas automáticas por palabra clave en DMs, que
Instagram admite con sus propias herramientas y socios aprobados, y que solo se
disparan después de que alguien comente primero. `/ig-dm` dice dónde está esa
línea.

**`/ig-viral` lee, no hace scraping.** Diez cuentas, una docena de reels cada
una, a velocidad humana, con tu propio navegador manejado por ti. Nunca te pide
la contraseña y nunca inicia sesión como tú. La recogida automatizada a gran
escala es lo que hace que restrinjan las cuentas, y esto no es un rastreador.

**Las cinco comprobaciones de detección son heurísticas locales, no APIs de
detectores.** Están basadas en las señales en las que se fijan los detectores
públicos y se ejecutan enteras en tu máquina. No son GPTZero, Originality,
Copyleaks, Winston ni Turnitin, no llaman a esos servicios y no pueden prometer
esos veredictos. Arreglar lo que miden suele mover esos números, porque miden
las mismas cosas de fondo. Esa es toda la afirmación. Nadie puede venderte con
honestidad algo "indetectable", y quien lo hace te está vendiendo otra cosa.

**La pasada de caracteres invisibles es real y es acotada.** Quita los
caracteres de ancho cero y de formato que acaban en el texto generado y
sobreviven a un copiar y pegar. Es una huella real y comprobable. No es una
afirmación sobre burlar un sistema de marca de agua criptográfica, y este repo
no la hace.

**Aquí no se inventa nada.** Ninguna métrica, cliente o resultado inventado va
con tu nombre. Si un borrador necesita una cifra que no has dado, vuelve con
`{{tu cifra}}` y un aviso, siempre. Las cifras de los ejemplos de las fórmulas
son ilustrativas.

**Las cifras de la plataforma caducan.** El tope de hashtags pasó de 30 a 5 en
diciembre de 2025 mientras se escribía el repo original, y el revisor tuvo el
número antiguo hasta que se comprobó. Si algo de aquí contradice lo que hace
Instagram cuando lo leas, tiene razón Instagram.

## Archivos

```
skills/ig-reel/hooks.json          26 fórmulas de hook: plantilla, ejemplo, frase en pantalla,
                                   para qué sirve, cómo se estropea y una regex (español e inglés)
skills/ig-reel/hookscore.py        el panel de cinco propiedades del hook
skills/ig-reel/beats.py            del guion a una escaleta cronometrada
skills/ig-caption/caption.py       la vista previa del corte y el revisor de descripciones
skills/ig-human/slop.json          el léxico: 220 términos en español, 154 en inglés,
                                   18 clases invisibles, 27 señales estructurales
skills/ig-human/humanize.py        las tres pasadas de limpieza
skills/ig-human/detect.py          el panel de cinco comprobaciones
skills/ig-viral/swipe.py           ranking por múltiplo y clasificación de fórmulas
skills/ig-profile/rubric.json      la nota del perfil sobre 100
templates/voice.md                 tu perfil de voz. Rellénalo primero.
```

## Créditos

Original de Jake Schincariol, [opusjake.ai](https://opusjake.ai):
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill).
Repo hermano, misma idea para otra plataforma:
[linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill).

Adaptación al español: [Freddiland](https://github.com/Freddiland).

## Licencia

MIT. Cógelo, cámbialo, publícalo. La licencia original se mantiene en
[`LICENSE`](LICENSE).
