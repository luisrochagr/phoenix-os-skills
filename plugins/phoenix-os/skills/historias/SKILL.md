---
name: historias
description: "Crea Historias de Instagram (Stories 1080×1920, 9:16) estratégicas para cualquier marca: guion frame por frame (gancho → valor → CTA con sticker) + diseño HTML renderizado a PNG, con stickers interactivos (encuestas, preguntas, quiz), safe zones y la ficha de marca del cliente. Úsala cuando pidan historias, stories, frames verticales 9:16, una secuencia de stories o adaptar una referencia o un carrusel a stories."
---

# Historias — activo de conversión para Instagram Stories

Esta skill produce **Historias de Instagram (Stories) que enganchan y convierten**, no "frames bonitos". Sirve para **cualquier marca**: usa la ficha de marca del cliente (plantilla en `references/ficha-marca.md`). Es la hermana vertical de `carrusel-tryhard` y reusa su mismo criterio de diseño.

Cada Historia tiene dos piezas, entregadas en orden:

1. **GUION** — el copy estratégico, mapeado **frame por frame** (gancho → valor → CTA con sticker).
2. **DISEÑO** — un archivo HTML con los frames de **1080×1920 (9:16)** que se exporta a PNG, con la identidad visual de la marca aplicada y las **safe zones** respetadas.

> **Regla de oro:** el prompt/diseño define ROL, FORMATO y estética; el COPY va en el GUION, siempre validado antes de diseñar. Nunca inventes cifras, casos ni resultados.

---

**Scripts** (en `scripts/`, rutas relativas a la carpeta de esta skill; salidas siempre en tu carpeta de trabajo): `fuentes.py` (fuentes en base64), `img_to_base64.py` (fotos y recortes), `render.py` (frames a PNG + avisos de desborde y safe zones), `efectos.py` (fondos, luz de borde, hoja de contacto).

---

## Diferencias clave vs. carrusel (léelo siempre)

Las Stories NO son un carrusel vertical. Cambian el formato, el consumo y los recursos:

- **Formato:** cada frame es `1080px × 1920px` (9:16), pantalla completa. `box-sizing:border-box`.
- **SAFE ZONES (crítico):** deja libres de texto vital la franja **superior ~250px** (foto de perfil, nombre, hora) y la **inferior ~320px** (barra de "Enviar mensaje" + stickers). Todo lo importante (titular, dato, CTA) va en el **centro** (aprox. y de 260 a 1600). Dibuja guías tenues al construir y revisa que nada caiga en las zonas muertas.
- **Consumo por toque:** la gente **tapea para avanzar** y se va en 1–2 s si no engancha. El **primer frame es un gancho** aún más agresivo que en carrusel.
- **Una sola idea por frame**, tipografía grande (se lee en móvil a distancia de pulgar), **poquísimo texto**.
- **Arco corto:** 3–7 frames. `gancho → valor rápido → CTA con sticker`. Cada frame promete el siguiente ("sigue →", contador "1/5").
- **Nativo y dinámico** gana a editorial rígido: movimiento, contraste, foco, mucho aire.
- **Barra de progreso ARRIBA** (segmentos = nº de frames) imitando el UI real de Stories: es un recurso visual muy natural aquí.

---

## Stickers interactivos (el motor de conversión de Stories)

En el diseño se **dibujan como placeholder** (para saber dónde y de qué tamaño irán); los stickers reales se colocan luego dentro de la app de Instagram. Reserva su espacio (~200–240px de alto libre donde vaya el sticker).

Repertorio y para qué sirve cada uno:
- **Encuesta (A/B)** → decisiones rápidas, altísima interacción ("¿Cuál te gusta más?").
- **Pregunta / caja de respuesta** ("Hazme una pregunta", "Responde con una palabra") → dispara **DMs y comentarios**, el activo que más convierte.
- **Quiz** (opción correcta) → educa jugando ("¿Cuál es cuero real?").
- **Slider con emoji** → medir deseo/temperatura ("¿Cuánto lo amas?").
- **Cuenta regresiva** → lanzamientos, drops, recordatorios.
- **Link / "Ver más"** → llevar al catálogo, web o WhatsApp (una sola acción).
- **Mención / GIF / Música** → comunidad y ritmo.

