#!/bin/bash
# =============================================
# Defola's Properties - Quick Setup Script
# =============================================
set -e

echo "============================================"
echo "  Setting up Defola's Properties Platform"
echo "============================================"
echo ""

# 1. Create virtual environment
echo "▶ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "▶ Installing dependencies..."
pip install -r requirements.txt

# 3. Copy env file
if [ ! -f ".env" ]; then
  echo "▶ Creating .env file from example..."
  cp .env.example .env
  echo "  ⚠  Please edit .env with your actual values before production!"
fi

# 4. Run migrations
echo "▶ Running database migrations..."
python manage.py migrate

# 5. Load sample data
echo "▶ Loading sample data (locations, properties, testimonials, team)..."
python manage.py loaddata fixtures/initial_data.json

# 6. Create superuser
echo ""
echo "▶ Creating admin superuser..."
echo "  (You will be prompted to enter username, email, and password)"
python manage.py createsuperuser

# 7. Collect static files
echo "▶ Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "▶ Start the development server:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "▶ Access the site at:     http://127.0.0.1:8000"
echo "▶ Access admin panel at:  http://127.0.0.1:8000/admin"
echo ""
