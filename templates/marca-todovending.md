# marca.md · TodoVending

Copia este archivo en `~/.claude/instagram/marca.md` (y el logo de
`templates/assets/` en `~/.claude/instagram/`). Lo leen las skills que generan
piezas visuales: `ig-carousel`, `ig-reel` (tarjetas y texto en pantalla) e
`ig-story`.

**Regla:** toda pieza visual usa SIEMPRE estos colores, esta tipografía y este
@. No se inventa paleta. Si una pieza necesita algo que no está aquí, se
pregunta antes.

## Identidad

- **Medio:** TodoVending, todovending.com
- **Cuenta de Instagram:** @todo_vending
- **Pie de fuente en piezas:** «Noticia completa en todovending.com»

## Colores

| Uso | Hex | Nota |
|---|---|---|
| Acento principal | `#cc2b41` | Rojo corporativo. Cifras grandes, palabras clave, viñetas, barra de progreso, fondo de la diapositiva final (CTA). |
| Texto | `#1b1b1d` | Titulares y negritas. |
| Texto secundario | `#3a3a3a` | Cuerpo de texto. |
| Gris | `#6e6b66` | Fuentes, numeración, @. |
| Fondo | `#f7f5f2` | Crema claro. Fondo por defecto. |
| Texto sobre rojo | `#ffffff` / `#fde8eb` | Titular blanco, cuerpo rosa muy claro. |
| Ámbar (secundario web) | `#e8a33d` | NO usar en piezas de Instagram: un solo acento. |

Fuente: variables `--ast-global-color-*` del tema Astra de todovending.com.

## Tipografía

- **Sora** (Google Fonts), pesos 400, 600, 700 y 800.
- Titulares en 800, interlineado 1,05, tracking ligeramente negativo.
- Cuerpo en 400; negritas en 700.
- Cifras protagonistas en 800, en rojo, muy grandes (200-230 px).

## Logo

- Archivo: `templates/assets/todovending-logo.png` (234x47 px, fondo
  transparente). Es la única versión disponible en la web.
- Usarlo SOLO a su tamaño real (234 px de ancho) o menor. No ampliarlo: se
  pixela. Si se necesita grande, pedir el SVG o un PNG de alta resolución.
- Sobre fondo rojo, dentro de una placa blanca con radio de 8 px.

## Plantillas de pieza

- **Carrusel 1080x1350:** etiqueta de sección en rojo arriba a la izquierda,
  numeración «3/10» arriba a la derecha, barra roja de progreso arriba, logo
  abajo a la izquierda y @todo_vending abajo a la derecha. Márgenes
  laterales de 120 px. Última diapositiva con fondo rojo.
- **Reel / historia 1080x1920:** logo y @ a partir de y=250. Texto entre
  y=400 e y=1450, con un margen derecho de 150 px para no chocar con los
  iconos. Última tarjeta con fondo rojo.

## Tono editorial

- Medio informativo del sector vending. Cifras siempre atribuidas («según
  ANEDA», «estimación de…»). No presentar estimaciones de parte como hechos.
- Comillas españolas « » en las citas.
