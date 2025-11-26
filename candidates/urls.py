from django.urls import path
from .views import (
    JobOfferListCreateView,
    JobOfferDetailView,
    ApplicationListCreateView,
)

urlpatterns = [
    path("offers/", JobOfferListCreateView.as_view(), name="job-list-create"),
    path("offers/<int:pk>/", JobOfferDetailView.as_view(), name="job-detail"),
    path("applications/", ApplicationListCreateView.as_view(), name="application-list-create"),
]