Estrategia: **un sticker por frame**, casi siempre en el frame de cierre (o uno intermedio de valor). Encuesta y pregunta son los reyes del engagement; priorízalos si el objetivo es alcance/DMs.

---

## Workflow

1. **El usuario dice "historia/story/stories"** (o pide frames verticales, o adaptar algo a stories).
2. **Marca.** Busca la ficha de marca en la conversación o el proyecto (`marca-{nombre}.md`). Si no hay, pide identidad visual O una referencia y arma la ficha con `references/ficha-marca.md`; entrégasela al usuario para que la guarde.
3. **Pregunta tema, objetivo y sticker/CTA:** ¿qué idea vende, a quién, y qué acción quieres (encuesta, pregunta, link "ver catálogo", "responde con…", seguir)?
4. **Escribe el GUION frame por frame** (abajo el formato) y valídalo con el usuario antes de diseñar.
5. **Si hay fotos**, conviértelas a base64 con `scripts/img_to_base64.py` (usa `--alpha` para recortes con transparencia; HEIC de iPhone: ver "Técnico").
6. **Construye el HTML 1080×1920** con el sistema de diseño de la marca, safe zones y placeholders de sticker. O entrega el master prompt para otra herramienta.
7. **Renderiza** con `python scripts/render.py build/historias.html out/ --nombre {Marca}_{Tema} --selector .frame --alto 1920 --safe-top 250 --safe-bottom 320` y **verifica**: safe zones, legibilidad, fuentes correctas, nada cortado. El script avisa desbordes, texto en las zonas muertas, fuentes con error e imágenes sin cargar.

### Prioriza por igual GUION y DISEÑO
Un gancho flojo hunde el mejor diseño; un diseño descuidado entierra un buen copy. Dedica esfuerzo real a ambos.

---

## GUION — formato de entrega (frame por frame)

Arco recomendado (ajusta 3–7 frames):
- **Frame 1 — GANCHO:** detiene el tap-away. Reframe, dato o pregunta punzante. Keyword en el acento de la marca (entre `[CORCHETES]`).
- **Frames 2–(n-1) — VALOR:** una idea/dato/tip por frame, concreto y verificable. Ritmo.
- **Frame n — CTA + STICKER:** una sola acción con el sticker que corresponda.

```
=== GUION — STORIES {MARCA}: "{tema}" ===
CONVENCIÓN: [CORCHETES]=va en el acento de la marca · STICKER=qué sticker interactivo · IMG=qué imagen

[FRAME 1 — GANCHO]   TÍTULO (con [keyword]) / SUBTEXTO corto / IMG o solo tipografía / "sigue →"
[FRAME 2 — VALOR]    IDEA única / dato concreto / IMG
[FRAME 3 — VALOR]    IDEA única / IMG
[FRAME 4 — CTA]      CTA (una acción) / STICKER: {encuesta | pregunta | quiz | link | responde} / IMG
```

Reglas del copy: una idea por frame; solo afirmaciones verdaderas; específico > genérico (números y hechos, no clichés); nada de "en esta historia te voy a…"; respeta la voz y las prohibiciones de la marca; el CTA pide UNA acción.

---

## Sistema de diseño (reutilizable, estética premium + dinámica)

Mismo ADN que `carrusel-tryhard`, adaptado a 9:16. Colores, tipografía y logo salen de la ficha de marca; lo de abajo es el sistema por defecto.

**Formato técnico**
- UN archivo HTML, CSS puro embebido. Cada frame es `<div class="frame">` de EXACTAMENTE `1080×1920`, apilados en vertical con separación, `box-sizing:border-box`.
- Padding interno lateral ~80px. **Contenido crítico entre y≈260 y y≈1600** (safe zones).
- El texto nunca desborda ni se corta: ajusta `font-size`.

**Superficies que ALTERNAN (dinamismo):** no repitas fondo. Alterna los fondos de la marca (ej.: claro → oscuro → claro → oscuro). Grano de papel con overlay SVG `feTurbulence` a `opacity:.04; mix-blend-mode:multiply`.

