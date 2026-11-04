---
name: "tryhard-edit"
description: "Edita reels/talking-head al estilo Tryhard Edit de Luis: cortes sin huecos, gancho disruptivo, tracking de cara, títulos detrás/delante del sujeto, motion graphics, blur y mucho SFX. Úsala cuando pidan tryhard edit o editar un reel con ese nivel."
---

# Tryhard Edit

Estilo de edición de reels verticales (1080×1920) creado con Luis Rocha sobre el reel de Sebas / Adsurdo (IMG_3680, nov-2026). Resultado de referencia: `Mis reels/3 Listos/IMG_3680_v5.mp4`. Scripts base: `Mis reels/_herramientas/tryhard-edit/tryhard_render.py` (imagen) y `tryhard_mix.py` (sonido).

La meta no es "editar bonito": es **ganar la atención en el primer segundo, convencer en el desarrollo y hacer que comenten**, con un acabado limpio y profesional, posicionando la marca.

---

## 0. Antes de empezar

1. Crea la lista de tareas. Lee `Mis reels/2 Mi estilo/mi-estilo.md` y `Mis reels/reglas-de-edicion.md` si existen.
2. Pide/ubica:
   - El bruto (en `1 Brutos` o adjunto). Si pesa >30 MB no se puede subir a la carpeta: edita en el contenedor y entrega solo el resultado.
   - Marca/cliente y cómo se escribe (ej.: **Adsurdo**, no "absurdo").
   - SFX: `/Users/usuario/Documents/RECURSOS EDITS/SOUND FX` (subcarpetas UI SFX, GENERIC FX, ARTFX Community Volume 2, BLOGOVSFX). Si no está conectada, pide que la conecte con "Add folder".
   - Fuentes: `~/Library/Fonts` → SF Pro Display (BLACKITALIC, HEAVYITALIC, SEMIBOLDITALIC, REGULAR, MEDIUM, BOLD). Nota de licencia: Apple limita SF Pro a diseños para sus plataformas; Inter es la alternativa libre si el cliente lo pide.
   - Canción de fondo (opcional; si no hay, se avisa y se recomienda añadirla en Instagram).

### Entorno: trampas ya resueltas
- Transcripción con faster-whisper necesita permitir en claude.ai → Settings → Capabilities: `huggingface.co` **y** `*.hf.co` (o `us.aws.cdn.hf.co` + `cas-server.xethub.hf.co`). No intentes saltarte bloqueos del proxy.
- faster-whisper puede fallar con `av.open(... metadata_errors)`: pásale el audio como numpy (`wave` → float32/32768).
- OpenCV 5 ya no trae los haarcascades y GitHub raw está bloqueado: instala `opencv-python-headless<5` (PyPI).
- rembg `u2net_human_seg` se descarga de GitHub releases (sí funciona).
- `git clone` dentro de la carpeta compartida falla: clona fuera y copia sin `.git`.
- `device_commit_files` admite ≤30 MB por archivo.
- La shell de la Mac (device_bash) es un Linux de Cowork; el trabajo pesado va en el contenedor.

---

## 1. Transcribir
- Proxy de trabajo: `scale=-2:1280,fps=30` → `a.wav` mono 16 kHz.
- faster-whisper `small`, `language='es'`, `word_timestamps=True` → `words.json` `[inicio, fin, palabra]`.
- Los tiempos de whisper al inicio de cada frase suelen adelantarse ~0,5 s: los silencios reales se miden con `silencedetect`.

## 2. Limpiar el contenido (errores del personaje son normales)
- Detecta **tomas repetidas** (misma frase dicha 2+ veces): quédate con la **última toma completa y limpia**.
- Quita **ideas repetidas** aunque cambie la redacción (ej.: "elevan las ventas… todos los días y hace que hayan ventas… todos los días").
- Quita arranques bajitos/de fondo, cues ("Dale"), muletillas.
- Corrige texto: nombres de marca, tildes ("de qué es").

## 3. Guion y aprobación
Guarda en `3 Listos/<video>_guion.md`: tabla por momentos (segundo, lo que dice, lo que se ve, efecto, herramienta) + lista SE QUEDA / SE VA con tiempos del bruto. Pregunta máximo 3 cosas con opción recomendada. **No edites hasta el "sí"** (salvo que el usuario ya haya dado vía libre).

## 4. Estructura cognitiva (lo que manda)
En Instagram el 99% está en piloto automático. Orden obligatorio:

