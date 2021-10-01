from django.contrib import admin

# Register your models here.
from .models import Person , Manager,Worker

admin.site.register(Person)
admin.site.register(Manager)
admin.site.register(Worker)
