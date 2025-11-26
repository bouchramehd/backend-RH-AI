from rest_framework import generics, permissions
from .models import JobOffer, Application
from .serializers import JobOfferSerializer, ApplicationSerializer
from ml_app.ollama_service import extract_text_from_pdf, score_cv_with_ollama


# List all job offers / create job offers
class JobOfferListCreateView(generics.ListCreateAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.AllowAny]  # later: restrict to recruiter


# Retrieve / update / delete a job offer
class JobOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.AllowAny]


# List & submit applications
class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.AllowAny]  # later: candidate only

    def perform_create(self, serializer):
        # 1. Save the application first
        application = serializer.save()

        # 2. Extract text from the uploaded CV (PDF)
        cv_path = application.cv_file.path
        cv_text = extract_text_from_pdf(cv_path)

        # 3. Get the job description
        job_description = application.job.description

        # 4. Call Ollama to get a relevance score
        score = score_cv_with_ollama(cv_text, job_description)

        # 5. Save the score and update status
        application.score = score
        application.status = "in_review"
        application.save()