| Momento | Objetivo mental | Cómo |
|---|---|---|
| 0–2 s | **Disrupción** (romper el patrón, dolor/pérdida) | Abrir con la frase más fuerte aunque esté más adelante en el bruto (reordenar). Texto gigante visible desde el fotograma 0, golpe de SFX, flash, sacudida, color de alerta. |
| Desarrollo 1 | **Problema / identificación** | Visualizar el dolor (gráfica cayendo en rojo, repetición en eco). |
| Desarrollo 2 | **Solución + autoridad + marca** | Nombre de la marca gigante detrás del sujeto, insignias (IA), inserto a pantalla completa. |
| Desarrollo 3 | **Prueba / resultado** | Contraste: medidor que se llena rojo→verde, gráfica subiendo en verde. |
| Cierre | **Acción** | Palabra de acción gigante + UI de comentario que se escribe sola + cierre en eco. |

También posiciona: la marca debe verse grande al menos una vez; lenguaje de paid media (rendimiento, atención, variantes, ventas) sin inventar cifras.

## 5. Cortes: cero huecos
- Silencios con `silencedetect=n=-36dB:d=0.18` **dentro** de cada frase elegida; corta todo >0,18 s dejando 0,06 s de margen.
- Fusiona microcortes <0,15 s del mismo tramo (no saltar dentro de una palabra).
- Ajusta cada tramo a fotogramas exactos (n/30) y recorta el audio a esa duración (`apad,atrim`) con fades de 12–15 ms → sin desincronía.
- Extrae del original a **1440×2560** para que los zooms no pierdan calidad. Concat → `base.mov`. Guarda `timeline.json` (src_a, src_b, off).

## 6. Tracking de cara
- Haar frontal (+ perfil de respaldo) sobre cada fotograma reducido a 480 px.
- Filtra imposibles (y fuera de rango, tamaño absurdo), interpola huecos, mediana 9 + media 11, **por tramo** (reinicia en cada corte) → `track.json` (x, y, ancho en coords de 1440×2560).
- La cámara centra la cara en x y la coloca al 42% de alto.

## 7. Imagen: reglas del Tryhard Edit

### Zona segura de Reels (obligatoria)
Nada de texto fuera de: arriba ≥250 px, abajo ≤1350 px, derecha ≤920 px, izquierda ≥60 px. Centro horizontal de textos ≈ x 480–490. Revisa con las zonas pintadas en rojo sobre los fotogramas.

### Subtítulos rápidos
- **Siempre debajo de la cara** (tracking): y = cara_y + 0,78·ancho_cara + 55, limitado a 760–1240; x sigue la cara dentro de la zona segura.
- 1–3 palabras; no terminar trozo en palabra débil (de, tu, la, y, te, un, lo, en, es, a, que); mínimo 0,28 s en pantalla.
- SF Pro Display **Regular 72** + palabras clave en **Heavy Italic 80**, en minúsculas naturales (marca e "IA" como se escriben).
- **Sin borde negro**. Solo sombra suave (blur 12–14, opacidad ~120–150).
- Entrada con **blur-in** (desenfoque 12→0 + escala 1,05→1 en 0,2 s). Nada de rebotes.
- Se ocultan mientras hay un título grande que dice lo mismo.

### Títulos grandes (SF Pro Display Black Italic)
- **Detrás del sujeto** (máscara rembg `u2net_human_seg` a 540×960, fondo atenuado ~27%): marca, conceptos clave y la palabra de acción (FATIGA/CREATIVA, ADSURDO, VENTAS, COMENTA). Colócalos según la cara: y = cara_y − 0,72·ancho_cara − 60, para que la cabeza solo roce la base de las letras y se lean enteros. Ancho máx. 860.
- **Delante, grande**: golpes (MATA en rojo, NEGOCIOS) y cierres con **eco** (LO MISMO, MASIVA): palabra principal delante, 3 copias decrecientes detrás del sujeto.
- Entrada blur-in + escala 1,12→1; salida con blur.
- Palabras pequeñas encima de las grandes, **juntas** (poco aire).

### Motion graphics (catálogo)
- Tarjeta de vidrio esmerilado (crop del fondo + blur 24 + blanco 150–175 alfa, radio 40, sombra suave) en la franja 290–600 px.
- Gráfica de rendimiento: curva que se dibuja, rojo cayendo (problema) / verde subiendo (solución), chip "↓ cayendo" / "↑ subiendo", punto final con halo.
- Medidor "Atención" 0→100% rojo→verde.
- Insignia "IA" degradado violeta con destellos, junto a la cabeza.
- Inserto a pantalla completa (como la referencia 1): fondo oscuro, tarjetas de anuncio que se multiplican 1→2→3→4→6→9 columnas, velo central y título "CIENTOS / de variantes".
- Caja de comentario de vidrio que se escribe sola ("Mi negocio es de..."), cursor azul, "Publicar" que se activa al terminar. Nunca se solapa con el título COMENTA.
- Degradado oscuro superior cuando hay texto sobre fondo claro.
- Paleta: blanco + rojo #FF3B30 (dolor) + verde #34C759 (resultado) + violeta #7A5CFF→#B36BFF (marca/IA).

