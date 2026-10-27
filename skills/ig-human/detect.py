#!/usr/bin/env python3
"""
detect.py - panel de cinco comprobaciones que puntúa cuánto parece escrito
por una máquina un borrador en español.

Qué es:  cinco heurísticas locales inspiradas en las señales que miden los
detectores públicos de IA: variación en la longitud de las frases, concreción,
vocabulario de relleno, huella tipográfica y voz. Todo se calcula en tu
equipo, a partir del texto. No se sube nada.

Qué NO es:  GPTZero, Originality, Copyleaks, Winston ni Turnitin. No llama a
sus API y no puede prometer su veredicto. Detecta lo mismo en lo que se fijan
todos, por eso arreglarlo suele mover también sus números; pero la única
afirmación honesta es la de esta línea.

Adaptado al español: no hay contracciones como en inglés, así que la VOZ se
mide con marcas de registro coloquial, presencia de la primera y la segunda
persona, y la densidad de adverbios en «-mente», que en español es una de las
huellas más claras del texto generado.

Cada comprobación devuelve una puntuación HUMANA de 0 a 100. Más es mejor.

Uso
  python3 detect.py borrador.txt
  pbpaste | python3 detect.py -
  python3 detect.py borrador.txt --json
  python3 detect.py antes.txt despues.txt      # compara dos borradores
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

# El punto de los miles («18.000») no cierra frase.
SENT_RE = re.compile(r"(?:[^.!?\n]|(?<=\d)\.(?=\d))+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?")
PRONOUNS = re.compile(
    r"(?<!\w)(?:yo|me|mi|mis|m[ií]o|m[ií]a|conmigo|nosotr[oa]s|nos|nuestr[oa]s?|"
    r"t[uú]|tus|te|ti|contigo|vosotr[oa]s|os|vuestr[oa]s?)(?!\w)", re.IGNORECASE)
COLLOQUIAL = re.compile(
    r"(?<!\w)(?:vale|mira|oye|o sea|pues|venga|t[ií]o|t[ií]a|en plan|flip\w*|curr\w*|"
    r"pasta|guay|mola|molan|a ver|ya ves|qu[eé] va|de coña|ni de coña|un mont[oó]n|"
    r"mogoll[oó]n|un rollo|chul[oa]|cutre|fatal|menud[oa]|la verdad|s[uú]per|"
    r"¿no\?|¿vale\?|¿sabes\?|¿eh\?)(?!\w)", re.IGNORECASE)
MENTE = re.compile(r"(?<!\w)[^\W\d_]{3,}mente(?!\w)", re.IGNORECASE)
NUMBERS = re.compile(r"\d[\d.,]*\s?(?:%|€)|[$€]\s?\d|(?<!\w)\d[\d.,]*(?!\w)")
# Las cifras dichas con letra, los días y los meses también son concretos. En
# español van en minúscula, así que no los cuenta el detector de nombres propios.
SPOKEN = re.compile(
    r"(?<!\w)(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|quince|veinte|"
    r"treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|cien|cientos|mil|"
    r"mill[oó]n|millones|docena|mitad|doble|triple|euros?|lunes|martes|mi[eé]rcoles|"
    r"jueves|viernes|s[aá]bado|domingo|enero|febrero|marzo|abril|mayo|junio|julio|agosto|"
    r"septiembre|setiembre|octubre|noviembre|diciembre)(?!\w)", re.IGNORECASE)
CAP_WORD = re.compile(r"(?<!\w)[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}(?!\w)")

_ACCENTS = {"a": "aá", "e": "eé", "i": "ií", "o": "oó", "u": "uúü",
            "á": "aá", "é": "eé", "í": "ií", "ó": "oó", "ú": "uúü", "ü": "uúü", "ñ": "nñ"}


def accent_pattern(phrase):
    out = []
    for ch in phrase.lower():
        if ch in _ACCENTS:
            out.append("[" + _ACCENTS[ch] + "]")
        elif ch.isspace():
            out.append(r"\s+")
        else:
            out.append(re.escape(ch))
    return re.compile(r"(?<!\w)" + "".join(out) + r"(?!\w)", re.IGNORECASE)


def proper_nouns(text):
    """Palabras en mayúscula que no están al principio de frase.

    En español se escriben en minúscula los meses, los días y los gentilicios,
    así que una mayúscula dentro de la frase suele ser un nombre de verdad.
    """
    found = set()
    for m in CAP_WORD.finditer(text):
        before = text[:m.start()].rstrip(" \t¿¡\"«(")
        if not before or before[-1] in ".!?:\n":
            continue
        found.add(m.group(0))
    return found


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Lleva `value` a 0-100, donde `human` -> 100 y `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """Las personas varían mucho la longitud de las frases. Los modelos, poco."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "demasiado corto para juzgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variación {cv:.2f} en {len(lens)} frases (lo deseable: 0,55 o más)"


