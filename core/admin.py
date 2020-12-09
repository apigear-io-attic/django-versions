from django.contrib import admin
from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Document


class DocumentAdminSite(VersionAdmin):
    pass


admin.site.register(Document, DocumentAdminSite)
