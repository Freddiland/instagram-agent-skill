---
name: ig-plan
description: >-
  Planifica la semana en Instagram: qué publicar, en qué formato, cuándo y con
  quién interactuar. Úsalo cuando el usuario diga "planifica mi semana", "qué
  publico", "calendario de contenidos", "no tengo nada que publicar", o quiera
  un calendario de publicación y una lista de cuentas con las que interactuar.
---

# ig-plan

La sala de control. Todo lo demás del pack ejecuta; esto decide qué se ejecuta.
Úsalo una vez a la semana, siempre el mismo día.

## Entrada

Si existen `~/.claude/instagram/voice.md`, `swipe.md` y `log.md`, léelos. El
swipe file son las pruebas del propio usuario, sacadas con `/ig-viral`, sobre
qué fórmulas están funcionando ahora en su nicho, y pesa más que cualquier cosa
de este archivo. El registro evita que el plan repita un tema de las dos
últimas semanas.

Si no existen, pide cuatro cosas y apúntalas:

1. Qué vende el usuario, y a quién.
2. Los tres o cuatro temas por los que quiere que se le conozca.
3. Qué ha pasado de verdad esta semana: una llamada con un cliente, una cifra,
   un error, algo que ha construido, una discusión. De ahí salen los posts.
4. Diez cuentas ante las que merece la pena dejarse ver.

## Qué publicar

De cuatro a cinco posts a la semana, y al menos tres de ellos Reels. Los Reels
son el único formato de Instagram que llega de forma fiable a gente que no sigue
la cuenta. Los carruseles profundizan con la gente que ya la sigue. Las
historias son diarias y se planifican aparte.

Mézclalos a lo largo de la semana, nunca dos del mismo tipo seguidos:

| tipo | cuántos | trabajo |
| --- | --- | --- |
| **Prueba** | 1 a la semana | algo que ha pasado, con una cifra. Reel. |
| **Enseñar** | 1 o 2 a la semana | una cosa que el espectador puede hacer hoy. Reel o carrusel. |
| **Opinión** | 1 a la semana | una postura que podría costarte seguidores. Reel. |
| **Historia** | 1 cada dos semanas | una escena con un coste. Reel. |
| **Oferta** | 1 cada dos semanas | lo que vendes, dicho claro, sin pedir perdón. Carrusel o historias. |

Para cada hueco da: el tema, el ángulo concreto a partir de lo que ha pasado de
verdad esta semana, el formato y el número de fórmula de hook de
`ig-reel/hooks.json`. No un tema, un ángulo. "IA" no es un plan. "El
presupuesto que perdimos porque el borrador tenía una raya" es un Reel.

## Cuándo publicar

Publica cuando la audiencia del usuario está despierta y no está trabajando.
Para la mayoría de las audiencias de consumo eso es a última hora de la tarde,
hora local; para una audiencia profesional, a primera hora de la mañana. En
España, ten en cuenta que los horarios van más tarde que en otros países: la
"última hora de la tarde" aquí suele ser después de las 20:00.

Pero dilo claro: **la hora importa muchísimo menos que los dos primeros
segundos.** Instagram seguirá enseñando un Reel durante días si funciona, y
enterrará uno bien programado que no funcione. Si el usuario está optimizando la
hora de publicación antes de que sus hooks funcionen, está puliendo lo que no
es, y tienes que decírselo.

Ancla las horas a la zona horaria de la audiencia, no a la del usuario, si no
coinciden.

## La ronda de interacción, que no es opcional

20 minutos al día, antes de publicar, no después. Haz una lista de 10:

- **5 de alcance**: cuentas con una audiencia que el usuario quiere, donde un
  buen comentario se ve. Comenta pronto, antes de que el hilo tenga 200.
- **3 iguales**: mismo tamaño, mismo campo. Es el grupo que devuelve.
- **2 compradores**: gente que podría comprar de verdad. Comenta durante semanas
  antes de cualquier DM, y nunca vendas en un comentario.

Pásale la lista a `/ig-comment`.

## Salida

```
SEMANA DEL 15 DE SEPTIEMBRE

LUN  solo interacción  (20 min, lista abajo)
MAR  20:30  REEL      PRUEBA    #5  Colapso de tiempo  - de 5 h a 20 min por presupuesto
MIÉ  solo historias + interacción
JUE  20:00  CARRUSEL  ENSEÑAR   descripción Trabajo B  - la cláusula desglosada en 4 diapositivas
VIE  20:30  REEL      OPINIÓN   #2  Orden negativa     - deja de hacer llamadas de descubrimiento
SÁB  -
DOM  19:00  REEL      HISTORIA  #21 Media frase        - el email del reembolso

HISTORIAS  todos los días, de 3 a 5 pantallas, caja de preguntas el jueves.

INTERACCIÓN  (5 alcance / 3 iguales / 2 compradores)
  ...

Dime "escribe el martes" y te lo redacto.
```

Escribe el plan en `~/.claude/instagram/plan.md` para que las otras skills puedan
leerlo. No se programa ni se publica nada en ningún sitio. Es un plan y lo
ejecuta el usuario.