def check_specificity(text):
    """Cifras, nombres y cosas concretas. El relleno es abstracto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "demasiado corto para juzgar"
    per100 = 100 / len(w)
    hits = (len(NUMBERS.findall(text)) + len(SPOKEN.findall(text))
            + len(proper_nouns(text)))
    density = hits * per100
    # En español hacen falta más palabras para lo mismo (artículos, preposiciones),
    # así que el umbral humano es algo más bajo que en inglés.
    score = scale(density, human=5.0, machine=0.4)
    return score, f"{hits} marcas concretas, {density:.1f} por cada 100 palabras (lo deseable: 3,5 o más)"


def check_slop(text, lex):
    """Densidad de vocabulario de relleno según el diccionario."""
    w = words(text)
    if not w:
        return 50.0, "vacío"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        n = len(accent_pattern(entry["find"]).findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} muletillas, {density:.1f} por cada 100 palabras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caracteres que no salen de un teclado de móvil.

    Las comillas latinas «» y los signos ¿ ¡ no cuentan: son español correcto.
    """
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisibles, {em} rayas, {curly} comillas curvas, "
              f"{ellip} puntos suspensivos de un carácter, {nbsp} espacios duros")
    return score, detail


def check_voice(text, lex):
    """Registro hablado, persona, adverbios en -mente y las formas por defecto del modelo."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "demasiado corto para juzgar"
    per100 = 100 / len(w)
    colloquial = len(COLLOQUIAL.findall(text)) * per100
    person = len(PRONOUNS.findall(text)) * per100
    mente = len(MENTE.findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(colloquial, human=1.5, machine=0.0) * 0.25
             + scale(person, human=7.0, machine=1.0) * 0.30
             + scale(mente, human=0.5, machine=3.0) * 0.15
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("viñetas-uniformes")
    detail = (f"{colloquial:.1f} marcas coloquiales, {person:.1f} pronombres de 1.ª/2.ª persona, "
              f"{mente:.1f} adverbios en -mente por cada 100 palabras, {tells} señal(es) estructural(es)")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["VARIACIÓN", "CONCRECIÓN", "MULETILLAS", "HUELLA", "VOZ"]


def run(text, lex):
    results = {}
    results["VARIACIÓN"] = check_burstiness(text)
    results["CONCRECIÓN"] = check_specificity(text)
    results["MULETILLAS"] = check_slop(text, lex)
    results["HUELLA"] = check_fingerprint(text)
    results["VOZ"] = check_voice(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # La comprobación más floja arrastra el veredicto: a un detector le basta una señal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASA" if overall >= 70 and min(scores) >= 55 else (
        "REVISAR" if overall >= 50 else "SOSPECHOSO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANEL DE DETECCIÓN DE IA" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA HUMANA':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASA":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Señal más floja: {weakest}. Arregla esa primero.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa cuánto parece escrito por una máquina un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para la entrada estándar")
    ap.add_argument("compare", nargs="?", help="segundo archivo, para ver el antes y el después")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASA" else 1)


if __name__ == "__main__":
    main()
