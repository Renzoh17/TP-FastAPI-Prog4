# 🚗 Gestión de Inventario de Autos y Ventas API

API RESTful construida con **FastAPI** y **SQLModel** para la gestión de un inventario de vehículos y el seguimiento de sus ventas. Utiliza **PostgreSQL** como base de datos relacional.

---

## 🚀 Tecnologías

| Tecnología | Descripción |
| :--- | :--- |
| **Python** | Lenguaje de programación principal. |
| **FastAPI** | Framework web de alto rendimiento para crear la API. |
| **SQLModel** | ORM (Object-Relational Mapper) basado en Pydantic y SQLAlchemy. |
| **PostgreSQL** | Base de datos relacional robusta y escalable. |
| **Uvicorn** | Servidor ASGI para correr la aplicación. |
| **python-dotenv** | Para cargar variables de entorno desde el archivo `.env`. |

---

## 🏗️ Estructura del Proyecto

```

proyecto/
├── main.py                     \# Aplicación FastAPI principal y configuración inicial.
├── database.py                 \# Configuración de conexión a PostgreSQL.
├── models.py                   \# Definición de modelos de datos (Auto y Venta) con validaciones.
├── repository.py               \# Patrón Repository para acceso a datos (CRUD, paginación, filtros).
├── autos.py                    \# Router con endpoints para la entidad Auto.
├── ventas.py                   \# Router con endpoints para la entidad Venta.
├── requirements.txt            \# Lista de dependencias Docker.
├── requirementsForPy.txt       \# Lista de dependencias Python (para correr sin Docker).
├── .env                        \# Variables de entorno para la DB.
├── Dockerfile                  \# Archivo para creación de la imagen.
└── docker-compose.yml          \# Archivo para crear las conexión entre la app y la bdd.


```

---

## 🔌 Endpoints de la API

La documentación interactiva de la API (Swagger UI) está disponible en: **`http://localhost:8000/docs`**

### Endpoints de Autos (`/autos`)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/autos/` | Crea un nuevo auto. |
| `GET` | `/autos/` | Lista autos con paginación (`skip`, `limit`). |
| `GET` | `/autos/marcaomodelo/search?query=...` | **Busca** autos por coincidencia parcial en **Marca o Modelo**. |
| `GET` | `/autos/{auto_id}` | Obtiene auto por ID. |
| `GET` | `/autos/chasis/{numero_chasis}` | **Busca** autos por número de chasis. |
| `PUT`| `/autos/{auto_id}` | Actualización completa del auto. |
| `GET` | `/autos/{auto_id}/with-ventas` | Obtiene un auto con sus ventas asociadas. |
| `DELETE` | `/autos/{auto_id}` | Elimina un auto. |

### Endpoints de Ventas (`/ventas`)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/ventas/` | Crea una nueva venta (requiere `auto_id`). |
| `GET` | `/ventas/` | Lista ventas con paginación. |
| `GET` | `/ventas/{venta_id}` | Obtiene venta por ID. |
| `PUT` | `/ventas/{venta_id}` | Actualización completa de la venta. |
| `DELETE` | `/ventas/{venta_id}` | Elimina una venta. |
| `GET` | `/ventas/auto/{auto_id}` | **Busca** ventas de un auto específico. |
| `GET` | `/ventas/comprador/{nombre}` | **Busca** ventas por nombre de comprador. |
| `GET` | `/ventas/filter/price?min=...` | **Filtra** ventas por rango de precio. |
| `GET` | `/ventas/filter/date?start=...` | **Filtra** ventas por rango de fechas (ISO 8601). |
| `GET` | `/ventas/{venta_id}/with-auto` | Obtiene una venta con los detalles del auto vendido. |

---

## ⚙️ Configuración y Ejecución (sin Docker)

### 1. Requisitos Previos

* **Python 3.10+**
* **PostgreSQL** (Servidor corriendo).

### 2. Instalación de Dependencias

```bash
# Activa tu entorno virtual (.venv)
source .venv/Scripts/activate  # o .venv/bin/activate

# Instala las dependencias
pip install -r requirementsForPy.txt
````

### 3\. Configuración de Variables de Entorno

Modifica el archivo llamado **`.env`** en el directorio raíz del proyecto con las credenciales de tu base de datos:

```env
# .env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=autos_db
```

O modifica la cadena de conexión en ese mismo archivo:

```env
# .env
DATABASE_URL=postgresql+psycopg2://{usuario}:{password}@{server}:{port}/{database}
```

### 4\. Ejecución del Servidor

Ejecuta la aplicación usando Uvicorn:

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`.

-----

## ⚙️ Configuración y Ejecución (con Docker - Mayor Compatibilidad)

### 1. Requisitos Previos

* **Git**
* **Docker Desktop**

### 2. Construir e Iniciar los Contenedores

Ejecuta el siguiente comando en la terminal, dentro de la carpeta raíz del proyecto (donde se encuentra el archivo `docker-compose.yml`)

```bash
# Crea el entorno
docker compose up --build
````

Este comando realiza las siguientes tareas automáticamente:
* **Constucción:** Usa el `Dockerfile` para crear la imagen de la aplicación (`app`) e instala todas las dependencias de Python (`requirements.txt`).
* **Servicio DB:** Descarga e inicia el contenedor de **PostgreSQL** (`db`).
* **Red:** Crea una red interna, permitiendo que la aplicación se conecte a la DB usando el nombre de host `db`.
* **Startup Check:** La aplicación espera a que la base de datos esté completamente lista antes de intentar conectarse y crear las tablas. 

### 3\. Acceso a la API

Una vez que se vea en la terminal el mensaje de Uvicorn `Application startup complete` (o similar) y los logs se detengan, la API esta lista para ser utilizada.

El servicio está mapeado al puerto `8000` de tu máquina local.

| Recurso | Dirección de Acceso |
| :--- | :--- |
| **Documentación interactiva (Swagger UI)** | `http://localhost:8000/docs` |
| **Documentación alternativa (Redoc)** | `http://localhost:8000/redoc` |
| **Raíz de la API** | `http://localhost:8000/` |

### 4\. Detalles de la Base de Datos

**1. Conexión Interna (Solo para el Contenedor `app`)**

La aplicación se conecta a la base datos usando la red interna de Docker:

* **Host:** `db`
* **URL (interna):** `postgresql://postgres:admin@db:5432/autos_db`

**2. Conexión Externa (Para Herramientas GUI)**

Si necesitas acceder a la base de datos directamente con una herramiento como DBeaver, TablePlus o pgAdmin:

| Parámetro | Valor |
| :--- | :--- |
| **Host/Servidor** | `localhost` (o `127.0.0.1`) |
| **Puerto** | `5432` |
| **Usuario** | `postgres` |
| **Contraseña** | `admin` |
| **Base de Datos** | `autos_db` |

### 🛑 Detener y Limpiar

Para detener y eliminar los contenedores y la red creada por Docker Compose:

```bash
docker compose down
```

**Nota:** Este comando **mantiene el volumen de datos (`postgres_data`)**. Si deseas eliminar la base de datos por completo y empezar desde cero (perdiendo todos los datos), usa:

```bash
docker compose down -v
```





