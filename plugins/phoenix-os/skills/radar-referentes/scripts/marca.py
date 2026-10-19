#!/usr/bin/env python3
"""
marca.py — Kit de marca Phoenix OS × Luis Rocha para los entregables del Radar.

Todo lo de marca sale de aquí, así cualquier persona del equipo que corra la skill
obtiene el mismo output brandeado sin tener que adjuntar nada.

Activos (en ../assets, ver assets/README.md):
  phoenix-logo.png      logo de Phoenix OS (fondo transparente)
  phoenix-p.png         símbolo P (mini logo); lockup() le suma 'PHOENIX OS'
  luis-rocha.png|jpg    foto de Luis
  fonts/*.otf           Inter / Inter Display (licencia OFL incluida)
Si falta un activo, se usa la marca de texto "Phoenix OS × Luis Rocha" y se avisa.

CLI:
  python marca.py check
      Revisa activos y fuentes. Córrelo al empezar.
  python marca.py tira CAPTURA.png SALIDA.png --creador maria.autos --x 6.2 --views 1200000 \
      --comentarios 340 --url https://instagram.com/reel/XXX --notas "Hook: ..." "..." "..." "..."
      Arma la tira de 4 cuadros brandeada (Paso 7).
  python marca.py css SALIDA.css [--base64]
      CSS con fuentes, colores y componentes para el HTML del PDF.
  python marca.py pdf PORTADA.html CUERPO.html SALIDA.pdf --nicho "Toyota USA" [--fecha 2026-10-18]
      Imprime portada (márgenes 0) + cuerpo A4 (márgenes 15 mm, pie de marca) y los une.
  python marca.py encabezado SALIDA.png --ancho 3600 --titulo "Radar · Toyota USA" --sub "5 referentes · oct 2026"
      Encabezado para la imagen de Miro.

Desde Python:  import sys; sys.path.insert(0, "<skill>/scripts"); import marca
"""
import argparse
import base64
import datetime as dt
import io
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    sys.exit("Falta Pillow: pip install Pillow --break-system-packages")

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONTS = ASSETS / "fonts"

NEGRO = "#000000"
LIMA = "#BDFA71"
BLANCO = "#F5F6F3"
GRIS = "#969B94"
ROJO = "#FF786C"
GRIS_OSCURO = "#1A1C1A"
FONDO_IG = (12, 16, 20)  # #0C1014, fondo oscuro de Instagram alrededor de las capturas
FIRMA = "Phoenix OS × Luis Rocha"

LOGO_NOMBRES = ["phoenix-logo.png", "phoenix-logo.webp", "phoenix-logo.jpg"]
P_NOMBRES = ["phoenix-p.png", "phoenix-p.webp"]
FOTO_NOMBRES = ["luis-rocha.png", "luis-rocha.jpg", "luis-rocha.jpeg", "luis-rocha.webp"]

PESOS = {
    "regular": "Inter-Regular.otf",
    "semibold": "Inter-SemiBold.otf",
    "bold": "Inter-Bold.otf",
    "display": "InterDisplay-Bold.otf",
    "display-black": "InterDisplay-Black.otf",
}


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _primero(nombres):
    for n in nombres:
        p = ASSETS / n
        if p.exists():
            return p
    return None


def activos():
    return {
        "logo": _primero(LOGO_NOMBRES),
        "p": _primero(P_NOMBRES),
        "foto": _primero(FOTO_NOMBRES),
        "fuentes": {k: (FONTS / v) if (FONTS / v).exists() else None for k, v in PESOS.items()},
    }


def check():
    a = activos()
    ok = True
    print("Kit de marca Phoenix OS × Luis Rocha")
    for k, etiqueta in (("logo", "Logo completo"), ("p", "Mini logo P"), ("foto", "Foto de Luis")):
        estado = a[k].name if a[k] else "FALTA -> se usa marca de texto"
        ok &= bool(a[k])
        print(f"  {etiqueta:14s} {estado}")
    for k, p in a["fuentes"].items():
        estado = p.name if p else "FALTA -> sans del sistema"
        ok &= bool(p)
        print(f"  Fuente {k:8s} {estado}")
    print("Todo listo." if ok else "Faltan activos: el entregable sale con marca de texto. Avísalo en una línea.")
    return ok


