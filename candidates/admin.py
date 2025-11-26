from django.contrib import admin
from .models import JobOffer, Application


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "is_active", "created_at")
    list_filter = ("is_active", "location")
    search_fields = ("title", "description")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job", "score", "status", "created_at")
    list_filter = ("status", "job")
    search_fields = ("candidate__username", "job__title")
