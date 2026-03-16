#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# FoodGram — Script de instalación y arranque
# Uso: bash setup.sh
# ─────────────────────────────────────────────────────────────
set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}🍽️  FoodGram — Setup automático${NC}"
echo "────────────────────────────────────────"

# 1. Entorno virtual
if [ ! -d "venv" ]; then
  echo -e "${YELLOW}→ Creando entorno virtual...${NC}"
  python3 -m venv venv
fi

echo -e "${YELLOW}→ Activando entorno virtual...${NC}"
source venv/bin/activate

# 2. Dependencias
echo -e "${YELLOW}→ Instalando dependencias...${NC}"
pip install -r requirements.txt -q

# 3. .env
if [ ! -f ".env" ]; then
  echo -e "${YELLOW}→ Creando .env desde .env.example...${NC}"
  cp .env.example .env
  echo -e "${RED}⚠️  Edita .env con tus credenciales de PostgreSQL antes de continuar.${NC}"
  echo "    Abre el archivo .env y configura DB_NAME, DB_USER, DB_PASSWORD."
  read -p "Presiona Enter cuando hayas configurado .env..." _
fi

# 4. Migraciones
echo -e "${YELLOW}→ Aplicando migraciones...${NC}"
python manage.py makemigrations
python manage.py migrate

# 5. Fixture de categorías
echo -e "${YELLOW}→ Cargando categorías de comida...${NC}"
python manage.py loaddata apps/posts/fixtures/categories.json

# 6. Seed de demo (opcional)
echo ""
read -p "¿Crear usuarios de demostración? (s/N): " create_demo
if [[ "$create_demo" =~ ^[sS]$ ]]; then
  python manage.py seed_data
fi

# 7. Superusuario
echo ""
read -p "¿Crear superusuario para el admin? (s/N): " create_super
if [[ "$create_super" =~ ^[sS]$ ]]; then
  python manage.py createsuperuser
fi

# 8. Archivos estáticos
echo -e "${YELLOW}→ Recopilando archivos estáticos...${NC}"
python manage.py collectstatic --noinput -v 0

echo ""
echo -e "${GREEN}✅  Setup completado correctamente.${NC}"
echo "────────────────────────────────────────"
echo -e "${CYAN}Inicia el servidor con:${NC}"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo -e "${CYAN}Abre en el navegador:${NC}  http://localhost:8000"
echo ""