# ---------------------------------------------------------------- fuentes y textos
def fuente(peso="bold", size=24):
    p = activos()["fuentes"].get(peso)
    if p:
        return ImageFont.truetype(str(p), size)
    try:  # fallback del sistema
        ruta = subprocess.run(["fc-match", "-f", "%{file}", "Inter:bold" if "bold" in peso or "display" in peso else "Inter"],
                              capture_output=True, text=True).stdout.strip()
        return ImageFont.truetype(ruta, size)
    except Exception:
        return ImageFont.load_default(size)


def _ancho(draw, txt, f):
    return draw.textlength(txt, font=f)


def recortar(draw, txt, f, max_w):
    """Recorta con '…' si no cabe."""
    if _ancho(draw, txt, f) <= max_w:
        return txt
    while txt and _ancho(draw, txt + "…", f) > max_w:
        txt = txt[:-1]
    return txt.rstrip() + "…"


def envolver(draw, txt, f, max_w, max_lineas=2):
    palabras, lineas, actual = txt.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if _ancho(draw, prueba, f) <= max_w:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    if len(lineas) > max_lineas:
        lineas = lineas[:max_lineas]
        lineas[-1] = recortar(draw, lineas[-1] + " …", f, max_w)
    return lineas


def fmt_num(n):
    n = int(n)
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}".replace(".", ",").replace(",0", "") + "M"
    if n >= 10_000:
        return f"{n/1_000:.0f}K"
    if n >= 1_000:
        return f"{n/1_000:.1f}".replace(".", ",").replace(",0", "") + "K"
    return str(n)


def fmt_x(x):
    return f"{float(x):.1f}".replace(".", ",") + "x"


# ---------------------------------------------------------------- piezas de marca
def mini_logo(alto=44):
    """Símbolo P. Si no existe, lo recorta del logo completo (cuadro izquierdo). Si no hay logo, chip de texto."""
    a = activos()
    src = a["p"]
    if src:
        im = Image.open(src).convert("RGBA")
    elif a["logo"]:
        logo = Image.open(a["logo"]).convert("RGBA")
        bbox = logo.getbbox() or (0, 0, *logo.size)
        logo = logo.crop(bbox)
        im = logo.crop((0, 0, min(logo.height, logo.width), logo.height))
    else:
        f = fuente("display-black", int(alto * 0.62))
        im = Image.new("RGBA", (alto, alto), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, alto - 1, alto - 1), radius=alto // 4, fill=hex2rgb(LIMA))
        d.text((alto / 2, alto / 2), "P", font=f, fill=hex2rgb(NEGRO), anchor="mm")
        return im
    im = im.crop(im.getbbox() or (0, 0, *im.size))
    return im.resize((max(1, round(im.width * alto / im.height)), alto), Image.LANCZOS)


def logo_completo(alto=64):
    a = activos()
    if not a["logo"]:
        f = fuente("display-black", int(alto * 0.6))
        tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        w = int(_ancho(tmp, "PHOENIX OS", f)) + 4
        im = Image.new("RGBA", (w, alto), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((0, alto / 2), "PHOENIX OS", font=f, fill=hex2rgb(BLANCO), anchor="lm")
        return im
    im = Image.open(a["logo"]).convert("RGBA")
    im = im.crop(im.getbbox() or (0, 0, *im.size))
    return im.resize((max(1, round(im.width * alto / im.height)), alto), Image.LANCZOS)


def lockup(alto=110, texto="PHOENIX OS"):
    """Símbolo P + 'PHOENIX OS' en Inter Display Black, para encabezados sobre negro."""
    p = mini_logo(alto)
    f = fuente("display-black", int(alto * 0.42))
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    w = p.width + int(alto * 0.22) + int(_ancho(tmp, texto, f)) + 4
    im = Image.new("RGBA", (w, alto), (0, 0, 0, 0))
    im.paste(p, (0, 0), p)
    ImageDraw.Draw(im).text((p.width + int(alto * 0.22), alto / 2), texto, font=f, fill=hex2rgb(BLANCO), anchor="lm")
    return im


def foto_circulo(diam=220, borde=6):
    """Foto de Luis en círculo con borde lima. Sin foto: círculo con iniciales LR."""
    a = activos()
    out = Image.new("RGBA", (diam, diam), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.ellipse((0, 0, diam - 1, diam - 1), fill=hex2rgb(LIMA))
    interior = diam - 2 * borde
    if a["foto"]:
        foto = ImageOps.exif_transpose(Image.open(a["foto"])).convert("RGBA")
        foto = ImageOps.fit(foto, (interior, interior), Image.LANCZOS, centering=(0.5, 0.35))
    else:
        foto = Image.new("RGBA", (interior, interior), hex2rgb(GRIS_OSCURO) + (255,))
        ImageDraw.Draw(foto).text((interior / 2, interior / 2), "LR", font=fuente("display-black", interior // 3),
                                  fill=hex2rgb(LIMA), anchor="mm")
    mask = Image.new("L", (interior, interior), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, interior - 1, interior - 1), fill=255)
    out.paste(foto, (borde, borde), mask)
    return out


def chip(texto, f, pad=(14, 7), fondo=LIMA, color=NEGRO):
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    w = int(_ancho(tmp, texto, f)) + 2 * pad[0]
    h = f.size + 2 * pad[1]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=hex2rgb(fondo))
    d.text((w / 2, h / 2), texto, font=f, fill=hex2rgb(color), anchor="mm")
    return im


def a_data_uri(path_o_img, fmt="PNG"):
    if isinstance(path_o_img, (str, Path)):
        p = Path(path_o_img)
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}[p.suffix[1:].lower()]
        return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
    buf = io.BytesIO()
    path_o_img.save(buf, format=fmt)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- tira de 4 cuadros (Paso 7)
