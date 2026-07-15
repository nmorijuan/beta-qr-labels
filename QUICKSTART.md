# 🚀 Inicio Rápido - QR Colmenas

Sigue estos pasos para tener tu aplicación funcionando en 5 minutos.

## ⚡ Opción 1: Ejecución Directa (Recomendado)

### Windows

```bash
# 1. Doble-clic en run.bat
# Eso es todo! La aplicación se abrirá en http://localhost:5000
```

### macOS/Linux

```bash
# 1. Ejecutar script
chmod +x run.sh
./run.sh

# La aplicación se abrirá en http://localhost:5000
```

## 📝 Opción 2: Manual

```bash
# 1. Clonar repositorio (si aún no lo hiciste)
git clone https://github.com/tuusuario/QR-Colmenas-Web.git
cd QR-Colmenas-Web

# 2. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python app.py
```

## 🌐 Acceder a la aplicación

Una vez que veas esto en la terminal:
```
 * Running on http://127.0.0.1:5000
```

Abre tu navegador y ve a: **http://localhost:5000**

## 📤 Usar la aplicación

### Paso 1: Preparar archivo Excel

Crea un archivo Excel con dos columnas:

| CODIGO | CODIGO-DNI |
|--------|-----------|
| QR001  | DNA-001   |
| QR002  | DNA-002   |

### Paso 2: Cargar en la app

1. Haz clic en el área de carga o arrastra el archivo
2. Verifica los datos en la vista previa
3. Haz clic en "Generar Etiquetas"

### Paso 3: Imprimir

- **Descargar ZPL**: Descarga el archivo para imprimirlo manualmente
- **Imprimir directo**: Selecciona tu impresora Zebra y haz clic en "Enviar a Imprimir"

## ❓ Ayuda

- ¿Tengo problemas? → Ver [README.md](README.md)
- ¿Quiero desplegar en la nube? → Ver [DEPLOY.md](DEPLOY.md)
- ¿Quiero contribuir? → Ver [CONTRIBUTING.md](CONTRIBUTING.md)

## 🔧 Verificación

Si algo no funciona, ejecuta:

```bash
python verify_setup.py
```

---

¡Listo! Ahora puedes generar e imprimir QR de colmenas. 🐝
