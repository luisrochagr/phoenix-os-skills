---
name: radar-referentes
description: "Radar de creadores/referentes de Instagram de un nicho, siempre a partir del brief del cliente (contexto, oferta y avatar): puntaje outlier calculado en código, capturas cuadro por cuadro de los reels ganadores, formatos probados, hooks, qué no copiar e ideas listas para grabar que atacan los dolores del avatar y cierran con la oferta. Entrega PDF, imagen para Miro y brief para IA, todo con la marca Phoenix OS × Luis Rocha. Úsala cuando pidan analizar referentes, competidores o creadores de un nicho, un radar, ver qué formatos funcionan, o sacar ideas de contenido a partir de cuentas de Instagram."
---

# Radar de referentes · Phoenix OS × Luis Rocha

Convierte una lista de @ de un nicho en ideas que el cliente puede grabar, respaldadas por métrica y con capturas de cada video. Es la herramienta de Phoenix OS (agencia donde Luis Daniel Rocha es CSM) para sus clientes y para negocios propios.

**Regla que gobierna todo: el mecanismo se copia, el contenido nunca.** El tema, el producto y los números son del cliente.

**Regla de entrada: el input es siempre un brief del cliente.** Contexto breve, **oferta** y **avatar**, además de los referentes. Los referentes se leen contra ese brief: un formato que gana 6x para otro creador no sirve si le habla a un público que el cliente no tiene o si no hay oferta que lo cierre. **Sin brief no se abre Instagram.**

Al correr la skill: consigue el brief (Paso 0), conecta lo que falte (Paso 1) y después ejecuta todo el proceso sin pedir más permisos que los obligatorios. Crea una lista de tareas con los pasos 2 a 9 y ve marcándolos.

**Archivos de esta skill** (rutas relativas a su carpeta):

| Archivo | Para qué |
|---|---|
| `scripts/marca.py` | Kit de marca: tiras brandeadas, CSS, PDF con portada y pie, encabezado de Miro |
| `scripts/outlier.py` | Puntaje outlier, tops, pares A/B y formatos, desde un CSV |
| `assets/` | Logo Phoenix OS, mini logo P, foto de Luis y fuentes Inter (ver `assets/README.md`) |
| `references/brief-cliente.md` | **Input obligatorio:** campos del brief (contexto, oferta, avatar), mínimo para arrancar y plantilla |
| `references/captura-instagram.md` | Cómo sacar views, datos, perfiles y tiras de 4 cuadros con Chrome |
| `references/entregables.md` | Especificación exacta del PDF, la imagen de Miro y el brief |

> Las rutas `scripts/…`, `references/…` y `assets/…` son relativas a la carpeta de esta skill. Al correr un script, usa la ruta completa de esa carpeta (la que aparece junto a la skill en la lista de skills disponibles) y deja las salidas en tu carpeta de trabajo, nunca dentro de la skill.

---

## Paso 0. El brief del cliente (obligatorio, antes de todo)

Lee `references/brief-cliente.md`. El brief puede venir como formulario llenado, documento o transcripción de la llamada con el cliente, o la ficha de marca (`marca-{cliente}.md`). Pásalo al formato de la plantilla y guárdalo como **`datos/brief.md`**.

**Mínimo para arrancar** (si falta, se pide en un solo mensaje antes del Paso 1):
1. **Contexto:** cliente, qué hace, dónde opera, en qué momento está y objetivo del radar.
2. **Oferta:** qué vende, CTA y canal (palabra clave, DM, WhatsApp, link), pruebas que puede demostrar.
3. **Avatar:** quién compra y al menos 3 dolores con sus palabras (ideal también objeciones y deseo).
4. **Referentes:** 3 a 5 @ (y reels puntuales que quieran replicar, si hay).
5. **Idioma** y **quién graba** (dueño a cámara, vendedor, solo voz en off).

