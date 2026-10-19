#!/usr/bin/env python3
"""
render.py — Renderiza cada slide del HTML a PNG y revisa desbordes.

Uso:
  python render.py build/carrusel.html out/ --nombre Marca_Campana [--selector .slide] [--ancho 1080 --alto 1350]

Hace:
  1. Abre el HTML con Chromium (Playwright), espera document.fonts.ready + 700 ms.
  2. element.screenshot() de cada slide -> out/{nombre}_{n}.png  (n empieza en 1)
  3. Hoja de contacto -> out/_contacto.png
  4. Avisa (no corrige) si:
     - un slide no mide exactamente ancho x alto
     - hay texto que desborda su caja (scrollWidth/scrollHeight > client)
     - hay un elemento con texto que se sale del slide
     - alguna fuente declarada no cargó (document.fonts con status 'error')
     - alguna <img> no cargó (naturalWidth = 0)
  Los avisos se revisan con la checklist del SKILL.md. Si no hay avisos, igual MIRA cada PNG.

Para slides 4:5 usa 1080x1350; para Stories 9:16:
  --alto 1920 --selector .frame --safe-top 250 --safe-bottom 320   (avisa texto en las zonas muertas)
"""
import argparse
import sys
from pathlib import Path

JS_REVISION = r"""
([sel, W, H, SAFE_T, SAFE_B]) => {
  const out = [];
  document.querySelectorAll(sel).forEach((s, i) => {
    const n = i + 1, r = s.getBoundingClientRect();
    if (Math.round(r.width) !== W || Math.round(r.height) !== H)
      out.push(`slide ${n}: mide ${Math.round(r.width)}x${Math.round(r.height)}, debe ser ${W}x${H}`);
    s.querySelectorAll('*').forEach(el => {
      const txt = (el.innerText || '').trim();
      if (!txt || el.children.length > 0 && [...el.children].some(c => (c.innerText||'').trim() === txt)) return;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return;
      if (el.scrollWidth > el.clientWidth + 2 && cs.overflow !== 'visible' && el.clientWidth > 0)
        out.push(`slide ${n}: texto desborda en ancho -> "${txt.slice(0, 40)}"`);
      const e = el.getBoundingClientRect();
      if (e.width > 0 && (e.left < r.left - 1 || e.right > r.right + 1 || e.top < r.top - 1 || e.bottom > r.bottom + 1))
        out.push(`slide ${n}: texto se sale del slide -> "${txt.slice(0, 40)}"`);
      else if (e.width > 0 && SAFE_T + SAFE_B > 0 && (e.top < r.top + SAFE_T || e.bottom > r.bottom - SAFE_B))
        out.push(`slide ${n}: texto en zona muerta (safe zone) -> "${txt.slice(0, 40)}"`);
    });
    s.querySelectorAll('img').forEach(img => {
      if (!img.complete || img.naturalWidth === 0) out.push(`slide ${n}: imagen sin cargar -> ${(img.getAttribute('src')||'').slice(0, 60)}`);
    });
  });
  document.fonts.forEach(f => { if (f.status === 'error') out.push(`fuente con error: ${f.family} ${f.weight} ${f.style}`); });
  return out;
}
"""


def main():
    ap = argparse.ArgumentParser(description="HTML de slides -> PNG + revisión")
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--nombre", default="slide")
    ap.add_argument("--selector", default=".slide")
    ap.add_argument("--ancho", type=int, default=1080)
    ap.add_argument("--alto", type=int, default=1350)
    ap.add_argument("--escala", type=float, default=1.0, help="device_scale_factor (2 = PNG al doble)")
    ap.add_argument("--safe-top", type=int, default=0, help="Stories: 250 (zona de perfil y hora)")
    ap.add_argument("--safe-bottom", type=int, default=0, help="Stories: 320 (barra de mensaje y stickers)")
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pngs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": a.ancho + 200, "height": a.alto + 200}, device_scale_factor=a.escala)
        pg.goto(Path(a.html).resolve().as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready.then(() => true)")
        pg.wait_for_timeout(700)
        slides = pg.query_selector_all(a.selector)
        if not slides:
            sys.exit(f"No encontré elementos '{a.selector}' en {a.html}")
        avisos = pg.evaluate(JS_REVISION, [a.selector, a.ancho, a.alto, a.safe_top, a.safe_bottom])
        for i, s in enumerate(slides, start=1):
            f = out / f"{a.nombre}_{i}.png"
            s.screenshot(path=str(f))
            pngs.append(f)
        b.close()

    sys.path.insert(0, str(Path(__file__).parent))
    from efectos import hoja_contacto
    hoja_contacto(pngs, out / "_contacto.png", columnas=min(len(pngs), 5))
    print(f"{len(pngs)} PNG en {out}/  ·  hoja de contacto: {out / '_contacto.png'}")
    if avisos:
        print(f"\n{len(avisos)} AVISOS (revísalos antes de entregar):")
        for x in dict.fromkeys(avisos):
            print("  -", x)
    else:
        print("Sin avisos automáticos. Igual mira cada PNG con la checklist.")


if __name__ == "__main__":
    main()
