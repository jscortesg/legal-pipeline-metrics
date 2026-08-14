
# Legal Pipeline Metrics

## Descripción

Legal Pipeline Metrics es una aplicación desarrollada en Python para generar, almacenar y visualizar métricas relacionadas con un pipeline de procesamiento documental jurídico.

El proyecto genera estadísticas a partir de información almacenada en PostgreSQL y las presenta mediante un dashboard interactivo construido con Streamlit.

La versión contenida en la rama `main` está diseñada para ejecutarse localmente, utilizando una instalación local de PostgreSQL y un entorno virtual de Python.

---

# Arquitectura

```text
┌─────────────────────┐
│     PostgreSQL      │
│                     │
│ legal_pipeline_prod │
└──────────┬──────────┘
           │
           │ psycopg
           │
┌──────────▼──────────┐
│       main.py       │
│                     │
│ Genera métricas     │
│ y tablas de salida  │
└──────────┬──────────┘
           │
           │ archivos
           │
┌──────────▼──────────┐
│      output/        │
└──────────┬──────────┘
           │
           │ lectura
           │
┌──────────▼──────────┐
│     Streamlit       │
│     Dashboard       │
└─────────────────────┘
```

---

# Estructura del proyecto

```text
legal-pipeline-metrics/

├── dashboard/
│   └── app.py
│
├── database/
│   ├── connection.py
│   └── queries.py
│
├── output/
│
├── provision/
│   └── backup.sql
│
├── stats/
│
├── visualize/
│
├── tests/
│
├── main.py
├── pyproject.toml
├── uv.lock
├── .env
└── README.md
```

---

# Requisitos

## Software requerido

- Python 3.13
- PostgreSQL 17 o superior
- Git

---

# Creación del entorno virtual

Desde la raíz del proyecto:

```powershell
python -m venv .venv
```

Activar:

```powershell
.venv\Scripts\activate
```

---

# Instalación de dependencias

Instalar uv:

```powershell
pip install uv
```

Instalar dependencias del proyecto:

```powershell
uv sync
```

---

# Configuración de PostgreSQL

Se requiere una instancia local de PostgreSQL.

Crear una base de datos llamada:

```text
legal_pipeline_prod
```

---

# Restauración de la base de datos

El proyecto incluye un backup SQL ubicado en:

```text
provision/backup.sql
```

Restaurar utilizando:

```powershell
psql -U postgres -d legal_pipeline_prod -f provision/backup.sql
```

o desde pgAdmin mediante la herramienta Query Tool.

---

# Verificación de la restauración

Ingresar a PostgreSQL:

```powershell
psql -U postgres -d legal_pipeline_prod
```

Listar tablas:

```sql
SELECT schemaname, tablename
FROM pg_tables
ORDER BY schemaname, tablename;
```

Deben existir tablas similares a:

```text
anexo
auditoria_generacion
cuaderno
documento
expediente
extraccion_corpus
inventario_jerarquia
```

Ejemplo:

```sql
SELECT COUNT(*) FROM documento;
```

Resultado esperado:

```text
400
```

---

# Configuración del archivo .env

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=legal_pipeline_prod
DB_USER=legal_user
DB_PASSWORD=tu_password
```

Modificar según la configuración local de PostgreSQL.

---

# Generación de métricas

La aplicación principal ejecuta consultas sobre la base de datos y genera tablas de salida utilizadas posteriormente por el dashboard.

Ejecutar:

```powershell
python main.py
```

o

```powershell
uv run python main.py
```

---

# Archivos generados

Los resultados se almacenan en:

```text
output/
```

Esta carpeta contiene las tablas utilizadas por el dashboard para la visualización de métricas.

---

# Ejecución del dashboard

Una vez generadas las métricas:

```powershell
streamlit run dashboard/app.py
```

o

```powershell
uv run streamlit run dashboard/app.py
```

---

# Acceso al dashboard

Abrir en el navegador:

```text
http://localhost:8501
```

---

# Flujo de trabajo recomendado

## 1. Activar entorno virtual

```powershell
.venv\Scripts\activate
```

## 2. Generar métricas

```powershell
uv run python main.py
```

## 3. Iniciar dashboard

```powershell
uv run streamlit run dashboard/app.py
```

## 4. Abrir navegador

```text
http://localhost:8501
```

---

# Actualización del proyecto

Actualizar repositorio:

```powershell
git pull
```

Actualizar dependencias:

```powershell
uv sync
```

Regenerar métricas:

```powershell
uv run python main.py
```

---

# Ejecución de pruebas

Ejecutar todos los tests:

```powershell
pytest
```

o

```powershell
uv run pytest
```

---

# Datos incluidos

El proyecto incluye un conjunto de datos completamente sintéticos destinados a:

- Validación funcional.
- Desarrollo local.
- Pruebas.
- Demostraciones.

No contiene información sensible ni datos productivos.

---

# Solución de problemas

## Error de conexión a PostgreSQL

Verificar:

- PostgreSQL en ejecución.
- Credenciales del archivo `.env`.
- Existencia de la base de datos.
- Puerto configurado correctamente.

---

## Error de tablas inexistentes

Verificar que el backup haya sido restaurado:

```powershell
psql -U postgres -d legal_pipeline_prod -f provision/backup.sql
```

---

## Dashboard sin información

Ejecutar nuevamente:

```powershell
uv run python main.py
```

para regenerar las métricas requeridas.

---

# Resultado final

Una vez configurado correctamente:

1. PostgreSQL contiene la base de datos restaurada.
2. `main.py` genera las métricas necesarias.
3. Streamlit visualiza los resultados.
4. El dashboard queda disponible en:

```text
http://localhost:8501
```

La rama `main` representa la versión de desarrollo local del proyecto, sin contenedores Docker y utilizando una instalación local de PostgreSQL.
