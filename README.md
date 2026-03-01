# HCA Yoga – Historia Clínica de Alumnos

Aplicación web desarrollada en Python con Flask para registrar y gestionar las historias clínicas de los alumnos del estudio de yoga.

Proyecto pensado para uso interno en la PC del estudio.

---

## 🧠 Objetivo

Permitir:

- Registrar datos personales del alumno
- Registrar información médica relevante
- Consultar listado de alumnos con búsqueda
- Ver detalle individual
- Editar y eliminar registros
- Exportar PDF individual y listado general

---

## 🏗 Stack Tecnológico

- Python 3.14.3
- Flask
- Flask-SQLAlchemy (ORM)
- SQLite
- python-dotenv
- Entorno virtual (venv)
- fpdf2 (PDF)

---

## 💻 Entorno de Desarrollo

Desarrollado en:

- macOS (Apple Silicon)
- Python 3.14.3

Verificación de versiones:

```bash
python3 --version
```

## 🚀 Instalación del Proyecto

Clonar el repositorio:

```
git clone <repo_url>
cd hca_yoga
```

Crear entorno virtual:

```
python3 -m venv venv
```

Activar entorno virtual:

Mac / Linux:

```
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

Instalar dependencias:

```
pip install -r requirements.txt
```

## 📦 Generar requirements.txt (en desarrollo)

Si se agregan nuevas dependencias:

```
pip freeze > requirements.txt
```

## 🔐 Variables de Entorno

Crear un archivo .env en la raíz del proyecto:

```
FLASK_ENV=development
SECRET_KEY=super_secret_key
```

## 🗂 Estructura del Proyecto

```
hca_yoga/
│
├── run.py
├── config.py
│
├── app/
│   ├── models/
│   ├── controllers/
│   ├── templates/
│   └── static/
│
├── requirements.txt
├── .env
└── .gitignore
```

## 🗄 Base de Datos

Base de datos: SQLite
Archivo local `hca_yoga.db`
No requiere instalación adicional.

Si el esquema cambia, borrar el archivo y reiniciar la app para que se regenere.

## ▶️ Ejecutar en Local

```bash
python run.py
```

Abrir en el navegador:

```
http://127.0.0.1:5000/
```

## 🪟 Windows (acceso directo)

1. Ejecutar `iniciar_app_windows.bat` para iniciar la app y abrir el navegador.
2. Para crear un acceso directo en el escritorio:

```powershell
.\crear_acceso_directo.ps1
```

El acceso directo abre la app y el navegador automáticamente.
Nota: el script usa `venv\Scripts\python.exe`, por lo que el entorno virtual debe existir en la carpeta del proyecto.

### ✅ Checklist de validación en Windows

1. Abrir PowerShell en la carpeta del proyecto.
2. Ejecutar:

```powershell
.\crear_acceso_directo.ps1
```

3. Verificar que se creó `HCA Yoga.lnk` en el escritorio.
4. Hacer doble clic en `HCA Yoga.lnk`.
5. Confirmar que abre `http://127.0.0.1:5000/` y carga la app.
6. Probar un PDF (listado o detalle) para validar `fpdf2`.

## 🛠 Troubleshooting rápido

Si `python run.py` no levanta después de cambiar de máquina o hacer pull:

1. Borrar y recrear `venv`.
2. Reinstalar dependencias con `pip install -r requirements.txt`.
3. Volver a probar `python run.py`.

Esto suele resolver entornos inconsistentes entre macOS y Windows.

## 🧾 PDF

- PDF individual desde el detalle del alumno.
- PDF listado desde el listado general (orden alfabético).

## 🖥 Uso Interno

La aplicación está pensada para ejecutarse en:
• Localhost
• Solo en la PC del estudio
• Sin exposición a internet (por ahora)

Esto simplifica:
• Seguridad
• Autenticación
• Infraestructura

## 🔄 Migración a la PC del Estudio

En la PC destino se deberá: 1. Instalar Python 3.14.x 2. Clonar el repositorio 3. Crear entorno virtual 4. Instalar dependencias 5. Configurar archivo .env 6. Ejecutar la app

Comandos básicos:

```
git clone <repo_url>
cd hca_yoga
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📌 Buenas Prácticas Implementadas

    •	Entorno virtual aislado
    •	Dependencias versionadas
    •	Configuración desacoplada
    •	Estructura tipo MVC
    •	Proyecto portable

⸻

## 📈 Futuras Mejoras

    •	Sistema de autenticación
    •	Backups automáticos
    •	Validaciones avanzadas
    •	Dashboard de métricas
    •	Encriptación de datos sensibles

⸻

## 🧘 Proyecto

Desarrollado para el estudio de yoga.
Uso interno.
Datos médicos confidenciales.

## 📦 Trasladar el proyecto sin Git

Si no usas `git clone`, podes copiar la carpeta completa (USB, WhatsApp, Drive) y funciona igual.

Checklist en la PC de destino:

1. Copiar la carpeta del proyecto completa.
2. Crear entorno virtual:

```bash
python -m venv venv
```

3. Activar entorno virtual:

```bash
venv\Scripts\activate
```

4. Instalar dependencias:

```bash
pip install -r requirements.txt
```

5. Ejecutar la app:

```bash
python run.py
```

Abrir:

```
http://127.0.0.1:5000/
```
