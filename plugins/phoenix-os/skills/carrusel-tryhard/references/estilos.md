# Método NIVEL ALTO, catálogo de estilos y estructuras validadas

---

## 1. Método NIVEL ALTO (obligatorio en cada slide)

### Concepto antes que diseño
- Cada carrusel nace de una **imagen incongruente o metáfora visual**: un personaje fuera de contexto con el producto cumpliendo un papel en su historia.
- **Título e imagen dicen lo mismo** en dos idiomas. Ejemplo validado: a un astronauta se le escapan unos audífonos → "No dejes ir LO QUE TE MANTIENE [VIVO]". La lógica es irónica: la cancelación de ruido te mantiene vivo porque deja afuera todo lo malo.
- **Título disruptivo:** orden, advertencia o golpe emocional de 3 a 6 palabras. Nada de "descubre" o "conoce".
- **La ironía es bienvenida** ("0 excusas", molestias "canceladas") siempre que se note que es humor: nunca datos técnicos falsos ni testimonios inventados.
- **Todo el carrusel vive en el mismo universo** y la historia avanza slide a slide.
- **Protagonismo:** en los slides de producto el producto es el centro, pero **el personaje no desaparece**: 230–430 px de alto, interactuando con el producto (agarrado, asomándose, sentado cerca). Un personaje de 120 px pierde el contexto.

**Cómo proponer conceptos (cuando el usuario no trae uno):** escribe 3, cada uno con: personaje o escena · qué papel cumple el producto en su historia · título de 3–6 palabras · por qué conecta con el dolor del lead. Ejemplo de fórmula: *{personaje en situación extrema} + {producto resuelve su problema} = {título que funciona literal y metafórico}*.

### Cuatro capas (atrás → adelante)
1. **Fondo con atmósfera:** escena o fondo por código con UNA luz dominante. Nunca color plano.
2. **Palabra(s) gigante(s):** condensada (Anton por defecto) al 80–90 % del ancho, autoajustada a 940–960 px, 1 o 2 líneas con line-height 0.9–0.93. Encima, un **acento en itálica serif** (Playfair Display Italic 800 por defecto) que abre la frase: "No dejes ir", "Tu sistema de", "Todo lo que se queda", "Tú, en".
3. **Protagonista recortado:** tapa como máximo ~35 % de la palabra; ocupa 50–65 % del lienzo y puede salirse por un borde.
4. **Primer plano desenfocado:** duplicado del producto con blur 16 px+ y opacidad ~0.45 en una esquina.

Encima va la **capa editorial** (constante en todo el carrusel): marca arriba a la izquierda (logo real, nunca escrito con tipografía si hay logo), sección al centro, contador "[ 01 / 05 ]" o una prueba real "[ 4 AÑOS DE DATA ]" a la derecha, esquinas en L, cuadrícula de 60 px enmascarada, keyword en la caja de la marca y pastilla "DESLIZA →" en una esquina libre.

### Movimiento y fusión
- **Producto en perspectiva** (`efectos.perspective`: se estrecha arriba y se inclina), rotado 20–40°.
- **Relación física con el personaje:** calcula con `efectos.rot_point` dónde queda su mano tras escalar y rotar, y ubica el producto respecto a ese punto (en el hook validado: 200 px a la derecha y 215 px abajo de la mano abierta).
- **Estela de aire** (`efectos.estela`): 5 a 7 trazos curvos blanco-azulados de la mano al producto, finos al inicio y gruesos al final, dos desenfoques sumados. Tiene que VERSE; si el producto queda pegado a la mano, sepáralo.
- **Fantasmas** (`efectos.fantasmas`): 2 o 3 copias pequeñas en la trayectoria con motion blur y opacidad 0.07–0.19. El producto final va NÍTIDO.
- **Brillo y anillos:** degradado radial suave del color de acento (alfa .2–.28) y anillos punteados concéntricos tipo panel.

### Luz y color
- **Luz de borde** (`efectos.grade`) en todos los recortes, con el color del ambiente, para que todo parezca de la misma escena.
- **El acento no domina:** fondo casi negro, nebulosas al 5–14 %, luz de borde ~.4–.45. El color fuerte solo en la caja de keyword, puntos de estado, flechas y tachados.
- **Titulares que impactan:** nada de tipografías delgadas o versalitas finas en titulares. Si la marca usa una serif delicada, va en acentos; el titular va en una de peso alto (Anton, Playfair Display Black 900, la condensada de la marca).

---

## 2. Catálogo de estilos (para elegir cuando no hay referencia)

