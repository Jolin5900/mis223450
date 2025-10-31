# mis223450/system/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url  # 導入 dj-database-url 用於解析雲端資料庫 URL
import logging

# 初始化日誌記錄器
logger = logging.getLogger(__name__)

# 載入 .env 檔案
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

# **注意：生產環境的 SECRET_KEY 將由 Render 環境變數注入**
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-fallback') 

# 部署時必須設置為 False
DEBUG = False 

# ----------------- ALLOWED_HOSTS (生產環境專用) -----------------
# 動態獲取 Render 服務的外部主機名
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    # 允許 Render 提供的外部主機名
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME]
else:
    # 本地開發時允許所有主機
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*'] 
# -----------------------------------------------------------------


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ----------------- WhiteNoise (新增: 處理靜態文件) -----------------
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    # ------------------------------------------------------------------
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'system.urls'

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/logout/'  
LOGIN_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 由於您的 'templates' 在 BASE_DIR (根目錄) 中
        'DIRS': [BASE_DIR / 'templates'], 
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

WSGI_APPLICATION = 'system.wsgi.application'


# ==============================================================================
# DATABASE
# ==============================================================================

# ----------------- PostgreSQL 連接 (PostgreSQL 修正) -----------------
DATABASES = {
    'default': dj_database_url.config(
        # Render 將在環境變數中提供 DATABASE_URL
        # 本地開發時，如果沒有 DATABASE_URL 環境變數，則使用 SQLite 作為備用
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600 
    )
}
# ------------------------------------------------------------------


# ==============================================================================
# STATIC AND MEDIA FILES
# ==============================================================================

# 靜態文件 URL
STATIC_URL = 'static/'

# 靜態文件收集目錄 (用於 collectstatic)
# **注意:** 由於您的 'static' 也在 BASE_DIR, 將收集到 'staticfiles' 避免衝突
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# 告訴 Django 在哪裡找額外的靜態文件
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 媒體文件設定 (用於處理使用者上傳的文件)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==============================================================================
# MISC
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'