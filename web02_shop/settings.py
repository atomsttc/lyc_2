"""
Django settings for web02_shop project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3z@k)k4jdbxjl26m86k$%@2=rh8m%m=u^xclx8d_75-r%w5#l4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework_simplejwt',
    'rest_framework',
    'corsheaders',
    'ckeditor',
    'users',
    'cart',
    'goods',
    'order'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 支持跨域访问
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'web02_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
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

WSGI_APPLICATION = 'web02_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'web02_shop',
        "USER": "root",
        "PASSWORD": "123456",
        "PORT": 3306,
        "HOST": "localhost"
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 允许所以用户跨域请求
CORS_ORIGIN_ALLOW_ALL = True

# 指定自定义用户类
AUTH_USER_MODEL = 'users.User'

# DRF的配置
REST_FRAMEWORK = {
    # 配置登录鉴权方式
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # 配置DRF使用的过滤器
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ],
    # 配置限流频率
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1/minute'
    }

}


# token的相关配置
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),  # 访问令牌的有效时间
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 刷新令牌的有效时间
    "ROTATE_REFRESH_TOKENS": False,  # 若为True，则刷新后新的refresh_token有更新的有效时间
    "BLACKLIST_AFTER_ROTATION": True,  # 若为True，刷新后的token将添加到黑名单中,

    "ALGORITHM": "HS256",  # 对称算法：HS256 HS384 HS512  非对称算法：RSA
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,  # if signing_key, verifying_key will be ignore.
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),  # Authorization: Bearer <token>
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",  # if HTTP_X_ACCESS_TOKEN, X_ACCESS_TOKEN: Bearer <token>
    "USER_ID_FIELD": "id",  # 使用唯一不变的数据库字段,将包含在生成的令牌中以标识用户
    "USER_ID_CLAIM": "user_id",
}
# 使用自定义的认证类进行身份认证(登录时验证用户信息)
AUTHENTICATION_BACKENDS = [
    'common.authenticate.MyBackend'
]

# 文件上传的保存的路径
MEDIA_ROOT = BASE_DIR / 'file/image'
# 指定文件的获取的url路径
MEDIA_URL = 'file/image/'

