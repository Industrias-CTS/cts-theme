# Cómo ejecutar y ver el diseño

## 1. Ver el lienzo publicado (sin instalar nada)

Abrir en el navegador:

> https://claude.ai/code/artifact/c6735804-7f9c-4f31-ac8c-090a11b5e0ef

- Lienzo con pan/zoom; cada hoja es un artboard.
- Con acceso de escritura se puede editar en sitio (clic para seleccionar,
  panel de propiedades, texto en línea) y **Guardar** publica la versión para
  todos. Solo lectura: ver y exportar PNG/PDF desde la barra del lienzo.
- El enlace comparte dentro de la organización; para externos, exportar PNG/PDF.

## 2. Ver una hoja localmente (revisión rápida)

Cada `artboards/*.dc.html` abre directo en un navegador:

```bash
google-chrome artboards/Colores.dc.html
# o
firefox artboards/Estructura.dc.html
```

Se ve la hoja tal cual (sin el editor del lienzo). Útil para revisar un cambio
antes de publicarlo.

## 3. Regenerar las hojas después de editar

Los `.dc.html` **no se editan a mano**: son salida de `build.py` (los tokens
están al inicio del archivo; cada hoja es una función `v_*`).

```bash
python3 build.py
# → escribe artboards/*.dc.html y artboards/canvas.json
```

Requisitos: Python 3 estándar (sin dependencias). El logo `logo-cts-blanco.png`
debe existir junto a `build.py`.

## 4. Publicar los cambios al lienzo

Desde Claude Code, en esta carpeta:

1. Invocar `/design` y pedir: *"re-siembra el Sistema de Diseño CTS desde
   ~/.projects/cts-theme/docs/demo/artboards y actualiza el lienzo
   existente"* (el enlace de arriba).
2. Claude re-siembra `sistema-diseno-cts.html` con todos los artboards +
   `canvas.json` + logo y lo guarda **al mismo enlace** (no crear uno nuevo).

`sistema-diseno-cts.html` es el lienzo sembrado completo: también abre en un
navegador como visor local con exportación PNG/PDF, pero se regenera en cada
publicación — no editarlo a mano.

## 5. Verificación visual (opcional)

Captura sin abrir ventana, para comparar antes/después:

```bash
google-chrome --headless=new --hide-scrollbars \
  --window-size=1440,1600 --screenshot=/tmp/hoja.png \
  "file://$PWD/artboards/Controles.dc.html"
```

Cuidar que el contenido de cada hoja quepa en la altura declarada en
`artboards/canvas.json` (lo que sobre se recorta en el lienzo).
