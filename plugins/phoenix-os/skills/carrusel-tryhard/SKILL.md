---
name: carrusel-tryhard
description: "Crea carruseles de Instagram de nivel alto para cualquier marca: concepto con metáfora visual, escena compuesta, tipografía gigante, guion slide por slide con el CTA y las palancas de neuromarketing que pide el objetivo, y PNG 1080×1350 listos para publicar con su caption. Antes de diseñar pregunta el fin del carrusel, el concepto, la marca y las referencias visuales. Úsala cuando pidan un carrusel, slides para Instagram, una portada o hook de carrusel, slides de producto o adaptar una referencia visual de carrusel."
---

# Carrusel TRYHARD — portadas y slides de alto performance

Produce carruseles de Instagram **al nivel de las mejores referencias de diseño**, no plantillas. Sirve para cualquier marca y cualquier persona del equipo: primero entiende para qué es el carrusel y cómo debe verse, después escribe y diseña.

Cada carrusel tiene dos piezas que se trabajan con el mismo cuidado:

1. **GUION** — concepto + copy slide por slide (hook → valor → CTA), con el CTA y las palancas que pide el objetivo.
2. **DISEÑO** — HTML por capas + composición en Python, renderizado a PNG 1080×1350.

> **Vara de calidad:** nada de producto plano sobre fondo plano, fichas con texto chico ni tipografías delgadas en titulares. El piso es una escena con concepto, palabra gigante y producto con movimiento (ver `references/estilos.md`, "Escena compuesta").

**Archivos de esta skill:**

| Archivo | Cuándo se lee |
|---|---|
| `references/objetivos-y-cta.md` | Paso 1: el fin del carrusel decide CTA, estructura y palancas de neuromarketing |
| `references/ficha-marca.md` | Paso 0: plantilla de marca (la misma en todas las skills del paquete) |
| `references/guion.md` | Paso 4: ángulos de hook, formato del guion, caption |
| `references/referencia-visual.md` | Paso 2: extraer el ADN de una referencia y traducirlo a la marca |
| `references/estilos.md` | Paso 2 y 6: método NIVEL ALTO, catálogo de estilos y estructuras validadas |
| `references/pipeline.md` | Paso 5 y 6: técnica (capas, fuentes, recortes, render) |
| `scripts/efectos.py` | Luz de borde, perspectiva, estela, fantasmas, fondos, hoja de contacto |
| `scripts/fuentes.py` | Embebe fuentes de Fontsource en base64 (Google Fonts suele estar bloqueado) |
| `scripts/render.py` | HTML → PNG por slide + hoja de contacto + avisos de desborde |

> Las rutas `scripts/…`, `references/…` y `assets/…` son relativas a la carpeta de esta skill. Al correr un script, usa la ruta completa de esa carpeta (la que aparece junto a la skill en la lista de skills disponibles) y deja las salidas en tu carpeta de trabajo, nunca dentro de la skill.

---

## Paso 0. Preguntas de entrada (antes de escribir o diseñar nada)

Salta lo que ya esté en la conversación. Si el usuario pide "solo el hook" o "un slide", pregunta solo lo indispensable y ve directo.

**Ronda 1 — con AskUserQuestion (una sola llamada, 4 preguntas):**

1. **¿Cuál es el fin del carrusel?** Alcance y guardados · Leads (comentar una palabra o escribir al DM) · Venta directa (link o WhatsApp) · Autoridad y confianza. (Lanzamiento o evento entra por "Otro".)
2. **¿Cómo quieres que se vea?** Te adjunto referencias · Usa un estilo del catálogo · Propónme 3 direcciones.
3. **¿Qué tenemos de la marca?** Ficha de marca lista · Te paso colores, fuentes y logo · Marca nueva: pregúntame.
4. **¿Qué recursos hay?** (multiselección) Fotos o PNG del producto · Personaje o escena · Fotos reales de la marca · Nada todavía.

**Ronda 2 — en un solo mensaje, solo lo que falte:**

- **Concepto:** qué vende o enseña, a quién (un lead concreto, no "emprendedores") y si ya tiene la idea o metáfora. **Si el usuario trae el concepto, ese concepto manda.**
- **Datos reales:** nombre del producto, funciones confirmadas, cifras, precio si va. Nada se inventa.
- **CTA:** la palabra clave a comentar, el link o el número, y qué recibe la persona a cambio (lead magnet).
- **Marca** (si no hay ficha): colores de fondo, acento y texto; tipografías; logo en PNG; voz en una frase; lo que nunca se dice. La plantilla completa está en `references/ficha-marca.md`.
- **Número de slides** (default: 5 a 6).

Si una respuesta no llega, toma el default más razonable, dilo en una línea y sigue.

---

## Workflow

1. **Objetivo → CTA y palancas.** Con el fin del carrusel, lee `references/objetivos-y-cta.md` y fija: el tipo de CTA, la estructura de slides y 2 o 3 palancas de neuromarketing que se sostengan con la verdad. Escríbelas en una línea al inicio del guion.
2. **Dirección visual.**
   - Con referencias: extrae su ADN con `references/referencia-visual.md`. **Una sola imagen puede contener varios slides** (láminas con cuadrícula de 4): se analiza cada uno y se mapea uno a uno.
   - Sin referencias: elige del catálogo de `references/estilos.md` o propón 3 direcciones (concepto + estilo + paleta) y deja que el usuario elija.
   - Siempre se traduce a la piel de la marca: colores, tipografía, logo y voz son los del cliente, nunca los de la referencia.
