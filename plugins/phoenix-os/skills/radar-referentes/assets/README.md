# Activos de marca — Phoenix OS × Luis Rocha

Estos archivos hacen que cualquier persona del equipo que corra el Radar obtenga el output con la marca, sin adjuntar nada.

| Archivo | Qué es | Formato recomendado |
|---|---|---|
| `phoenix-logo.png` | Logo de Phoenix OS (hoy: el símbolo P con el fénix) | PNG con fondo transparente, versión para fondo negro |
| `phoenix-p.png` | Símbolo P (mini logo de tiras, portada y encabezado) | PNG transparente; el actual mide 244×275 px, si hay versión más grande o SVG, reemplázalo |
| `luis-rocha.jpg` | Foto de Luis, recortada cuadrada al rostro | Cuadrada, rostro centrado, mínimo 600 px |
| `fonts/` | Inter e Inter Display | Incluidas, licencia SIL OFL 1.1 (`fonts/LICENSE-Inter.txt`) |

En encabezados, `marca.lockup()` arma "P + PHOENIX OS" en Inter Display Black. Si `phoenix-p.png` no existe, `marca.py` recorta el cuadro izquierdo del logo. Si falta el logo o la foto, usa la marca de texto y lo avisa.

**Para actualizar la marca:** reemplaza el archivo con el mismo nombre, corre `python scripts/marca.py check` y sube el cambio al repo.
