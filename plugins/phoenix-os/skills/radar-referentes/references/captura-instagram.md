# Captura en Instagram con Claude in Chrome

Todo esto se hace en una pestaña nueva de Chrome, con las herramientas de `chrome-browser` ya cargadas. **Nunca inicies sesión en Instagram por el usuario.** Si su sesión ya está abierta en Chrome, se aprovecha (carga más reels al hacer scroll).

---

## Datos (Ruta B)

1. Abre `https://www.instagram.com/{usuario}/reels/`.
   - Sin sesión salen 12 reels: **los 3 primeros son fijados** (hits viejos) y 9 recientes. Con la sesión del usuario abierta, hacer scroll carga más.
2. **Views de la grilla:** cada `a[href*="/reel/"]` tiene las views en su `innerText`. Guárdalas tal cual ("1,2 M", "45.6K"): `outlier.py` las convierte.
3. **Shortcodes:** las herramientas bloquean salidas que parecen base64. Devuélvelos como `sc.split('').join('.')` y reconstrúyelos quitando los puntos.
4. **Likes, comentarios, fecha y caption:** `fetch('/{usuario}/reel/{sc}/')` + `DOMParser` + `meta[name="description"]`. Formato: `N likes, M comments - usuario el FECHA: "caption"`.
   - Espacia **1,2 s** entre requests.
   - Las promesas no se devuelven: guarda en `window.__data` y léelo en otra llamada.
   - La salida se corta cerca de 1.500 caracteres: **lee en bloques de 6 filas**.
   - Convierte la fecha a AAAA-MM-DD antes de guardarla.
5. Anota el **idioma, seguidores y bio** de cada perfil → `datos/creadores.csv`.
6. Marca `fijado = 1` en los reels fijados (los 3 primeros de la grilla sin sesión; con sesión, los que muestran el ícono de fijado).

Guarda todo en `datos/reels.csv` **antes** de analizar.

---

## Perfil y grilla (una captura por creador)

1. En `/{usuario}/reels/`, oculta el diálogo de login, aplica `document.body.style.zoom='0.4'` y `scrollTo(0,0)`.
2. `zoom` con `save_to_disk` sobre la columna central (aprox. región **598,28 a 972,638** en un viewport de 1568 px). Sale una imagen de ~720×1177.
3. De ahí se recortan (con Pillow):
   - **Encabezado** (foto, nombre, bio): y de 0 a ~185–212 según el perfil.
   - **Miniaturas** de la grilla: celdas de **166×262** desde x=22, paso **168** en x y **263** en y. La fila 1 empieza entre y=378 y 404 según el perfil.
   - **Verifícalo armando una hoja de contacto** con todas las miniaturas antes de usarlas. El orden de la grilla es el mismo de la Ruta B (así se cruza cada miniatura con su shortcode).

---

## Tira de 4 cuadros (cada ganador y cada contraste)

**La pestaña tiene que estar visible** (`document.visibilityState === 'visible'`); si no, Chrome no carga los videos y hay que pedirle al usuario que ponga la ventana al frente unos minutos.

En la página del reel (`/reel/{sc}/`) corre:

```js
document.querySelectorAll('div[role="dialog"]').forEach(function(d){var p=d;for(var i=0;i<6&&p.parentElement&&p.parentElement!==document.body;i++)p=p.parentElement;p.style.display='none';});window.__strip='run';(async function(){var sl=function(ms){return new Promise(function(r){setTimeout(r,ms)})};var v;for(var k=0;k<40;k++){v=document.querySelector('video');if(v&&v.readyState>=2&&isFinite(v.duration))break;if(v){v.muted=true;try{v.play()}catch(e){}}await sl(250);}if(!v||!isFinite(v.duration)){window.__strip='novideo';return;}v.pause();var D=v.duration;var ts=[0.3,2,D*0.5,D*0.9];var W=270,H=480;var c=document.createElement('canvas');c.width=W*4+6;c.height=H;c.style.cssText='position:fixed;left:0;top:0;z-index:2147483647;background:#000';document.body.appendChild(c);var g=c.getContext('2d');for(var i=0;i<ts.length;i++){await new Promise(function(res){var done=false;var f=function(){if(!done){done=true;v.removeEventListener('seeked',f);setTimeout(res,450);}};v.addEventListener('seeked',f);v.currentTime=Math.min(ts[i],D-0.1);setTimeout(f,4000);});try{g.drawImage(v,i*(W+2),0,W,H);}catch(e){}}window.__strip='done:'+D.toFixed(1);})();
```

1. Espera **9 s**.
2. Confirma que `window.__strip` diga `done:<duración>` y **anota la duración** (columna `duracion_s`).
3. `zoom` con `save_to_disk` sobre **0,0 a 1086,480** → `capturas/{sc}.png`.
4. Máximo **2 reels por `browser_batch`**.
5. Si dice `novideo`, revisa la visibilidad de la pestaña y vuelve a intentar.

Luego `marca.py tira` corta los 4 cuadros solo (4×270 px con 2 px de separación, escalado a lo que haya salido en la captura) y arma la tira brandeada.

---

## Problemas comunes

| Síntoma | Causa | Arreglo |
|---|---|---|
| `novideo` en todos los reels | Pestaña oculta o ventana minimizada | Pedir que la ventana de Chrome quede al frente |
| Shortcodes cortados o bloqueados | La salida parece base64 | `sc.split('').join('.')` |
| La salida de JS llega cortada | Límite ~1.500 caracteres | Leer `window.__data` en bloques de 6 filas |
| Las miniaturas no coinciden con los reels | Fila 1 desplazada (378–404) | Hoja de contacto y ajustar el y de inicio |
| Instagram pide login a cada rato | Sin sesión | Trabajar con los 12 reels visibles y reportarlo en límites |