**Tipografía (legible):** la de la marca. Si no tiene, por defecto titulares en **Fraunces** (serif display, 600–700; NO uses versalitas finas tipo Cormorant Unicase en títulos largos: se lee mal), apoyo en **Jost** y acento/keyword en **Fraunces itálica** del color de acento con línea fina debajo. **Embébelas en base64** con `python scripts/fuentes.py fraunces:600,700,700i jost:400,500 -o build/fuentes.css` (Google Fonts suele estar bloqueado y por link la fuente puede cambiar al exportar).

**Recursos de dinamismo (probados):**
- **Barra de progreso arriba** (segmentos = nº de frames), estilo UI de Stories.
- **Números/letras “fantasma”** gigantes de fondo (`opacity ~.07`, color de acento) para profundidad.
- **Subrayado de color** por frame (rota colores de la paleta) como punto de color.
- **Zig-zag**: alterna la posición de vector/foco entre frames.
- **Píldora "sigue →"** o flecha de avance.
- Números protagonistas gigantes (Fraunces 700) como gancho — los números detienen el scroll.

**Fotos:** a sangre (`object-fit:cover`, 1080×1920) + **degradado** inferior para legibilidad; texto en la zona central-baja segura, en el color claro de la marca con el acento y sombra suave. Recortes 9:16 enfocando el producto. Embeber SIEMPRE como base64 data URI (nunca rutas/URLs: html2canvas las deja en blanco).

**Placeholder de sticker:** un rectángulo/redondeado tenue con etiqueta ("ENCUESTA", "PREGUNTA", "VER MÁS") donde irá el sticker real, respetando su alto.

---

## MASTER PROMPT (reutilizable) — pégalo en otra herramienta o síguelo tú

Reemplaza los campos `{ }` con el perfil de la marca.

```
Actúa como diseñador de conversión + copywriter de respuesta directa de élite para la marca "{MARCA}" ({DESCRIPCION}). Crea una SECUENCIA DE HISTORIAS de Instagram (Stories) que enganche en el primer segundo, retenga el tap y termine en una acción con sticker. No quiero "frames bonitos": quiero un activo de conversión con estética premium.

FORMATO TÉCNICO (OBLIGATORIO)
- UN archivo HTML con CSS puro embebido (sin frameworks).
- {N} frames. Cada frame es un <div class="frame"> de EXACTAMENTE 1080px × 1920px (9:16). box-sizing:border-box.
- SAFE ZONES: deja libres de texto vital los ~250px superiores y ~320px inferiores. Todo lo importante en el centro.
- Barra de progreso arriba con {N} segmentos (UI de Stories). El texto nunca desborda.

TIPOGRAFÍA
- Titulares: {TIPO_TITULAR}. Apoyo: {TIPO_APOYO}. Acento/keyword: {TIPO_ACENTO} en {COLOR_ACENTO} con línea fina debajo.
- Fuentes embebidas como @font-face en base64 (nada de Google Fonts por link); exportar tras await document.fonts.ready.

IMÁGENES
- Toda imagen embebida como base64 data URI (nunca rutas ni URLs). Fotos a sangre con degradado inferior para legibilidad.

SISTEMA DE DISEÑO
- Fondos que ALTERNAN entre {SUPERFICIES}. Acento ÚNICO: {COLOR_ACENTO}. Texto: {COLORES_TEXTO}.
- Dinamismo: número/letra fantasma de fondo, subrayado de color por frame, píldora "sigue →", números gigantes de gancho.
- Wordmark de marca: {WORDMARK}. Una idea por frame, alto contraste, mucho aire, cero emojis dentro del diseño.

ESTRUCTURA (función de cada frame — NO escribas el copy, lo doy en el GUION)
- Frame 1: GANCHO (titular enorme + keyword en acento). Detener el tap-away.
- Frames intermedios: VALOR (una idea/dato por frame).
- Frame final: CTA + PLACEHOLDER DE STICKER ({encuesta | pregunta | quiz | link | responde}).

VOZ DE MARCA
{VOZ} · Respeta el copy del guion. {PROHIBICIONES}

EXPORT
- Botón que exporta cada frame a PNG con html2canvas 1.4.1 (scale:2, width:1080, height:1920, backgroundColor explícito por frame, windowWidth/Height 1080/1920, ~600ms entre descargas).

ESPERA: responde "Listo, envíame el guion y las imágenes" y no generes nada hasta recibir (1) el GUION frame por frame y (2) las imágenes en base64.
```

