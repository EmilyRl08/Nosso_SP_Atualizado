
import os
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from django.core.exceptions import ImproperlyConfigured


# Caminho principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


# Carregar variáveis do arquivo .env
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass


# Funções auxiliares
def env_bool(nome, padrao=False):
    valor = os.environ.get(nome)

    if valor is None:
        return padrao

    return valor.strip().lower() in ("1", "true", "yes", "sim", "on")


def env_lista(nome):
    return [
        item.strip()
        for item in os.environ.get(nome, "").split(",")
        if item.strip()
    ]

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()

SUPABASE_SERVICE_ROLE_KEY = os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY", ""
).strip()

# Segurança
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-chave-apenas-para-desenvolvimento"
)

DEBUG = env_bool("DEBUG", True)

ALLOWED_HOSTS = env_lista("ALLOWED_HOSTS")

CSRF_TRUSTED_ORIGINS = env_lista("CSRF_TRUSTED_ORIGINS")


# Aplicativos instalados
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "noticias",
]


# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URLs
ROOT_URLCONF = "config.urls"


# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# BANCO DE DADOS - SUPABASE POSTGRESQL
def banco_de_dados():

    url = os.environ.get("DATABASE_URL", "").strip()

    if not url:
        raise ImproperlyConfigured(
            "DATABASE_URL não encontrada. Configure o Supabase no arquivo .env."
        )

    dados = urlparse(url)

    if dados.scheme not in ("postgres", "postgresql"):
        raise ImproperlyConfigured(
            "DATABASE_URL precisa ser uma conexão PostgreSQL válida."
        )

    if not dados.hostname or not dados.username or not dados.password:
        raise ImproperlyConfigured(
            "A conexão DATABASE_URL está incompleta."
        )

    porta = dados.port or 5432

    opcoes = {
        chave: valores[0]
        for chave, valores in parse_qs(dados.query).items()
    }

    opcoes.setdefault("sslmode", "require")

    configuracao = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": unquote(dados.path.lstrip("/")) or "postgres",
        "USER": unquote(dados.username),
        "PASSWORD": unquote(dados.password),
        "HOST": dados.hostname,
        "PORT": porta,
        "CONN_MAX_AGE": int(
            os.environ.get("DB_CONN_MAX_AGE", "60")
        ),
        "OPTIONS": opcoes,
    }

    # Configuração para Transaction Pooler do Supabase
    if porta == 6543:
        configuracao["DISABLE_SERVER_SIDE_CURSORS"] = True
        configuracao["CONN_MAX_AGE"] = 0

    return {
        "default": configuracao
    }


DATABASES = banco_de_dados()


# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Idioma e fuso horário
LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Arquivos estáticos
STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Armazenamento de arquivos
STORAGES = {
    "default": {
        "BACKEND": "noticias.storage.SupabaseStorage",
        "OPTIONS": {
            "bucket": "noticias",
            "public": True,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Buckets adicionais
STORAGES["curriculos"] = {
    "BACKEND": "noticias.storage.SupabaseStorage",
    "OPTIONS": {
        "bucket": "curriculos",
        "public": False,
    },
}

STORAGES["certificados"] = {
    "BACKEND": "noticias.storage.SupabaseStorage",
    "OPTIONS": {
        "bucket": "certificados",
        "public": False,
    },
}


# Chave padrão dos modelos
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# API Geoapify
GEOAPIFY_API_KEY = os.environ.get("GEOAPIFY_API_KEY", "")
