# 🍽️ FoodGram

Red social minimalista para compartir comida, construida con Django + TailwindCSS + PostgreSQL.

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Django 4.2 (patrón MVC) |
| Base de datos | PostgreSQL |
| Frontend | TailwindCSS (CDN) + Lucide Icons |
| Autenticación | Django Auth personalizado (email como PK) |
| Almacenamiento | Whitenoise (archivos estáticos) |

## Características

- ✅ Autenticación con email como clave primaria (no editable)
- ✅ Registro, login y cierre de sesión
- ✅ Feed personalizado (posts de usuarios seguidos)
- ✅ Explorar todos los posts por categoría
- ✅ Crear, editar y eliminar publicaciones (foto + plato + descripción + ubicación + categoría)
- ✅ Sistema de likes con AJAX
- ✅ Comentarios
- ✅ Seguir / dejar de seguir usuarios
- ✅ Perfil público con grid de posts (estilo Instagram)
- ✅ Dashboard: gestión de mis posts + configuración de cuenta
- ✅ Diseño oscuro con palette azul
- ✅ Responsive (mobile-first)

## Estructura del proyecto

```
foodgram/
├── foodgram/               # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/              # Modelo User + auth + dashboard
│   │   ├── models.py       # User (email PK), Follow
│   │   ├── views.py        # Register, Login, Profile, Dashboard
│   │   ├── forms.py
│   │   └── urls.py
│   ├── posts/              # Publicaciones
│   │   ├── models.py       # Post, Like, Comment, Category
│   │   ├── views.py        # CRUD + likes + comentarios
│   │   ├── forms.py
│   │   └── fixtures/categories.json
│   └── feed/               # Feed y Explorar
│       ├── views.py
│       └── urls.py
├── templates/
│   ├── base.html
│   ├── partials/           # navbar, post_card
│   ├── users/              # login, register, profile
│   ├── posts/              # create, detail, edit
│   ├── feed/               # home, explore
│   └── dashboard/          # index, settings
├── static/
├── media/
├── requirements.txt
└── .env.example
```

## Instalación

### 1. Clonar y crear entorno virtual

```bash
git clone <repo-url>
cd foodgram
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

Contenido del `.env`:
```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DB_NAME=foodgram
DB_USER=postgres
DB_PASSWORD=tupassword
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Crear la base de datos

```bash
# En psql
CREATE DATABASE foodgram;
```

### 4. Aplicar migraciones y cargar datos iniciales

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata apps/posts/fixtures/categories.json
```

### 5. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

Abrir: [http://localhost:8000](http://localhost:8000)

## URLs principales

| URL | Descripción |
|-----|-------------|
| `/` | Feed principal |
| `/explore/` | Explorar todos los posts |
| `/auth/login/` | Iniciar sesión |
| `/auth/register/` | Crear cuenta |
| `/auth/profile/<username>/` | Perfil de usuario |
| `/posts/create/` | Nueva publicación |
| `/posts/<id>/` | Detalle de publicación |
| `/auth/dashboard/` | Dashboard personal |
| `/auth/dashboard/settings/` | Configuración de cuenta |
| `/admin/` | Panel de administración Django |

## Patrón MVC en Django

| MVC | Django |
|-----|--------|
| Model | `apps/*/models.py` |
| View (Template) | `templates/**/*.html` |
| Controller (View) | `apps/*/views.py` |

## Historial de commits

El repositorio tiene commits organizados por etapas:
1. `init: estructura base del proyecto`
2. `feat: modelo User personalizado con email como PK`
3. `feat: app posts con modelos Post, Like, Comment, Category`
4. `feat: app feed con vistas home y explore`
5. `feat: templates base, navbar y autenticación`
6. `feat: templates de feed, posts y perfil de usuario`
7. `feat: dashboard de usuario (posts + configuración)`
8. `feat: fixtures de categorías`
9. `docs: README con instrucciones de instalación`