### Cámara y transiciones
- Zoom alternado por tramo (abierto 1,0–1,07 / cerrado 1,16–1,40) con deriva suave; cortes virtuales en tramos largos (>3,5 s).
- Gancho en plano cerrado (≈1,32–1,40).
- Pulso de zoom (+5%) en golpes clave; sacudida corta en MATA, VENTAS, MASIVA.
- **Transición = blur** (desenfoque gaussiano ~18 px que cae en 0,1 s a cada lado del corte), también al entrar/salir del inserto. Flash blanco de 2 fotogramas solo en el golpe del gancho.

## 8. Sonido
- Voz: `acompressor threshold=-20dB ratio=3 attack=5 release=80 makeup=2`.
- SFX de la carpeta del usuario, **muchos pero discretos**: cada uno normalizado a pico −3 dBFS, recortado y con fade; el **bus de SFX ≈8 dB por debajo de la voz** (si queda más alto, bájalo en bloque).
- Mapa base (ajusta a los eventos):
  - Apertura: Metallic Hit · Aparición de segunda palabra: UI Dissolve · Golpe rojo: Flash · Palabra siguiente: HIT blogovs
  - Cortes: Whoosh Sound Effect 01 / Swoosh / Woosh 02 / Hollow Whoosh
  - Gráfica aparece: Data Load (1,3 s) · Curva toca fondo: Failure · Eco: Transition Rapid Click
  - Insignia IA: Digital Burst · Antes del inserto: últimos 1 s de Reverse Drum Riser (termina en el corte) · Cada nivel de tarjetas: UI Button 2 · Título del inserto: Snap
  - Medidor: TIC blogovs · Gráfica verde: UI Menu · Palabra de resultado: Metallic Hit
  - Caja de comentario: Notification · Tecleo: UI Button 2 cada 2 letras (muy bajo) · Cierre: Rapid Click + Snap
- **No usar Clean Swoosh** (no le gusta a Luis).
- Música (si la dan): por debajo de la voz con ducking (sidechaincompress), sin tapar la voz.
- Master: `alimiter 0.85` → loudnorm en 2 pasadas a **−14 LUFS, TP −1,5** (lineal).

## 9. Revisión y entrega
- Hoja de contacto de ~24 fotogramas con zonas seguras pintadas. Comprueba: gancho entendible sin sonido en 2 s, nada tapa cara/manos, títulos de detrás legibles, nada fuera de zona segura, sin choques entre gráficos.
- Mide LUFS final y la relación voz/SFX.
- Exporta 1080×1920 H.264 CRF 17 + AAC 192k `+faststart`. Guarda en `3 Listos/<video>_vN.mp4` (nunca borrar versiones anteriores), envíalo al chat y resume en pocas líneas qué se hizo y qué ajustarías. Di claramente que no puedes escucharlo y pide revisar uniones, volumen de SFX y sincronía en el móvil.

---

## Preferencias de Luis (feedback acumulado)
- Quiere "más": movimiento, motion graphics, SFX — pero limpio y profesional, inspirado en sus referencias (subtítulos de 1–3 palabras, claves en grande, notificaciones/pizarra, insertos a pantalla completa).
- NO: borde negro en letras, Clean Swoosh, rebotes exagerados, pastillas blancas tipo etiqueta, huecos de silencio, textos en zonas que tapa Instagram, textos que tapan cara o manos.
- SÍ: blur en letras y transiciones, SF Pro (Black Italic títulos, Regular subtítulos, Italic énfasis), textos detrás del sujeto, subtítulos debajo de la cara.
- Él prefiere que avances y decidas con criterio; pregunta solo lo imprescindible.

## Cómo reutilizar los scripts
`tryhard_render.py` está escrito para IMG_3680; para un video nuevo cambia:
- `timeline.json`, `track.json`, `words.json` del nuevo video.
- `EV` (ventanas de cada evento), `NO_SUBS`, `VCUTS`, `CAM` (zoom por tramo), `PUNCH`, `SHAKE`, textos de títulos y sus posiciones, `KEY` (palabras en Heavy Italic), textos de gráficas y comentario.
- Prueba fotogramas sueltos: `python3 tryhard_render.py 0.3 2.5 6.9 ...` (guarda `p5_<t>.png`) antes del render completo.
`tryhard_mix.py`: edita la lista `EVENTS` (archivo, desde, duración, segundo, volumen) y el tecleo.