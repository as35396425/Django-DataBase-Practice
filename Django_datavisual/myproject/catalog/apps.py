from django.apps import AppConfig
from django.http import HttpResponse

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    