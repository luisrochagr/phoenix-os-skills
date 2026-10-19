#!/usr/bin/env python3
"""
efectos.py — Recursos del método NIVEL ALTO para componer slides (Pillow + numpy).

Importar desde el script de composición:
    import sys; sys.path.insert(0, "<carpeta de la skill>/scripts")
    from efectos import *

Funciones:
    recortar_fondo(path)                 -> RGBA sin fondo (rembg si está; si el PNG ya trae alfa, lo usa)
    grade(im, color=(90,140,230))        -> luz de borde con el color del ambiente + tono frío
    perspective(im, top_shrink, skew)    -> producto en perspectiva (se estrecha arriba)
    motion_blur(im, dx, dy)              -> desenfoque de movimiento (fantasmas)
    rot_point(px, py, w, h, ang, scale)  -> dónde queda un punto tras escalar + rotar (PIL rotate ccw, expand)
    place(canvas, im, cx, cy, alpha)     -> pega centrado en (cx, cy)
    fondo_espacio(w, h, ...)             -> fondo de espacio con nebulosas, estrellas y planeta opcional
    fondo_luz(w, h, base, luz, pos)      -> fondo oscuro con UNA luz dominante (esquina o centro)
    grano(im, fuerza)                    -> grano de papel / película
    estela(w, h, p0, p1, ...)            -> capa con 5-7 trazos de aire de p0 a p1
    fantasmas(canvas, im, p0, p1, n)     -> 2-3 copias con motion blur en la trayectoria
    difuminar_zona(im, caja, radio)      -> difumina logos ajenos conservando el alfa
    hoja_contacto(paths, salida)         -> hoja con todos los PNG para revisar
Probado con Pillow 12 y numpy 2.
"""
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter


# ---------------------------------------------------------------- recortes
def recortar_fondo(path, min_lado=500):
    """Quita el fondo. Si el PNG ya trae transparencia real, la usa. Escala 2x las fotos chicas."""
    im = Image.open(path)
    if im.mode in ("RGBA", "LA") and np.array(im.split()[-1]).min() < 250:
        out = im.convert("RGBA")
    else:
        try:
            from rembg import new_session, remove  # pip install "rembg[cpu]" --break-system-packages
        except ImportError as e:
            raise SystemExit('Falta rembg: pip install "rembg[cpu]" --break-system-packages') from e
        out = remove(im.convert("RGB"), session=new_session("isnet-general-use"), alpha_matting=True).convert("RGBA")
    out = out.crop(out.getbbox() or (0, 0, *out.size))
    if min(out.size) < min_lado:
        out = out.resize((out.width * 2, out.height * 2), Image.LANCZOS)
    return out


# ---------------------------------------------------------------- luz y geometría
def grade(im, strength=.45, dy=14, dx=4, cool=.92, color=(90, 140, 230)):
    """Luz de borde con el color del ambiente + corrección fría, para que todo parezca de la misma escena."""
    a = np.array(im.split()[3]).astype(float) / 255
    rgb = np.array(im)[..., :3].astype(float) * np.array([.9, .93, 1.0]) * cool
    e = np.clip(a - np.roll(np.roll(a, -dy, 0), -dx, 1), 0, 1) * a
    e = np.array(Image.fromarray((e * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(4))).astype(float) / 255 * a
    rgb += e[..., None] * np.array(color) * 1.6 * strength
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a * 255]).astype("uint8"), "RGBA")


def perspective(im, top_shrink=.16, skew=.06):
    w, h = im.size
    return im.transform((w, h), Image.QUAD, [w * top_shrink, 0, 0, h, w, h, w * (1 - top_shrink) + w * skew, 0], Image.BICUBIC)


def motion_blur(im, dx, dy, steps=14):
    acc = sum(np.array(im.transform(im.size, Image.AFFINE, (1, 0, -dx * (i / (steps - 1) - .5), 0, 1, -dy * (i / (steps - 1) - .5)),
                                    Image.BILINEAR)).astype(float) for i in range(steps))
    return Image.fromarray((acc / steps).astype("uint8"), "RGBA")


def rot_point(px, py, w, h, ang, scale):
    """Desplazamiento desde el centro de la imagen rotada (PIL rotate ccw con expand) para el punto (px, py) del original."""
    x, y = (px - w / 2) * scale, (py - h / 2) * scale
    t = math.radians(ang)
    return x * math.cos(t) + y * math.sin(t), -x * math.sin(t) + y * math.cos(t)


def place(canvas, im, cx, cy, alpha=1.0):
    if alpha < 1:
        a = im.split()[3].point(lambda v: int(v * alpha))
        im = im.copy()
        im.putalpha(a)
    canvas.alpha_composite(im, (int(cx - im.size[0] / 2), int(cy - im.size[1] / 2)))


# ---------------------------------------------------------------- fondos
def _nebulosa(w, h, cx, cy, sx, sy, color, fuerza):
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    g = np.exp(-(((xx - cx) / sx) ** 2 + ((yy - cy) / sy) ** 2))
    return g[..., None] * np.array(color) * fuerza


