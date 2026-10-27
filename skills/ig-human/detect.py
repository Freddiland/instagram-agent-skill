#!/usr/bin/env python3
"""
detect.py - un panel de cinco comprobaciones que puntúa cuánto parece escrito
por una máquina un borrador.

Qué es:  cinco heurísticas locales basadas en las señales que de verdad miden
los detectores públicos de IA: variación en la longitud de las frases,
concreción, vocabulario de relleno, huella tipográfica y voz. Todo se calcula en
tu máquina a partir del texto. No se sube nada.

Qué NO es:  GPTZero, Originality, Copyleaks, Winston ni Turnitin. No llama a sus
APIs y no puede prometer su veredicto. Detecta las cosas en las que todos se
fijan, y por eso arreglarlas suele mover también sus números, pero la única
afirmación honesta es la de esta línea.

Detecta si el texto está en español o en inglés (o lo fuerzas con --lang). En
inglés, la voz se mide con contracciones ("don't", "I'm"); el español no tiene
contracciones equivalentes, así que ahí se mide con marcadores coloquiales
("vale", "pues", "o sea", "en plan"...). Esos umbrales en español son una
estimación razonada, no una calibración: tómalos como orientación.

Cada comprobación devuelve una puntuación HUMANA de 0 a 100. Más alto es mejor.

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

SENT_RE = re.compile(r"(?:[^.!?\n]|(?<=\d)[.,](?=\d))+[.!?]*")  # "1.400 €" no corta la frase
WORD_RE = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)?")
CONTRACTIONS = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PRONOUNS_EN = re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE)
PRONOUNS_ES = re.compile(r"\b(yo|me|m[ií]|mis|conmigo|nosotros|nosotras|nos|nuestro|nuestra"
                         r"|nuestros|nuestras|t[uú]|tus|te|ti|contigo|vosotros|vosotras|os"
                         r"|vuestro|vuestra|vuestros|vuestras)\b", re.IGNORECASE)
# Marcadores de registro hablado en español de España. Una máquina casi nunca
# escribe "en plan" ni "pues" en una descripción.
COLLOQUIAL_ES = re.compile(
    r"\b(?:vale|pues|o sea|en plan|t[ií]o|t[ií]a|mola|flipa\w*|eh|hombre|venga|oye|mira"
    r"|a ver|jo|buah|rollo|guay|tela|curro|currar|pasta|pillar|pill[eé]|liada|lio|l[ií]o"
    r"|movida|palo|cutre|chulo|chula|currazo|ya ves|fatal|super|s[uú]per|vamos)\b"
    r"|¿no\?|¿eh\?|¿vale\?", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d,.]*%?\b|[$€]\d|\d\s?€")
PROPER = re.compile(r"(?<![.!?]\s)(?<![¿¡])(?<!^)\b[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}\b", re.MULTILINE)

ES_HINTS = {"el", "la", "los", "las", "de", "que", "y", "en", "un", "una", "es", "por",
            "con", "para", "se", "lo", "mi", "te", "tu", "pero", "más", "mas", "como",
            "del", "al", "este", "esta", "esto", "hoy", "porque", "muy", "todo", "ya",
            "eso", "también", "hay", "son", "fue", "está", "yo", "sin", "cuando", "así"}
EN_HINTS = {"the", "and", "to", "of", "in", "is", "it", "you", "that", "for", "on",
            "with", "this", "my", "i", "was", "are", "but", "not", "have", "be", "at",
            "so", "we", "they", "what", "your", "just", "do", "can", "don't", "it's"}

ACCENTS = {"a": "aáà", "e": "eéè", "i": "iíï", "o": "oóò", "u": "uúü"}
BASE = {c: k for k, v in ACCENTS.items() for c in v}


def detect_lang(text):
    toks = re.findall(r"[^\W\d_]+(?:'[a-z]+)?", text.lower())
    es = sum(1 for t in toks if t in ES_HINTS)
    en = sum(1 for t in toks if t in EN_HINTS)
    return "en" if en > es else "es"


def lexeme_pattern(find):
    out = []
    for ch in find:
        low = ch.lower()
        if low in BASE:
            out.append("[" + ACCENTS[BASE[low]] + "]")
        elif ch == " ":
            out.append(r"\s+")
        else:
            out.append(re.escape(ch))
    return re.compile(r"(?<!\w)" + "".join(out) + r"(?!\w)", re.IGNORECASE)


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Lleva value a 0-100, donde `human` -> 100 y `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """Las personas varían mucho la longitud de las frases. Los modelos escriben parejo."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "demasiado corto para juzgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variación {cv:.2f} en {len(lens)} frases (lo ideal: 0,55 o más)"


