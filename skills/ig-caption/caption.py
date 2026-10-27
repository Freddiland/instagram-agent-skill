#!/usr/bin/env python3
"""
caption.py - revisa la descripción de un post de Instagram y enseña
exactamente lo que muestra el feed antes del "... más".

Instagram le da a la descripción unos 125 caracteres en el feed y esconde el
resto detrás de un toque. Casi todas las descripciones que fallan, fallan ahí:
el hook está en la tercera frase, o la primera línea es un saludo, o todo
empieza con un hashtag. Esto imprime la ventana visible en una caja para que la
leas como la lee un desconocido haciendo scroll, y luego comprueba las ocho
cosas que merece la pena comprobar.

El corte de 125 caracteres es una aproximación. El número real cambia con el
dispositivo, el tamaño de letra y dónde caen tus saltos de línea, que es
justo por lo que conviene dejar margen en vez de una descripción calculada para
acabar en el 125. Cámbialo con --truncate si quieres probar uno más estricto.

Funciona en español y en inglés.

Uso
  python3 caption.py descripcion.txt
  python3 caption.py descripcion.txt --keywords "contratos para freelance,precios de agencia"
  pbpaste | python3 caption.py -
  python3 caption.py descripcion.txt --json
"""

import argparse
import json
import re
import sys
import textwrap
import unicodedata

LIMIT = 2200             # Límite duro de Instagram para la descripción.
TRUNCATE = 125           # Más o menos donde el feed corta en "... más".
HASHTAG_LIMIT = 5        # Tope de Instagram por post o reel desde el 18 de
                         # diciembre de 2025, antes 30. Lo anunció la cuenta
                         # @Creators: "using fewer (up to 5) more targeted
                         # hashtags, rather than many generic ones, can improve
                         # both your content's performance and people's
                         # experience".

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+"
                     r"|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app|es|eu|cat|me|link)/\S*",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(r"[$€]\s?\d|\b\d[\d,.]*\b|(?<!^)(?<![¿¡])\b[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}\b",
                         re.MULTILINE)


def fold(text):
    nfd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


# Las peticiones se buscan sobre el texto sin tildes, así "guárdalo" y
# "guardalo" cuentan igual. La palabra clave de "comenta X" se exige en
# mayúsculas: es como se pide en la práctica y evita confundirla con
# "comenta lo que quieras".
ASKS = [
    (re.compile(r"(?i:\bcomment (?:the word |\")?)[A-Za-z0-9]{2,}\b"
                r"|\b(?i:comenta|escribe|pon)(?i:me)?\s+(?:(?i:la palabra)\s+)?[\"«]?[A-ZN0-9]{3,}\b"),
     "comentar una palabra clave"),
    (re.compile(r"(?i)\b(?:dm|message) me\b|\b(?:escribeme|mandame|enviame)(?: un)?"
                r"(?: (?:dm|md|mensaje|privado))?\b|\bpor (?:dm|md|privado)\b"), "escribir por DM"),
    (re.compile(r"(?i)\bsave (?:this|it)\b|\bguarda(?:lo|la|telo|tela)\b"
                r"|\bguarda (?:esto|este|esta|el post|el reel)\b"), "guardar"),
    (re.compile(r"(?i)\bshare (?:this|it)\b|\bcompartelo\b|\bcomparte (?:esto|este|esta|con)\b"),
     "compartir"),
    (re.compile(r"(?i)\bfollow (?:me|for)\b|\bsigueme\b|\bsiguenos\b"), "seguir"),
    (re.compile(r"(?i)\blink in (?:my )?bio\b|\b(?:link|enlace) (?:en|de) (?:mi |la )?bio\b"),
     "link en la bio"),
    (re.compile(r"(?i)\b(?:swipe|tap) (?:through|left|right|for|to)\b|\bdesliza\b"),
     "deslizar o tocar"),
    (re.compile(r"(?i)\btell me\b|\bwhat would you\b|\bwhich one\b"
                r"|\bdime\b|\bcuentame\b|\bque harias\b|¿con cual\b|¿cual (?:te|elegirias)\b"),
     "responder a una pregunta"),
]

FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
               "#trending", "#instagood", "#love", "#follow", "#like4like", "#reels",
               "#reelsinstagram", "#viralreels", "#instadaily",
               "#parati", "#paratii", "#paratipage", "#fypシ", "#explorar", "#tendencia",
               "#tendencias", "#amor", "#sigueme", "#sígueme", "#megusta", "#likeforlike",
               "#reelsespaña", "#reelsespana", "#instamood", "#españa", "#espana"}


def visible_window(text, cut):
    """Lo que enseña el feed. Instagram corta a mitad de palabra, así que esto también."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE ENSEÑA EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(cabe entera)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    folded = fold(stripped)
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(folded)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LONGITUD", "FALLO" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} por encima del límite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("PRIMERA LÍNEA", "FALLO", "la descripción empieza con una línea en blanco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMERA LÍNEA", "FALLO",
            "empieza con un hashtag o una mención, en el único sitio que merece una frase")
    elif len(first_line) > cut:
        add("PRIMERA LÍNEA", "AVISO",
            f"{len(first_line)} caracteres, así que se corta en el {cut} a media idea. "
            "Bien si el corte deja intriga, mal si corta una subordinada")
    else:
        add("PRIMERA LÍNEA", "OK", f"{len(first_line)} caracteres, se ve entera")

    add("HOOK CONCRETO", "OK" if CONCRETE_RE.search(window) else "AVISO",
        f"{len(CONCRETE_RE.findall(window))} cifra(s) o nombre(s) en la ventana visible"
        + ("" if CONCRETE_RE.search(window) else " - nada comprobable antes del toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FALLO", f"{len(tags)} hashtags, por encima del tope de Instagram "
                                 f"({HASHTAG_LIMIT}). Los que pasan del quinto no cuentan y el "
                                 "bloque se ve antiguo")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "AVISO", f"{len(tags)} hashtags, en el tope, y "
                                 f"{len(filler)} genéricos. Gasta los cinco en temas")
    elif filler:
        add("HASHTAGS", "AVISO", f"{len(tags)} hashtags, {len(filler)} genéricos "
                                 f"({', '.join(filler[:3])}). Esos no describen nada")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("SITIO HASHTAGS", "OK", "no hay hashtags que colocar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("SITIO HASHTAGS", "AVISO", "hay un hashtag dentro de la ventana visible, "
                                       "gastando espacio del feed en una etiqueta")
    else:
        add("SITIO HASHTAGS", "OK", "los hashtags están debajo del corte")

    add("ENLACES", "AVISO" if links else "OK",
        f"{len(links)} enlace(s) en la descripción, y la descripción no es clicable. "
        f"Llévalo a la bio o al DM" if links else "no hay enlaces muertos en el texto")

    if len(asks) == 1:
        add("UNA PETICIÓN", "OK", f"una llamada a la acción: {asks[0]}")
    elif not asks:
        add("UNA PETICIÓN", "AVISO", "no hay llamada a la acción. Decide para qué es este post")
    else:
        add("UNA PETICIÓN", "AVISO", f"{len(asks)} peticiones ({', '.join(asks)}). "
                                     "Dos peticiones es lo mismo que ninguna")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "AVISO" if density > 4 else "OK",
        f"{len(emoji)} emoji, {density:.1f} por cada 100 caracteres"
        + (" - parece decoración" if density > 4 else ""))

    if keywords:
        low = fold(stripped.lower())
        win_low = fold(window.lower())
        found = [k for k in keywords if fold(k.lower()) in low]
        missing = [k for k in keywords if fold(k.lower()) not in low]
        in_window = [k for k in found if fold(k.lower()) in win_low]
        status = "OK" if not missing else ("AVISO" if found else "FALLO")
        add("BÚSQUEDA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} en la ventana visible" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FALLO")
    warns = sum(1 for c in checks if c["status"] == "AVISO")
    verdict = "CORREGIR" if fails else ("REVISAR" if warns else "LISTA")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DE DESCRIPCIÓN  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} petición(es)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<5} {c['check']:<15} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDICTO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa la descripción de un post de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con la descripción, o -")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caracteres visibles antes de '... más' (por defecto {TRUNCATE})")
    ap.add_argument("--keywords", default="",
                    help="términos separados por comas por los que quieres que te encuentren")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "LISTA" else 1)


if __name__ == "__main__":
    main()
