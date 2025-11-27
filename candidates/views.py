from rest_framework import generics, permissions
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.exceptions import PermissionDenied
from .models import JobOffer, Application
from .serializers import JobOfferSerializer, ApplicationSerializer
from ml_app.ollama_service import extract_text_from_pdf, score_cv_with_ollama


# ---------------------
# Offres d'emploi
# ---------------------
class JobOfferListCreateView(generics.ListCreateAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def get_queryset(self):
        # Si recruteur, on peut filtrer uniquement ses offres
        user = self.request.user
        if user.is_authenticated and user.role == "recruiter":
            return JobOffer.objects.filter(recruiter=user)
        # Pour les autres (candidats ou non connectés), afficher toutes les offres actives
        return JobOffer.objects.filter(is_active=True)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "recruiter":
            raise PermissionDenied("Seul un recruteur peut créer une offre.")
        serializer.save(recruiter=user)


class JobOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def perform_update(self, serializer):
        # Seul le recruteur qui a créé l'offre peut modifier
        if self.request.user != serializer.instance.recruiter:
            raise PermissionDenied("Vous ne pouvez pas modifier cette offre.")
        serializer.save()

    def perform_destroy(self, instance):
        # Seul le recruteur qui a créé l'offre peut supprimer
        if self.request.user != instance.recruiter:
            raise PermissionDenied("Vous ne pouvez pas supprimer cette offre.")
        instance.delete()


# ---------------------
# Candidatures
# ---------------------
class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == "candidate":
                # Le candidat voit uniquement ses candidatures
                return Application.objects.filter(candidate=user)
            elif user.role == "recruiter":
                # Le recruteur voit les candidatures pour ses offres
                return Application.objects.filter(job__recruiter=user)
        return Application.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "candidate":
            raise PermissionDenied("Seul un candidat peut postuler.")
        application = serializer.save(candidate=user)
        cv_text = extract_text_from_pdf(application.cv_file.path)
        job_description = application.job.description
        score = score_cv_with_ollama(cv_text, job_description)
        application.score = score
        application.status = "in_review"
        application.save()
