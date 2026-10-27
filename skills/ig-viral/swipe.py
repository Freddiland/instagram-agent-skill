#!/usr/bin/env python3
"""
swipe.py - ordena los reels que has recopilado según cuánto superaron a su
propia cuenta, nombra la fórmula de hook de cada uno y escribe el archivo de
referencias (swipe file).

La razón de ser de este script es una corrección: las visitas a secas no son
una prueba. Una cuenta de 2.000.000 de seguidores con 400.000 visitas ha tenido
un día flojo. Una cuenta de 4.000 seguidores con 400.000 visitas ha dado con
algo. Esto ordena por el múltiplo sobre la referencia de la propia cuenta, que
es la única versión de «se hizo viral» que te dice algo que puedas copiar.

La entrada es un archivo separado por tabuladores que rellenas mientras
navegas, un reel por fila, con una línea de cabecera con los nombres de las
columnas (en español o en inglés):

    cuenta    seguidores   mediana   visitas   hook
    @alguien  48000        11000     412000    nadie te cuenta que tus primeros 30 fracasan

`mediana` son las visitas habituales recientes de esa cuenta y es la mejor
referencia. Si solo tienes `seguidores`, deja la mediana vacía y el script lo
dirá. `hook` es la primera frase del reel, dicha o en pantalla, con sus palabras.

Uso
  python3 swipe.py capturados.tsv
  python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
  python3 swipe.py capturados.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")
WORD_RE = re.compile(r"[\w$€%'’-]+")

# Nombres de columna aceptados, en español o en inglés.
COLUMNS = {
    "cuenta": "account", "account": "account",
    "seguidores": "followers", "followers": "followers",
    "mediana": "median", "median": "median",
    "visitas": "views", "vistas": "views", "reproducciones": "views", "views": "views",
    "hook": "hook", "gancho": "hook",
}

try:                                              # opcional: puntuar también los hooks
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
except Exception:                                 # ig-viral copiado sin ig-reel
    score_hook = None


def fold(text):
    """Minúsculas y sin tildes, para que «cuentá» y «cuenta» casen igual."""
    t = unicodedata.normalize("NFD", text)
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE),
             re.compile(fold(by_id[i]["match"]), re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    """Prueba el hook tal cual y sin tildes: en los comentarios casi nadie las pone."""
    if not formulas:
        return None, "sin clasificar"
    plain = fold(hook)
    for fid, name, pattern, folded in formulas:
        if pattern.search(hook) or folded.search(plain):
            return fid, name
    return None, "sin clasificar"


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [COLUMNS.get(fold(c.strip().lower()), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        try:
            r["views"] = int(re.sub(r"[^\d]", "", r.get("views", "")) or 0)
        except ValueError:
            continue
        for k in ("followers", "median"):
            digits = re.sub(r"[^\d]", "", r.get(k, "") or "")
            r[k] = int(digits) if digits else None
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    return {
        "baseline": "mediana de la cuenta" if used_median else "número de seguidores",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == "sin clasificar"),
    }


def render(a, out=sys.stdout):
    head = (f"REFERENCIAS  ·  {a['n']} reels  ·  {a['accounts']} cuentas  ·  "
            f"referencia: {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        views = f"{r['views']:,}".replace(",", ".")
        print(f"  {mult:>7}  hook {score:>3}  {fid} {r['formula'][:22]:<22} "
              f"{r.get('account', '')[:16]:<16} {views:>9}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("QUÉ ESTÁ FUNCIONANDO EN ESTE LOTE", file=out)
    if a["top_formulas"]:
        print("  tercio superior por múltiplo:  "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  nota mediana del hook:         arriba {a['top_hook_score']:.0f}  "
              f"frente a abajo {a['bottom_hook_score']:.0f}", file=out)
    print(f"  longitud mediana del hook:     arriba {a['top_words']} palabras  "
          f"frente a abajo {a['bottom_words']} palabras", file=out)
    print(f"  sin clasificar:                {a['unclassified']} de {a['n']}. Léelos a mano: "
          "ahí se esconde una fórmula que aún no tienes.", file=out)
    print("\n  Un lote recogido a mano es un indicio, no una prueba. Doce reels no "
          "enseñan nada;\n  cuarenta de seis cuentas enseñan algo. Recoge más antes "
          "de creértelo.\n", file=out)


def to_markdown(a):
    dots = lambda n: f"{n:,}".replace(",", ".")
    lines = ["# Archivo de referencias (swipe file)", "",
             f"{a['n']} reels de {a['accounts']} cuentas. "
             f"Ordenados por múltiplo sobre la referencia ({a['baseline']}).", ""]
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- visitas: {dots(r['views'])}  referencia: {dots(r['baseline'])}",
                  f"- nota del hook: {r['hook_score']}  palabras: {r['words']}",
                  f"- hook: «{r['hook']}»", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Ordena los reels recopilados por múltiplo sobre su cuenta.")
    ap.add_argument("input", nargs="?", default="-", help="archivo TSV, o - para la entrada estándar")
    ap.add_argument("--hooks", default=HOOKS, help="ruta a ig-reel/hooks.json")
    ap.add_argument("--out", help="escribe también aquí el archivo de referencias en markdown")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("no hay filas utilizables. Hace falta un archivo separado por tabuladores con, "
              "al menos, visitas y hook.", file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("aviso: no se encuentra hooks.json, las fórmulas no se nombran. Usa --hooks.",
              file=sys.stderr)
    if score_hook is None:
        print("aviso: no se puede importar hookscore.py, se omiten las notas de los hooks.",
              file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"escrito {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
