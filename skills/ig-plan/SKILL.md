---
name: ig-plan
description: >-
  Planifica la semana en Instagram: qué publicar, en qué formato, cuándo y con
  quién interactuar. Úsala cuando el usuario diga «planifica mi semana», «qué
  publico», «calendario de contenidos», «no tengo nada que publicar», o quiera
  un calendario de publicación y una lista de cuentas con las que
  interactuar.
---

# ig-plan

La sala de control. Todo lo demás del paquete ejecuta; esta decide qué se
ejecuta. Úsala una vez a la semana, siempre el mismo día.

**Idioma:** el plan, en español de España.

## Lo que necesitas

Si existen `~/.claude/instagram/voice.md`, `swipe.md` y `log.md`, léelos. El
archivo de referencias son las pruebas del propio usuario, sacadas con
`/ig-viral`, sobre qué fórmulas funcionan ahora en su nicho, y manda más que
cualquier cosa de este archivo. El registro evita que el plan repita un tema de
las dos últimas semanas.

Si no existen, pide cuatro cosas y apúntalas:

1. Qué vende el usuario y a quién.
2. Los tres o cuatro temas por los que quiere que lo conozcan.
3. Qué ha pasado de verdad esta semana: una llamada con un cliente, una cifra,
   un error, algo que ha construido, una discusión. De ahí salen los posts.
4. Diez cuentas ante las que merece la pena dejarse ver.

## Qué publicar

Cuatro o cinco publicaciones a la semana, y al menos tres de ellas Reels. Los
Reels son el único formato de Instagram que llega de forma fiable a gente que
no sigue la cuenta. Los carruseles profundizan con quien ya la sigue. Las
historias son diarias y se planifican aparte.

Mezcla a lo largo de la semana, nunca dos del mismo tipo seguidos:

| tipo | cuántos | trabajo |
| --- | --- | --- |
| **Prueba** | 1 a la semana | algo que ha pasado, con una cifra. Reel. |
| **Enseñar** | 1 o 2 a la semana | una cosa que el espectador puede hacer hoy. Reel o carrusel. |
| **Opinión** | 1 a la semana | una postura que te podría costar seguidores. Reel. |
| **Historia** | 1 cada dos semanas | una escena con un coste. Reel. |
| **Oferta** | 1 cada dos semanas | lo que vendes, dicho claro, sin pedir perdón. Carrusel o historias. |

Para cada hueco da: el tema, el enfoque concreto a partir de lo que ha pasado
esta semana, el formato y el número de fórmula de hook de `ig-reel/hooks.json`.
No un tema: un enfoque. «IA» no es un plan. «El presupuesto que perdimos porque
el borrador tenía una raya de ChatGPT» es un Reel.

## Cuándo publicar

Publica cuando su público está despierto y no está trabajando. En España, para
la mayoría del público de consumo eso es a última hora de la tarde o por la
noche, más tarde que en otros países por los horarios españoles; para un
público profesional, a primera hora de la mañana o a mediodía. Es una
orientación, no un dato: la pestaña de estadísticas del propio usuario, que
dice cuándo está conectado su público, manda.

Pero dilo claro: **la hora importa mucho menos que los dos primeros
segundos.** Instagram sigue enseñando un Reel durante días si funciona, y
entierra uno publicado a la hora perfecta si no funciona. Si el usuario está
optimizando la hora de publicación antes de que le funcionen los hooks, está
puliendo lo que no es, y se lo tienes que decir.

Usa la zona horaria del público, no la del usuario, si no coinciden (por
ejemplo, si su público está en Latinoamérica o en Canarias).

## La ronda de interacción, que no es opcional

20 minutos al día, antes de publicar, no después. Haz una lista de 10:

- **5 de alcance**: cuentas con un público que el usuario quiere, donde un buen
  comentario se ve. Comenta pronto, antes de que el hilo tenga 200 comentarios.
- **3 iguales**: mismo tamaño, mismo campo. Es el grupo que devuelve el gesto.
- **2 compradores**: gente que de verdad podría comprar. Comenta durante semanas
  antes de cualquier mensaje privado, y nunca vendas en un comentario.

Pásale la lista a `/ig-comment`.

## Salida

```
SEMANA DEL 15 DE SEPTIEMBRE

LUN  solo interacción  (20 min, lista abajo)
MAR  20:30  REEL      PRUEBA   #5  Colapso de tiempo  - presupuesto de 5 h a 20 min
MIÉ  solo historias + interacción
JUE  21:00  CARRUSEL  ENSEÑAR  texto Trabajo B        - la cláusula en 4 diapositivas
VIE  20:30  REEL      OPINIÓN  #2  Orden negativa     - deja de hacer llamadas de descubrimiento
SÁB  -
DOM  21:30  REEL      HISTORIA #21 A mitad de frase   - el correo pidiendo la devolución

HISTORIAS  todos los días, de 3 a 5 pantallas, caja de preguntas el jueves.

INTERACCIÓN  (5 alcance / 3 iguales / 2 compradores)
  ...

Di «escribe el martes» y lo redacto.
```

Escribe el plan en `~/.claude/instagram/plan.md` para que lo puedan leer las
demás skills. No se programa ni se publica nada en ningún sitio. Es un plan, y
lo ejecuta el usuario.
