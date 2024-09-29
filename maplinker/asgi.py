import os
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles import views as static_views

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maplinker.settings')

application = get_asgi_application()

