#!/usr/bin/env python3
"""
outlier.py — Puntaje outlier del Radar de referentes, calculado en código (nunca a ojo).

Entrada: un CSV con una fila por reel (ver ESQUEMA abajo).
Salida (en --out):
  reels_puntuados.csv   cada reel con x, conv, edad, estado y etiquetas TOP
  resumen.json          por creador: mediana, tops, ganadores, fallidos, fijados, avisos
  resumen.md            tablas listas para revisar o pegar en el reporte

Uso:
  python outlier.py datos/reels.csv --out analisis/ [--hoy 2026-10-18] [--creadores datos/creadores.csv]

ESQUEMA de reels.csv (encabezados en minúscula; las columnas opcionales pueden faltar):
  creador      @ sin arroba (obligatoria)
  shortcode    código del reel (obligatoria)
  views        número o texto de Instagram: 1,2 M · 45.6K · 12,3 mil · 1.234 (obligatoria)
  fijado       1/0, si/no, true/false (obligatoria)
  likes        número o texto (obligatoria; vacío = likes ocultos)
  comentarios  número o texto (obligatoria)
  fecha        AAAA-MM-DD (obligatoria)
  url, caption, duracion_s, formato, hook   (opcionales; `formato` activa el conteo de formatos probados)

ESQUEMA de creadores.csv (opcional): creador, seguidores, idioma, bio

Reglas (las mismas del SKILL.md):
  - La mediana de cada creador sale de sus reels NO fijados con 5 días o más.
    Si quedan menos de 5, se usa todo lo no fijado y se avisa (mediana inestable).
  - x = views / mediana del creador (1 decimal).  conv = comentarios por 1.000 likes.
  - 3x o más = estudiar · 5x o más = replicar · 0,5x o menos (con 5+ días) = fallido.
  - Reels de menos de 5 días = "nuevo": nunca cuentan como fallidos.
  - Fijados se reportan aparte: su x dice qué construyó la cuenta, no cómo le va hoy.
  - Par A/B: mismo creador, misma fecha, uno rinde 3 veces o más que el otro.
"""
import argparse
import csv
import json
import re
import statistics
import sys
from datetime import date, datetime
from pathlib import Path

OBLIGATORIAS = ["creador", "shortcode", "views", "fijado", "likes", "comentarios", "fecha"]
DIAS_MADURO = 5
MIN_LIKES_CONV = 30  # por debajo, "más conversación por like" es ruido


# ---------------------------------------------------------------- parseo
def parse_num(v):
    """Convierte '1,2 M', '45.6K', '12,3 mil', '1.234', '1,234', '987' a int. Vacío -> None."""
    if v is None:
        return None
    s = str(v).strip().lower().replace(" ", " ")
    if s in ("", "-", "—", "n/a", "na", "none", "null", "oculto"):
        return None
    s = s.replace("views", "").replace("reproducciones", "").replace("likes", "").strip()
    mult = 1
    m = re.match(r"^([\d.,\s]+)\s*(k|mil|m|mill\.?|millones|mm|b)?$", s)
    if not m:
        raise ValueError(f"No entiendo el número: {v!r}")
    num, suf = m.group(1).replace(" ", ""), (m.group(2) or "")
    if suf in ("k", "mil"):
        mult = 1_000
    elif suf in ("m", "mill", "mill.", "millones", "mm"):
        mult = 1_000_000
    elif suf == "b":
        mult = 1_000_000_000
    if suf:  # con sufijo, la coma o el punto es decimal
        return int(round(float(num.replace(",", ".")) * mult))
    if "," in num and "." in num:  # 1.234,5 o 1,234.5: el último separador es el decimal
        dec = "," if num.rfind(",") > num.rfind(".") else "."
        mil = "." if dec == "," else ","
        return int(round(float(num.replace(mil, "").replace(dec, "."))))
    for sep in (",", "."):
        if sep in num:
            partes = num.split(sep)
            if all(len(p) == 3 for p in partes[1:]):  # separador de miles
                return int("".join(partes))
            return int(round(float(num.replace(sep, "."))))
    return int(num)


def parse_bool(v):
    return str(v).strip().lower() in ("1", "si", "sí", "true", "yes", "y", "x", "fijado")


def parse_fecha(v):
    s = str(v).strip()[:10]
    return datetime.strptime(s, "%Y-%m-%d").date()


