# 🚀 Guía de Despliegue - QR Colmenas

Esta guía te ayudará a desplegar tu aplicación QR Colmenas en diferentes plataformas.

## 📋 Tabla de contenidos

1. [Despliegue Local](#despliegue-local)
2. [Despliegue en Docker](#despliegue-en-docker)
3. [Despliegue en la Nube](#despliegue-en-la-nube)
4. [Configuración de Producción](#configuración-de-producción)

---

## 🏠 Despliegue Local

### Opción 1: Ejecución Directa

```bash
# 1. Clonar el repositorio
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

# 4. Ejecutar aplicación
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

### Opción 2: Con Gunicorn (Recomendado)

```bash
pip install gunicorn

# Ejecutar con gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

---

## 🐳 Despliegue en Docker

### Prerequisitos

- Docker instalado: https://www.docker.com/get-started
- Docker Compose (opcional)

### Opción 1: Con Docker Compose (Recomendado)

```bash
# Desde la carpeta del proyecto
docker-compose up -d

# Verificar que está corriendo
docker-compose ps

# Ver logs
docker-compose logs -f web

# Detener
docker-compose down
```

### Opción 2: Con Docker manualmente

```bash
# Construir imagen
docker build -t qr-colmenas .

# Ejecutar contenedor
docker run -d -p 5000:5000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/data:/app/data --name qr-app qr-colmenas

# Acceder a http://localhost:5000

# Detener contenedor
docker stop qr-app
docker rm qr-app
```

---

## ☁️ Despliegue en la Nube

### Opción 1: Heroku

#### Requisitos
- Cuenta en Heroku: https://www.heroku.com
- Heroku CLI instalado

#### Pasos

```bash
# 1. Login a Heroku
heroku login

# 2. Crear aplicación
heroku create nombre-de-tu-app

# 3. Desplegar código
git push heroku main

# 4. Abrir aplicación
heroku open

# 5. Ver logs
heroku logs --tail
```

**Nota:** Heroku tiene limitaciones en el almacenamiento. Los archivos se borran después de reiniciar el dyno.

### Opción 2: Railway

#### Requisitos
- Cuenta en Railway: https://railway.app

#### Pasos

```bash
# 1. Instalar Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Crear proyecto
railway init

# 4. Desplegar
railway up
```

### Opción 3: Render

#### Requisitos
- Cuenta en Render: https://render.com

#### Pasos

1. Conecta tu repositorio de GitHub
2. Crea un nuevo "Web Service"
3. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app`
4. Deploy

### Opción 4: PythonAnywhere

#### Requisitos
- Cuenta en PythonAnywhere: https://www.pythonanywhere.com

#### Pasos

1. Abre tu consola bash en PythonAnywhere
2. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/QR-Colmenas-Web.git
   ```
3. Crea un entorno virtual
4. Instala dependencias
5. Configura una aplicación web Flask
6. Tu app estará en `https://tuusuario.pythonanywhere.com`

### Opción 5: AWS (EC2)

#### Pasos básicos

```bash
# 1. Conectar a tu instancia EC2
ssh -i tu-key.pem ec2-user@tu-ip-publica

# 2. Instalar dependencias
sudo yum install python3 python3-pip git

# 3. Clonar repositorio
git clone https://github.com/tuusuario/QR-Colmenas-Web.git
cd QR-Colmenas-Web

# 4. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 5. Instalar dependencias
pip install -r requirements.txt
pip install gunicorn

# 6. Ejecutar con supervisor o systemd
```

**Recomendación:** Usa Gunicorn + Nginx para mejor rendimiento.

---

## ⚙️ Configuración de Producción

### Variables de entorno

Crea un archivo `.env` (NO lo subas a GitHub):

```env
# Flask
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-esto

# Configuración
UPLOAD_MAX_SIZE=5242880  # 5MB en bytes

# En Heroku/Railway, configura usando el dashboard
```

### Seguridad

1. **Cambiar SECRET_KEY**: Genera una clave fuerte
   ```bash
   python -c 'import secrets; print(secrets.token_hex(32))'
   ```

2. **HTTPS**: Asegúrate de que tu dominio use HTTPS

3. **CORS**: Configura CORS si necesitas acceso desde otros dominios

4. **Limpieza de archivos**: Implementa un cron job para limpiar archivos viejos:
   ```bash
   0 0 * * * find /app/uploads -mtime +7 -delete
   ```

### Monitoreo

Para producción, considera usar:
- **Sentry**: Para seguimiento de errores
- **New Relic**: Para monitoreo de rendimiento
- **CloudFlare**: Para DDoS y caché

---

## 🔧 Troubleshooting

### Puerto ocupado

```bash
# Cambiar puerto en Flask
python app.py --port 8000

# O ejecutar en diferente puerto
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

### Permisos en Linux

```bash
chmod 755 init-git.sh
chmod 755 uploads/
chmod 755 data/
```

### Limpiar cache de Docker

```bash
docker system prune -a
docker volume prune
```

---

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs: `docker-compose logs web`
2. Abre un issue en GitHub
3. Consulta la documentación de Flask: https://flask.palletsprojects.com/

---

**¡Listo! Tu aplicación QR Colmenas está en la nube** 🚀
