#!/usr/bin/env python3
"""
hookscore.py - puntúa la primera frase de un Reel en las cinco cosas que
comparten los hooks fuertes, y ordena un lote de ellos entre sí.

Qué es:  cinco heurísticas locales, calculadas en tu máquina solo a partir del
texto. Miden propiedades que suelen compartir los hooks que retienen la
atención: una longitud que se dice en menos de tres segundos, un dato concreto,
algo en juego, lo importante delante y no al final, y un espectador al que
apuntar.

Qué NO es:  un predictor de visualizaciones. Se probó con 74 hooks reales de
vídeo corto (en inglés), transcritos de los tres primeros segundos de los ocho
mejores y los ocho peores vídeos de cinco canales. Separa bien un hook real de
uno escrito mal a propósito: AUC 0,83, y 9 de 10 hooks malos quedaron por debajo
de la mediana real. Separar los éxitos de un buen creador de sus fracasos lo
hace casi al azar: AUC 0,56, donde 0,50 es tirar una moneda.

Así que úsalo para lo que mide bien. Detecta saludos, preámbulos, hooks sin
nada concreto y hooks que tardan cinco segundos en decirse. No te dirá cuál de
dos hooks decentes va a funcionar, y nada que lea texto puede hacerlo, porque
eso lo deciden tu cara, tu edición, tu audio y a quién se lo enseña Instagram.
Fíate más de la gráfica de retención que de este script.

Funciona en español y en inglés: las listas de palabras incluyen los dos
idiomas y las tildes se ignoran al comparar ("perdí" y "perdi" cuentan igual).
La adaptación al español no se ha validado con un corpus de hooks en español.

Cada comprobación devuelve de 0 a 100. Más alto es mejor.

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

WORD_RE = re.compile(r"[\w$%'’€-]+")
UNIT = (r"(?:%|k\b|x\b|hrs?\b|hours?\b|mins?\b|minutes?\b|days?\b|weeks?\b|months?\b"
        r"|years?\b|h\b|horas?\b|minutos?\b|segundos?\b|seg\b|dias?\b|días?\b"
        r"|semanas?\b|mes\b|meses\b|años?\b|anos?\b|euros?\b|€)")
NUMBER_RE = re.compile(
    r"[$€]\s?\d[\d.,]*"                              # dinero, símbolo delante
    r"|\b\d[\d.,]*\s?" + UNIT + r"?",                # una cifra, con o sin unidad
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<!^)(?<![¿¡])\b[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")


def fold(text):
    """Minúsculas y sin tildes, para comparar con las listas."""
    nfd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


# Los hooks hablados dicen los números en voz alta. "Cero euros" y "veinte mil"
# son tan concretos como "0 €" y "20.000 €". "Uno", "un" y "primero" no están a
# propósito: son relleno mucho más a menudo que una cantidad.
# Todas las listas van sin tildes porque se comparan con fold().
SPOKEN_NUMBERS = {
    # inglés
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
    "billion", "dozen", "half", "twice", "triple",
    # español
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "quince", "veinte", "treinta", "cuarenta",
    "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien", "ciento",
    "cientos", "mil", "millon", "millones", "docena", "mitad", "doble",
}
MONEY_WORDS = {
    "dollars", "dollar", "bucks", "grand", "percent", "cents",
    "millionaire", "billionaire", "revenue", "profit", "salary", "rent",
    "euros", "euro", "pavos", "dolares", "dolar", "centimos", "facturacion",
    "facture", "facturo", "beneficio", "beneficios", "sueldo", "salario",
    "alquiler", "millonario", "millonaria", "ingresos", "nomina", "dinero",
    "pasta", "precio", "tarifa",
}

# Palabras que ponen algo en juego. Un hook sin ninguna es una afirmación; con
# una, es un motivo para seguir mirando.
STAKES = {
    # inglés
    "stop", "never", "wrong", "mistake", "mistakes", "lost", "lose", "losing",
    "cost", "costs", "broke", "broken", "failed", "failure", "fail", "nobody",
    "no", "not", "don't", "dont", "doesn't", "didn't", "can't", "won't",
    "quit", "quitting", "fired", "deleted", "delete", "killed", "kills", "kill",
    "replaced", "replaces", "cut", "beat", "free", "paid", "charged", "hired",
    "saved", "first",
    "banned", "illegal", "worst", "hate", "hated", "wasted", "waste", "scam",
    "lie", "lied", "lying", "truth", "secret", "hidden", "stole", "stolen",
    "before", "until", "instead", "but", "except", "unless", "problem",
    "risk", "danger", "warning", "regret", "wish", "should", "shouldn't",
    "still", "already", "only", "without", "versus", "vs", "actually",
    # español
    "deja", "dejad", "dejar", "nunca", "jamas", "nadie", "ni", "error",
    "errores", "mal", "perdi", "perdimos", "perder", "pierdes", "perdiendo",
    "cuesta", "costo", "costaron", "cuestan", "arruine", "arruinado",
    "falle", "fallo", "fracaso", "fracase", "fracasan", "despidieron",
    "despedido", "borre", "borra", "borrar", "elimine", "mate", "mata",
    "sustitui", "sustituyo", "reemplazo", "gratis", "pague", "pagas", "pagaba",
    "cobre", "cobras", "cobraba", "contrate", "ahorre", "ahorras", "primer",
    "primera", "primeros", "primeras", "prohibido", "ilegal", "peor", "odio",
    "odiaba", "tire", "tiras", "malgaste", "estafa", "mentira", "menti",
    "mienten", "verdad", "secreto", "oculto", "robe", "robo", "antes", "hasta",
    "pero", "salvo", "excepto", "problema", "riesgo", "peligro", "cuidado",
    "ojo", "arrepiento", "ojala", "deberias", "todavia", "ya", "solo", "sin",
    "contra", "realmente", "nadie",
}

# Arranques que gastan el primer segundo sin decir nada.
WEAK_OPENERS = [
    # inglés
    "so", "ok", "okay", "hey", "hi", "hello", "guys", "yo", "alright",
    "welcome", "today", "basically", "honestly", "look", "listen", "um",
    "just", "let", "lets", "let's", "i wanted", "i want", "one of",
    "have you", "did you", "do you", "are you", "in this", "in today",
    "the thing", "a lot", "there is", "there are", "this is", "it is",
    "as a", "when it", "if you've", "you know",
    # español
    "hola", "buenas", "bueno", "pues", "vale", "venga", "chicos", "chicas",
    "gente", "hoy", "bienvenidos", "bienvenidas", "basicamente", "sinceramente",
    "oye", "escucha", "eh", "em", "a ver", "en este", "en el video", "quiero",
    "queria", "os quiero", "os traigo", "te traigo", "uno de", "una de",
    "sabias", "alguna vez", "te has", "has pensado", "como sabeis", "la cosa",
    "hay que", "esto es", "es que", "cuando se", "si alguna",
]

# Imperativos que se ganan la primera posición.
IMPERATIVES = {
    "stop", "steal", "copy", "delete", "try", "watch", "read", "save",
    "use", "build", "make", "write", "send", "take", "start", "quit",
    "never", "always", "don't", "dont", "do", "put", "run", "check",
    "deja", "dejad", "roba", "robame", "copia", "borra", "prueba", "mira",
    "lee", "guarda", "usa", "haz", "escribe", "envia", "manda", "toma",
    "empieza", "nunca", "siempre", "pon", "revisa", "apunta", "olvidate",
    "cobra", "sube", "cambia", "quita", "no",
}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:stop scrolling|don'?t scroll"
                r"|(?:deja|para) de (?:hacer )?scroll|no hagas scroll|no pases de largo)"),
     "Empieza con \"deja de hacer scroll\". Pedir atención demuestra que no te la has ganado."),
    (re.compile(r"(?i)\b(?:in (?:this|today'?s) (?:video|reel)|i'?m going to show you"
                r"|i'?ll show you how"
                r"|en (?:este|el) (?:v[ií]deo|reel)(?: de hoy)?"
                r"|(?:hoy )?(?:te|os) voy a (?:enseñar|ensenar|mostrar|contar|explicar))\b"),
     "Preámbulo de vídeo. Bórralo y empieza por la recompensa."),
    (re.compile(r"(?i)^\s*(?:hey |hi |what'?s up |welcome "
                r"|hola\b|buenas\b|qu[eé] tal\b|bienvenid[oa]s\b)"),
     "Saludo. Nadie ha entrado al feed para que le saluden."),
    (HASHTAG_RE,
     "Hashtag en el hook. Los hashtags van al final de la descripción, si es que van."),
    (EMOJI_RE,
     "Emoji en el hook. El texto en pantalla a tamaño de hook tiene sitio para palabras "
     "o para un emoji, no para las dos cosas."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "18.000 €" o "$18,000" es una palabra cuando se dice, así que aquí también.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text))


def tokens(text):
    return [fold(x).strip("'’") for x in words(text)]


def check_length(text):
    """Un hook tiene que aterrizar antes de que se mueva el pulgar. Unos dos segundos."""
    w = words(text)
    n = len(w)
    secs = n / 2.75                      # ~165 palabras por minuto, hablado
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > 60:                       # dos líneas de texto grande en pantalla
        score -= 12
    return clamp(score), (f"{n} palabras, {chars} caracteres, ~{secs:.1f} s hablado "
                          "(lo ideal: 5-12 palabras)")


def check_specificity(text):
    """Una cosa concreta gana a tres abstractas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = tokens(text)
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} dato(s) concreto(s)" + (f": {found}" if found else
                   " - ni una cifra, ni un nombre, nada comprobable"))


