# Referencias visuales — extraer el ADN y traducirlo a la marca

Cuando el usuario pasa capturas de carruseles que le gustan ("quiero que se vea así"), no se copian literal: **se extrae su ADN visual y se traduce a la identidad del cliente**. Se conserva la estructura y los recursos que hacen funcionar la referencia; cambia toda la piel de marca.

> **Regla:** una referencia es inspiración de **estructura**, no una plantilla de **marca**. Si el resultado se parece más a la referencia que al cliente, algo salió mal.

---

## Paso 1 — Separar los slides

**Una sola imagen puede contener varios slides** (láminas con cuadrícula de 2×2, tiras horizontales, capturas del perfil). Antes de analizar:

1. Cuenta cuántos slides hay en cada imagen y recórtalos (Pillow) si hace falta mirarlos de cerca.
2. Numera cada slide de referencia (R1, R2…) y anota de qué imagen salió.
3. Si no se ve claro qué es un slide y qué es otro, pregúntalo en vez de suponer.

## Paso 2 — Extraer el ADN de cada slide

Responde cada punto. Si algo no se ve claro, dilo en vez de inventarlo:

- **Concepto:** ¿hay una metáfora o escena incongruente (personaje fuera de contexto, objeto gigante)? ¿Qué dice la imagen y qué dice el título?
- **Fondo:** ¿color plano, escena, luz de esquina, nebulosa, grano, grid técnico, degradado?
- **Tipografía:** ¿condensada gigante, grotesca ultra bold, serif display, itálica para acentos, manuscrita, mono para etiquetas? ¿Cuánto del ancho ocupa el titular? ¿Mayúsculas o minúsculas? ¿Tracking?
- **Color de acento único:** el que resalta keywords. Casi siempre hay UNO.
- **Recurso estrella:** ¿cómo se resalta la palabra clave? Caja de color, corchetes, subrayado, píldora, itálica dorada con línea.
- **Capas:** qué va detrás del texto, qué va delante, qué se sale del cuadro.
- **Movimiento:** perspectiva, rotación, estela, desenfoque, fantasmas, brillo.
- **Elementos editoriales:** marca, contador, sección, esquinas en L, cuadrícula, reglas con números, íconos técnicos, "desliza →".
- **Composición:** dónde cae el peso, cuánto aire, qué toca el borde.
- **Función en el carrusel:** ¿es hook, presentación, característica, prueba, CTA?

## Paso 3 — Mapear a los slides del guion

Para cada slide del guion, decide qué recurso de qué referencia aplica (R1 → slide 1, R3 → slide 4…). La referencia da el molde; el guion da el contenido; el objetivo (`objetivos-y-cta.md`) decide qué lleva el último slide.

## Paso 4 — Traducir a la marca del cliente

| De la referencia | Al cliente |
|---|---|
| Color de acento | El acento de la marca |
| Tipografía | La de la marca, o una del mismo peso y estilo (ver `pipeline.md`, "Fuentes") |
| Héroe visual | Los recursos reales del cliente (producto, personaje, fotos) |
| Logo, marca y textos | Los del cliente. **Nunca** se dejan logos, nombres ni frases de la referencia |
| Voz | La de la marca, siempre |

Se conserva: estructura, capas, dónde cae el acento, cómo se resalta la keyword, ritmo visual.

## Paso 5 — Si la marca no tiene ficha todavía

La referencia + lo que cuente el usuario es el material para crearla. Rellena la ficha de marca (`references/ficha-marca.md`) con los colores y tono **reales** del cliente, no los de la referencia, y entrégasela al usuario para que la guarde y la reutilice.

---

## Lo que se aprende de las referencias de alto performance

Patrones que se repiten en las referencias que mejor funcionan (escalera saliendo de la tecla ESC, superhéroe sobre una valla, astronauta leyendo en una colina de flores, armadura con flores, loro con anillo, lámina de 4 slides de producto con audífonos):

- La imagen cuenta una historia en un segundo; el título la completa.
- La palabra gigante es fondo y figura a la vez: el protagonista la tapa en parte.
- Un solo color fuerte, el resto casi negro o neutro.
- El producto nunca está quieto ni plano: perspectiva, rotación o acercamiento.
- La capa editorial (marca, contador, esquinas) hace que se vea "de revista", no de plantilla.
