---
name: ig-profile
description: >-
  Puntúa un perfil de Instagram sobre 100 con una rúbrica de 12 apartados y
  reescribe lo que pierde puntos: nombre, bio, enlace, destacadas, las tres
  fijadas y la cuadrícula. Úsala cuando el usuario diga «optimiza mi perfil»,
  «arregla mi bio», «puntúa mi Instagram», «por qué no me sigue la gente», o
  pegue su perfil y pregunte cómo se lee.
---

# ig-profile

Casi todo el mundo optimiza aquí lo que no es. El perfil no es un escaparate
por el que la gente pasea. Es una **pantalla de decisión** a la que se llega
desde un reel, y tiene unos tres segundos para contestar una pregunta: ¿hay
más de eso aquí, y es para mí?

**Idioma:** la puntuación y las reescrituras, en español de España. Las
destacadas y la bio, en el idioma en que busca su público.

## Lo que necesitas

Pide al usuario que pegue o haga captura de: el campo de nombre, el @, la bio,
a dónde lleva el enlace, los nombres de las destacadas, lo que está fijado y
las nueve primeras portadas de la cuadrícula. Para una primera pasada basta una
captura de la parte de arriba del perfil más las dos primeras filas de la
cuadrícula.

No inicies sesión en Instagram en su nombre.

## Puntúalo

Lee `rubric.json` en esta carpeta. Doce apartados, 100 puntos, cada uno con cómo
es la nota máxima y cómo suele fallar. Puntúa todos, enseña la tabla y da el
total. Sé honesto. La mayoría de los perfiles sacan entre 30 y 49 en la primera
pasada, y una nota generosa no sirve para nada.

```
NOTA DEL PERFIL  38/100

  campo de nombre      2/12   solo el nombre, ninguna palabra que nadie busque
  primera línea bio    3/12   tres sustantivos y un emoji de café
  tres fijadas         0/10   nada fijado
  destacadas           2/8    «Random», «Vida», «2023»
  cuadrícula legible   4/8    seis de nueve portadas son una cara a mitad de frase
  ...
```

## Luego reescribe, en este orden

Arregla de mayor a menor según los puntos perdidos. No lo reescribas todo de
golpe: el usuario tiene que ir cambiando de verdad cada cosa.

**1. El campo de nombre (30 caracteres).** La línea en negrita debajo de la
foto, no el @. Es el campo que compara el buscador de Instagram, y la mayoría
de las cuentas ponen ahí un nombre y nada más. El formato que funciona:
`{Nombre} | {lo que haces, con las palabras que se buscan}`. Da tres opciones.
En español los términos de búsqueda suelen ser más largos, así que cuenta los
caracteres: 30 es el máximo.

**2. La primera línea de la bio.** Para quién es y qué cambia. No un cargo, no
adjetivos, no una lista de identidades separadas por barras. El resto de los
150 caracteres lleva una prueba o una oferta clara.

**3. Las tres fijadas.** Tres huecos, tres trabajos distintos: la mejor prueba,
la explicación más clara de la oferta y la mejor presentación de la persona. Es
el arreglo con más efecto de todo el perfil y son cuatro toques. Una
cuadrícula sin fijadas enseña lo último que se publicó, que es lanzar una
moneda.

**4. Destacadas.** De cuatro a seis, con el nombre de las preguntas que hace un
comprador: Precios, Resultados, Cómo funciona, Sobre mí. No «Random». Borra el
resto.

**5. El enlace.** Un solo destino que cuadre con lo que acaba de prometer la
bio. Se permiten cinco; dos ya es un menú, y un menú convierte peor que una
puerta.

**6. Las portadas de la cuadrícula.** Las nueve primeras, a tamaño miniatura.
Las portadas de los reels se eligen, no se dejan en el primer fotograma. Cuatro
palabras de texto en una portada hacen que la cuadrícula se entienda de un
vistazo.

## Salida

Tabla de puntuación y luego las reescrituras como bloques listos para copiar,
en orden de arreglo, cada uno pasado por `/ig-human`. Vuelve a puntuar al final
y enseña la diferencia con honestidad. Si la reescritura llega a 84 y no a 98,
di 84, y di qué falta, que suele ser una cuadrícula, el hábito de subir
historias y una publicación fijada que todavía no existe. Nada de eso es una
reescritura.

Esta skill no guarda nada en Instagram. El usuario edita cada campo.
