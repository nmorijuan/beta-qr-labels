# 🐝 QR Colmenas - Generador de Etiquetas

Una aplicación web para generar e imprimir etiquetas QR de colmenas desde archivos Excel. Diseñada para impresoras Zebra ZT230.

![Flask](https://img.shields.io/badge/Flask-3.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Características

- ✅ Interfaz web moderna y responsive
- 📤 Carga de archivos Excel (.xlsx, .xls)
- 👁️ Previsualización de datos antes de generar
- 🏷️ Generación de etiquetas ZPL
- 🖨️ Envío directo a impresoras Zebra
- ⬇️ Descarga de archivos ZPL
- 📱 Compatible con desktop y móvil
- 🌐 Acceso remoto desde cualquier lugar

## 📋 Requisitos

- Python 3.8 o superior
- pip
- Navegador web moderno
- (Opcional) Impresora Zebra ZT230

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/QR-Colmenas-Web.git
cd QR-Colmenas-Web
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 📖 Uso

### Paso 1: Cargar archivo Excel

1. Accede a `http://localhost:5000`
2. Arrastra tu archivo Excel o haz clic para seleccionar
3. El archivo debe contener las columnas: **CODIGO** y **CODIGO-DNI**

### Paso 2: Previsualizar datos

- Se mostrará automáticamente una vista previa de los datos
- Verifica que los datos sean correctos
- Haz clic en "Generar Etiquetas" para continuar

### Paso 3: Generar y imprimir

- Las etiquetas se generarán en formato ZPL
- Puedes descargar el archivo ZPL
- O enviar directamente a imprimir (si tienes una impresora Zebra)

## 📊 Formato del archivo Excel

El archivo Excel debe tener las siguientes columnas:

| CODIGO | CODIGO-DNI |
|--------|-----------|
| QR001  | DNA-001   |
| QR002  | DNA-002   |
| QR003  | DNA-003   |

**Notas:**
- Los nombres de las columnas deben ser exactos
- Se pueden agregar más columnas que serán ignoradas
- Máximo 5MB de tamaño de archivo

## 🖨️ Configuración de impresora (Windows)

Para imprimir directamente desde la aplicación:

1. Instala los drivers de tu impresora Zebra
2. Asegúrate de que aparezca en "Dispositivos e impresoras"
3. En la aplicación, selecciona tu impresora del dropdown
4. Haz clic en "Enviar a Imprimir"

## 📝 Configuración de etiquetas

Los parámetros de las etiquetas se pueden ajustar en [src/generar_zpl_web.py](src/generar_zpl_web.py):

```python
# Tamaño de etiqueta (25 x 25 mm)
ANCHO = 197  # pixels
ALTO = 197   # pixels

# Posiciones de elementos
CODIGO_X = 15      # posición X del código
CODIGO_Y = 10      # posición Y del código
QR_X = 42          # posición X del QR
QR_Y = 35          # posición Y del QR
QR_MAGNIFICACION = 5  # tamaño del QR

DNI_X = 30         # posición X del DNI
DNI_Y = 165        # posición Y del DNI
```

## 🌐 Despliegue en la nube

### Opción 1: Heroku

```bash
# Crear app en Heroku
heroku create tu-app-nombre

# Desplegar
git push heroku main

# Abrir aplicación
heroku open
```

### Opción 2: PythonAnywhere

1. Crea una cuenta en [pythonanywhere.com](https://www.pythonanywhere.com)
2. Carga tu código
3. Configura una aplicación Flask
4. Tu app estará disponible en `https://tuusuario.pythonanywhere.com`

### Opción 3: DigitalOcean / AWS / Google Cloud

Consulta la documentación de cada plataforma para desplegar aplicaciones Flask.

## 🐛 Solución de problemas

### "No se puede cargar el archivo"
- Verifica que el archivo sea .xlsx o .xls
- Asegúrate de que no supera 5MB
- Intenta renombrando el archivo sin caracteres especiales

### "Columnas faltantes"
- El Excel debe tener exactamente las columnas: CODIGO y CODIGO-DNI
- Verifica la ortografía (mayúsculas/minúsculas)

### "La impresora no aparece"
- En Windows: Asegúrate de que la impresora está instalada en Windows
- Verifica que los drivers están actualizados
- Intenta reiniciar la aplicación

### "El QR no se genera correctamente"
- Verifica que el código no tenga caracteres especiales
- Intenta con valores más cortos (máximo 60 caracteres)
- Comprueba la magnificación del QR

## 📦 Estructura del proyecto

```
QR-Colmenas-Web/
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias
├── .gitignore                 # Git ignore
├── README.md                  # Este archivo
│
├── src/
│   ├── generar_zpl.py        # Generador ZPL original
│   ├── generar_zpl_web.py    # Generador ZPL para web
│   ├── imprimir_zpl.py       # Impresión de ZPL
│   ├── imprimir_lote.py      # Impresión en lotes
│   └── main.py               # Script principal original
│
├── templates/
│   └── index.html            # Interfaz web
│
├── static/
│   ├── style.css             # Estilos
│   └── script.js             # Lógica del cliente
│
├── uploads/                  # Archivos subidos (temporal)
├── data/                     # Datos de ejemplo
└── output/                   # Etiquetas generadas
```

## 🔐 Seguridad

- Los archivos se validan antes de procesarse
- Máximo tamaño de archivo: 5MB
- Los archivos se almacenan temporalmente
- Se utiliza `secure_filename` de Werkzeug
- CORS está deshabilitado por defecto

## 💡 Tips de uso

1. **Backup**: Siempre haz backup de tus archivos Excel
2. **Prueba**: Prueba primero con pocas etiquetas antes de hacer lotes grandes
3. **Formateo**: Los códigos QR funcionan mejor sin espacios ni caracteres especiales
4. **Impresora**: Verifica la configuración de la impresora antes de imprimir
5. **Etiquetas**: Ajusta los parámetros de posición según tu tipo de etiqueta

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios mayores:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Desarrollado para la gestión de colmenas y apicultura.

## 📞 Soporte

Para reportar problemas o sugerencias, abre un [issue en GitHub](https://github.com/tuusuario/QR-Colmenas-Web/issues).

---

**Hecho con ❤️ para los apicultores** 🐝
