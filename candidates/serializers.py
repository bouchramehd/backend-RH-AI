from rest_framework import serializers
from .models import JobOffer, Application

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    candidate_username = serializers.CharField(source="candidate.username", read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ("score", "status")
