---
name: calendario-contenido
description: "Arma calendarios o parrillas de contenido para una marca o cliente con un método en orden: 10 problemas del avatar, ángulos y pilares, formatos ganadores del nicho (con el radar de referentes) y estructura semanal (atracción, dolor, prueba social, venta, estilo de vida), entregado como hoja filtrable. Úsala cuando pidan un calendario, parrilla, plan de contenido del mes o de la semana, o ordenar contenido ya grabado de un cliente."
---

# Calendario de contenido — método base

Este es el basamento para cualquier calendario de contenido, sea de una marca propia o de un cliente. Se sigue en orden: cada paso se construye sobre el anterior. No se salta al calendario sin tener primero los problemas y los ángulos.

## Paso 1 — Los 10 problemas del avatar

Listar 10 problemas reales del cliente ideal.

- Escritos con las palabras del avatar, no con jerga de marketing ("no me llegan clientes por Instagram", no "baja tasa de conversión orgánica").
- Concretos y específicos: cada uno debe poder convertirse en un video por sí solo.
- Para cada problema anotar: el dolor (qué siente), la consecuencia (qué le cuesta) y el deseo (qué quiere lograr).
- Fuentes: la ficha de marca (`references/ficha-marca.md`, sección Avatar), entrevistas o llamadas con el cliente, transcripciones (Fathom u otra), comentarios, DMs, reseñas, preguntas frecuentes.
- Si falta información para llegar a 10, preguntar al usuario antes de inventar.

## Paso 2 — Ángulos de comunicación = pilares de contenido

De cada problema sacar ángulos de comunicación. Esos ángulos son los pilares de contenido.

Ángulos útiles para derivar de un problema:
- Error común que lo causa
- Mito o creencia falsa
- Contraintuitivo / opinión polémica
- Antes y después
- Historia (propia o de un cliente)
- Paso a paso / cómo se resuelve
- Comparación (camino A vs camino B)
- Costo de no resolverlo

Agrupar los ángulos en 3–5 pilares claros. Cada pieza del calendario debe poder rastrearse a un problema y a un pilar.

## Paso 3 — Formatos ganadores del mercado

Identificar qué formatos están funcionando en el nicho ahora (no en general).

- Revisar referentes y competidores del nicho con la skill `radar-referentes`: usa los formatos que salgan como **probados** (3x o más en 2 creadores) y marca como "a probar" los de un solo creador.
- Anotar cada formato con evidencia: quién lo usa, qué rendimiento tiene, por qué funciona.
- Ejemplos de formato: talking head, B-roll con voz en off, carrusel educativo, historias con encuesta/caja de preguntas, testimonio en video, detrás de cámaras, tendencia adaptada.
- Para adaptar un formato ajeno a la marca, usar la skill `adaptador`.

## Paso 4 — Estructura semanal

Con problemas, pilares y formatos definidos, se arma la semana con este objetivo por día:

| Día | Objetivo |
|---|---|
| Lunes | Atracción + lead magnet |
| Martes | Convencimiento + dolores |
| Miércoles | No definido en el método base: preguntar al usuario qué va, o dejarlo libre |
| Jueves | Prueba social |
| Viernes | Dolores + venta |
| Sábado y domingo | Estilo de vida |

Notas por objetivo:
- **Atracción + lead magnet**: contenido de alcance (hook fuerte, tema amplio del nicho) con CTA a un recurso gratuito.
- **Convencimiento + dolores**: tocar un problema del Paso 1 a fondo, romper objeciones, mostrar que entiendes al avatar.
- **Prueba social**: testimonios, resultados, casos, capturas, antes/después de clientes.
- **Dolores + venta**: agitar el dolor y presentar la oferta con CTA directo.
- **Estilo de vida**: humanizar la marca o a la persona, día a día, valores, detrás de cámaras.

## Paso 5 — Llenar el calendario

Cada pieza del calendario lleva estas columnas:

Fecha · Día · Objetivo del día · Problema (del Paso 1) · Pilar/ángulo · Formato · Hook · CTA · Red(es) · Estado (grabado / por grabar / guionizado / publicado)

- Rotar los 10 problemas a lo largo del mes para no repetir el mismo dolor dos semanas seguidas.
- Entregar el calendario como hoja (tipo Sheets si está disponible) para que se pueda filtrar y actualizar.
- Para escribir cada pieza: `creador-de-guiones` (reels hablados), `guion-broll` (B-roll con voz en off), `carrusel-tryhard` (carruseles), `historias` (stories).

## Caso especial: cliente con contenido ya grabado

Cuando el cliente ya tiene material grabado, el método sigue siendo la base, pero el orden cambia:

1. Hacer igual los Pasos 1 y 2 (problemas y pilares), porque son el criterio para clasificar.
2. Inventariar el material grabado: listar cada pieza con una línea de qué dice.
3. Etiquetar cada pieza con problema, pilar, formato y el objetivo de día al que mejor encaja.
4. Acomodar las piezas en la estructura semanal.
5. Detectar los huecos (días u objetivos sin pieza) y solo esos se guionizan y se mandan a grabar.
6. Marcar en la columna Estado qué está grabado y qué falta.

## Programación en Metricool (opcional)

Si Metricool está conectado:
- Usar el mejor horario por red (`getBestTimeToPostByNetwork`) para sugerir la hora de cada pieza.
- Revisar lo ya programado (`getScheduledPosts`) para no duplicar.
- Programar solo con confirmación explícita del usuario, pieza por pieza o lote aprobado. Preferir enviar a revisión (`createScheduledPostForReview`) cuando el contenido es de un cliente.