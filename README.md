
# Legal Pipeline Metrics - Dockerización completa

## Descripción

Este proyecto contiene un dashboard interactivo desarrollado en Python y Streamlit para visualizar métricas asociadas al pipeline de procesamiento de documentos legales.

La rama `feature/docker-postgres` introduce una dockerización completa del proyecto, incluyendo:

- Imagen propia del dashboard.
- Imagen propia de PostgreSQL.
- Carga automática de una base de datos sintética.
- Orquestación mediante Docker Compose.
- Despliegue reproducible en cualquier equipo.

---

# Arquitectura

```text
┌───────────────────────────┐
│      Dashboard            │
│     Streamlit             │
│                           │
│ localhost:8501            │
└─────────────┬─────────────┘
              │
              │ psycopg
              │
┌─────────────▼─────────────┐
│      PostgreSQL 17        │
│                           │
│ Base cargada desde        │
│ backup.sql                │
└───────────────────────────┘
```

---

# Estructura relevante

```text
legal-pipeline-metrics/

├── dashboard/
├── database/
├── output/
├── provision/
│   └── backup.sql
│
├── postgres/
│   └── Dockerfile
│
├── Dockerfile
├── docker-compose.yaml
├── pyproject.toml
├── uv.lock
└── main.py
```

---

# Componentes

## Dashboard

La aplicación Streamlit se construye utilizando el Dockerfile ubicado en la raíz del proyecto.

### Dockerfile

```dockerfile
FROM python:3.13

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync --no-dev

COPY . .

EXPOSE 8501

CMD sh -c "uv run python main.py && uv run streamlit run dashboard/app.py --server.address=0.0.0.0 --server.port=8501"
```

### Responsabilidades

- Instalar dependencias.
- Ejecutar la generación de métricas.
- Levantar Streamlit.
- Exponer el puerto 8501.

---

## PostgreSQL

Se construyó una imagen personalizada basada en PostgreSQL 17.

### Ubicación

```text
postgres/Dockerfile
```

### Contenido

```dockerfile
FROM postgres:17

COPY provision/backup.sql /docker-entrypoint-initdb.d/backup.sql
```

### Objetivo

Incorporar el backup directamente dentro de la imagen.

Durante la primera inicialización PostgreSQL ejecuta automáticamente cualquier script ubicado en:

```text
/docker-entrypoint-initdb.d/
```

Por tanto, la base se reconstruye automáticamente sin necesidad de restauraciones manuales.

---

# Docker Compose

Archivo:

```text
docker-compose.yaml
```

Contenido:

```yaml
services:

  postgres:

    build:
      context: .
      dockerfile: postgres/Dockerfile

    container_name: legal-postgres

    environment:
      POSTGRES_DB: legal_pipeline_prod
      POSTGRES_USER: legal_user
      POSTGRES_PASSWORD: legal_password

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data

    restart: unless-stopped

  dashboard:

    build: .

    depends_on:
      - postgres

    env_file:
      - .env

    ports:
      - "8501:8501"

    volumes:
      - ./output:/app/output

    restart: unless-stopped

volumes:
  postgres_data:
```

---

# Construcción

Desde la raíz del proyecto:

```powershell
docker compose build
```

---

# Ejecución

```powershell
docker compose up -d
```

---

# Verificar contenedores

```powershell
docker compose ps
```

o

```powershell
docker ps
```

Debe aparecer algo similar a:

```text
legal-postgres
dashboard-1
```

---

# Acceso al dashboard

Abrir:

```text
http://localhost:8501
```

También es posible acceder desde el enlace generado automáticamente por Docker Desktop en la columna **Port(s)**.

---

# Reiniciar servicios

```powershell
docker compose restart
```

---

# Detener servicios

```powershell
docker compose stop
```

---

# Apagar completamente

```powershell
docker compose down
```

---

# Eliminar también el volumen de PostgreSQL

```powershell
docker compose down -v
```

## Importante

Al eliminar el volumen:

```text
postgres_data
```

la base se reconstruirá automáticamente desde:

```text
backup.sql
```

la próxima vez que se ejecute:

```powershell
docker compose up -d
```

---

# Flujo de actualización

Si se realizan cambios en el código:

```powershell
git pull

docker compose build

docker compose up -d
```

---

# Publicación en Docker Hub

## Dashboard

```powershell
docker tag legal-pipeline-metrics-dashboard:latest jscortesg90/legal-pipeline-metrics-dashboard:1.0.0

docker push jscortesg90/legal-pipeline-metrics-dashboard:1.0.0
```

## PostgreSQL

```powershell
docker tag legal-pipeline-metrics-postgres:latest jscortesg90/legal-pipeline-metrics-postgres:1.0.0

docker push jscortesg90/legal-pipeline-metrics-postgres:1.0.0
```

---

# Despliegue utilizando imágenes publicadas

Una vez publicadas en Docker Hub, el proyecto puede ejecutarse sin necesidad de compilar localmente.

```yaml
services:

  postgres:

    image: jscortesg90/legal-pipeline-metrics-postgres:1.0.0

    environment:
      POSTGRES_DB: legal_pipeline_prod
      POSTGRES_USER: legal_user
      POSTGRES_PASSWORD: legal_password

    ports:
      - "5432:5432"

  dashboard:

    image: jscortesg90/legal-pipeline-metrics-dashboard:1.0.0

    depends_on:
      - postgres

    ports:
      - "8501:8501"
```

Posteriormente:

```powershell
docker compose up -d
```

---

# Datos de prueba

La imagen PostgreSQL incluye un backup SQL con datos completamente sintéticos destinados a:

- Pruebas funcionales.
- Validación del dashboard.
- Demostraciones.
- Desarrollo local.

No contiene información productiva ni datos sensibles.

---

# Resultado final

Con la implementación realizada en la rama `feature/docker-postgres`, el proyecto queda completamente autocontenido:

- Código fuente versionado en Git.
- Dashboard dockerizado.
- PostgreSQL dockerizado.
- Datos sintéticos integrados.
- Despliegue reproducible.
- Restauración automática de la base.

La puesta en marcha completa puede realizarse mediante:

```powershell
docker compose up -d
```

y el dashboard queda disponible inmediatamente en:

```text
http://localhost:8501
```