Usa AskUserQuestion solo para lo que tenga opciones (idioma, quién graba); lo demás se pide como texto. Lo que el cliente no sepa queda `POR CONFIRMAR` en el brief y va a "Límites"; **nunca se completa con algo plausible**.

**No preguntes por la marca:** el logo, la foto de Luis y las fuentes ya vienen en `assets/`. Corre `python scripts/marca.py check` al empezar. Si falta algún activo, el kit usa la marca de texto "Phoenix OS × Luis Rocha" y tú lo avisas en una línea; si el usuario adjunta el archivo en la conversación, cópialo a una carpeta de trabajo y úsalo (la carpeta de la skill puede ser de solo lectura).

No preguntes formato de entrega: siempre son los tres entregables del Paso 9.

## Paso 1. Conexiones

1. **Windsor.ai** (datos en volumen). Busca sus herramientas con ToolSearch (`windsor get_data get_connectors`).
   - Si no aparecen: `SearchMcpRegistry` con `["windsor"]` y `SuggestConnectors` con su `directoryUuid` para que el usuario lo conecte. Explícale en 3 líneas: en Windsor se agrega el conector **Instagram Public**, se autoriza con su propia cuenta Business o Creator y se escriben los @ de los referentes (no hay que conectar el Instagram de cada referente; cada @ cuenta como una cuenta del plan). Para auditar la cuenta del propio cliente (guardados, compartidos, alcance) se usa el conector **Instagram** (Insights) con acceso admin.
   - No te quedes esperando: si Windsor no está listo, sigue con la ruta de Chrome y úsalo cuando aparezca.
2. **Claude in Chrome** (views, capturas y videos). Lee primero la skill `chrome-browser` (viene con Claude), carga las herramientas en una sola ToolSearch (incluye `browser_batch`, `javascript_tool`, `get_page_text`) y trabaja en una pestaña nueva. **Nunca inicies sesión en Instagram por el usuario.**
3. Si no hay ni Chrome ni Windsor, dilo y pide que conecte uno de los dos; sin datos no hay análisis.

## Paso 2. Traer los datos

**Ruta A, Windsor:** Instagram Public por @: `media_permalink, media_product_type, media_caption, media_like_count, media_comments_count, media_timestamp, profile_followers_count`, 30 a 50 posts por creador. No trae views, guardados, compartidos ni transcripciones de cuentas ajenas: las views salen de la Ruta B.

**Ruta B, Chrome:** sigue `references/captura-instagram.md`, sección "Datos".

Guarda todo en **`datos/reels.csv`** con estas columnas exactas (las de `outlier.py`):

`creador, shortcode, url, views, fijado, likes, comentarios, fecha, caption, duracion_s, formato, hook`

- `views`, `likes` y `comentarios` pueden ir tal como los muestra Instagram ("1,2 M", "45.6K", "12,3 mil"): el script los convierte.
- `fecha` en AAAA-MM-DD. `fijado` en 1/0. Likes ocultos = celda vacía.
- Y en **`datos/creadores.csv`**: `creador, seguidores, idioma, bio`.

## Paso 3. Puntaje outlier (en código, nunca a ojo)

```bash
python scripts/outlier.py datos/reels.csv --creadores datos/creadores.csv --hoy AAAA-MM-DD --out analisis/
```

Sale `analisis/reels_puntuados.csv`, `resumen.json` y `resumen.md`. El script aplica las reglas:

- `x` = views ÷ mediana del creador. La mediana sale de sus reels **no fijados con 5 días o más** (si quedan menos de 5, usa todo lo no fijado y avisa "mediana inestable").
- `conv` = comentarios por cada 1.000 likes (vacío si los likes están ocultos).
- **3x o más se estudia; 5x o más se replica.** 0,5x o menos con 5+ días = fallido.
- Reels de menos de 5 días = "nuevo": nunca cuentan como fallidos.
- Fijados se reportan aparte: su x dice qué construyó la cuenta, no cómo le va hoy.
- Tops por creador: top views, top likes, top comentarios, mejor reciente, más conversación por like y peor reciente.
- **Pares A/B candidatos**: mismo creador, mismo día, uno rinde 3 veces o más que el otro. Confírmalos en las tiras (mismo set o formato) antes de usarlos: es la mejor evidencia de qué hook funciona.

