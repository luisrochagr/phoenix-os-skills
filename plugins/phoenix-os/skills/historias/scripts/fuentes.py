#!/usr/bin/env python3
"""
fuentes.py — Embebe fuentes de Fontsource (npm) como @font-face en base64.

Por qué: Google Fonts suele estar bloqueado en el entorno y, aunque cargue, la fuente
puede cambiar al exportar. Embebida en base64 con font-display:block, nunca cambia.

Uso:
  python fuentes.py anton:400 inter:400,700,900 playfair-display:800i -o build/fuentes.css
  python fuentes.py fraunces:600,700,700i jost:400,500 -o build/fuentes.css --subsets latin latin-ext

Formato: <id-fontsource>:<peso>[i][,<peso>[i]...]   (i = itálica)
El id es el nombre en minúsculas con guiones (https://fontsource.org): anton, inter, playfair-display,
pinyon-script, quattrocento-sans, fraunces, jost, bebas-neue, archivo-black, dm-serif-display...

Requiere npm (usa `npm pack`, no instala nada globalmente).
"""
import argparse
import base64
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


def bajar(paquete, destino):
    r = subprocess.run(["npm", "pack", f"@fontsource/{paquete}", "--silent"], cwd=destino, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"No pude bajar @fontsource/{paquete}: {r.stderr.strip()[:300]}")
    tgz = Path(destino) / r.stdout.strip().splitlines()[-1]
    carpeta = Path(destino) / paquete
    with tarfile.open(tgz) as t:
        t.extractall(carpeta, filter="data")
    return carpeta / "package"


def caras(pkg, peso, italica, subsets):
    css_file = pkg / (f"{peso}-italic.css" if italica else f"{peso}.css")
    if not css_file.exists():
        disponibles = sorted(p.stem for p in pkg.glob("*.css") if re.match(r"^\d{3}(-italic)?$", p.stem))
        sys.exit(f"{pkg.parent.name}: no existe el peso {peso}{' itálica' if italica else ''}. Disponibles: {', '.join(disponibles)}")
    texto = css_file.read_text(encoding="utf-8")
    salida = []
    for bloque in re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})", texto, re.S):
        subset, regla = bloque
        if subset.replace(f"{pkg.parent.name}-", "") not in subsets and subset not in subsets:
            continue
        m = re.search(r"url\(\./(files/[^)]+?\.woff2)\)", regla)
        if not m:
            continue
        b64 = base64.b64encode((pkg / m.group(1)).read_bytes()).decode()
        regla = re.sub(r"src:[^;]+;", f"src:url(data:font/woff2;base64,{b64}) format('woff2');", regla)
        regla = re.sub(r"font-display:\s*\w+", "font-display:block", regla)
        salida.append(regla)
    if not salida:  # paquetes sin comentarios por subset: tomar todo
        for regla in re.findall(r"@font-face\s*\{.*?\}", texto, re.S):
            m = re.search(r"url\(\./(files/[^)]+?\.woff2)\)", regla)
            if m and any(s in m.group(1) for s in subsets):
                b64 = base64.b64encode((pkg / m.group(1)).read_bytes()).decode()
                regla = re.sub(r"src:[^;]+;", f"src:url(data:font/woff2;base64,{b64}) format('woff2');", regla)
                salida.append(re.sub(r"font-display:\s*\w+", "font-display:block", regla))
    return salida


def main():
    ap = argparse.ArgumentParser(description="Fontsource -> @font-face en base64")
    ap.add_argument("fuentes", nargs="+", help="id:pesos  (ej. anton:400 inter:400,700,900 playfair-display:800i)")
    ap.add_argument("-o", "--out", default="fuentes.css")
    ap.add_argument("--subsets", nargs="+", default=["latin", "latin-ext"])
    a = ap.parse_args()

    reglas = []
    with tempfile.TemporaryDirectory() as tmp:
        for spec in a.fuentes:
            pid, _, pesos = spec.partition(":")
            pkg = bajar(pid, tmp)
            for p in (pesos or "400").split(","):
                italica = p.endswith("i")
                n = reglas.__len__()
                reglas += caras(pkg, p.rstrip("i"), italica, a.subsets)
                print(f"  ✓ {pid} {p}  ({len(reglas) - n} subsets)")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text("\n".join(reglas) + "\n", encoding="utf-8")
    kb = Path(a.out).stat().st_size / 1024
    print(f"{a.out}: {len(reglas)} @font-face · {kb:.0f} KB. Usa la familia tal como la nombra Fontsource (ej. 'Anton', 'Playfair Display').")


if __name__ == "__main__":
    main()