def check_stakes(text):
    """Tensión, coste, negación. Algo que el espectador podría perder."""
    hits = [x for x in tokens(text) if x in STAKES]
    markers = sorted(set(hits))
    if re.search(r"[$€]\s?\d|\d\s?(?:€|euros?\b)", text, re.IGNORECASE):
        markers.append("un precio")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marcador(es) de tensión" + (f": {', '.join(markers[:4])}" if markers else
                                               " - no hay nada en juego en esta frase")
    return clamp(score), detail


def check_frontload(text):
    """La palabra interesante no puede estar en la posición nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = tokens(text)
    opener = " ".join(low[:3])
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        if low[0] == weak or opener.startswith(weak + " ") or opener == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "no hay ninguna palabra con carga en toda la frase"
    elif payload <= 3:
        base = 100.0
        where = f"carga en la palabra {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"carga en la palabra {payload + 1}, podría ir antes"
    else:
        base = 40.0
        where = f"carga en la palabra {payload + 1}, demasiado tarde"
    detail = where + (f"; arranque flojo \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


# El español omite el pronombre: "Perdí 18.000 €" es primera persona y
# "¿Cobras por horas?" es segunda, sin "yo" ni "tú". Así que la persona también
# se lee en el verbo. Son listas cortas de formas frecuentes, no un analizador.
SECOND_PERSON_VERBS = {
    "quieres", "tienes", "haces", "sabes", "puedes", "eres", "necesitas",
    "publicas", "vendes", "cobras", "crees", "piensas", "deberias", "has",
    "subes", "grabas", "usas", "sigues", "pierdes", "gastas", "buscas",
    "odias", "intentas", "empiezas", "trabajas", "llevas", "vas", "estas",
}
NOT_SECOND = {"existe", "triste", "insiste", "consiste", "resiste", "pista",
              "lista", "vista", "revista", "artista", "este", "estas", "esas",
              "hasta"}
FIRST_PERSON_VERBS = {
    "tengo", "hago", "llevo", "soy", "estoy", "he", "hice", "dije", "tuve",
    "estuve", "fui", "puse", "vine", "supe", "quise", "pude", "gano", "cobro",
    "vendo", "tardaba", "tardo", "pensaba", "creia", "odiaba", "pagaba",
    "cobraba", "hemos", "tenemos", "hicimos", "perdimos", "ganamos",
}
NOT_FIRST = {"aquí", "allí", "ahí", "así", "café", "bebé", "jabalí", "rubí",
             "menú", "esquí", "maniquí", "sí", "tú", "mí", "dé", "sé", "té", "qué"}


def spanish_person(text):
    raw = [x.lower() for x in words(text)]
    low = [fold(x) for x in raw]
    # "estas" solo cuenta como verbo si va con un adjetivo o gerundio detrás;
    # sin acento es demasiado ambiguo, así que solo se acepta "estás".
    second = [x for x, r in zip(low, raw)
              if (x in SECOND_PERSON_VERBS and (x != "estas" or r == "estás"))
              or (len(x) >= 6 and re.search(r"(?:aste|iste)$", x) and x not in NOT_SECOND)]
    first = [r for r, x in zip(raw, low)
             if x in FIRST_PERSON_VERBS
             or (len(r) >= 4 and r[-1] in "éí" and r not in NOT_FIRST)]
    return second, first


def check_address(text):
    """Apuntado a un espectador, o flotando en el aire."""
    low = fold(text)
    w = tokens(text)
    second, first = spanish_person(text)
    if re.search(r"\b(you|your|you're|youre|yourself"
                 r"|tu|tus|te|ti|contigo|vosotros|vosotras|os|vuestro|vuestra"
                 r"|vuestros|vuestras|usted)\b", low) or second:
        return 100.0, "le habla al espectador" + (f" (\"{second[0]}\")" if second else "")
    if w and w[0] in IMPERATIVES:
        return 90.0, f"empieza en imperativo (\"{w[0]}\")"
    if re.search(r"\b(i|my|me|we|our|yo|mi|mis|conmigo|nosotros|nosotras|nos"
                 r"|nuestro|nuestra|nuestros|nuestras)\b", low) or first:
        return 70.0, "primera persona, sin espectador nombrado"
    return 35.0, "tercera persona, no hay nadie en la sala"


CHECKS = ["LONGITUD", "CONCRECIÓN", "TENSIÓN", "ARRANQUE", "DESTINATARIO"]


def run(text):
    results = {
        "LONGITUD": check_length(text),
        "CONCRECIÓN": check_specificity(text),
        "TENSIÓN": check_stakes(text),
        "ARRANQUE": check_frontload(text),
        "DESTINATARIO": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más débil pone el techo al hook, igual que en detect.py: basta
    # una propiedad mala para que el pulgar siga bajando.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FUERTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "DÉBIL")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nPUNTUACIÓN DEL HOOK", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'TOTAL':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  DESCALIFICANTE  {f}", file=out)
    if verdict != "FUERTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Propiedad más débil: {weakest}. Arregla esa y vuelve a pasarlo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE HOOKS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        más débil: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})",
              file=out)
        for f in r["flags"]:
            print(f"        descalificante: {f}", file=out)
    print("\nGraba el primero. Si el primero está por debajo de 50, ninguno de estos es el hook.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa el hook de un Reel en cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un hook por línea, o -")
    ap.add_argument("--hook", help="puntúa un solo hook pasado en la línea de comandos")
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
