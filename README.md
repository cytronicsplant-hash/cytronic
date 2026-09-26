# Sitio web de Cytronics Plant

Sitio estático (HTML, CSS y JS, sin frameworks).

## Editar
Los textos están en `build.py`. Después de cambiarlos:

```
python build.py
```

Eso regenera `index.html` y las páginas de `servicios/`. No edites esos HTML a mano.
Los estilos están en `styles.css` y el comportamiento en `script.js`.

## Ver en local
```
python -m http.server 8080
```
y abrir http://localhost:8080

## Formulario
Usa FormSubmit (`FORM_ENDPOINT` en `build.py`). El primer envío llega a
cytronicsplant@gmail.com con un enlace de activación que hay que aprobar una vez.
