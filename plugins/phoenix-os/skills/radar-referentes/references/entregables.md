# Entregables del Radar — especificación

Los tres siempre, con la marca Phoenix OS × Luis Rocha que sale de `scripts/marca.py`. Ningún número se escribe de memoria: todos vienen de `analisis/reels_puntuados.csv` y `analisis/resumen.json`. Todo lo del cliente (oferta, avatar, dolores, CTA, pruebas) viene de `datos/brief.md`.

---

## 1. PDF — `Radar-referentes-{nicho}.pdf`

### Cómo se arma

1. `python scripts/marca.py css entrega/marca.css` → CSS con fuentes Inter, colores y componentes (`.seccion`, `.num`, `.chip`, `.negro`, `.hook`, `.metrica`, `.ficha`, `.cols2`, `img.tira`, `.portada`, `.kpis`, `.foto`, `.logo`).
2. Escribe dos HTML que enlacen ese CSS:
   - `portada.html` con `@page{size:A4;margin:0}` y un solo `<div class="portada">`.
   - `cuerpo.html` con una `<section class="seccion">` por sección (cada una empieza en página nueva).
   - Imágenes por `file://` o ruta relativa (logo, foto, tiras).
   - Para el logo y la foto en la portada usa los archivos de `assets/` o `marca.a_data_uri(marca.foto_circulo(400))`.
3. `python scripts/marca.py pdf entrega/portada.html entrega/cuerpo.html Radar-referentes-{nicho}.pdf --nicho "{nicho}"`
   → portada con márgenes 0 + cuerpo A4 con márgenes de 15 mm y pie "Phoenix OS × Luis Rocha · Radar de referentes · {nicho} · fecha · página", unidos con pypdf.

### Orden (lo aplicable primero)

Cada sección empieza en página nueva con su número en chip lima.

1. **Portada negra:** etiqueta "RADAR DE REFERENTES · ANÁLISIS DE CREADORES", título del nicho, nombre del cliente, referentes, fecha, 3 números clave en lima, foto de Luis en círculo con borde lima y logo.
2. **Ideas para grabar:** arriba, caja **"Para quién es"** (clase `.metrica`): cliente · oferta + CTA · avatar y sus 3 dolores principales, en 3 líneas. Debajo, tabla resumen (idea, dolor que ataca, formato de origen, métrica del referente, qué medir), regla de hook y metas.
3. **Una ficha por idea, en una sola página:** encabezado negro con el hook en lima, línea "Ataca: {dolor con sus palabras} → cierra con: {CTA del brief}", caja de métrica, tira de referencia de ~100 mm, tabla de tiempos, edición en 2 columnas, pie con caption · CTA · qué medir. Renderiza y revisa que **ninguna ficha se pase de página**.
4. **Lección de hook:** el par A/B con las dos tiras y una tabla.
5. **Formatos que se repiten:** encabezado negro, mecanismo, por qué lo suben, ojo, y las tiras que no salieron en las fichas.
6. **Qué no copiar:** tabla patrón · evidencia.
7. **Una página por referente:** perfil + ganadores/fallidos + tabla de tops.
8. **Método y datos:** tabla de referentes, gráfico de puntos en escala log (carril por creador, líneas en 1x y 3x, recientes 3x+ en lima, fijados en aro, resto gris), los N reels y los límites (incluye los campos del brief `POR CONFIRMAR`).
9. **Anexo · Brief del cliente:** contexto, oferta y avatar tal como quedaron en `datos/brief.md`, con fecha y fuente.
10. **Cómo usar el brief para IA.**

### Revisión

Rasteriza todas las páginas (`pdftoppm -r 40`) y arma una hoja de contacto; mira también una ficha a 110 dpi. Busca: fichas partidas en dos páginas, tiras faltantes, textos cortados, números que no coinciden con el CSV, ideas cuyo dolor o CTA no estén en el brief.

---

## 2. Imagen para Miro — `Radar-{nicho}-Miro.png`

3600 px de ancho (versión mejorada de la plantilla "Análisis de Competencia"):

- **Encabezado:** `marca.encabezado(3600, "Radar · {nicho}", "{n} referentes · {fecha}")` (logo, título y foto).
- **Franja "Cómo leerlo":** x = veces la mediana del creador · 3x se estudia · 5x se replica · lima = ganador · rojo = fallido.
- **Una columna por referente:**
  - recorte del perfil (solo foto, nombre y bio, **misma altura en todas**);
  - caja de datos (mediana, mejor reciente, seguidores, motor);
  - fila **GANADORES**: 4 miniaturas de la grilla con chip de x, views, comentarios y etiquetas TOP VIEWS / TOP LIKES / TOP COMENT. / MEJOR RECIENTE (columna `tops` del CSV);
  - fila **FALLIDOS** con el porqué;
  - caja **LECCIÓN** en lima.
- **Banda inferior:** "Para quién es" (cliente · oferta · avatar en una línea), formatos probados, A/B de hook e ideas con el dolor que ataca cada una.
- Recorta los textos que no quepan con "…" (`marca.recortar`). Fuentes y colores de `marca.py`.

Revisa la imagen completa y un recorte ampliado de una columna antes de entregar.

---

## 3. Brief para IA — `brief-guiones-{nicho}.md`

Para pegar en cualquier IA (o pasarlo a `creador-de-guiones`). Lleva, en este orden:

1. **Instrucciones para la IA:** "usa solo estos mecanismos, no inventes datos; si falta un dato, márcalo como [POR CONFIRMAR]".
2. **Datos del cliente, llenos desde `datos/brief.md`:** quién graba, negocio, ciudad, idioma, avatar con sus dolores y objeciones (con sus palabras), oferta, promesa, palabra clave del CTA y canal, lead magnet, pruebas que puede demostrar, tono y lo prohibido. Solo lo que esté `POR CONFIRMAR` en el brief se deja así.
3. **Reglas fijas:** hook que invita o pregunta y deja algo vacío en pantalla; caption que termina en pregunta; una sola acción; sin estereotipos; números verificables; voz humana (sin "no se trata de X sino de Y", sin "descubre", sin tríos rítmicos); qué evitar (lo de "Qué no copiar").
4. **Las ideas completas:** dolor del avatar que ataca, cómo conecta con la oferta, métrica del referente con link, hook, tiempos, edición, caption, CTA, qué medir, condición.
5. **Formato de salida:** tabla `tiempo · en pantalla · se dice · plano y edición`; caption; CTA; qué medir; datos a confirmar.
6. **Un guion de ejemplo completo** para calibrar, escrito para ese avatar y esa oferta.
7. **Links de referencia** de cada reel citado.

---

## Cierre en el chat

Entrega los tres con `SendUserFile` y cierra con **3 hallazgos** en pocas líneas (el formato más fuerte, la lección de hook y lo que no hay que copiar). Si salió con marca de texto porque faltaba un activo, dilo en una línea.
