#!/usr/bin/env python3
"""
img_to_base64.py — Prepara imágenes para incrustarlas en el HTML (Stories o carruseles).

Qué hace, por cada imagen de una carpeta (o archivos sueltos):
  1. Convierte HEIC/HEIF a JPG si hace falta.
  2. Redimensiona a máx. --max-width px de ancho (default 1080), calidad ~82.
  3. Genera el data URI  data:image/jpeg;base64,...  y lo guarda en un .txt.
  4. Arma un HTML de prueba (_preview.html) que embebe TODAS las imágenes,
     para verificar que renderizan antes de construir el carrusel final.

Por qué base64: html2canvas "ensucia" (taints) el canvas con rutas locales o
URLs externas y no pinta la imagen. Incrustada como data URI, siempre se ve.

Uso:
  python img_to_base64.py <carpeta_o_imagen> [-o salida] [--max-width 1080] [--quality 82] [--alpha]

  --alpha  conserva la transparencia (WebP con alfa) para recortes de producto o personaje.
           Sin --alpha, todo se aplana sobre blanco a JPEG (fotos a sangre).

Requisitos: Pillow.  Para HEIC: pillow-heif (opcional; si no está, avisa y omite HEIC).
  pip install Pillow pillow-heif --break-system-packages
"""
import argparse
import base64
import io
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Falta Pillow. Instala:  pip install Pillow --break-system-packages")

# Soporte HEIC opcional
try:
    import pillow_heif  # type: ignore
    pillow_heif.register_heif_opener()
    HEIC_OK = True
except Exception:
    HEIC_OK = False

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".bmp", ".tif", ".tiff"}


def collect_images(path: Path):
    if path.is_file():
        return [path]
    return sorted(p for p in path.iterdir() if p.suffix.lower() in EXTS)


def process(img_path: Path, max_width: int, quality: int, alpha: bool = False):
    """Devuelve (data_uri, ancho, alto) tras convertir/redimensionar (JPEG, o WebP con alfa si alpha=True)."""
    ext = img_path.suffix.lower()
    if ext in {".heic", ".heif"} and not HEIC_OK:
        print(f"  ⚠️  {img_path.name}: HEIC no soportado (instala pillow-heif). Omitido.")
        return None

    im = Image.open(img_path)
    if alpha:
        im = im.convert("RGBA")
        if im.width > max_width:
            im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="WEBP", quality=max(quality, 90))
        return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode("ascii"), im.width, im.height
    # Aplanar transparencia sobre blanco para JPG
    if im.mode in ("RGBA", "P", "LA"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")

    if im.width > max_width:
        h = round(im.height * max_width / im.width)
        im = im.resize((max_width, h), Image.LANCZOS)

    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=quality, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}", im.width, im.height


def main():
    ap = argparse.ArgumentParser(description="Imágenes -> base64 data URI para Stories y carruseles.")
    ap.add_argument("input", help="Carpeta con imágenes o una imagen suelta.")
    ap.add_argument("-o", "--output", default=None, help="Carpeta de salida (default: <input>/base64).")
    ap.add_argument("--max-width", type=int, default=1080, help="Ancho máximo en px (default 1080).")
    ap.add_argument("--quality", type=int, default=82, help="Calidad JPEG (default 82).")
    ap.add_argument("--alpha", action="store_true", help="Conserva transparencia (WebP con alfa).")
    args = ap.parse_args()

    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        sys.exit(f"No existe: {in_path}")

    out_dir = Path(args.output).expanduser().resolve() if args.output else (
        (in_path if in_path.is_dir() else in_path.parent) / "base64"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    images = collect_images(in_path)
    if not images:
        sys.exit("No se encontraron imágenes.")

    print(f"Procesando {len(images)} imagen(es) -> {out_dir}")
    preview_imgs = []
    for img in images:
        result = process(img, args.max_width, args.quality, args.alpha)
        if not result:
            continue
        data_uri, w, h = result
        txt_path = out_dir / f"{img.stem}.txt"
        txt_path.write_text(data_uri, encoding="utf-8")
        kb = len(data_uri) / 1024
        print(f"  ✓ {img.name}  ({w}×{h}, ~{kb:.0f} KB base64)  -> {txt_path.name}")
        preview_imgs.append((img.stem, data_uri, w, h))

    # HTML de prueba
    cards = "\n".join(
        f'<figure><img src="{uri}" alt="{name}"><figcaption>{name} · {w}×{h}</figcaption></figure>'
        for name, uri, w, h in preview_imgs
    )
    preview = f"""<!doctype html><meta charset="utf-8">
<title>Preview base64 — {len(preview_imgs)} imágenes</title>
<style>
 body{{font-family:system-ui,Arial,sans-serif;background:#111;color:#eee;margin:0;padding:24px}}
 h1{{font-size:18px;font-weight:600}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}}
 figure{{margin:0;background:#1c1c1c;border-radius:10px;overflow:hidden}}
 img{{width:100%;display:block}}
 figcaption{{padding:8px 10px;font-size:12px;color:#aaa}}
</style>
<h1>Verifica que TODAS las imágenes se ven (ninguna en blanco). {len(preview_imgs)} imágenes.</h1>
<div class="grid">{cards}</div>
"""
    preview_path = out_dir / "_preview.html"
    preview_path.write_text(preview, encoding="utf-8")
    print(f"\nHTML de prueba: {preview_path}")
    print("Abre ese archivo y confirma que todas las imágenes renderizan antes de armar el carrusel.")


if __name__ == "__main__":
    main()
