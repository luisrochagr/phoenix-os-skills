# Pipeline técnico (Python + Pillow + HTML + Playwright)

Probado en el entorno de Claude (Linux, Pillow 12, Playwright con Chromium). En una máquina local hace falta: Python 3.10+, `pip install pillow numpy playwright pypdf --break-system-packages`, `playwright install chromium`, y Node/npm para las fuentes.

---

## Carpetas y scripts

```
proyecto/
  recursos/      lo que manda el usuario (fotos, PNG, logo)
  s/             recursos preparados (recortes graduados, fondos, capas bg/fg)
  build/         fuentes.css + carrusel.html
  out/           PNG finales + _contacto.png
  prep.py        prepara recursos (recortes, grade, perspectiva, escenas)
  build.py       arma el HTML
```

Scripts de la skill (en `scripts/`):

```bash
python scripts/fuentes.py anton:400 inter:400,700,900 playfair-display:800i -o build/fuentes.css
python scripts/render.py build/carrusel.html out/ --nombre {Marca}_{Campaña}
```

Y en `prep.py`: `sys.path.insert(0, "<skill>/scripts"); from efectos import *`.

---

## Fuentes

- **Google Fonts suele estar bloqueado** en el entorno, y cargar fuentes por link hace que cambien al exportar. Siempre: `scripts/fuentes.py` → `@font-face` en base64 con `font-display:block`.
- **Set por defecto (si la marca no tiene):** Anton (palabra gigante) · Playfair Display 800 itálica (acento) · Inter 400/700/900 (apoyo y editorial).
- Otras de Fontsource que funcionan: `pinyon-script` (manuscrita, estilo B), `playfair-display:900` (titulares serif con impacto), `quattrocento-sans`, `fraunces`, `jost`, `bebas-neue`, `archivo-black`, `dm-serif-display`.
- Si la marca tiene una fuente propia (.woff2/.otf/.ttf), embébela en base64 igual: `src:url(data:font/woff2;base64,...)`.
- Autoajuste de palabras gigantes: cada línea gigante va en su propio elemento `.gig` con `white-space:nowrap` y `display:inline-block`, y un script al cargar reduce el `font-size` mientras el ancho pase de 940–960 px:

```js
document.fonts.ready.then(()=>document.querySelectorAll('.gig').forEach(el=>{
  let s=parseFloat(getComputedStyle(el).fontSize);
  while(el.scrollWidth>950&&s>40){s-=2;el.style.fontSize=s+'px';}}));
```

## Recortes

- `efectos.recortar_fondo(path)`: si el PNG ya trae alfa, lo usa; si no, rembg (`pip install "rembg[cpu]" --break-system-packages`, sesión `isnet-general-use`, `alpha_matting=True`) y recorta al bbox. Fotos de menos de 500 px se escalan 2× antes de graduar.
- Logos ajenos en personajes u objetos (agencias, banderas, marcas): `efectos.difuminar_zona(im, caja)`.
- **Recortes con borde recto** (personaje que se asoma desde el borde de una tarjeta):
  - Mide la columna/fila del corte leyendo el alfa por filas.
  - Posiciona con `left = anchoContenedor - xCorte*escala` y `top = altoContenedor - yCorte*escala`.
  - Lo que sobresale del corte (la mano que agarra el borde) se recorta aparte y se pone encima, fuera del contenedor.

## Hook con escena compleja (dos capas)

Componer a 2× (2160×2700) en Pillow y reducir a 1080×1350, en dos capas:

- `bg.png` (detrás del texto): `efectos.fondo_espacio()` o `fondo_luz()` o la escena del usuario, graduada.
- `fg.png` (encima del texto, transparente): personaje, estela, fantasmas, producto, primer plano desenfocado.

Orden en el HTML: bg → cuadrícula → palabras (z 1) → fg (z 3) → caja keyword (z 5) → editorial y botón (z 6–8).

Colocar al personaje por un punto clave (ej. la mano o el casco): `acx = objetivo_x - rot_point(px, py, w, h, ang, escala)[0]`.

**Fondo de espacio** (`efectos.fondo_espacio`): base (6,7,10) + 2 nebulosas gaussianas al 6–10 %; planeta = círculo de radio ~2050 a 2× centrado bajo el lienzo, borde al 55 % y atmósfera al 35 % en el color de acento; ~2400 estrellas; glow final. Varía posición e intensidad de las nebulosas por slide (`seed`, `nebulosas=`); el planeta se usa en el hook y en el cierre.

## Slides de producto

Recursos ya graduados, posicionados con CSS (`position:absolute`, `transform:rotate`), brillos en divs radiales, tarjetas con `overflow:hidden` para los acercamientos, personaje como `<img>`.

## Imágenes en el HTML

- **Todo embebido en base64** (data URI): rutas locales y URLs externas pueden salir en blanco al exportar.
- WebP q92 para recortes, JPEG q92 para fondos. HTML final entre 0,5 y 1,5 MB.
- Si el HTML se va a exportar con html2canvas en otra herramienta, las sombras van horneadas en el PNG (`efectos.sombra_horneada`), porque html2canvas no soporta `drop-shadow`.

## Render y revisión

1. `scripts/render.py` → un PNG por slide, `_contacto.png` y avisos (tamaño del slide, texto que desborda o se sale, fuentes con error, imágenes sin cargar).
2. Mira la hoja de contacto y **cada PNG**.
3. Arma recortes ampliados (Pillow `crop` + `resize` 2×) de las zonas delicadas: estela, tarjetas, personajes, bordes rectos.
4. Pasa la checklist del SKILL.md. Itera hasta que no quede nada.

## Entrega

- PNG: `{Marca}_{Campaña}_{n}.png` (1080×1350).
- HTML editable (todo embebido, abre en cualquier navegador).
- Caption en bloque de código.
- Si el usuario quiere exportar desde el navegador sin Python, agrega al HTML un botón con html2canvas 1.4.1 (`scale:2`, `width:1080`, `height:1350`, `backgroundColor` explícito, `useCORS:true`, `await document.fonts.ready` antes, ~600 ms entre descargas).
