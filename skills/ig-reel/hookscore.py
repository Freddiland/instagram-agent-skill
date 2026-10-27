#!/usr/bin/env python3
"""
hookscore.py - puntúa la primera frase de un Reel en las cinco cosas que
comparten los hooks fuertes, y ordena un lote de ellos entre sí.

Qué es:  cinco heurísticas locales, calculadas en tu equipo a partir del texto.
Miden propiedades que suelen tener los hooks que retienen: una duración que se
dice en menos de tres segundos, algo concreto, algo en juego, lo interesante al
principio y no al final, y un espectador al que apuntar.

Qué NO es:  un predictor de visitas. La versión original en inglés se probó con
74 hooks reales de vídeos cortos (los tres primeros segundos de los ocho
mejores y los ocho peores vídeos de cinco canales). Distinguía bien un hook
real de uno escrito para ser malo: AUC 0,83. Distinguía casi nada los aciertos
de un buen creador de sus fallos: AUC 0,56, donde 0,50 es lanzar una moneda.

Esta adaptación al español NO se ha vuelto a validar con hooks en español. Las
listas de palabras y los umbrales están traducidos y ajustados a la sintaxis
española, pero tómalo como un filtro de hooks claramente flojos, no como una
medición.

Para lo que sirve: detecta saludos, preámbulos, hooks sin nada concreto y hooks
que tardan cinco segundos en decirse. No te dirá cuál de dos hooks decentes va a
viajar, y nada que lea texto puede hacerlo, porque eso lo deciden tu cara, tu
edición, tu audio y a quién se lo enseña Instagram. Fíate antes de la gráfica de
retención que de este script.

Cada comprobación devuelve de 0 a 100. Más es mejor.

Uso
  python3 hookscore.py hooks.txt              # un hook por línea, ordenados
  python3 hookscore.py --hook "Perdí 18.000 € por una cláusula que faltaba."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py hooks.txt --json
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata

WORD_RE = re.compile(r"[\w$€%'’-]+")
NUMBER_RE = re.compile(
    r"[$€]\s?\d[\d.]*(?:,\d+)?"                          # dinero, delante
    r"|\b\d[\d.]*(?:,\d+)?\s?"                           # una cifra, con o
    r"(?:%|€|k\b|x\b|h\b|horas?\b|min\b|minutos?\b"       # sin unidad
    r"|seg\b|segundos?\b|días?\b|semanas?\b|mes\b|meses\b|años?\b|euros?\b)?",
    re.IGNORECASE)
CAP_WORD = re.compile(r"(?<!\w)[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}(?!\w)")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")


def fold(word):
    """Minúsculas y sin tildes: «Perdí» y «perdi» son la misma palabra aquí."""
    w = unicodedata.normalize("NFD", word.lower())
    return "".join(c for c in w if unicodedata.category(c) != "Mn").strip("'’")


def folded_set(words):
    return {fold(w) for w in words}


# Los hooks hablados dicen las cifras en voz alta. «Cero euros» y «veinte mil»
# son tan concretos como «0 €» y «20.000 €». «Uno» y «primero» no están a
# propósito: son relleno mucho más a menudo que una cantidad.
SPOKEN_NUMBERS = folded_set([
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "quince", "veinte", "treinta", "cuarenta", "cincuenta",
    "sesenta", "setenta", "ochenta", "noventa", "cien", "cientos", "mil", "millón",
    "millones", "docena", "mitad", "medio", "doble", "triple",
])
MONEY_WORDS = folded_set([
    "euros", "euro", "pavos", "dólares", "céntimos", "facturación", "facturé",
    "factura", "ingresos", "beneficio", "beneficios", "sueldo", "salario",
    "alquiler", "millonario", "cobré", "cobro",
])

# Palabras que ponen algo en juego. Un hook sin ninguna es una afirmación; con
# una, es un motivo para seguir mirando.
STAKES = folded_set([
    "deja", "dejé", "dejar", "nunca", "jamás", "mal", "error", "errores",
    "equivocado", "perdí", "pierdes", "perder", "perdiendo", "perdimos", "costó",
    "cuesta", "cuestan", "arruiné", "ruina", "fracasé", "fracaso", "fallé", "fallo",
    "nadie", "no", "ni", "dejes", "quité", "despedido", "despidieron", "borré",
    "borra", "eliminé", "cerré", "sustituyó", "reemplazó", "gratis", "pagué", "pagas",
    "cobras", "contraté", "ahorré", "ahorras", "prohibido", "ilegal", "peor", "odio",
    "odiaba", "tiré", "desperdicié", "estafa", "mentira", "mienten", "verdad",
    "secreto", "oculto", "escondido", "robé", "robaron", "antes", "hasta", "pero",
    "excepto", "salvo", "problema", "riesgo", "peligro", "cuidado", "ojo",
    "arrepiento", "ojalá", "debería", "deberías", "todavía", "aún", "ya", "solo",
    "sólo", "sin", "versus", "vs", "realmente", "casi",
])

# Aperturas que gastan el primer segundo en no decir nada. Se comparan contra el
# principio de la frase ya en minúsculas y sin tildes.
WEAK_OPENERS = [fold(x) for x in [
    "bueno", "vale", "hola", "hey", "ey", "buenas", "chicos", "chicas", "gente",
    "amigos", "bienvenidos", "bienvenidas", "hoy", "básicamente", "sinceramente",
    "la verdad", "mira,", "escucha", "eh", "em", "pues", "solo quería", "quería",
    "quiero", "os quiero", "uno de", "una de", "alguna vez", "sabías", "sabéis",
    "sabes", "has ", "habéis", "estás ", "en este", "en el vídeo",
    "hay ", "esto es", "es ", "cuando ", "ya sabéis", "o sea", "así que",
    "entonces", "venga", "qué tal", "muy buenas",
]]

# Imperativos que se ganan la primera posición.
IMPERATIVES = folded_set([
    "deja", "para", "roba", "róbame", "copia", "cópiate", "borra", "elimina", "prueba",
    "mira", "lee", "guarda", "guárdalo", "usa", "haz", "hazlo", "crea", "escribe",
    "manda", "envía", "coge", "empieza", "nunca", "siempre", "no", "pon", "apunta",
    "apúntate", "revisa", "cambia", "sube", "cobra", "sal", "olvídate", "quita",
])
SECOND_PERSON = re.compile(
    r"(?<!\w)(?:tú|tu|tus|te|ti|contigo|vosotr[oa]s|os|vuestr[oa]s?|usted|ustedes|"
    r"estás|eres|tienes|haces|quieres|necesitas|puedes|sabes|vas|has|debes|sigues|"
    r"crees|pagas|cobras|publicas|subes|pierdes|ganas|vendes|usas|escribes|grabas|"
    r"estáis|sois|tenéis|hacéis|queréis|necesitáis|podéis|sabéis|vais|habéis|cobráis)(?!\w)",
    re.IGNORECASE)
FIRST_PERSON = re.compile(
    r"(?<!\w)(?:yo|me|mi|mis|conmigo|nosotr[oa]s|nos|nuestr[oa]s?|tengo|hice|perdí|gané|"
    r"cobré|pagué|empecé|dejé|aprendí|descubrí|probé|llevo|estuve|fui|soy|estoy|"
    r"publiqué|subí|vendí|facturé|tardo|tardaba|hacía|pagaba|cobraba|pensaba|creía|tenía|"
    r"publicaba)(?!\w)", re.IGNORECASE)

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:deja de (?:hacer )?scroll|para de (?:hacer )?scroll|no hagas scroll|no pases de largo)"),
     "Empieza con «deja de hacer scroll». Pedir atención demuestra que no te la has ganado."),
    (re.compile(r"(?i)\b(?:en (?:este|el) (?:vídeo|video|reel)(?: de hoy)?|(?:te|os) voy a (?:enseñar|mostrar|contar)|(?:te|os) enseño cómo)\b"),
     "Preámbulo de vídeo. Bórralo y empieza por lo que prometes."),
    (re.compile(r"(?i)^\s*¡?(?:hola|hey|ey|buenas|qué tal|que tal|bienvenid[oa]s?|muy buenas)\b"),
     "Saludo. Nadie ha venido al feed a que le saluden."),
    (HASHTAG_RE,
     "Hashtag en el hook. Los hashtags van al final del texto, si es que van."),
    (EMOJI_RE,
     "Emoji en el hook. El texto en pantalla a tamaño de hook tiene sitio para palabras o para un emoji, no para las dos cosas."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # «18.000» es una palabra al decirlo, así que aquí también.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text))


def proper_nouns(text):
    found = set()
    for m in CAP_WORD.finditer(text):
        before = text[:m.start()].rstrip(" \t¿¡\"«(")
        if not before or before[-1] in ".!?:\n":
            continue
        found.add(m.group(0))
    return found


def check_length(text):
    """Un hook tiene que llegar antes de que se mueva el pulgar. Unos dos segundos."""
    w = words(text)
    n = len(w)
    secs = n / 2.85                      # ~170 palabras por minuto, en voz alta
    chars = len(text.strip())
    # En español hacen falta algo más de palabras que en inglés para decir lo
    # mismo (artículos y preposiciones), así que la horquilla se abre un poco.
    if 5 <= n <= 14:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 14) * 10)
    if chars > 70:                       # dos líneas de texto grande en pantalla
        score -= 12
    return clamp(score), f"{n} palabras, {chars} caracteres, ~{secs:.1f} s en voz alta (lo deseable: 5-14 palabras)"


def check_specificity(text):
    """Una cosa concreta vale más que tres abstractas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = proper_nouns(text)
    spoken = [w.lower() for w in words(text) if fold(w) in SPOKEN_NUMBERS or fold(w) in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} marca(s) concreta(s)" + (f": {found}" if found else
                   ": ninguna cifra, ningún nombre, nada comprobable"))


