#!/usr/bin/env python3
"""
beats.py - convierte el guion de un Reel en una escaleta cronometrada antes de grabar.

Calcula cuánto se tarda en decir cada línea, las apila en códigos de tiempo y
marca las cuatro cosas que matan un Reel en la edición: un hook que pasa de los
tres segundos, un bloque lo bastante largo como para que el espectador se vaya,
varias líneas seguidas sin nada concreto, y una duración total que no cuadra con
lo que dijiste que ibas a hacer.

Los tiempos son una estimación a partir del número de palabras y un ritmo en
palabras por minuto. Sirven para planificar la edición, no sustituyen a grabar.
Pon tu propio ritmo con --wpm cuando te hayas cronometrado leyendo un guion en
voz alta. En español las palabras son más cortas y hay más palabras de enlace
que en inglés, así que el ritmo en palabras por minuto suele salir algo más
alto: la mayoría de la gente cae entre 150 y 210, y aquí el valor por defecto es
170. Mídete: es una estimación, no un dato.

Uso
  python3 beats.py guion.txt
  python3 beats.py guion.txt --target 30
  python3 beats.py guion.txt --wpm 185 --target 45
  pbpaste | python3 beats.py -
  python3 beats.py guion.txt --json
"""

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[\w$€%'’-]+")
# El punto de los miles («18.000») no cierra frase.
SENT_RE = re.compile(r"(?:[^.!?]|(?<=\d)\.(?=\d))+[.!?]*")
CAP_WORD = re.compile(r"(?<!\w)[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}(?!\w)")
CONCRETE_RE = re.compile(
    r"[$€]\s?\d|\d[\d.,]*\s?(?:€|%)|(?<!\w)\d[\d.,]*(?!\w)|"
    r"(?<!\w)(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|quince|veinte|"
    r"treinta|cuarenta|cincuenta|cien|mil|mill[oó]n|millones|euros?|lunes|martes|"
    r"mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo|enero|febrero|marzo|abril|mayo|junio|"
    r"julio|agosto|septiembre|octubre|noviembre|diciembre)(?!\w)", re.IGNORECASE)
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "e", "o", "u", "pero",
    "si", "de", "del", "a", "al", "en", "por", "para", "con", "sin", "que", "esto",
    "este", "esta", "eso", "ese", "esa", "lo", "le", "les", "se", "es", "son", "era",
    "fue", "ser", "estar", "está", "están", "tú", "tu", "tus", "te", "yo", "mi", "mis",
    "me", "nos", "os", "su", "sus", "él", "ella", "ellos", "así", "solo", "no", "ni",
    "ya", "hay", "he", "ha", "has", "hemos", "muy", "más", "como", "cuando", "uno",
    "todo", "todos", "qué", "cómo", "porque", "pues",
}

HOOK_WINDOW = 3.0        # segundos. Después de esto, el pulgar ya ha decidido.
MAX_BEAT = 4.0           # segundos en una idea sin que cambie nada en pantalla.
ABSTRACT_RUN = 3         # bloques seguidos sin nada comprobable.


def words(text):
    # «18.000» es una palabra al decirlo, así que aquí también.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text))


def concrete(text):
    """Cifras, cantidades dichas con letra, días, meses y nombres propios."""
    n = len(CONCRETE_RE.findall(text))
    for m in CAP_WORD.finditer(text):
        before = text[:m.start()].rstrip(" \t¿¡\"«(")
        if before and before[-1] not in ".!?:\n":
            n += 1
    return n


def pretty(token):
    """Vuelve a poner el punto de los miles para mostrarlo."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def split_beats(raw, wps):
    """Una línea es un bloque, salvo que sea demasiado larga para serlo."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Párrafo largo: se parte por las frases para que los tiempos signifiquen
        # algo, y el informe dice que se ha partido.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=170, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": n,
            "text": text,
            "concrete": concrete(text),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    # Etiqueta las posiciones sobre las que de verdad se construye un Reel.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "HOOK"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "HOOK" else "HOOK/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MITAD"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"el hook dura {rows[0]['dur']:.1f} s, pasa de los {HOOK_WINDOW:.0f} s")
        notes.append(f"El bloque 1 tarda {rows[0]['dur']:.1f} s en decirse. Déjalo en "
                     f"{int(HOOK_WINDOW * wps)} palabras o menos, o el hook llega cuando "
                     "la decisión ya está tomada.")
    if rows[0]["concrete"] == 0:
        notes.append("El bloque 1 no tiene ninguna cifra ni ningún nombre. Los hooks sin "
                     "nada comprobable son los que se pasan de largo.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f} s en un solo bloque")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Bloque(s) {', '.join(map(str, long_beats))}: pasan de {MAX_BEAT:.0f} s. "
                     "Parte la línea o cambia lo que se ve en pantalla dentro de ella. "
                     "Un plano quieto es donde la gente se va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Los bloques {start}-{r['n']} no tienen nada concreto. "
                             "Mete una cifra, un nombre o un precio en alguno.")
        else:
            run, start = 0, None

    # ¿La última línea te devuelve a la primera?
    def keep(w):
        return w.lower() not in STOPWORDS and any(c.isalnum() for c in w)
    first = {w.lower() for w in words(rows[0]["text"]) if keep(w)}
    last = {w.lower() for w in words(rows[-1]["text"]) if keep(w)}
    loop = sorted(pretty(w) for w in first & last)
    if loop:
        notes.append(f"Hay bucle: el último bloque repite «{', '.join(loop[:3])}» del hook. "
                     "Las segundas reproducciones son alcance gratis.")
    else:
        notes.append("No hay bucle. El último bloque no comparte ninguna palabra con el hook, "
                     "así que el vídeo acaba plano. Repetir una palabra del bloque 1 es la "
                     "segunda reproducción más barata que vas a conseguir.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"La duración cuadra ({total:.1f} s frente a {target:g} s).")
        elif delta > 0:
            notes.append(f"{delta:.1f} s por encima del objetivo. Recorta unas {int(delta * wps)} palabras.")
        else:
            notes.append(f"{-delta:.1f} s por debajo del objetivo. Añade {int(-delta * wps)} palabras "
                         "o grábalo corto. Corto suele ser lo correcto.")

    return {
        "wpm": wpm, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"ESCALETA  ·  {a['total_words']} palabras  ·  ~{a['total_seconds']:.1f} s "
            f"a {a['wpm']:g} ppm" + (f"  ·  objetivo {a['target']:g} s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<8}" if r["label"] else " " * 8
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<8}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Cronometra el guion de un Reel en una escaleta.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del guion, o - para la entrada estándar")
    ap.add_argument("--wpm", type=float, default=170, help="ritmo al hablar en palabras por minuto (por defecto 170)")
    ap.add_argument("--target", type=float, help="duración objetivo en segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("guion vacío", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