| Estilo | Cómo se ve | Para qué sirve |
|---|---|---|
| **A · Escena compuesta** (vara de calidad) | Fondo de escena con luz dominante, itálica serif + palabra condensada gigante, personaje recortado tapando parte, producto con estela y fantasmas | Hooks de producto, lanzamientos, todo lo que necesite detener el scroll |
| **B · Manuscrita sobre condensada + reglas laterales** | Script (Pinyon Script) sobre palabra condensada con degradado, producto delante, reglas laterales con números y rótulos, íconos técnicos arriba | Estética, moda, producto premium, "estilos/guía" |
| **C · Etiqueta en caja + palabra gigante en minúscula** | Fila superior con fecha, @usuario y categoría; Inter 800 gigante con tracking negativo; segunda palabra pequeña a la derecha | Educativos, colecciones de recursos, alcance |
| **D · Luz de esquina + titular de color + sublínea blanca** | Fondo oscuro con brillo de esquina (`efectos.fondo_luz`), producto enorme saliendo del cuadro | Venta directa, producto único, mensajes cortos |
| **E · Colección (un slide por producto)** | Nombre GIGANTE con "Nº 01" encima, recorte tapando ~40 % inferior, lupa de detalle, pastillas de variante, fondos alternados con grano | Catálogos, colecciones de moda, calzado, accesorios |

Cuando el usuario pide "propónme 3 direcciones", combina un **concepto** + un **estilo** + la **paleta de la marca** y descríbelos en 2 líneas cada uno.

---

## 3. Estructura validada — carrusel de producto (5 slides)

1. **HOOK (concepto):** escena narrativa completa (método de arriba).
2. **PRESENTACIÓN:** itálica + 2 líneas gigantes a la izquierda; producto grande a la derecha tapando parte de las letras; **pastilla de estado** con punto ("● {función} · ON"); **tarjeta de vidrio** (degradado oscuro, borde blanco 12 %, radio 28) con título, texto y el personaje asomándose; **fila de 3 datos** abajo con línea superior (condensada 84 px + etiqueta en mayúsculas), reales si los hay o irónicos evidentes (FUERA / ON / 0).
3. **CARACTERÍSTICAS (cuadrícula 2×2):** itálica + palabra gigante; 4 tarjetas de 464×420, radio 30, fondo radial oscuro, borde blanco 10 %; cada una con un **acercamiento real** (la foto completa escalada 1.2–1.6× y desplazada dentro de la tarjeta con `overflow:hidden`, así nunca se ven los bordes del recorte); degradado oscuro abajo y texto Inter 900 38 px. Recurso validado: texto **tachado con línea de acento de 5 px** + "CANCELADO.". El personaje flota en una esquina (~270 px).
4. **FUNCIÓN ESTRELLA:** arriba itálica + keyword en caja ("ACTIVADA"); al centro un **acercamiento gigante** del producto (~1200 px, saliéndose por abajo) con brillo y anillos; **dos columnas enfrentadas** ("AFUERA" / "ADENTRO", condensada 74 px + lista corta); **el personaje ~430 px agarrado al producto**.
5. **VENTAJAS + CTA:** itálica + palabra gigante; **lista de 4 ventajas** a la izquierda (Inter 900 36 px + gris 21 px con separador); producto rotado a la derecha con brillo; el personaje en su propia zona (esquina inferior derecha, ~230 px) **sin que nada lo tape**; abajo el cierre del concepto ("NO LOS [SUELTES]") + pastilla del CTA; fondo con el mismo universo del hook para cerrar el círculo.

## 4. Estructura validada — colección (un slide por producto)

- **Hook:** fondo de la marca con brillo radial, palabra del concepto gigante con el acento en itálica encima, producto recortado enorme tapando la mitad inferior, línea de gancho + "Desliza" + pastilla con flecha.
- **Un slide por producto/variante:** nombre GIGANTE con "Nº 01" en el color de acento encima; recorte tapando ~40 % inferior; **lupa de detalle** (círculo de 200–230 px con zoom real de la textura, aro del color de acento, rótulo "EL DETALLE"); pastillas de variante (modelo, silueta, talla); bloque inferior con título + keyword, 1–2 líneas, barra de progreso y "DESLIZA →". **Fondos alternados** (oscuro / claro de la marca), ambos con grano.
- **CTA:** variante del hook en el fondo contrario, con la pregunta del concepto ("¿Cuál es tu…?"), bodegón de todos los productos y pastilla del CTA.
- Nombres reales de cada producto; avisa de los dudosos (un estampado que no es lo que dice el nombre, un material no confirmado).

## 5. Estructura para carruseles sin producto (alcance, leads, autoridad)

- **Hook:** estilo A o C, con la brecha de curiosidad del objetivo.
- **Valor:** un slide por idea, con número grande o contador; un recurso visual por slide (tachado, antes/después, columnas enfrentadas, cifra gigante, captura real enmarcada).
- **Prueba:** captura o dato real con su fuente en la capa editorial.
- **CTA:** el del objetivo, con la keyword en la caja y la razón para actuar ahora.