Los avisos de `resumen.md` van a "Límites" del reporte. **No recalcules nada a mano**: si cambias un dato, vuelve a correr el script.

## Paso 4. Capturas (obligatorias: todo formato del que se habla va con su captura)

Sigue `references/captura-instagram.md`, secciones "Perfil y grilla" y "Tira de 4 cuadros". Lo esencial:

- **La pestaña tiene que estar visible.** Si `document.visibilityState` es `hidden`, Chrome no carga los videos: pide al usuario que ponga al frente la ventana de Chrome unos minutos.
- Tira de cada ganador y de cada contraste (0,3 s hook · 2 s · mitad · final). Anota la duración que devuelve el script: sirve para la edición.
- Mira cada tira: de ahí salen el hook exacto (texto en pantalla de 0 a 3 s), el formato, el estilo de edición y el remate. **El audio no se transcribe**: dilo en el reporte.
- **No se usan capturas de reels que se apoyan en estereotipos étnicos o de grupo:** en la imagen de Miro van difuminadas con la nota "no se copia" y en el PDF sin tira.

## Paso 5. Etiquetar formatos y recalcular

Con las tiras vistas, llena las columnas `formato` (nombre corto y consistente: "cliente llega al dealer", "talking head con precio en pantalla"…) y `hook` (texto exacto en pantalla) en `datos/reels.csv` y **vuelve a correr `outlier.py`**. Así la tabla de formatos (probado / a probar / sin evidencia) sale del mismo cálculo.

## Paso 6. Análisis

De cada ganador: hook exacto, tipo de hook, formato, escenario, dónde está el remate, **edición** (plano, cámara, texto fijo, subtítulos, gráficos, duración), por qué lo suben (alcance, confianza, autoridad, leads) y **si le habla al avatar del brief** (mismo comprador, mismo dolor, mismo nivel de precio). Un ganador que le habla a otro público se reporta en formatos con la nota "no es nuestro público" y no se convierte en idea.

- **Formato probado:** el mismo mecanismo con 3x o más en 2 creadores.
- **A probar:** un solo creador con 2 o más ganadores del mismo mecanismo.
- **Mira los del mismo formato que fallaron:** dicen qué variable hace ganar (ej.: el formato "cliente llega al dealer" gana cuando el cliente trae un conflicto de dinero; sin eso queda en 0,7x).
- **Qué no copiar:** lo que se repite en los reels de 0,5x o menos (patrocinados, salirse del nicho, hablarle a colegas en vez de a compradores, tandas sin hook ni caption) y lo que choca con la oferta, el avatar o lo prohibido del brief.
- Nada de cifras que el cliente no pueda probar.

## Paso 7. Ideas aplicables al nicho (3 a 5)

Cada idea sale del cruce **formato ganador × dolor del avatar × oferta del cliente**. Si una idea no ataca un dolor del brief, no cierra con su CTA o necesita una prueba que el cliente no tiene, no entra.

Cada idea es una ficha con: título, formato de origen y estado, **dolor del avatar que ataca** (con sus palabras), **cómo conecta con la oferta**, **hook exacto** + nota de qué se ve en el primer segundo, **métrica del referente** que la respalda (x, views y link), por qué funciona, condición, estructura por tiempos (0-2 s, desarrollo, remate, cierre), **edición** (plano, cámara, texto en pantalla, subtítulos, gráficos, duración según los referentes), caption que termina en pregunta, CTA (una sola acción: el **CTA y canal del brief**), **qué medir** (meta: 3x la mediana del propio cliente; juzgar una serie después de 3 episodios), variantes siguientes y la tira de referencia.

Regla de hook para todas: el hook invita o pregunta y deja algo vacío en pantalla; la respuesta llega al final.