Bloque de export (html2canvas) — recuerda `backgroundColor` explícito según la superficie del frame y `height:1920`.

---

## Ficha de marca → campos del master prompt

La plantilla completa está en `references/ficha-marca.md`. Para Stories importan además: **handle**, **wordmark o logo** (siempre el logo real en PNG; si el nombre lleva un signo que la fuente pinta mal, como una vocal con macrón, dibuja el signo por CSS anclado a la letra en vez de usar el carácter precompuesto) y el **sticker o CTA por defecto**.

```
{MARCA} · {DESCRIPCION} · {COLOR_ACENTO} · {SUPERFICIES} · {COLORES_TEXTO}
{TIPO_TITULAR} · {TIPO_APOYO} · {TIPO_ACENTO} · {WORDMARK} · {VOZ} · {PROHIBICIONES}
```

---

## Librería de VECTORES de moda (line-art, viewBox 0 0 240 300, stroke=currentColor en el color de acento, width 3–4, round)
Colócalos con un "halo" (círculo fino del color de acento detrás) como ancla. **Renderiza a PNG y míralos antes de usar** (`convert vec.svg vec.png`); ensancha los que salgan estrechos.
```
dress:    <path d="M120 40c-8-5-2-16 6-11"/><path d="M120 48 L88 76 M120 48 L152 76"/><path d="M88 76 C82 100 78 120 74 150 L60 250 C90 268 150 268 180 250 L166 150 C162 120 158 100 152 76"/><path d="M98 68 Q120 86 142 68"/><path d="M120 92 L120 250"/>
top:      <path d="M120 54c-8-5-2-16 6-11"/><path d="M120 62 L86 92 M120 62 L154 92"/><path d="M86 92 C82 112 80 128 80 150 L92 232 C110 246 130 246 148 232 L160 150 C160 128 158 112 154 92"/><path d="M100 84 Q120 100 140 84"/>
trousers: <path d="M92 54 L148 54 L150 74 L90 74 Z"/><path d="M90 74 L84 250 L116 250 L120 110 L124 250 L156 250 L150 74"/><path d="M120 74 L120 104"/>
coat:     <path d="M120 40 L82 70 L78 262 L120 262 L162 262 L158 70 Z"/><path d="M120 40 L100 84 M120 40 L140 84 M120 84 L120 250"/><path d="M80 152 L160 152"/><rect x="108" y="143" width="24" height="18"/><circle cx="102" cy="120" r="3.5"/><circle cx="102" cy="200" r="3.5"/>
blazer:   <path d="M120 42 L88 68 L98 158 M120 42 L152 68 L142 158"/><path d="M88 68 C70 74 60 86 56 104 L72 258 L120 258 M152 68 C170 74 180 86 184 104 L168 258 L120 258"/><path d="M120 60 L104 100 L120 126 L136 100 Z"/><circle cx="120" cy="152" r="3.5"/><circle cx="120" cy="178" r="3.5"/>
knit:     <path d="M86 74 L120 88 L154 74 L188 104 L166 132 L154 122 L154 246 L86 246 L86 122 L74 132 L52 104 Z"/><path d="M102 76 Q120 96 138 76"/><path d="M98 232 L98 246 M112 232 L112 246 M128 232 L128 246 M142 232 L142 246"/>
scarf:    <path d="M96 64 Q120 50 144 64"/><path d="M96 64 L82 232 L120 244 L120 74"/><path d="M144 64 L158 232 L120 244 L120 74"/><path d="M82 232 L80 250 M92 236 L91 254 M108 240 L108 258 M120 244 L120 262 M132 240 L132 258 M148 236 L149 254 M158 232 L160 250"/><path d="M104 96 Q120 108 136 96 M100 150 Q120 164 140 150"/>
belt:     <path d="M40 118 L150 118 L150 158 L40 158"/><rect x="150" y="112" width="46" height="52" rx="6"/><path d="M172 112 L172 90 Q172 78 160 78 L120 78"/><circle cx="118" cy="138" r="5"/><path d="M150 138 L162 138"/>
shoe:     <path d="M30 196 Q34 168 70 166 Q120 164 150 158 Q182 152 190 176 L196 210 L182 210 L176 190 Q150 200 110 202 Q70 204 48 206 Z"/><path d="M182 210 L188 236 L202 236 L196 210"/><path d="M92 168 Q96 186 78 196"/>
rack:     <path d="M40 92 L200 92"/><path d="M58 92 L58 250 M182 92 L182 250"/><path d="M90 92 L74 118 M90 92 L106 118 M90 118 L90 138"/><path d="M150 92 L134 118 M150 92 L166 118 M150 118 L150 138"/><path d="M78 138 Q74 160 72 180 L82 226 Q90 234 98 226 L108 180 Q106 160 102 138"/><path d="M138 138 Q134 160 132 180 L142 226 Q150 234 158 226 L168 180 Q166 160 162 138"/>
follow:   <circle cx="120" cy="150" r="92"/><path d="M120 112 L120 188 M82 150 L158 150"/>
dialog:   <path d="M56 78 L150 78 Q164 78 164 92 L164 150 Q164 164 150 164 L96 164 L74 186 L74 164 L70 164 Q56 164 56 150 Z"/><path d="M84 108 L136 108 M84 132 L120 132"/>
```

