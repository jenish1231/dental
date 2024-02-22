from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.apps import apps

# Get all models from the app
app_models = apps.get_app_config("flagapp").get_models()

# Automatically register all models in the admin interface
for model in app_models:
    admin.site.register(model)