def check_stakes(text):
    """Tensión, coste, negación. Algo que el espectador podría perder."""
    hits = [x.lower() for x in words(text) if fold(x) in STAKES]
    markers = sorted(set(hits))
    if re.search(r"[$€]\s?\d|\d[\d.,]*\s?(?:€|euros?\b)", text, re.IGNORECASE):
        markers.append("un precio")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marca(s) de tensión" + (f": {', '.join(markers[:4])}" if markers else
                                          ": no hay nada en juego en esta frase")
    return clamp(score), detail


def check_frontload(text):
    """La palabra interesante no puede estar en la posición nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = [fold(x) for x in w]
    head = fold(text.strip().lstrip("¿¡\"«'"))
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        if head.startswith(weak) and (len(head) == len(weak) or not head[len(weak)].isalnum()
                                      or weak.endswith((" ", ","))):
            penalty, hit_opener = 30, weak.strip(" ,")
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) and any(c.isdigit() for c in w[i])
                or (i and w[i] in proper_nouns(text))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "no hay ninguna palabra con carga en la frase"
    elif payload <= 3:
        base = 100.0
        where = f"carga en la palabra {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"carga en la palabra {payload + 1}, podría ir antes"
    else:
        base = 40.0
        where = f"carga en la palabra {payload + 1}, demasiado tarde"
    detail = where + (f"; apertura floja «{hit_opener}»" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Apunta a un espectador, o flota en el aire."""
    w = [fold(x) for x in words(text)]
    if SECOND_PERSON.search(text):
        return 100.0, "le habla al espectador"
    if w and w[0] in IMPERATIVES:
        return 90.0, f"empieza en imperativo («{w[0]}»)"
    if FIRST_PERSON.search(text):
        return 70.0, "primera persona, sin espectador"
    return 35.0, "tercera persona, no hay nadie en la sala"


CHECKS = ["DURACIÓN", "CONCRECIÓN", "TENSIÓN", "ARRANQUE", "DESTINATARIO"]


def run(text):
    results = {
        "DURACIÓN": check_length(text),
        "CONCRECIÓN": check_specificity(text),
        "TENSIÓN": check_stakes(text),
        "ARRANQUE": check_frontload(text),
        "DESTINATARIO": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más floja pone el techo, con la misma lógica que detect.py:
    # basta una propiedad mala para que el pulgar siga bajando.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FUERTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "VALE" if overall >= 50 else "FLOJO")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nPUNTUACIÓN DEL HOOK", file=out)
    print("=" * 62, file=out)
    print(f"  «{text.strip()}»\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  DESCALIFICA  {f}", file=out)
    if verdict != "FUERTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Propiedad más floja: {weakest}. Arregla esa y vuelve a pasarlo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nCLASIFICACIÓN DE HOOKS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        más floja: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        descalifica: {f}", file=out)
    print("\nGraba el primero. Si el primero está por debajo de 50, ninguno de estos es el hook.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa un hook de Reel en cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un hook por línea, o -")
    ap.add_argument("--hook", help="puntúa un solo hook escrito en la línea de comandos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("no hay nada que puntuar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