def check_specificity(text):
    """Cifras, nombres y sustantivos concretos. El relleno es abstracto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "demasiado corto para juzgar"
    per100 = 100 / len(w)
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} dato(s) concreto(s), {density:.1f} por cada 100 palabras (lo ideal: 4 o más)"


def check_slop(text, lex, lang):
    """Densidad de vocabulario de relleno según el léxico."""
    w = words(text)
    if not w:
        return 50.0, "vacío"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        if entry.get("lang", "en") != lang:
            continue
        n = len(lexeme_pattern(entry["find"]).findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} término(s) de relleno, {density:.1f} por cada 100 palabras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caracteres que no produce el teclado de un móvil."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”«»")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisible(s), {em} raya(s), {curly} comilla(s) curva(s) o angular(es), "
              f"{ellip} puntos suspensivos de un carácter, {nbsp} espacio(s) duro(s)")
    return score, detail


def check_voice(text, lex, lang):
    """Registro, persona y las formas por las que tiran los modelos."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "demasiado corto para juzgar"
    per100 = 100 / len(w)
    if lang == "es":
        register = len(COLLOQUIAL_ES.findall(text)) * per100
        person = len(PRONOUNS_ES.findall(text)) * per100
        register_label = "marcadores coloquiales"
        register_human = 1.5
    else:
        register = len(CONTRACTIONS.findall(text)) * per100
        person = len(PRONOUNS_EN.findall(text)) * per100
        register_label = "contracciones"
        register_human = 3.0
    tells = 0
    names = []
    for s in lex["structures"]:
        if s.get("lang", "en") not in (lang, "any"):
            continue
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(register, human=register_human, machine=0.0) * 0.35
             + scale(person, human=8.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("uniform-bullets")
    detail = (f"{register:.1f} {register_label}, {person:.1f} pronombres personales "
              f"por cada 100 palabras, {tells} señal(es) estructural(es)")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["RITMO", "CONCRECIÓN", "RELLENO", "HUELLA", "VOZ"]


def run(text, lex, lang="auto"):
    if lang == "auto":
        lang = detect_lang(text)
    results = {}
    results["RITMO"] = check_burstiness(text)
    results["CONCRECIÓN"] = check_specificity(text)
    results["RELLENO"] = check_slop(text, lex, lang)
    results["HUELLA"] = check_fingerprint(text)
    results["VOZ"] = check_voice(text, lex, lang)
    scores = [results[c][0] for c in CHECKS]
    # La comprobación más débil arrastra el veredicto: a un detector le basta una señal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "APTO" if overall >= 70 and min(scores) >= 55 else (
        "REVISAR" if overall >= 50 else "MARCADO")
    return results, overall, verdict, lang


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, lang, label=None, out=sys.stdout):
    title = "PANEL DE DETECCIÓN DE IA" + (f"  -  {label}" if label else "") + f"  ·  idioma: {lang}"
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA HUMANA':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "APTO":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Señal más débil: {weakest}. Arregla esa primero.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa cuánto parece escrito por una máquina un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("compare", nargs="?", help="segundo archivo, para ver el antes y el después")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lang", default="auto", choices=["auto", "es", "en"],
                    help="idioma del texto (por defecto se detecta)")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload, rendered = [], []
    for name, text in targets:
        results, overall, verdict, lang = run(text, lex, args.lang)
        rendered.append((name, results, overall, verdict, lang))
        payload.append({
            "source": name,
            "lang": lang,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for name, results, overall, verdict, lang in rendered:
        render(results, overall, verdict, lang,
               label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "APTO" else 1)


if __name__ == "__main__":
    main()