def area_util(im, tol=10):
    """Bbox de lo que no es el fondo #0C1014 de Instagram (ni blanco puro de borde)."""
    rgb = im.convert("RGB")
    fondo = Image.new("RGB", rgb.size, FONDO_IG)
    from PIL import ImageChops
    diff = ImageChops.difference(rgb, fondo).convert("L").point(lambda v: 255 if v > tol else 0)
    return diff.getbbox() or (0, 0, *rgb.size)


def cortar_cuadros(captura):
    """La tira JS mide 4×270 + 3×2 px de separación (1086×480). Escala a lo que salió en la captura."""
    im = Image.open(captura).convert("RGB")
    x0, y0, x1, y1 = area_util(im)
    im = im.crop((x0, y0, x1, y1))
    esc = im.width / 1086
    cuadros = []
    for i in range(4):
        left = round(i * 272 * esc)
        cuadros.append(im.crop((left, 0, min(im.width, left + round(270 * esc)), im.height)))
    return cuadros


def tira(captura, salida, creador, x, views, comentarios, url="", notas=None,
         chips=("0,3 s · HOOK", "2 s", "MITAD", "FINAL"), cuadro_w=300):
    """Tira brandeada: barra superior lima con métricas, mini logo, chip por cuadro, nota bajo cada cuadro y pie."""
    notas = list(notas or [])[:4] + [""] * (4 - len(notas or []))
    cuadros = cortar_cuadros(captura)
    cuadro_h = round(cuadro_w * 16 / 9)
    gap, margen, barra, nota_h, pie = 18, 28, 78, 74, 54
    W = margen * 2 + cuadro_w * 4 + gap * 3
    H = barra + cuadro_h + nota_h + pie
    out = Image.new("RGB", (W, H), hex2rgb(NEGRO))
    d = ImageDraw.Draw(out)

    f_barra, f_chip, f_nota, f_pie = fuente("bold", 22), fuente("bold", 17), fuente("semibold", 17), fuente("regular", 15)
    linea = f"@{creador.lstrip('@').upper()}  ·  {fmt_x(x)} SU MEDIANA  ·  {fmt_num(views)} VIEWS  ·  {fmt_num(comentarios)} COMENTARIOS"
    logo = mini_logo(40)
    d.text((margen, barra / 2), recortar(d, linea, f_barra, W - 2 * margen - logo.width - 20), font=f_barra,
           fill=hex2rgb(LIMA), anchor="lm")
    out.paste(logo, (W - margen - logo.width, (barra - logo.height) // 2), logo)

    for i, c in enumerate(cuadros):
        c = ImageOps.fit(c, (cuadro_w, cuadro_h), Image.LANCZOS)
        x0 = margen + i * (cuadro_w + gap)
        out.paste(c, (x0, barra))
        ch = chip(chips[i], f_chip)
        out.paste(ch, (x0 + 10, barra + 10), ch)
        for j, ln in enumerate(envolver(d, notas[i], f_nota, cuadro_w, 2)):
            d.text((x0, barra + cuadro_h + 12 + j * 24), ln, font=f_nota, fill=hex2rgb(BLANCO))

    y_pie = H - pie / 2
    d.line((margen, H - pie, W - margen, H - pie), fill=hex2rgb(GRIS_OSCURO), width=1)
    d.text((margen, y_pie), recortar(d, url, f_pie, W * 0.6), font=f_pie, fill=hex2rgb(GRIS), anchor="lm")
    d.text((W - margen, y_pie), FIRMA, font=f_pie, fill=hex2rgb(GRIS), anchor="rm")
    Path(salida).parent.mkdir(parents=True, exist_ok=True)
    out.save(salida, optimize=True)
    return salida


# ---------------------------------------------------------------- encabezado (Miro)
def encabezado(ancho=3600, titulo="Radar de referentes", sub="", alto=300):
    im = Image.new("RGB", (ancho, alto), hex2rgb(NEGRO))
    d = ImageDraw.Draw(im)
    m = 90
    logo = lockup(110)
    im.paste(logo, (m, (alto - logo.height) // 2), logo)
    foto = foto_circulo(200, 8)
    im.paste(foto, (ancho - m - foto.width, (alto - foto.height) // 2), foto)
    x_txt = m + logo.width + 80
    max_w = ancho - x_txt - foto.width - m - 80
    d.text((x_txt, alto / 2 - 30), recortar(d, titulo, fuente("display-black", 96), max_w), font=fuente("display-black", 96),
           fill=hex2rgb(BLANCO), anchor="ls")
    if sub:
        d.text((x_txt, alto / 2 + 50), recortar(d, sub, fuente("semibold", 44), max_w), font=fuente("semibold", 44),
               fill=hex2rgb(LIMA), anchor="ls")
    d.text((ancho - m - foto.width - 30, alto / 2), FIRMA, font=fuente("semibold", 34), fill=hex2rgb(GRIS), anchor="rm")
    return im


# ---------------------------------------------------------------- CSS y PDF (Paso 8)
def css(base64_fuentes=False):
    """CSS de marca para el HTML del PDF. Por defecto usa file:// (Playwright local)."""
    caras = []
    for peso, (familia, w) in {"regular": ("Inter", 400), "semibold": ("Inter", 600), "bold": ("Inter", 700),
                               "display": ("Inter Display", 700), "display-black": ("Inter Display", 900)}.items():
        p = activos()["fuentes"].get(peso)
        if not p:
            continue
        src = ("data:font/otf;base64," + base64.b64encode(p.read_bytes()).decode()) if base64_fuentes else p.as_uri()
        caras.append(f"@font-face{{font-family:'{familia}';src:url('{src}') format('opentype');font-weight:{w};font-display:block}}")
    return "\n".join(caras) + f"""
:root{{--negro:{NEGRO};--lima:{LIMA};--blanco:{BLANCO};--gris:{GRIS};--rojo:{ROJO};--gris-oscuro:{GRIS_OSCURO}}}
*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{margin:0;font-family:'Inter',system-ui,sans-serif;color:#111;background:#fff;font-size:10.5pt;line-height:1.45}}
h1,h2,h3{{font-family:'Inter Display','Inter',sans-serif;font-weight:900;letter-spacing:-.01em;margin:0 0 .4em}}
.seccion{{break-before:page}}
.seccion:first-child{{break-before:auto}}
.num{{display:inline-block;background:var(--lima);color:#000;font-weight:700;border-radius:99px;padding:2px 12px;margin-right:10px;font-size:.8em}}
.chip{{display:inline-block;background:var(--lima);color:#000;font-weight:700;border-radius:99px;padding:2px 10px;font-size:8.5pt}}
.chip.rojo{{background:var(--rojo)}}
.negro{{background:var(--negro);color:var(--blanco);border-radius:14px;padding:16px 20px}}
.negro .hook{{color:var(--lima);font-family:'Inter Display';font-weight:900;font-size:17pt;line-height:1.15}}
.lima{{color:var(--lima)}} .gris{{color:var(--gris)}} .rojo{{color:var(--rojo)}}
.metrica{{border:2px solid var(--lima);border-radius:12px;padding:10px 14px}}
.ficha{{break-inside:avoid;page-break-inside:avoid}}
table{{width:100%;border-collapse:collapse;font-size:9pt}}
th{{text-align:left;background:#000;color:var(--blanco);padding:6px 8px;font-weight:700}}
td{{padding:6px 8px;border-bottom:1px solid #e6e6e2;vertical-align:top}}
.cols2{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
img.tira{{width:100%;border-radius:8px;display:block}}
.portada{{width:210mm;height:297mm;background:#000;color:var(--blanco);padding:22mm 18mm;position:relative;overflow:hidden}}
.portada .etiqueta{{color:var(--lima);font-weight:700;letter-spacing:.14em;font-size:9pt}}
.portada h1{{font-size:44pt;line-height:1;margin-top:10mm;color:var(--blanco)}}
.portada .kpis{{display:flex;gap:10mm;margin-top:14mm}}
.portada .kpi b{{display:block;color:var(--lima);font-family:'Inter Display';font-weight:900;font-size:34pt;line-height:1}}
.portada .foto{{position:absolute;right:18mm;bottom:22mm;width:46mm;height:46mm;border-radius:50%;border:2mm solid var(--lima);object-fit:cover}}
.portada .logo{{height:12mm}}
"""


def pie_html(nicho, fecha=None):
    fecha = fecha or dt.date.today().strftime("%d/%m/%Y")
    return (f"<div style=\"width:100%;font-family:Inter,Arial,sans-serif;font-size:7.5pt;color:{GRIS};padding:0 15mm;"
            f"display:flex;justify-content:space-between\"><span>{FIRMA} · Radar de referentes · {nicho} · {fecha}</span>"
            f"<span>Página <span class=\"pageNumber\"></span> de <span class=\"totalPages\"></span></span></div>")


def pdf(portada_html, cuerpo_html, salida, nicho, fecha=None):
    """Portada aparte con márgenes 0 + cuerpo A4 con márgenes 15 mm y pie de marca; se unen con pypdf."""
    from playwright.sync_api import sync_playwright
    from pypdf import PdfWriter
    salida = Path(salida)
    tmp_p, tmp_c = salida.with_suffix(".portada.pdf"), salida.with_suffix(".cuerpo.pdf")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(Path(portada_html).resolve().as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(tmp_p), format="A4", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        pg.goto(Path(cuerpo_html).resolve().as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(tmp_c), format="A4", print_background=True, display_header_footer=True,
               header_template="<div></div>", footer_template=pie_html(nicho, fecha),
               margin={"top": "15mm", "right": "15mm", "bottom": "16mm", "left": "15mm"})
        b.close()
    w = PdfWriter()
    for f in (tmp_p, tmp_c):
        w.append(str(f))
    with open(salida, "wb") as fh:
        w.write(fh)
    tmp_p.unlink()
    tmp_c.unlink()
    return salida


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description="Kit de marca Phoenix OS × Luis Rocha")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("check")
    t = sp.add_parser("tira")
    t.add_argument("captura"); t.add_argument("salida")
    t.add_argument("--creador", required=True); t.add_argument("--x", type=float, required=True)
    t.add_argument("--views", type=int, required=True); t.add_argument("--comentarios", type=int, required=True)
    t.add_argument("--url", default=""); t.add_argument("--notas", nargs="*", default=[])
    c = sp.add_parser("css"); c.add_argument("salida"); c.add_argument("--base64", action="store_true")
    p = sp.add_parser("pdf")
    p.add_argument("portada"); p.add_argument("cuerpo"); p.add_argument("salida")
    p.add_argument("--nicho", required=True); p.add_argument("--fecha", default=None)
    e = sp.add_parser("encabezado")
    e.add_argument("salida"); e.add_argument("--ancho", type=int, default=3600)
    e.add_argument("--titulo", default="Radar de referentes"); e.add_argument("--sub", default="")
    a = ap.parse_args()

    if a.cmd == "check":
        sys.exit(0 if check() else 1)
    if a.cmd == "tira":
        print(tira(a.captura, a.salida, a.creador, a.x, a.views, a.comentarios, a.url, a.notas))
    elif a.cmd == "css":
        Path(a.salida).write_text(css(a.base64), encoding="utf-8"); print(a.salida)
    elif a.cmd == "pdf":
        print(pdf(a.portada, a.cuerpo, a.salida, a.nicho, a.fecha))
    elif a.cmd == "encabezado":
        encabezado(a.ancho, a.titulo, a.sub).save(a.salida); print(a.salida)


if __name__ == "__main__":
    main()
