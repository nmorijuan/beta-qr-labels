# 🤝 Guía de Contribución

Agradecemos tu interés en contribuir a QR Colmenas. Este documento te guiará sobre cómo hacerlo.

## 📋 Código de Conducta

Por favor, sé respetuoso y constructivo en todas las interacciones.

## 🐛 Reportar Bugs

Si encuentras un bug, por favor abre un issue en GitHub con:

1. **Descripción clara** del problema
2. **Pasos para reproducir**
3. **Comportamiento esperado** vs **actual**
4. **Screenshots** (si es relevante)
5. **Ambiente**: Windows/Mac/Linux, versión de Python, navegador

## 💡 Sugerencias de Mejoras

Nos encantaría recibir tus ideas:

1. Abre un issue con la etiqueta `enhancement`
2. Describe la funcionalidad que propones
3. Explica por qué sería útil
4. Muestra ejemplos si es posible

## 🔧 Contribuir Código

### Configurar el entorno

```bash
# Fork el repositorio en GitHub

# Clona tu fork
git clone https://github.com/TU_USUARIO/QR-Colmenas-Web.git
cd QR-Colmenas-Web

# Crea una rama para tu feature
git checkout -b feature/mi-nueva-feature

# Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Instala dependencias
pip install -r requirements.txt
```

### Hacer cambios

1. **Escribe código limpio** siguiendo PEP 8
2. **Añade comentarios** donde sea necesario
3. **Prueba tu código** localmente
4. **Actualiza la documentación** si es necesario

### Commits

Usa mensajes descriptivos:

```bash
git commit -m "Añadir validación de correo en formulario"
git commit -m "Arreglar bug en generación de QR"
git commit -m "Mejorar rendimiento de carga de archivos"
```

### Push y Pull Request

```bash
# Sube tu rama
git push origin feature/mi-nueva-feature

# Crea un Pull Request en GitHub
# Describe qué cambios hiciste y por qué
```

## 📝 Estilos de Código

### Python

```python
# ✓ Bien
def generar_zpl(archivo_excel):
    """Genera etiquetas ZPL desde un archivo Excel."""
    # Código aquí
    pass

# ✗ Evitar
def GenZpl(f):
    # código
    pass
```

### JavaScript

```javascript
// ✓ Bien
function cargarArchivo(archivo) {
    if (!archivo) return;
    // código
}

// ✗ Evitar
function loadFile(file){
// código
}
```

### HTML/CSS

```html
<!-- ✓ Bien -->
<div class="upload-area" id="uploadArea">
    <p class="upload-text">Arrastra tu archivo aquí</p>
</div>

<!-- ✗ Evitar -->
<div id="upload">
    <p style="color: blue; font-size: 16px;">Arrastra aquí</p>
</div>
```

## 🧪 Testing

Por favor prueba tus cambios:

```bash
# Ejecuta la aplicación localmente
python app.py

# Prueba en diferentes navegadores
# Prueba con archivos de diferentes tamaños
# Verifica que los estilos se vean bien en móvil
```

## 📚 Documentación

Si añades una nueva feature, por favor documenta:

1. El código (comentarios y docstrings)
2. El README.md (si es una feature importante)
3. Las instrucciones de uso

## 🎯 Áreas donde podemos ayuda

- 🌐 Soporte multiidioma (i18n)
- 📊 Estadísticas y análiticas
- 🔒 Autenticación de usuarios
- 💾 Base de datos para historial
- 🎨 Temas oscuros/claros
- 📱 Aplicación móvil
- 🔌 Integración con APIs externas

## 📞 Preguntas

¿Tienes dudas? 

- Abre un issue con la etiqueta `question`
- Revisa los issues existentes
- Consulta la documentación

## ✨ Gracias

¡Gracias por contribuir a QR Colmenas! Cada contribución, sin importar su tamaño, es valiosa.

---

**Recuerda:** Los cambios deben pasar por review antes de ser mergeados. Sé paciente y constructivo con los comentarios.

¡Feliz coding! 🐝
