import os
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load environment variables from a .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-insecure-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'project',

    # Third-party apps
    'tinymce',
    'cloudinary',
    'cloudinary_storage',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'flora.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'flora.wsgi.application'

# Cloudinary configuration for media storage
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Database configuration (PostgreSQL via Neon)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Jazzmin admin customization
JAZZMIN_SETTINGS = {
    "site_title": "Flora",
    "site_header": "Admin Dashboard",
    "site_brand": "Hashim",
    "welcome_sign": "Welcome to store Admin!",
    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "project.Product": "fas fa-box-open",
        "project.Category": "fas fa-th-list",
        "project.Order": "fas fa-shopping-bag",
        "project.Contact": "fas fa-envelope",
        "project.Cart": "fas fa-shopping-cart",
        "project.productimage": "fas fa-images",
        "project.discount": "fas fa-tags",
        "project.voucher": "fas fa-ticket-alt",
    },
    "order_with_respect_to": [
        "project.Category", 
        "project.Product", 
        "project.Discount", 
        "project.Voucher", 
        "project.Order"
    ],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Products", "model": "project.Product"},
        {"name": "Orders", "model": "project.Order"},
        {"name": "Customers", "model": "project.Customer"},
    ],
    "usermenu_links": [
        {"name": "Profile", "url": "admin:auth_user_change", "icon": "fas fa-user"},
        {"name": "Support", "url": "https://yourstore.com/support", "icon": "fas fa-life-ring"},
        {"name": "Logout", "url": "admin:logout", "icon": "fas fa-sign-out-alt"},
    ],
    "hide_apps": ["auth", "sessions"],
    "hide_models": ["auth.User", "auth.Group"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "custom_css": "admin/custom.css",
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "theme": "cosmo",
    "custom_dashboard": "admin/index.html",
}

JAZZMIN_UI_TWEAKS = {
    "sidebar_nav_compact_style": False,
    "actions_sticky_top": True,
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (served from CDN)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] 
# Authentication redirects
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Enforce trailing slashes in URLs
APPEND_SLASH = True

