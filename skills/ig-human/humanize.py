#!/usr/bin/env python3
"""
humanize.py - quita la huella de máquina de un borrador.

Tres pasadas, en este orden:

  1. INVISIBLES   borra o normaliza los caracteres que un teclado humano nunca
                  produce: espacios y uniones de ancho cero, word joiners,
                  guiones blandos, BOM, caracteres de etiqueta Unicode, espacios
                  de no separación y estrechos. Sobreviven al copiar y pegar y
                  son la señal más mecánica de cualquier texto generado.
  2. TIPOGRAFÍA   raya -> coma, guion medio -> guion, comillas curvas o
                  angulares -> rectas, puntos suspensivos de un carácter -> tres
                  puntos, viñeta -> guion. Los signos de apertura ¿ y ¡ no se
                  tocan nunca.
  3. LÉXICO       sustituye el léxico de relleno de slop.json por palabras
                  normales, conservando las mayúsculas y sin tocar los enlaces.

Detecta si el texto está en español o en inglés y aplica solo las entradas de
ese idioma. Puedes forzarlo con --lang es o --lang en.

Las señales estructurales (tríadas, "no es solo X, es Y", muros de hashtags)
se SEÑALAN, nunca se reescriben solas: cambiar la forma de una frase necesita
criterio, así que eso es trabajo del modelo, no de una expresión regular.

Uso
  python3 humanize.py borrador.txt
  python3 humanize.py borrador.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py borrador.txt --json
  python3 humanize.py borrador.txt -o limpio.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"(?:[^.!?\n]|(?<=\d)[.,](?=\d))+[.!?]*")  # "1.400 €" no corta la frase

ES_HINTS = {"el", "la", "los", "las", "de", "que", "y", "en", "un", "una", "es", "por",
            "con", "para", "se", "lo", "mi", "te", "tu", "pero", "más", "mas", "como",
            "del", "al", "este", "esta", "esto", "hoy", "porque", "muy", "todo", "ya",
            "eso", "también", "hay", "son", "fue", "está", "yo", "sin", "cuando", "así"}
EN_HINTS = {"the", "and", "to", "of", "in", "is", "it", "you", "that", "for", "on",
            "with", "this", "my", "i", "was", "are", "but", "not", "have", "be", "at",
            "so", "we", "they", "what", "your", "just", "do", "can", "don't", "it's"}


def detect_lang(text):
    """'es' o 'en' según qué palabras frecuentes dominan. Empate: español."""
    toks = re.findall(r"[^\W\d_]+(?:'[a-z]+)?", text.lower())
    es = sum(1 for t in toks if t in ES_HINTS)
    en = sum(1 for t in toks if t in EN_HINTS)
    return "en" if en > es else "es"


ACCENTS = {"a": "aáà", "e": "eéè", "i": "iíï", "o": "oóò", "u": "uúü"}
BASE = {c: k for k, v in ACCENTS.items() for c in v}


def lexeme_pattern(find):
    """Patrón de una entrada del léxico: sin distinguir tildes ni mayúsculas, y con
    límites de palabra que también funcionan si la entrada empieza o acaba en un
    signo."""
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


def entries_for(lex, lang):
    return [e for e in lex["phrases"] + lex["words"] if e.get("lang", "en") == lang]


def structures_for(lex, lang):
    return [s for s in lex["structures"] if s.get("lang", "en") in (lang, "any")]


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> '\\u200b';  'U+E0000-U+E007F' -> (inicio, fin)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Cambia los enlaces por marcadores para que ninguna pasada reescriba dentro."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Borra o convierte en espacio los caracteres invisibles. Devuelve (texto, hallazgos)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": "borrado" if entry["action"] == "delete" else "espacio"})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Cualquier carácter de formato (Cf) que quede es invisible por definición.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "otros caracteres de formato invisibles", "count": len(stray),
                     "action": "borrado"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n,
                     "to": entry["to"].strip() or "(espacio)"})
        if ch == "—":
            # " palabra — palabra " y "palabra—palabra" acaban en coma + espacio.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # usado como raya
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # Una coma insertada delante de otra puntuación queda mal. Una raya al
    # principio de línea (diálogo) tampoco debe dejar una coma colgando.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    text = re.sub(r"(?m)^,\s*", "", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def pass_lexical(text, lex, lang):
    """Sustituye palabras y frases de relleno. Las más largas primero, para que
    las frases ganen a las palabras sueltas."""
    hits = []
    entries = sorted(entries_for(lex, lang), key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        pattern = lexeme_pattern(find)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(borrado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Limpieza tras los borrados. Borrar una cláusula entera deja puntuación
    # huérfana ("sistema. ." o una línea que ahora empieza con una coma), y eso
    # queda peor que el relleno.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # un espacio que dejó un borrado.
                                                      # Las sangrías más hondas son a propósito.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)      # una raya pasó a coma y luego
                                                      # se borró la cláusula de detrás
    text = re.sub(r"([¿¡])\s+", r"\1", text)           # "¿ qué" tras un borrado
    text = re.sub(r"([¿¡])[,;:]\s*", r"\1", text)
    text = re.sub(r"¿\s*\?|¡\s*!", "", text)           # una pregunta que se quedó vacía
    text = text.replace("...", "\x00ELL\x00")          # protege los puntos suspensivos reales
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Una raya que pasó a coma seguida de un conector deja dos frases pegadas
    # ("es importante, además, es una prueba"). Se convierte en punto.
    text = re.sub(r",\s*(also|so|still|basically|in the end|además|así que|aun así|básicamente"
                  r"|al final|también)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex, lang):
    flags = []
    for s in structures_for(lex, lang):
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # La uniformidad en la longitud de las frases también es estructural.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Frases de longitud uniforme (variación {cv:.2f})",
                "count": len(lens),
                "fix": "Parte una frase por la mitad. Deja que otra se alargue. Las máquinas "
                       "escriben parejo.",
            })
    return flags


SENT_START = r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))"


def restore_capitals(original, text):
    """Borrar un arranque deja la siguiente palabra en minúscula.

    Solo se arregla para quien ya pone mayúscula al empezar las frases: escribir
    todo en minúsculas a propósito es un estilo, no un error, y pasarle por
    encima sería justo lo que este script existe para evitar.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*[¿¡\"«(]*([^\W\d_])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text

    def up(m):
        lead, letter = m.group(1), m.group(2)
        return lead + letter.upper()

    return re.sub(SENT_START + r"(\s*[¿¡\"(]*)([^\W\d_])", up, text)


def humanize(text, lex, lang="auto"):
    if lang == "auto":
        lang = detect_lang(text)
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex, lang)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "lang": lang,
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex, lang),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("INFORME DEL HUMANIZADOR")
    print(f"idioma: {report['lang']}  ·  {total} restos de máquina eliminados, "
          f"{len(report['structures'])} señales estructurales para reescribir", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISIBLES")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFÍA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LÉXICO DE RELLENO")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. SEÑALES ESTRUCTURALES  (no se arreglan solas: reescríbelas tú)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report[k] for k in ("invisible", "typographic", "lexical", "structures")):
        head("LIMPIO")
        print("  No hay nada que quitar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Quita la huella de máquina de un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("-o", "--out", help="escribe el texto limpio aquí en vez de en stdout")
    ap.add_argument("--report", action="store_true", help="imprime lo que cambió, en stderr")
    ap.add_argument("--json", action="store_true", help="emite {text, report} en JSON")
    ap.add_argument("--lang", default="auto", choices=["auto", "es", "en"],
                    help="idioma del texto (por defecto se detecta)")
    ap.add_argument("--lexicon", default=LEX, help="ruta a slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex, args.lang)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"escrito en {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