def fmt_x(x):
    return "—" if x is None else f"{x:.1f}".replace(".", ",") + "x"


def fmt_num(n):
    if n is None:
        return "—"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}".replace(".", ",").replace(",0", "") + "M"
    if n >= 10_000:
        return f"{n/1_000:.0f}K"
    if n >= 1_000:
        return f"{n/1_000:.1f}".replace(".", ",").replace(",0", "") + "K"
    return str(n)


# ---------------------------------------------------------------- análisis
def cargar(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    if not filas:
        sys.exit(f"{path} está vacío.")
    faltan = [c for c in OBLIGATORIAS if c not in filas[0]]
    if faltan:
        sys.exit(f"A {path} le faltan columnas obligatorias: {', '.join(faltan)}")
    return filas


def analizar(filas, hoy, creadores_info):
    avisos, reels, vistos = [], [], set()
    for i, f in enumerate(filas, start=2):
        sc = f["shortcode"].strip()
        cr = f["creador"].strip().lstrip("@")
        if (cr, sc) in vistos:
            avisos.append(f"Fila {i}: reel duplicado {cr}/{sc}, se ignora.")
            continue
        vistos.add((cr, sc))
        try:
            r = {
                "creador": cr,
                "shortcode": sc,
                "url": (f.get("url") or "").strip() or f"https://www.instagram.com/reel/{sc}/",
                "views": parse_num(f["views"]),
                "fijado": parse_bool(f["fijado"]),
                "likes": parse_num(f["likes"]),
                "comentarios": parse_num(f["comentarios"]) or 0,
                "fecha": parse_fecha(f["fecha"]),
                "caption": (f.get("caption") or "").strip(),
                "duracion_s": f.get("duracion_s") or "",
                "formato": (f.get("formato") or "").strip(),
                "hook": (f.get("hook") or "").strip(),
            }
        except ValueError as e:
            avisos.append(f"Fila {i} ({cr}/{sc}): {e}. Se ignora.")
            continue
        if r["views"] is None:
            avisos.append(f"Fila {i} ({cr}/{sc}): sin views, se ignora.")
            continue
        if r["likes"] is None:
            avisos.append(f"{cr}/{sc}: likes ocultos; conv queda vacío.")
        r["edad_dias"] = (hoy - r["fecha"]).days
        if r["edad_dias"] < 0:
            avisos.append(f"{cr}/{sc}: fecha en el futuro ({r['fecha']}). Revisa --hoy o la fecha.")
        reels.append(r)

    por_creador = {}
    for r in reels:
        por_creador.setdefault(r["creador"], []).append(r)

    resumen = {"hoy": hoy.isoformat(), "creadores": {}, "pares_ab": [], "formatos": {}, "avisos": avisos}
    for cr, lista in por_creador.items():
        no_fijados = [r for r in lista if not r["fijado"]]
        base = [r for r in no_fijados if r["edad_dias"] >= DIAS_MADURO]
        inestable = False
        if len(base) < 5:
            inestable = True
            base = no_fijados or lista
            avisos.append(f"{cr}: solo {len([r for r in no_fijados if r['edad_dias'] >= DIAS_MADURO])} reels maduros; "
                          f"mediana calculada con {len(base)} reels (inestable).")
        med = statistics.median(r["views"] for r in base) if base else 0
        if med <= 0:
            avisos.append(f"{cr}: mediana 0; no se puede calcular x.")
        for r in lista:
            r["mediana_creador"] = med
            r["x"] = round(r["views"] / med, 1) if med else None
            r["conv"] = round(r["comentarios"] / r["likes"] * 1000) if r["likes"] else None
            if r["fijado"]:
                r["estado"] = "fijado"
            elif r["edad_dias"] < DIAS_MADURO:
                r["estado"] = "nuevo"
            elif r["x"] is not None and r["x"] >= 5:
                r["estado"] = "replicar"
            elif r["x"] is not None and r["x"] >= 3:
                r["estado"] = "estudiar"
            elif r["x"] is not None and r["x"] <= 0.5:
                r["estado"] = "fallido"
            else:
                r["estado"] = "normal"
            r["tops"] = []

        recientes = [r for r in no_fijados if r["edad_dias"] >= DIAS_MADURO and r["x"] is not None]

        def marcar(r, etiqueta):
            if r:
                r["tops"].append(etiqueta)
                return r["shortcode"]
            return None

        tops = {
            "top_views": marcar(max(no_fijados, key=lambda r: r["views"], default=None), "TOP VIEWS"),
            "top_likes": marcar(max((r for r in no_fijados if r["likes"]), key=lambda r: r["likes"], default=None), "TOP LIKES"),
            "top_comentarios": marcar(max(no_fijados, key=lambda r: r["comentarios"], default=None), "TOP COMENT."),
            "mejor_reciente": marcar(max(recientes, key=lambda r: r["x"], default=None), "MEJOR RECIENTE"),
            "mas_conversacion": marcar(max((r for r in no_fijados if r["conv"] is not None and (r["likes"] or 0) >= MIN_LIKES_CONV),
                                           key=lambda r: r["conv"], default=None), "MÁS CONVERSACIÓN"),
            "peor_reciente": marcar(min(recientes, key=lambda r: r["x"], default=None), "PEOR RECIENTE"),
        }
        info = creadores_info.get(cr, {})
        resumen["creadores"][cr] = {
            "reels": len(lista),
            "fijados": len(lista) - len(no_fijados),
            "base_mediana": len(base),
            "mediana_views": med,
            "mediana_inestable": inestable,
            "seguidores": parse_num(info.get("seguidores")) if info.get("seguidores") else None,
            "idioma": info.get("idioma", ""),
            "tops": tops,
            "ganadores": [r["shortcode"] for r in sorted(lista, key=lambda r: -(r["x"] or 0)) if r["estado"] in ("replicar", "estudiar")],
            "fallidos": [r["shortcode"] for r in sorted(lista, key=lambda r: (r["x"] or 0)) if r["estado"] == "fallido"],
            "fijados_detalle": [{"shortcode": r["shortcode"], "x": r["x"]} for r in lista if r["fijado"]],
        }
        if len(lista) < 9:
            avisos.append(f"{cr}: muestra chica ({len(lista)} reels). Repórtalo en límites.")

        # pares A/B: mismo día, maduros, no fijados
        por_dia = {}
        for r in recientes:
            por_dia.setdefault(r["fecha"], []).append(r)
        for dia, rs in por_dia.items():
            if len(rs) < 2:
                continue
            alto, bajo = max(rs, key=lambda r: r["x"]), min(rs, key=lambda r: r["x"])
            if bajo["x"] and alto["x"] / bajo["x"] >= 3:
                resumen["pares_ab"].append({
                    "creador": cr, "fecha": dia.isoformat(),
                    "gana": alto["shortcode"], "x_gana": alto["x"],
                    "pierde": bajo["shortcode"], "x_pierde": bajo["x"],
                    "nota": "Confirma en las tiras que sea el mismo set/formato antes de usarlo como A/B.",
                })

    # formatos probados (solo si se etiquetó la columna formato)
    etiquetados = [r for r in reels if r["formato"] and not r["fijado"] and r["x"] is not None]
    if etiquetados:
        formatos = {}
        for r in etiquetados:
            d = formatos.setdefault(r["formato"], {"ganadores": {}, "fallidos": 0, "total": 0})
            d["total"] += 1
            if r["x"] >= 3:
                d["ganadores"].setdefault(r["creador"], []).append(r["shortcode"])
            if r["estado"] == "fallido":
                d["fallidos"] += 1
        for fmt, d in formatos.items():
            n_cr = len(d["ganadores"])
            n_win = sum(len(v) for v in d["ganadores"].values())
            d["estado"] = "probado" if n_cr >= 2 else ("a probar" if n_win >= 2 else "sin evidencia")
        resumen["formatos"] = formatos

    return reels, resumen


# ---------------------------------------------------------------- salida
def escribir(reels, resumen, out):
    out.mkdir(parents=True, exist_ok=True)
    campos = ["creador", "shortcode", "url", "fecha", "edad_dias", "fijado", "views", "likes", "comentarios",
              "mediana_creador", "x", "conv", "estado", "tops", "formato", "hook", "duracion_s", "caption"]
    with open(out / "reels_puntuados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for r in sorted(reels, key=lambda r: (r["creador"], -(r["x"] or 0))):
            fila = dict(r)
            fila["fecha"] = r["fecha"].isoformat()
            fila["tops"] = " | ".join(r["tops"])
            fila["fijado"] = int(r["fijado"])
            w.writerow(fila)

    with open(out / "resumen.json", "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2, default=str)

    idx = {(r["creador"], r["shortcode"]): r for r in reels}
    L = [f"# Radar — puntaje outlier (hoy: {resumen['hoy']})", ""]
    L += ["| Creador | Reels | Mediana | Mejor reciente | Ganadores (3x+) | Fallidos | Nota |", "|---|---|---|---|---|---|---|"]
    for cr, d in resumen["creadores"].items():
        mr = idx.get((cr, d["tops"]["mejor_reciente"]))
        L.append(f"| @{cr} | {d['reels']} ({d['fijados']} fijados) | {fmt_num(d['mediana_views'])} | "
                 f"{fmt_x(mr['x']) if mr else '—'} | {len(d['ganadores'])} | {len(d['fallidos'])} | "
                 f"{'mediana inestable' if d['mediana_inestable'] else ''} |")
    L += ["", "## Ganadores (3x o más)", "", "| Creador | Reel | x | Views | Coment. | conv | Estado | Tops |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted((r for r in reels if r["estado"] in ("replicar", "estudiar")), key=lambda r: -r["x"]):
        L.append(f"| @{r['creador']} | [{r['shortcode']}]({r['url']}) | {fmt_x(r['x'])} | {fmt_num(r['views'])} | "
                 f"{r['comentarios']} | {r['conv'] if r['conv'] is not None else '—'} | {r['estado']} | {', '.join(r['tops'])} |")
    L += ["", "## Fallidos (0,5x o menos, 5+ días)", "", "| Creador | Reel | x | Views |", "|---|---|---|---|"]
    for r in sorted((r for r in reels if r["estado"] == "fallido"), key=lambda r: r["x"]):
        L.append(f"| @{r['creador']} | [{r['shortcode']}]({r['url']}) | {fmt_x(r['x'])} | {fmt_num(r['views'])} |")
    L += ["", "## Fijados (aparte)", "", "| Creador | Reel | x |", "|---|---|---|"]
    for r in (r for r in reels if r["fijado"]):
        L.append(f"| @{r['creador']} | [{r['shortcode']}]({r['url']}) | {fmt_x(r['x'])} |")
    if resumen["pares_ab"]:
        L += ["", "## Pares A/B candidatos", ""]
        for p in resumen["pares_ab"]:
            L.append(f"- @{p['creador']} {p['fecha']}: {p['gana']} ({fmt_x(p['x_gana'])}) vs {p['pierde']} ({fmt_x(p['x_pierde'])})")
    if resumen["formatos"]:
        L += ["", "## Formatos", "", "| Formato | Estado | Creadores con 3x+ | Fallidos | Total |", "|---|---|---|---|---|"]
        for fmt, d in sorted(resumen["formatos"].items(), key=lambda kv: kv[1]["estado"]):
            L.append(f"| {fmt} | {d['estado']} | {', '.join('@' + c for c in d['ganadores']) or '—'} | {d['fallidos']} | {d['total']} |")
    if resumen["avisos"]:
        L += ["", "## Avisos (van a 'Límites' del reporte si aplican)", ""] + [f"- {a}" for a in resumen["avisos"]]
    (out / "resumen.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Puntaje outlier del Radar de referentes.")
    ap.add_argument("reels", help="CSV con una fila por reel")
    ap.add_argument("--out", default="analisis", help="Carpeta de salida")
    ap.add_argument("--hoy", default=None, help="Fecha de corte AAAA-MM-DD (default: hoy)")
    ap.add_argument("--creadores", default=None, help="CSV opcional con seguidores/idioma/bio")
    a = ap.parse_args()

    hoy = parse_fecha(a.hoy) if a.hoy else date.today()
    info = {}
    if a.creadores:
        with open(a.creadores, newline="", encoding="utf-8-sig") as f:
            info = {r["creador"].strip().lstrip("@"): r for r in csv.DictReader(f)}
    reels, resumen = analizar(cargar(a.reels), hoy, info)
    escribir(reels, resumen, Path(a.out))
    n_cr = len(resumen["creadores"])
    n_win = sum(len(d["ganadores"]) for d in resumen["creadores"].values())
    print(f"OK: {len(reels)} reels de {n_cr} creadores · {n_win} ganadores (3x+) · "
          f"{len(resumen['pares_ab'])} pares A/B · {len(resumen['avisos'])} avisos -> {a.out}/")


if __name__ == "__main__":
    main()
