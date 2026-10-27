#!/usr/bin/env python3
"""
humanize.py - quita la huella de máquina de un borrador en español.

Tres pasadas, en este orden:

  1. INVISIBLES   borra o normaliza los caracteres que un teclado humano no
                  produce: espacios de ancho cero, unidores de palabra, guiones
                  blandos, BOM, caracteres de etiqueta Unicode, espacios duros y
                  estrechos. Sobreviven al copiar y pegar y son la huella más
                  mecánica de un texto generado.
  2. TIPOGRAFÍA   raya -> coma, semirraya -> guion, comillas curvas -> rectas,
                  carácter de puntos suspensivos -> tres puntos, viñeta -> guion.
                  Las comillas latinas «» y los signos ¿ ¡ se respetan: son
                  español correcto, no huella.
  3. LÉXICO       sustituye las muletillas de slop.json por palabras normales,
                  ignorando tildes y mayúsculas al buscar, conservando las
                  mayúsculas al sustituir y sin tocar los enlaces.

Las señales estructurales («No es solo X, es Y», tríadas, muros de hashtags,
mayúsculas en cada palabra del título) se INFORMAN, nunca se reescriben solas:
cambiar la forma de una frase necesita criterio, y eso es trabajo del modelo,
no de una expresión regular.

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
# El punto de los miles («18.000») no cierra frase.
SENT_RE = re.compile(r"(?:[^.!?\n]|(?<=\d)\.(?=\d))+[.!?]*")

# Cada vocal acepta su versión con tilde (y la u, la diéresis), para que
# «crucial», «Crucial» y una «adentremonos» escrita sin tilde caigan igual.
_ACCENTS = {"a": "aá", "e": "eé", "i": "ií", "o": "oó", "u": "uúü", "n": "nñ"}
_ACCENTS.update({"á": "aá", "é": "eé", "í": "ií", "ó": "oó", "ú": "uúü", "ü": "uúü", "ñ": "nñ"})


def accent_pattern(phrase):
    """Expresión que encuentra `phrase` sin importar tildes, mayúsculas ni espacios."""
    out = []
    for ch in phrase.lower():
        if ch == "n":
            out.append("n")                 # la ñ no se pierde: «año» no es «ano»
        elif ch in _ACCENTS:
            out.append("[" + _ACCENTS[ch] + "]")
        elif ch.isspace():
            out.append(r"\s+")
        else:
            out.append(re.escape(ch))
    # Bordes por caracteres de palabra, no por \b: así funcionan también las
    # entradas que empiezan por ¿ o terminan en ?
    return re.compile(r"(?<!\w)" + "".join(out) + r"(?!\w)", re.IGNORECASE)


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> 0x200b;  'U+E0000-U+E007F' -> (inicio, fin)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Cambia los enlaces por marcadores para que ninguna pasada los toque."""
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
    # Cualquier otro carácter de formato (Cf) es invisible por definición.
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
            # Raya de diálogo a principio de línea: se quita sin más.
            text = re.sub(r"(?m)^([ \t]*)—\s*", r"\1", text)
            # Inciso «palabra — palabra» o «palabra—palabra»: coma y espacio.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10 -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # usada como raya
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # Una coma insertada delante de otra puntuación queda mal.
    text = re.sub(r",\s*([,.;:!?»])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    first = next((c for c in src if c.isalpha()), "")
    if first.isupper():
        i = next((k for k, c in enumerate(repl) if c.isalpha()), 0)
        return repl[:i] + repl[i].upper() + repl[i + 1:]
    return repl


def pass_lexical(text, lex):
    """Sustituye muletillas. Primero las más largas, para que ganen las frases."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        pattern = accent_pattern(entry["find"])
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": entry["find"], "replace": entry["replace"] or "(borrado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Limpieza tras los borrados. Quitar una cláusula entera deja puntuación
    # huérfana («sistema. .», una línea que empieza por coma, «. , y luego»),
    # y eso queda peor que la muletilla.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)      # un espacio dejado por un borrado.
                                                     # Las sangrías más hondas son a propósito.
    text = re.sub(r"\s+([,.;:!?»])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?»])", r"\1", text)     # una raya se volvió coma y luego
                                                     # se borró la cláusula de detrás
    text = re.sub(r"([.!?])\s*,\s*", r"\1 ", text)    # «frase. , y sigue» -> «frase. Y sigue»
    text = re.sub(r"([¿¡])\s*,\s*", r"\1", text)      # «¿, qué...» -> «¿qué...»
    text = text.replace("...", "\x00ELL\x00")         # protege los puntos suspensivos reales
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    # Una frase que se ha quedado en una conjunción suelta («... Y.») sobra.
    text = re.sub(r"(?:(?<=[.!?])|^)\s*(?:y|e|o|ni|pero)\s*[.!?]+", "", text,
                  flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Una raya convertida en coma seguida de un conector deja dos frases
    # pegadas («es importante, además, demuestra»). Se convierte en punto.
    text = re.sub(r",\s*(además|así que|aun así|básicamente|al final)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
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
                "fix": "Parte una frase en dos. Deja que otra se alargue. La máquina escribe igualado.",
            })
    return flags


_START = r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))(\s*[¿¡\"«(]*)([a-záéíóúñü])"


def restore_capitals(original, text):
    """Borrar una apertura deja la palabra siguiente en minúscula.

    Solo se corrige si quien escribe pone mayúscula al empezar frase: una voz
    en minúsculas a propósito es un estilo, no un defecto, y pisarla sería
    justo lo que este script existe para evitar.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*[¿¡\"«(]*([A-Za-zÁÉÍÓÚÑÜáéíóúñü])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(_START, lambda m: m.group(1) + m.group(2).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("INFORME DEL HUMANIZADOR")
    print(f"{total} huellas de máquina eliminadas, "
          f"{len(report['structures'])} señales estructurales marcadas para reescribir", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISIBLES")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFÍA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. MULETILLAS")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. SEÑALES ESTRUCTURALES  (no se arreglan solas: reescríbelas tú)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPIO")
        print("  No hay nada que quitar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Quita la huella de máquina de un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para la entrada estándar")
    ap.add_argument("-o", "--out", help="escribe aquí el texto limpio en vez de en pantalla")
    ap.add_argument("--report", action="store_true", help="muestra qué ha cambiado (por stderr)")
    ap.add_argument("--json", action="store_true", help="devuelve {text, report} en JSON")
    ap.add_argument("--lexicon", default=LEX, help="ruta a slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"escrito {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
