# Revisión antes de subir (18 oct 2026)

Qué se encontró al juntar las skills, qué se corrigió y qué queda pendiente. Sirve también como registro de cambios de la versión 1.0.0.

---

## Datos incorrectos o contradictorios que se corrigieron

| Dónde | Problema | Qué se hizo |
|---|---|---|
| `historias` | Tenía un perfil de Offbasic que describía venta de réplicas 1:1 de productos de marcas ajenas, keyword `PRECIO` y Aliados "en pausa" | Se eliminaron todos los perfiles de marca. Además, regla explícita en `adaptador` y `carrusel-tryhard`: cero contenido para réplicas o marcas ajenas |
| `carrusel`, `carrusel-tryhard`, `creador-de-guiones`, `historias` | Perfil viejo de Offbasic (Aliados, `PROTOCOLO`) que `adaptador` ya marcaba como obsoleto desde el 26 ago | Perfiles fuera; todas las skills leen una sola **ficha de marca** |
| `adaptador` vs `carrusel-tryhard` | Áurica: uno decía titulares en Cormorant Unicase y verde `#10312A`; el otro (más nuevo) que ambos estaban rechazados | Perfiles fuera. La lección quedó como regla general: titulares con peso, nada de versalitas finas |
| `creador-de-guiones` | Ejemplos de hook con "un aliado me mandó captura…", "importación", "producto que ya se mueve" (modelo de negocio viejo) | Reescritos con ejemplos neutros |
| `creador-de-guiones` | El ejemplo ✅ de humanización usaba un guion largo, que la misma skill prohíbe como "tell" de IA | Corregido |
| `calendario-contenido` | Nombres de clientes (Jorge, Diego) | Quitados |
| `guion-broll` | Sección "por marca" con Áurica, Offbasic, Ohclock y la marca personal; ejemplo firmado por Áurica | Reemplazada por guía según el tipo de marca; ejemplo sin marca |
| `historias` | Cargaba fuentes por Google Fonts (suele estar bloqueado y la fuente cambia al exportar) | Fuentes embebidas en base64 con `scripts/fuentes.py` |

## Radar de referentes

| Antes | Ahora |
|---|---|
| Había que adjuntar logo y foto en cada conversación; si no, salía sin marca | Logo, símbolo P, foto de Luis y fuentes Inter viven en `assets/`. `marca.py check` avisa si falta algo |
| La tira, el CSS del PDF y el pie se armaban a mano cada vez | `scripts/marca.py` lo hace igual siempre: tira brandeada, CSS, PDF (portada + cuerpo + pie), encabezado de Miro |
| El puntaje outlier estaba como fragmento de código | `scripts/outlier.py` con esquema de CSV fijo, convierte "1,2 M" / "45.6K" / "12,3 mil", tops, pares A/B, formatos probados y avisos para "Límites" |
| `conv` fallaba si los likes estaban ocultos (división por cero) | Queda vacío y se avisa |
| Nuevo paso 5 | Etiquetar `formato` y `hook` después de ver las tiras y recalcular: la tabla de formatos sale del mismo cálculo |
| Revisión final | Ahora exige cruzar cada número de los entregables contra `reels_puntuados.csv` |

**Cambio de criterio que debes validar:** la mediana de cada creador ahora se calcula con sus reels **no fijados de 5 días o más** (antes: todos los no fijados). Los reels recién publicados todavía no juntan sus views y bajaban la mediana, inflando la x de todos los demás. Si quedan menos de 5 reels maduros, se usa todo lo no fijado y se marca "mediana inestable".

## Carrusel tryhard

- Ahora sirve para cualquier marca: **preguntas de entrada** (fin del carrusel, cómo debe verse, qué hay de la marca, qué recursos hay) y una segunda ronda para concepto, datos reales y CTA.
- Nuevo `references/objetivos-y-cta.md`: el objetivo decide el CTA, la estructura y 2–3 palancas de neuromarketing, cada una con su **condición de verdad** (falsa escasez, testimonios o cifras inventadas: prohibidos).
- Lo mejor de la skill `carrusel` (ángulos de hook, ADN de referencias visuales) se fusionó aquí; la skill `carrusel` vieja no se sube.
- Scripts probados: `efectos.py` (luz de borde, perspectiva, estela, fantasmas, fondos, hoja de contacto), `fuentes.py`, `render.py` (PNG por slide + avisos de desborde).

## Qué no se subió (y por qué)

| Skill | Motivo |
|---|---|
| `operador` | Es tu plan personal: decisiones, fases, links privados |
| `carrusel` | Reemplazada por `carrusel-tryhard` |
| `motion-graphics` | No la pediste en esta tanda (se puede sumar después) |
| `plan-accion-hyper-club` | No la pediste en esta tanda |
| Skills de navegador, documentos, etc. | Vienen con Claude |

## Pendientes

- [ ] **Validar el cambio de criterio de la mediana** (arriba).
- [ ] **Logo en alta resolución o SVG** del símbolo P: el actual mide 244×275 px; se ve bien en tiras y encabezados, pero en una portada grande o impresa conviene uno más grande.
- [ ] **Miércoles en `calendario-contenido`**: el método base no lo define (hoy pregunta o lo deja libre).
- [ ] Probar el radar completo con un nicho real después de instalar, para ver la ruta de Chrome en la cuenta de otra persona del equipo.
