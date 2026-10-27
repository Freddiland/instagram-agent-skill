---
name: ig-profile
description: >-
  Puntúa un perfil de Instagram sobre 100 con una rúbrica de 12 apartados y
  reescribe lo que pierde puntos: campo del nombre, bio, enlace, destacadas,
  los tres fijados y la cuadrícula. Úsalo cuando el usuario diga "optimiza mi
  perfil", "arregla mi bio", "puntúa mi Instagram", "por qué no me sigue la
  gente", o pegue su perfil y pregunte cómo se ve.
---

# ig-profile

Casi todo el mundo optimiza aquí lo que no es. El perfil no es un escaparate
por el que se pasea la gente. Es una **pantalla de decisión** a la que se llega
desde un reel, y tiene unos tres segundos para responder una pregunta: ¿hay más
de esto aquí, y es para mí?

## Entrada

Pídele al usuario que pegue o haga captura de: el campo del nombre, el
@usuario, la bio, a dónde lleva el enlace, los nombres de las destacadas, lo que
hay fijado y las nueve primeras portadas de la cuadrícula. Una captura de la
parte de arriba del perfil más las dos primeras filas de la cuadrícula basta
para una primera pasada.

No inicies sesión en Instagram en su nombre.

## Puntuarlo

Lee `rubric.json` en esta carpeta. Doce apartados, 100 puntos, cada uno con cómo
es la nota máxima y cómo suele fallar. Puntúa todos, enseña la tabla y da el
total. Sé honesto. La mayoría de los perfiles sacan entre 30 y 49 en la primera
pasada, y una nota generosa no sirve para nada.

```
NOTA DEL PERFIL  38/100

  campo del nombre     2/12   solo el nombre, ninguna palabra que alguien busque
  primera línea bio    3/12   tres sustantivos y un emoji de café
  tres fijados         0/10   nada fijado
  destacadas           2/8    "Random", "Vida", "2023"
  cuadrícula legible   4/8    seis de nueve portadas son una cara a media frase
  ...
```

## Después, reescribir en este orden

Arregla de más a menos puntos perdidos. No lo reescribas todo de golpe: el
usuario tiene que ir a cambiar cada cosa él mismo.

**1. El campo del nombre (30 caracteres).** La línea en negrita bajo la foto,
no el @usuario. Es el campo contra el que busca Instagram, y la mayoría de las
cuentas ponen ahí el nombre y nada más. Formato que funciona:
`{Nombre} | {a qué te dedicas, con palabras que se buscan}`. Da tres opciones.

**2. La primera línea de la bio.** Para quién es y qué cambia. Ni un cargo, ni
adjetivos, ni una lista de identidades separadas por barras. El resto de los 150
caracteres lleva una prueba o una oferta clara.

**3. Los tres fijados.** Tres huecos, tres trabajos distintos: la mejor prueba,
la explicación más clara de la oferta, la mejor presentación de la persona. Es
el arreglo con más palanca de todo el perfil y son cuatro toques. Una
cuadrícula sin fijados enseña lo último que se publicó, que es tirar una moneda.

**4. Destacadas.** De cuatro a seis, con el nombre de las preguntas que hace un
comprador: Precios, Resultados, Cómo funciona, Sobre mí. Nada de "Random". Borra
el resto.

**5. El enlace.** Un destino que encaje con lo que acaba de prometer la bio. Se
permiten cinco; dos ya es un menú, y un menú convierte peor que una puerta.

**6. Las portadas de la cuadrícula.** Las nueve primeras a tamaño miniatura. Las
portadas de los reels se eligen, no se dejan en el primer fotograma que salió.
Cuatro palabras de texto en una portada hacen que la cuadrícula se lea de un
vistazo.

## Salida

La tabla de puntos y después las reescrituras como bloques listos para copiar,
en orden de prioridad, cada una pasada por `/ig-human`. Vuelve a puntuar al
final y enseña la diferencia con honestidad. Si la reescritura llega a 84 y no
a 98, di 84, y di qué necesita el resto, que suele ser una cuadrícula, la
costumbre de subir historias y un post fijado que todavía no existe. Nada de eso
es una reescritura.

Esta skill no guarda nada en Instagram. El usuario edita cada campo.
