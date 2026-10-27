#!/usr/bin/env python3
"""
caption.py - revisa el texto de una publicación de Instagram y enseña
exactamente lo que se ve en el feed antes del «... más».

Instagram muestra unos 125 caracteres del texto en el feed y esconde el resto
detrás de un toque. Casi todos los textos que fallan, fallan ahí: el hook está
en la tercera frase, la primera línea es un saludo o todo empieza por un
hashtag. Este script imprime esa ventana visible en un recuadro para que la
leas como la lee un desconocido haciendo scroll, y después revisa las ocho
cosas que merece la pena revisar.

El corte de 125 caracteres es aproximado. El número real cambia con el móvil,
el tamaño de letra y dónde caen tus saltos de línea, y por eso conviene dejar
margen en vez de calcular un texto que acabe justo en 125. Cámbialo con
--truncate si quieres probar uno más estrecho.

Uso
  python3 caption.py texto.txt
  python3 caption.py texto.txt --keywords "presupuestos para clientes,precios de agencia"
  pbpaste | python3 caption.py -
  python3 caption.py texto.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # Límite máximo de texto de Instagram.
TRUNCATE = 125           # Más o menos donde el feed corta con «... más».
HASHTAG_LIMIT = 5        # Máximo por publicación o reel desde el 18 de diciembre
                         # de 2025 (antes eran 30). Lo anunció la cuenta @Creators,
                         # recomendando usar pocos hashtags (hasta 5) y más
                         # específicos en lugar de muchos genéricos.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|"
                     r"\b[a-z0-9-]+\.(?:com|es|eu|cat|eus|gal|co|io|net|org|ai|app|shop|store|link|me)/\S*",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CAP_WORD = re.compile(r"(?<!\w)[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}(?!\w)")
NUMBER_RE = re.compile(
    r"[$€]\s?\d|\d[\d.,]*\s?(?:€|%)|(?<!\w)\d[\d.,]*(?!\w)|"
    r"(?<!\w)(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|doce|quince|veinte|"
    r"treinta|cincuenta|cien|mil|mill[oó]n|millones|euros?)(?!\w)", re.IGNORECASE)


def concrete_markers(text):
    """Cifras (también dichas con letra) y nombres propios que no abren frase."""
    found = NUMBER_RE.findall(text)
    for m in CAP_WORD.finditer(text):
        before = text[:m.start()].rstrip(" \t¿¡\"«(")
        if before and before[-1] not in ".!?:\n":
            found.append(m.group(0))
    return found


# La palabra clave se busca en MAYÚSCULAS a propósito («Comenta CONTRATO»): por
# eso esa parte no lleva la marca de ignorar mayúsculas.
ASKS = [
    (re.compile(r"(?i:\bcomenta(?:d)?\b)\s+(?:(?i:la palabra)\s+)?[\"«]?[A-ZÁÉÍÓÚÑ0-9]{2,}(?!\w)"),
     "comentar una palabra clave"),
    (re.compile(r"(?i)\b(?:escríbeme|escribeme|mándame|mandame|envíame|enviame|háblame)\b[^.!?\n]{0,20}"
                r"\b(?:md|dm|privado|mensaje)\b|\bpor (?:md|dm|privado)\b"), "escribir por privado"),
    (re.compile(r"(?i)\bguárd(?:alo|ala|atelo|atela|ate esto)\b|\bguarda (?:esto|este|esta)\b"), "guardar"),
    (re.compile(r"(?i)\bcompárt(?:elo|ela|elo con)\b|\bcomparte (?:esto|este|esta)\b|\b(?:mándaselo|mandaselo|envíaselo|enviaselo)\b"),
     "compartir"),
    (re.compile(r"(?i)\bsígueme\b|\bsigueme\b|\bdale a seguir\b"), "seguir"),
    (re.compile(r"(?i)\b(?:enlace|link) (?:en|de) (?:la |mi )?(?:bio|perfil)\b"), "enlace en la bio"),
    (re.compile(r"(?i)\bdesliza\b|\bpasa (?:a la|las|al)\b|\btoca (?:para|aquí)\b"), "deslizar o tocar"),
    (re.compile(r"(?i)\bcuéntame\b|\bcuentame\b|\bdime\b|\bqué harías\b|\bcuál (?:prefieres|elegirías|eliges)\b"),
     "responder a una pregunta"),
]

FILLER_TAGS = {"#viral", "#fyp", "#parati", "#paratii", "#explore", "#explorar", "#explorepage",
               "#foryou", "#foryoupage", "#trending", "#tendencia", "#tendencias", "#instagood",
               "#love", "#follow", "#sígueme", "#sigueme", "#seguidores", "#follow4follow",
               "#siguemeytesigo", "#like4like", "#likeforlike", "#megusta", "#reels",
               "#reelsinstagram", "#viralreels", "#instadaily", "#instagram"}


def visible_window(text, cut):
    """Lo que enseña el feed. Instagram corta en mitad de palabra, así que esto también."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE SE VE EN EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(cabe el texto entero)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LONGITUD", "FALLO" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} por encima del límite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("PRIMERA LÍNEA", "FALLO", "el texto empieza con una línea en blanco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMERA LÍNEA", "FALLO",
            "empieza por un hashtag o una mención, en la única posición que merece una frase")
    elif len(first_line) > cut:
        add("PRIMERA LÍNEA", "AVISO",
            f"{len(first_line)} caracteres, así que se corta en el {cut} a mitad de idea. "
            "Bien si el corte deja intriga, mal si corta una subordinada")
    else:
        add("PRIMERA LÍNEA", "OK", f"{len(first_line)} caracteres, entra entera")

    marks = concrete_markers(window)
    add("HOOK CONCRETO", "OK" if marks else "AVISO",
        f"{len(marks)} cifra(s) o nombre(s) en la parte visible"
        + ("" if marks else ": nada comprobable antes del toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FALLO", f"{len(tags)} hashtags, por encima del máximo de {HASHTAG_LIMIT}. "
                                 "Los que pasan del quinto no cuentan y el bloque suena a antiguo")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "AVISO", f"{len(tags)} hashtags, en el máximo, y "
                                 f"{len(filler)} de ellos genéricos. Usa los cinco para temas")
    elif filler:
        add("HASHTAGS", "AVISO", f"{len(tags)} hashtags, {len(filler)} genéricos "
                                 f"({', '.join(filler[:3])}). No describen nada")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("UBICACIÓN TAGS", "OK", "no hay hashtags que colocar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"(?!\w)", window) for t in tags):
        add("UBICACIÓN TAGS", "AVISO", "hay un hashtag en la parte visible, "
                                       "gastando espacio del feed en una etiqueta")
    else:
        add("UBICACIÓN TAGS", "OK", "los hashtags están debajo del corte")

    add("ENLACES", "AVISO" if links else "OK",
        f"{len(links)} enlace(s) en el texto, y el texto no es clicable. "
        f"Llévalo a la bio o al privado" if links else "no hay enlaces muertos en el texto")

    if len(asks) == 1:
        add("UNA PETICIÓN", "OK", f"una llamada a la acción: {asks[0]}")
    elif not asks:
        add("UNA PETICIÓN", "AVISO", "no hay llamada a la acción. Decide para qué es este post")
    else:
        add("UNA PETICIÓN", "AVISO", f"{len(asks)} peticiones ({', '.join(asks)}). "
                                     "Dos peticiones es lo mismo que ninguna")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "AVISO" if density > 4 else "OK",
        f"{len(emoji)} emojis, {density:.1f} por cada 100 caracteres"
        + (": parecen decoración" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "OK" if not missing else ("AVISO" if found else "FALLO")
        add("BÚSQUEDA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} en la parte visible" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FALLO")
    warns = sum(1 for c in checks if c["status"] == "AVISO")
    verdict = "CORREGIR" if fails else ("REVISAR" if warns else "LISTO")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DEL TEXTO  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} petición(es)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<5} {c['check']:<17} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDICTO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa el texto de una publicación de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con el texto, o - para la entrada estándar")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caracteres visibles antes de «... más» (por defecto {TRUNCATE})")
    ap.add_argument("--keywords", default="", help="términos, separados por comas, por los que quieres que te encuentren")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "LISTO" else 1)


if __name__ == "__main__":
    main()
