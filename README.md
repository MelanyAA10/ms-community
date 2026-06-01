# ms-community — BookLoop Community Microservice

Microservicio de comunidad para BookLoop, desarrollado en **Python con FastAPI** siguiendo **arquitectura hexagonal**.

## Tecnologías
- **Python 3.11** + **FastAPI**
- **PostgreSQL** (Azure Database for PostgreSQL)
- **SQLAlchemy** como ORM
- **Azure App Service** para el despliegue
- **GitHub Actions** para CI/CD

## Justificación de PostgreSQL
El microservicio de comunidad maneja datos relacionales por naturaleza: posts, likes, comentarios y perfiles están interrelacionados. PostgreSQL permite consultas eficientes con JOINs, garantiza integridad referencial y es ideal para las estadísticas de comunidad (conteos, agregaciones). Se usa como segundo tipo de almacenamiento junto a MongoDB (ms-libros).

## Arquitectura Hexagonal

```
app/
├── domain/                  # Núcleo del negocio
│   ├── models/post.py       # Entidad Post
│   └── exceptions/          # Excepciones de dominio
├── application/             # Casos de uso
│   ├── ports/in/            # Interfaces de entrada
│   ├── ports/out/           # Interfaces de salida
│   └── services/            # Implementación de casos de uso
└── infrastructure/          # Adaptadores
    ├── persistence/         # Adaptador PostgreSQL
    └── web/                 # Adaptador HTTP (FastAPI)
```

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/v1/community/posts/{page}/{size}` | Lista paginada de posts |
| POST | `/v1/community/posts` | Crear un nuevo post |
| POST | `/v1/community/posts/{id}/like` | Dar like a un post |
| GET | `/health` | Health check |

## Variables de entorno

```env
DATABASE_URL=postgresql://adminbookloop:<password>@bookloop-community-db.postgres.database.azure.com:5432/community_db
```

## Correr localmente

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger disponible en: `http://localhost:8000/docs`
<!-- trigger 2 --> 