## Paso 8. Marca (siempre con `scripts/marca.py`)

Phoenix OS × Luis Rocha: fondo negro `#000`, verde lima `#BDFA71`, texto blanco `#F5F6F3`, gris `#969B94`, rojo para fallidos `#FF786C`. Fuentes Inter / Inter Display (incluidas en `assets/fonts`). Mini logo P y foto de Luis en círculo con borde lima.

**Tiras:** una por ganador y por contraste:

```bash
python scripts/marca.py tira capturas/{sc}.png tiras/{creador}-{sc}.png --creador {creador} --x {x} \
  --views {views} --comentarios {comentarios} --url {url} --notas "qué pasa en 0,3 s" "en 2 s" "en la mitad" "al final"
```

La tira detecta sola el área útil de la captura (lo que no es el fondo `#0C1014`), corta los 4 cuadros y agrega: barra superior lima "CREADOR · Nx SU MEDIANA · VIEWS · COMENTARIOS", mini logo arriba a la derecha, chip lima por cuadro ("0,3 s · HOOK", "2 s", "MITAD", "FINAL"), una línea blanca bajo cada cuadro, el link del reel y "Phoenix OS × Luis Rocha" al pie. **Los valores de x, views y comentarios se copian de `reels_puntuados.csv`, nunca se escriben de memoria.**

## Paso 9. Entrega (último paso, siempre los tres)

Especificación completa en `references/entregables.md`. En corto:

1. **PDF** `Radar-referentes-{nicho}.pdf`: HTML con `marca.py css` y `marca.py pdf` (portada a sangre + cuerpo A4 con pie de marca). **Lo aplicable primero**: portada → ideas para grabar (con caja "Para quién es": cliente · oferta · avatar) → una ficha por idea en una sola página → lección de hook (A/B) → formatos que se repiten → qué no copiar → una página por referente → método y datos → brief del cliente (anexo) → cómo usar el brief para IA.
2. **Imagen para Miro** `Radar-{nicho}-Miro.png`, 3600 px de ancho, con `marca.encabezado()` arriba y una columna por referente.
3. **Brief para IA** `brief-guiones-{nicho}.md`, para pegar en cualquier IA: los datos del cliente van **llenos desde `datos/brief.md`** (solo lo pendiente queda `POR CONFIRMAR`), con un guion de ejemplo completo escrito para ese avatar y esa oferta.

**Revisión antes de entregar (obligatoria):**
- Cada número del PDF, la imagen y el brief coincide con `reels_puntuados.csv` (búscalos uno por uno; si no coincide, se corrige el entregable, no el CSV).
- Abre el PDF renderizado (miniaturas de todas las páginas): ninguna ficha se pasa de página, ninguna tira falta, ningún texto se corta.
- Abre la imagen de Miro completa y un recorte ampliado de una columna.
- Cada idea nombra un dolor que está en `datos/brief.md` y cierra con el CTA del brief; ninguna usa una prueba que no esté en el brief.
- `marca.py check` pasó, o avisaste que salió con marca de texto.

Entrega los tres con `SendUserFile` y cierra con 3 hallazgos en pocas líneas. Si el usuario quiere editarlo en equipo, ofrece el mismo contenido como documento editable.

## Límites que siempre se reportan

Los campos del brief que quedaron `POR CONFIRMAR`, tamaño de la muestra por creador, si hubo o no sesión de Instagram, que el audio no está transcrito, que los fijados son de otra época, que los reels de menos de 5 días todavía suman views y los avisos de `resumen.md`.

## Después

- Para escribir los guiones completos, pasa el brief para IA a la skill `creador-de-guiones` (reels hablados) o `guion-broll` (voz en off sin cara).
- Si el cliente todavía no tiene ficha de marca, `datos/brief.md` es la base para crearla con `adaptador`.
- Para meter las ideas en un calendario, usa `calendario-contenido` (el radar es su Paso 3).
- Para adaptar un reel puntual a una marca, usa `adaptador`.
