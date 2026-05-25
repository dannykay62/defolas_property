# 🏠 Defola's Properties — Production-Ready Real Estate Platform

A premium, full-stack Django real estate platform built for the Nigerian market. Features WhatsApp integration, property management, inquiry system, and more.

---

## ✨ Features

- **Premium UI** — Tailwind CSS, mobile-first, teal brand design
- **Property Listings** — Grid view, filters, search, pagination
- **Property Detail** — Gallery, video embed, amenities, inquiry form
- **WhatsApp Integration** — Floating button, per-property WhatsApp links
- **Call Now Button** — Prominent on all pages and property listings
- **Schedule Inspection** — Inquiry type with preferred date picker
- **Save/Favourite** — Logged-in users can save properties
- **Inquiry System** — Per-property contact forms saved to database
- **Custom Admin** — Beautiful admin dashboard with image previews
- **SEO Ready** — Slug URLs, meta tags, Open Graph, sitemap.xml
- **Sample Data** — 6 properties, locations, testimonials, team members
- **Unit Tests** — Full test suite for models, views, and forms
- **Deployment Ready** — Gunicorn + WhiteNoise configuration

---

## 🚀 Quick Start (Local Development)

### Option A — Automated Setup (Recommended)

```bash
git clone <your-repo>
cd defola_properties
chmod +x setup.sh
./setup.sh
```

### Option B — Manual Setup

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings (WhatsApp number, email, etc.)

# 4. Run migrations
python manage.py migrate

# 5. Load sample data
python manage.py loaddata fixtures/initial_data.json

# 6. Create admin account
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

### Access the App

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000` | Homepage |
| `http://127.0.0.1:8000/properties/` | Property listings |
| `http://127.0.0.1:8000/admin/` | Admin dashboard |
| `http://127.0.0.1:8000/sitemap.xml` | Sitemap |

---

## ⚙️ Configuration (`.env`)

Edit `.env` to customise:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

WHATSAPP_NUMBER=+2348012345678   # Your WhatsApp number
PHONE_NUMBER=+2348012345678      # Your call number
CONTACT_EMAIL=info@yoursite.com

# Email (for production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 🗂️ Project Structure

```
defola_properties/
├── defola_project/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                    # Homepage, About, Contact
│   ├── models.py            # SiteSettings, TeamMember
│   ├── views.py
│   ├── urls.py
│   └── context_processors.py
├── properties/              # Main property app
│   ├── models.py            # Property, Location, Inquiry, etc.
│   ├── views.py
│   ├── forms.py
│   ├── admin.py             # Custom admin
│   ├── sitemaps.py
│   ├── tests.py
│   └── templatetags/
│       └── property_tags.py
├── accounts/                # User auth & dashboard
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── templates/               # All HTML templates
│   ├── base.html            # Base with nav + footer
│   ├── core/
│   │   ├── home.html
│   │   ├── about.html
│   │   └── contact.html
│   ├── properties/
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── saved.html
│   │   └── _card.html       # Reusable property card
│   └── accounts/
│       ├── login.html
│       └── dashboard.html
├── static/
│   ├── css/
│   └── js/main.js
├── fixtures/
│   └── initial_data.json    # 6 properties + sample data
├── media/                   # User-uploaded files
├── requirements.txt
├── .env.example
├── setup.sh
└── manage.py
```

---

## 🛠️ Admin Panel Guide

Access at `/admin/` with your superuser credentials.

### Adding Properties

1. Go to **Properties → Properties → Add Property**
2. Fill in title, description, price, location, type
3. Scroll to **Images** section — upload multiple images
4. Set the first image as **Primary** (ticked)
5. Toggle **Is Featured** to show on homepage
6. Set **Status** to Available / Pending / Sold

### Managing Inquiries

- Go to **Properties → Inquiries**
- View customer name, phone, email, and message
- Update status: New → In Progress → Resolved
- Use bulk actions to mark multiple as resolved

### Bulk Actions on Properties

Select properties and choose from the **Action** dropdown:
- Mark as Available / Sold / Pending
- Mark / Remove from Featured

---

## 🧪 Running Tests

```bash
python manage.py test properties --verbosity=2
```

Tests cover:
- Model creation, slug auto-generation, uniqueness
- Formatted price, absolute URLs, meta descriptions
- List view, detail view, 404 handling
- Filter by type, search by keyword
- Inquiry submission and property linking
- Save/unsave property (auth required)

---

## 🌐 Deployment (Production)

### Option 1: VPS (Ubuntu/Debian)

```bash
# 1. On server — install Python, pip, nginx
sudo apt update && sudo apt install python3-pip python3-venv nginx

# 2. Clone your project
git clone <repo> /var/www/defola_properties
cd /var/www/defola_properties

# 3. Setup venv + install
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
nano .env   # Set DEBUG=False, ALLOWED_HOSTS=yourdomain.com, strong SECRET_KEY

# 5. Collect static + migrate
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py createsuperuser

# 6. Configure Gunicorn systemd service
sudo nano /etc/systemd/system/defola.service
```

Gunicorn service file:
```ini
[Unit]
Description=Defola's Properties Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/defola_properties
EnvironmentFile=/var/www/defola_properties/.env
ExecStart=/var/www/defola_properties/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/defola.sock \
    defola_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable defola && sudo systemctl start defola
```

Nginx config (`/etc/nginx/sites-available/defola`):
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /var/www/defola_properties/staticfiles/;
    }

    location /media/ {
        alias /var/www/defola_properties/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/defola.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/defola /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Add SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

### Option 2: Render.com (Easiest)

1. Push your code to GitHub
2. Create new **Web Service** on Render
3. Set **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Set **Start Command**: `gunicorn defola_project.wsgi:application`
5. Add Environment Variables from `.env.example`
6. Set `DEBUG=False` and `ALLOWED_HOSTS=your-render-url.onrender.com`

---

## 🔧 settings.py for Production

Add WhiteNoise to serve static files efficiently:

```python
# Already in MIDDLEWARE (add after SecurityMiddleware):
'whitenoise.middleware.WhiteNoiseMiddleware',

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 📱 Key URLs

| Path | View |
|------|------|
| `/` | Homepage (hero, featured, CTA) |
| `/properties/` | All properties (filterable, paginated) |
| `/properties/<slug>/` | Property detail page |
| `/properties/<slug>/inquiry/` | Submit inquiry (POST) |
| `/properties/<slug>/save/` | Toggle save (POST, auth required) |
| `/properties/saved/` | User's saved properties |
| `/about/` | About page with team |
| `/contact/` | Contact page with form |
| `/accounts/login/` | Login page |
| `/accounts/dashboard/` | User dashboard |
| `/sitemap.xml` | SEO sitemap |
| `/admin/` | Admin dashboard |

---

## 📞 Support

Built with ❤️ for the Nigerian real estate market.

WhatsApp: configured via `WHATSAPP_NUMBER` in `.env`
