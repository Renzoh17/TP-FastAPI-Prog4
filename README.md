```markdown
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
├── main.py             \# Aplicación FastAPI principal y configuración inicial.
├── database.py         \# Configuración de conexión a PostgreSQL.
├── models.py           \# Definición de modelos de datos (Auto y Venta) con validaciones.
├── repository.py       \# Patrón Repository para acceso a datos (CRUD, paginación, filtros).
├── autos.py            \# Router con endpoints para la entidad Auto.
├── ventas.py           \# Router con endpoints para la entidad Venta.
├── requirements.txt    \# Lista de dependencias Python.
└── .env                \# Variables de entorno para la DB.

````

---

## ⚙️ Configuración y Ejecución

### 1. Requisitos Previos

* **Python 3.10+**
* **PostgreSQL** (Servidor corriendo).

### 2. Instalación de Dependencias

```bash
# Activa tu entorno virtual (.venv)
source .venv/bin/activate  # o .\venv\Scripts\activate

# Instala las dependencias
pip install -r requirements.txt
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

### 4\. Ejecución del Servidor

Ejecuta la aplicación usando Uvicorn:

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

-----

## 🔌 Endpoints de la API

La documentación interactiva de la API (Swagger UI) está disponible en: **`http://127.0.0.1:8000/docs`**

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

```
```