### Paleta de referencia para contenido de moda/estilo (enseñar a combinar; NO reemplaza la paleta de la marca)
```
Neutros: Crema #EFEBE0 · Arena #D8C7A8 · Grafito #2E3843 · Oliva #6E7245 · Camel #B08C5A · Chocolate #4A3527 · Hueso #F3EFE6 · Marino #1B3A57
Color:   Mantequilla #EFDB8E · Terracota #C06B4B · Vino #6E2233 · Mostaza #C9A227 · Salvia #97A585 · Azul seda #7BA3C9
Combos:  Oliva·Mantequilla·Azul "Cálido con carácter" · Crema·Camel·Chocolate "Monocromo tierra" · Marino·Hueso·Camel "Clásico atemporal" · Terracota·Salvia·Crema "Otoño suave"
Regla enseñable: 3 base + 2 protagonistas (máx.) + 1 acento.
```

---

## Técnico

- **Render:** `scripts/render.py` (Playwright) es el camino por defecto. **Export desde el navegador** (si el usuario lo quiere): botón con **html2canvas 1.4.1** (`scale:2`, `width:1080, height:1920`, `backgroundColor` explícito por frame, `windowWidth/Height 1080/1920`, `setTimeout ~600ms`). Si el entorno tiene navegador headless, screenshotea directo tras cargar fuentes.
- **Fotos HEIC de iPhone:** traen gain-map HDR que rompe el lector estándar de libheif (*"Too many auxiliary image references"*). Solución: parsear el contenedor ISO-BMFF, extraer el item primario (suele ser un **grid** de tiles HEVC) y decodificar cada tile con **libde265** vía `ctypes`, reensamblar el grid y convertir YUV→RGB (BT.709 limitado); guardar JPG y embeber en base64.
- **Verificación (obligatoria):** abre el HTML y confirma (1) fuentes correctas, (2) imágenes/vectores pintados, (3) **nada crítico en las safe zones** (superior 250 / inferior 320), (4) ningún texto cortado, (5) placeholders de sticker con espacio suficiente. Exporta el frame 1 y míralo: es donde más se nota cualquier fallo.

---

## Principios que no cambian entre marcas
- Una idea por frame. Gancho brutal en el frame 1. Poquísimo texto, tipografía grande.
- La keyword va en el acento de la marca. Cero emojis dentro del diseño.
- Solo afirmaciones verdaderas y verificables; específico gana a genérico.
- Respeta voz y prohibiciones de la marca. El CTA pide UNA acción, con el sticker correcto.
- Safe zones sagradas. Dinamismo sí, pero legibilidad primero.