3. **Concepto.** Si no lo trajo el usuario, propón 3 conceptos de metáfora visual incongruente con su título (método NIVEL ALTO, `references/estilos.md`) y que elija uno.
4. **Guion primero** (`references/guion.md`), mostrado para validar antes de diseñar.
5. **Recursos:** PNG sin fondo del producto y del personaje (`efectos.recortar_fondo`). Si no hay escena ni personaje y hace falta uno, escribe el prompt para Midjourney / Gemini / ChatGPT (no hay generador de imágenes aquí).
6. **Diseño:** prepara imágenes (luz de borde, perspectiva, acercamientos, logos ajenos difuminados), construye el HTML por capas (`references/pipeline.md`), **renderiza con `scripts/render.py`, revisa cada PNG con la checklist e itera**.
7. **Entrega:** PNG (`{Marca}_{Campaña}_{n}.png`), HTML editable y **caption listo para pegar**. Una línea de qué se hizo; los PNG con `SendUserFile`.

---

## Método NIVEL ALTO (resumen; detalle en `references/estilos.md`)

1. **Concepto antes que diseño:** cada carrusel nace de una imagen incongruente o metáfora visual (un personaje fuera de contexto con el producto cumpliendo un papel en su historia). **Título e imagen dicen lo mismo** en dos idiomas. Título disruptivo de 3 a 6 palabras: orden, advertencia o golpe emocional; nada de "descubre" o "conoce". Todo el carrusel vive en el mismo universo y la historia avanza slide a slide.
2. **Cuatro capas** (atrás → adelante): fondo con atmósfera y UNA luz dominante → palabra(s) gigante(s) al 80–90 % del ancho con un acento en itálica serif encima → protagonista recortado (tapa máximo ~35 % de la palabra) → primer plano desenfocado. Encima, la capa editorial (marca, sección, contador, esquinas, cuadrícula, keyword, "DESLIZA →").
3. **Movimiento y fusión:** producto en perspectiva y rotado, relación física con el personaje (`rot_point`), estela de aire visible, fantasmas, brillo y anillos.
4. **Luz y color:** luz de borde en todos los recortes; **el acento no domina** (fondo casi negro, nebulosas al 5–14 %; el color fuerte solo en la keyword, puntos de estado, flechas y tachados).
5. **Protagonismo:** en los slides de producto el producto es el centro, pero el personaje no desaparece (230–430 px de alto, interactuando con el producto).

---

## Checklist de revisión del render (OBLIGATORIA en cada iteración)

- `render.py` sin avisos, o cada aviso explicado.
- Las líneas gigantes no se pisan y el título se lee completo.
- **Ningún personaje tapado** por el producto ni por textos. Si choca, se le busca otra zona con buena proporción.
- **Recortes con borde recto** (personajes cortados, como el que se asoma): el borde recto coincide EXACTO con el borde de su contenedor (ver `references/pipeline.md`).
- Textos dentro de tarjetas sin superposición (título de 3 líneas → bajar el texto de apoyo).
- Nada importante cortado (producto, botón, caja). Si el botón choca, se mueve de lado.
- Personaje legible en todos los slides.
- **Recortes ampliados** de las zonas delicadas (estela, tarjetas, personajes) revisados antes de entregar.
- La keyword y el CTA son los del Paso 0. Un solo CTA.
- Ningún dato, cifra, testimonio o escasez que no haya confirmado el usuario.

---

## Qué puedo y qué no

- **Sí:** recortar, iluminar, poner en perspectiva y rotar; estelas, fantasmas, brillos y anillos; fondos por código (espacio, nebulosa, planeta, luz de esquina, grano); acercamientos; composición tipográfica.
- **No:** crear una escena fotorrealista nueva (no hay generador de imágenes). En ese caso escribo el prompt para otra herramienta o uso la escena que mande el usuario.
- **Marcas ajenas:** si el producto parece de otra marca, no se nombra ni se ponen sus logos, tampoco en caption ni hashtags. Los logos en personajes (agencias espaciales, banderas, marcas) se **difuminan** con `efectos.difuminar_zona`. Revisar licencias de imágenes de banco. Nunca se hace contenido para productos falsificados o réplicas.
- **Datos:** nunca inventar batería, funciones, cifras, precios, materiales ni testimonios; usar solo lo confirmado y pedir el resto. La ironía es bienvenida siempre que se note que es humor ("0 excusas", molestias "canceladas").

---

## Principios

- **Una idea por slide**, alto contraste y jerarquía clara. Cero emojis dentro del diseño.
- **La keyword va en la caja o el acento de la marca.**
- **Solo afirmaciones verdaderas.** Neuromarketing sí, manipulación no: cada palanca tiene que sostenerse con un hecho real.
- **El hook lo es todo**, siempre con el método NIVEL ALTO.
- **Respetar la voz de la marca y sus prohibiciones.**
- **Un solo CTA**, el que decidió el objetivo.
- **Nombres de producto reales**, avisando de los dudosos.
- **Revisar cada render antes de mostrarlo.** Los detalles que más se notan: personajes tapados, bordes que no encajan, textos superpuestos.

## Formato

Cada slide mide `1080 × 1350 px` (4:5). En el HTML se apilan con 40 px de separación y se renderiza cada uno a PNG, con márgenes internos de 64 px y posicionamiento absoluto por capas. El texto nunca desborda ni se corta. Lo estándar es de 5 a 6 slides (hook + 3–4 de valor + CTA); puede ir de 5 a 8 si el guion lo pide.

## Después

- Para convertir el carrusel en reel: `creador-de-guiones` o `guion-broll`.
- Para versión en Stories 9:16: `historias`.
- Si el carrusel nace de una referencia viral ajena: primero `adaptador` (mecanismo), después esta skill (diseño).