def fondo_espacio(w=2160, h=2700, base=(6, 7, 10), acento=(150, 180, 230), planeta=True, horizonte=.86,
                  nebulosas=((.25, .3, .10), (.8, .55, .06)), estrellas=2400, seed=7):
    """Espacio casi negro con UNA luz dominante. Componer a 2x (2160x2700) y reducir a 1080x1350."""
    rnd = random.Random(seed)
    arr = np.zeros((h, w, 3)) + np.array(base, float)
    for fx, fy, fz in nebulosas:  # nebulosas gaussianas al 5-14%
        arr += _nebulosa(w, h, w * fx, h * fy, w * .35, h * .25, acento, fz)
    img = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB")
    d = ImageDraw.Draw(img)
    for _ in range(estrellas):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        b = int(rnd.random() ** 3 * 230)
        r = .6 if b < 150 else 1.3
        d.ellipse((x - r, y - r, x + r, y + r), fill=(b, b, min(255, b + 12)))
    if planeta:
        r = 2050 * w / 2160
        cy = h * horizonte + r
        yy, xx = np.mgrid[0:h, 0:w].astype(float)
        dist = np.sqrt((xx - w / 2) ** 2 + (yy - cy) ** 2)
        arr = np.array(img).astype(float)
        dentro = dist < r
        arr[dentro] = arr[dentro] * .15 + np.array(base) * .85  # el planeta tapa estrellas
        borde = np.exp(-((dist - r) / 34) ** 2) * .55
        atm = np.where(dist > r, np.exp(-(dist - r) / 130), 0) * .35
        arr += (borde + atm)[..., None] * np.array(acento)
        img = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB")
    return ImageChops.lighter(img, img.filter(ImageFilter.GaussianBlur(3))).convert("RGBA")


def fondo_luz(w=1080, h=1350, base=(10, 10, 12), luz=(0, 85, 255), pos=(1.0, 0.0), radio=.9, fuerza=.28):
    """Fondo oscuro con una luz de esquina o de centro. pos en fracción del lienzo."""
    arr = np.zeros((h, w, 3)) + np.array(base, float)
    arr += _nebulosa(w, h, w * pos[0], h * pos[1], w * radio, h * radio * .8, luz, fuerza)
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB").convert("RGBA")


def grano(im, fuerza=10, seed=3):
    rng = np.random.default_rng(seed)
    arr = np.array(im.convert("RGBA")).astype(float)
    arr[..., :3] += rng.normal(0, fuerza, arr.shape[:2])[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGBA")


# ---------------------------------------------------------------- movimiento
def estela(w, h, p0, p1, trazos=6, color=(205, 225, 255), amplitud=60, ancho_max=7, seed=5):
    """Trazos curvos finos al inicio y gruesos al final; dos desenfoques sumados (3 + 10 px). Tiene que VERSE."""
    rnd = random.Random(seed)
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) or 1
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    for k in range(trazos):
        off = (k - (trazos - 1) / 2) * amplitud / trazos * 2
        fase = rnd.uniform(0, math.pi)
        pts = []
        for i in range(41):
            t = i / 40
            onda = math.sin(t * math.pi * 1.2 + fase) * amplitud * .35
            pts.append((x0 + (x1 - x0) * t + nx * (off * t + onda * t), y0 + (y1 - y0) * t + ny * (off * t + onda * t)))
        for i in range(40):
            t = i / 40
            d.line([pts[i], pts[i + 1]], fill=color + (int(40 + 200 * t),), width=max(1, int(1 + ancho_max * t)))
    return ImageChops.add(capa.filter(ImageFilter.GaussianBlur(3)), capa.filter(ImageFilter.GaussianBlur(10)))


def fantasmas(canvas, im, p0, p1, n=3, alphas=(.07, .13, .19), escala=.75):
    """Copias pequeñas en la trayectoria con motion blur. El producto final va NÍTIDO (pégalo después)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    for i in range(n):
        t = (i + 1) / (n + 1)
        g = im.resize((max(1, int(im.width * escala)), max(1, int(im.height * escala))), Image.LANCZOS)
        g = motion_blur(g, dx * .08, dy * .08)
        place(canvas, g, p0[0] + dx * t, p0[1] + dy * t, alphas[min(i, len(alphas) - 1)])


def difuminar_zona(im, caja, radio=12):
    """Difumina un logo ajeno (NASA, banderas, marcas) dentro de caja=(x0,y0,x1,y1) conservando el alfa."""
    im = im.copy()
    zona = im.crop(caja)
    alfa = zona.split()[3]
    borrosa = zona.filter(ImageFilter.GaussianBlur(radio))
    borrosa.putalpha(alfa)
    im.paste(borrosa, caja[:2])
    return im


def sombra_horneada(im, dx=18, dy=44, blur=26, opacidad=.5):
    """Sombra dentro del PNG (útil si se exporta con html2canvas, que no soporta drop-shadow)."""
    pad = blur * 3 + max(abs(dx), abs(dy))
    out = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    s = Image.new("RGBA", im.size, (0, 0, 0, 255))
    s.putalpha(im.split()[3].point(lambda v: int(v * opacidad)))
    out.alpha_composite(s, (pad + dx, pad + dy))
    out = out.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(im, (pad, pad))
    return out


# ---------------------------------------------------------------- revisión
def hoja_contacto(paths, salida, ancho_miniatura=360, columnas=5, fondo=(40, 40, 40)):
    ims = [Image.open(p).convert("RGB") for p in paths]
    if not ims:
        raise ValueError("No hay imágenes para la hoja de contacto")
    th = [im.resize((ancho_miniatura, round(im.height * ancho_miniatura / im.width))) for im in ims]
    filas = math.ceil(len(th) / columnas)
    alto = max(t.height for t in th)
    hoja = Image.new("RGB", (columnas * (ancho_miniatura + 16) + 16, filas * (alto + 16) + 16), fondo)
    for i, t in enumerate(th):
        hoja.paste(t, (16 + (i % columnas) * (ancho_miniatura + 16), 16 + (i // columnas) * (alto + 16)))
    Path(salida).parent.mkdir(parents=True, exist_ok=True)
    hoja.save(salida)
    return salida
