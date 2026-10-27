# Instagram agent skill, en español

Trece skills de Claude para llevar una cuenta de Instagram, **adaptadas al
español de España**. Gratis, licencia MIT, sin registro, sin clave de API y sin
nada que conectar.

Es una adaptación del repositorio original de Jake Schincariol,
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill),
escrito para inglés. Aquí no solo se han traducido los textos: las herramientas
que puntúan y limpian se han reescrito para la sintaxis, la tipografía y las
muletillas del español (ver [Qué cambia respecto al original](#qué-cambia-respecto-al-original)).

Una de las skills escribe tus Reels a partir de 26 fórmulas de hook y puntúa el
hook antes de que pierdas una toma. Otra busca los reels que de verdad están
funcionando en tu nicho y los ordena por cuánto superaron a su propia cuenta.
Otra escribe el texto del post y te enseña exactamente lo que se ve en el feed
antes del «... más». Otra puntúa tu perfil sobre 100 y reescribe lo que pierde
puntos. Otra planifica la semana.

Y una es el humanizador, que es lo que hace usables las demás. Quita las rayas,
las muletillas de IA, los calcos del inglés y los caracteres invisibles de un
borrador, y puntúa lo que queda con un panel de cinco comprobaciones antes de
que lo veas.

**No se publica nada hasta que digas que sí.** Estas skills escriben. Publicas tú.

## Instalación

### En Claude Code

```bash
git clone https://github.com/Freddiland/instagram-agent-skill.git
mkdir -p ~/.claude/skills ~/.claude/instagram
cp -r instagram-agent-skill/skills/ig-* ~/.claude/skills/
cp instagram-agent-skill/templates/voice.md ~/.claude/instagram/voice.md
```

Para usarlas solo en un proyecto, copia las mismas carpetas en `.claude/skills/`
dentro del repositorio del proyecto.

Para actualizar después de un cambio en este repositorio:

```bash
cd instagram-agent-skill && git pull
cp -r skills/ig-* ~/.claude/skills/
```

### En claude.ai

Cada carpeta de `skills/` se empaqueta como un archivo `.skill` (un zip con la
carpeta dentro) y se guarda con el botón «Guardar habilidad». Guarda también
`ig-reel` aunque no lo vayas a usar directamente: `ig-audit`, `ig-plan`,
`ig-repurpose` e `ig-viral` usan sus fórmulas de hook.

En claude.ai la carpeta `~/.claude/instagram/` no se conserva entre
conversaciones, así que adjunta tu `voice.md` cuando lo necesites.

### Tu voz

Dedica diez minutos a `voice.md`. Rellénalo, o mándale a Claude tres de tus
reels y dile «escríbeme el voice.md a partir de estos». Todas las skills lo
leen. Aquí importa más que en otras redes, porque las palabras las tienes que
decir en voz alta.

## Las trece

| comando | qué hace |
| --- | --- |
| `/ig-reel` | De una idea a un Reel. Tres hooks de [26 fórmulas](skills/ig-reel/hooks.json), puntuados, y luego el guion, el texto en pantalla y una escaleta cronometrada. |
| `/ig-viral` | Busca lo que está funcionando en tu nicho, lo ordena por múltiplo sobre la mediana de cada cuenta, nombra la fórmula y escribe el archivo de referencias. |
| `/ig-caption` | El texto del post, revisado. Te enseña los 125 caracteres que se ven en el feed antes del toque. |
| `/ig-carousel` | Carruseles. La portada que se gana el deslizamiento, el texto de cada diapositiva y los archivos de 1080x1350. |
| `/ig-story` | La secuencia diaria de historias, qué sticker hace cada trabajo y el embudo a privado que empieza cuando ellos mueven primero. |
| `/ig-profile` | Puntúa tu perfil con una [rúbrica de 12 apartados](skills/ig-profile/rubric.json) sobre 100 y lo reescribe empezando por lo que más resta. |
| `/ig-plan` | La semana. Qué publicar, en qué formato, cuándo y las 10 cuentas con las que interactuar. |
| `/ig-human` | El humanizador. Dos scripts que funcionan de verdad. |
| `/ig-comment` | Comentarios en posts ajenos. Nueve tipos, elegidos según lo que es el post. Nunca «🔥🔥🔥». |
| `/ig-reply` | El hilo de tu propio post. Clasifica en palabra clave / cliente / fondo / pregunta / apoyo / ruido y escribe en ese orden. |
| `/ig-dm` | La entrega de la palabra clave, el primer mensaje, la propuesta de colaboración y los dos seguimientos. Dos. |
| `/ig-repurpose` | Un vídeo, pódcast o newsletter convertido en una semana de reels y carruseles que se sostienen solos. |
| `/ig-audit` | Autopsia de lo que ya has publicado. Ordena por múltiplo y envíos por alcance, no por visualizaciones. |

## Las herramientas que funcionan de verdad

Sin dependencias, sin red, sin subir nada. Se ejecutan en tu equipo, sobre tu
texto, con Python 3.

### Hooks

```bash
python3 hookscore.py hooks.txt              # ordena tus opciones
python3 beats.py guion.txt --target 30      # cronométralo antes de grabar
```

Salida real con cuatro hooks de prueba:

```
CLASIFICACIÓN DE HOOKS
==============================================================================
->  81.4 FUERTE  Nadie te cuenta que tus primeros 30 reels están para fracasar.
        más floja: TENSIÓN (70)
    81.4 FUERTE  Perdí 18.000 € por una cláusula que faltaba en el contrato.
        más floja: DESTINATARIO (70)
    54.4 VALE    Deja de hacer scroll si quieres crecer en Instagram en 2026 🔥
        más floja: TENSIÓN (70)
        descalifica: Empieza con «deja de hacer scroll». Pedir atención demuestra que no te la has ganado.
        descalifica: Emoji en el hook. ...
     5.4 FLOJO   Hola chicos, hoy quería hablaros de estrategia de contenidos
        más floja: ARRANQUE (0)
        descalifica: Saludo. Nadie ha venido al feed a que le saluden.
```

`beats.py` calcula cuánto se tarda en decir cada línea, las apila en códigos de
tiempo y marca las cuatro cosas que matan un Reel en la edición: un hook de más
de tres segundos, un bloque lo bastante largo como para que el espectador se
vaya, varias líneas seguidas sin nada concreto y que no haya bucle con la
primera línea. El ritmo por defecto es de 170 palabras por minuto; cronométrate
y usa `--wpm`.

### El texto del post

```bash
python3 caption.py texto.txt --keywords "contratos para autónomos,precios freelance"
```

Imprime primero la ventana visible, en un recuadro, como la lee un desconocido
haciendo scroll, y luego revisa longitud, primera línea, concreción, hashtags
(máximo cinco por publicación desde diciembre de 2025), enlaces, número de
peticiones, emojis y términos de búsqueda.

### El humanizador

```bash
python3 humanize.py borrador.txt --report      # lo limpia y enseña cada cambio
python3 detect.py borrador.txt                  # lo puntúa, cinco comprobaciones
python3 detect.py antes.txt despues.txt         # demuestra la diferencia
```

**Qué se quita solo:**

- **Caracteres invisibles.** Espacios y unidores de ancho cero, guiones blandos,
  marcas de orden de bytes, caracteres de etiqueta Unicode, espacios duros.
- **Tipografía.** Raya a coma, semirraya a guion, comillas curvas a rectas,
  el carácter único de puntos suspensivos a tres puntos. Las comillas latinas
  «» y los signos ¿ ¡ se respetan.
- **Las muletillas.** 300 palabras y frases con sustituciones en español, con
  la concordancia de género y número cuidada. Incluye el relleno típico de la IA
  en español («adentrémonos», «en el mundo actual», «juega un papel
  fundamental», «cabe destacar que»), los calcos del inglés («al final del día»,
  «mover la aguja») y un bloque de Instagram («deja de hacer scroll», «en el
  vídeo de hoy», «sígueme para más»). Vive en
  [`slop.json`](skills/ig-human/slop.json) y está para editarlo.

**Qué se marca en lugar de arreglarse:** «No es solo X, es Y», «No se trata de X,
se trata de Y», tríadas, el preámbulo de vídeo, listas con emojis, tres
palabras seguidas en mayúsculas, muros de hashtags, cebos de seguir, mayúscula
en cada palabra de un título, conectores de redacción al inicio de frase y
frases de longitud uniforme. Cambiar la forma de una frase necesita criterio.

Salida real con un texto escrito para ser lo peor posible, antes y después de
`humanize.py` (con las señales estructurales todavía sin reescribir):

```
  NOTA HUMANA   #######.................  30.1   SOSPECHOSO
  30.1 SOSPECHOSO  ->  57.5 REVISAR   (+27.4)
```

El resto hasta PASA lo pone la reescritura a mano de las señales marcadas.

### El archivo de referencias

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

Las visitas a secas no son una prueba. Una cuenta de 2.000.000 de seguidores con
400.000 visitas ha tenido un martes flojo. Una de 4.000 seguidores con 400.000
visitas ha dado con algo. `swipe.py` ordena por el múltiplo sobre la mediana de
cada cuenta, nombra la fórmula del hook (ignorando tildes) e imprime lo que
separa el tercio de arriba del de abajo. Acepta cabeceras en español
(`cuenta`, `seguidores`, `mediana`, `visitas`, `hook`) o en inglés.

## Qué cambia respecto al original

| pieza | en inglés | en esta versión |
| --- | --- | --- |
| `slop.json` | 154 términos en inglés | 300 términos en español con sus formas de género y número, calcos del inglés y bloque de Instagram; 18 señales estructurales (2 nuevas, propias del español) |
| `humanize.py` / `detect.py` | palabras ASCII, contracciones | letras con tilde y ñ, búsqueda sin tildes, punto de los miles, ¿ ¡ « », la VOZ se mide con registro coloquial, 1.ª/2.ª persona y adverbios en -mente |
| `hooks.json` | 26 fórmulas y patrones en inglés | 26 fórmulas reescritas en español con sus patrones; cada ejemplo se clasifica como su propia fórmula |
| `hookscore.py` | listas en inglés, 5-12 palabras | listas en español (cifras con letra, €, tú/vosotros), 5-14 palabras porque el español necesita algo más de palabras |
| `beats.py` | 165 ppm | 170 ppm por defecto, palabras vacías en español, cifras con letra, días y meses como datos concretos |
| `caption.py` | peticiones en inglés | peticiones en español («Comenta CONTRATO», «escríbeme por privado»...), hashtags con tildes, dominios .es/.cat/.eu |
| `swipe.py` | cabeceras en inglés | cabeceras en español o inglés, clasificación sin tildes |
| subtítulos de `ig-viral` | `en.*` | `es.*` |

## La letra pequeña, que es la parte honesta

**Esta adaptación no se ha validado con un corpus en español.** El original
probó `hookscore.py` con 74 hooks reales de vídeos cortos en inglés: separaba
bien un hook real de uno escrito para ser malo (AUC 0,83) y casi nada los
aciertos de un buen creador de sus fallos (AUC 0,56, donde 0,50 es lanzar una
moneda). Esta versión traduce y ajusta las listas y los umbrales, pero no
repite esa medición. Úsala para descartar hooks claramente flojos, no para
elegir entre dos decentes. Los umbrales de `detect.py` también vienen del
inglés: un texto humano puede salir en REVISAR.

**Estas skills no publican en Instagram.** Existe una API oficial de
publicación para cuentas profesionales, y necesita una app de desarrollador de
Meta, una página vinculada, un token de larga duración y una revisión de la
app, que no es algo que una skill te pueda dar. Casi todo lo demás que se usa
para automatizar publicaciones, comentarios, seguimientos o mensajes es
automatización del navegador o una herramienta de terceros, y ambas incumplen
las [Condiciones de uso de Instagram](https://help.instagram.com/581066165581870)
y provocan bloqueos. Así que todas las skills terminan igual: un bloque listo
para copiar, y lo publicas tú.

La excepción son las respuestas automáticas por palabra clave en mensajes
privados, que Instagram permite con sus propias herramientas y partners
aprobados, y que solo saltan después de que alguien comente primero. `/ig-dm`
dice dónde está esa línea.

**`/ig-viral` lee, no rastrea.** Diez cuentas, una docena de reels por cuenta, a
velocidad humana, con tu navegador. Nunca te pide la contraseña ni inicia
sesión por ti.

**Las cinco comprobaciones de detección son heurísticas locales, no API de
detectores.** No son GPTZero, Originality, Copyleaks, Winston ni Turnitin, no
llaman a esos servicios y no pueden prometer sus veredictos. Nadie puede
venderte «indetectable» con honestidad.

**Nada se inventa.** Ni métricas, ni clientes, ni resultados a tu nombre. Si un
borrador necesita una cifra que no has dado, vuelve con `{{tu cifra}}` dentro.

**Las cifras de la plataforma caducan.** El límite de hashtags pasó de 30 a 5 en
diciembre de 2025. Si algo de aquí contradice lo que hace Instagram cuando lo
leas, Instagram tiene razón.

## Archivos

```
skills/ig-reel/hooks.json          26 fórmulas de hook: plantilla, ejemplo, versión en pantalla,
                                   para qué sirve, cómo se estropea y un patrón de detección
skills/ig-reel/hookscore.py        el panel de cinco propiedades del hook
skills/ig-reel/beats.py            del guion a una escaleta cronometrada
skills/ig-caption/caption.py       la vista previa del corte y la revisión del texto
skills/ig-human/slop.json          el diccionario: 300 términos, 18 clases invisibles, 18 señales
skills/ig-human/humanize.py        las tres pasadas de limpieza
skills/ig-human/detect.py          el panel de cinco comprobaciones
skills/ig-viral/swipe.py           orden por múltiplo y clasificación de fórmulas
skills/ig-profile/rubric.json      la nota del perfil sobre 100
templates/voice.md                 tu perfil de voz. Rellénalo primero.
```

## Créditos

Original de Jake Schincariol, [opusjake.ai](https://opusjake.ai):
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill).
Adaptación al español: [Freddiland](https://github.com/Freddiland).

## Licencia

MIT, igual que el original. Ver [LICENSE](LICENSE).
