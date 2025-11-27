from sentence_transformers import SentenceTransformer, util
import torch

# Charge un modèle d'embeddings efficace
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def score_cvs_batch(cv_texts: list[str], job_description: str) -> list[float]:
    """
    cv_texts : liste des textes de CV
    job_description : description du poste
    retourne : liste de scores entre 0 et 100 pour chaque CV
    """
    # Crée l'embedding du job
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    # Crée les embeddings pour tous les CV
    cv_embeddings = model.encode(cv_texts, convert_to_tensor=True, batch_size=16)

    # Calcul des similarités cosinus (vecteur du job vs chaque CV)
    similarities = util.cos_sim(cv_embeddings, job_embedding)

    # Convertit en scores 0-100
    scores = (similarities.squeeze().tolist())  # tensor -> liste
    if isinstance(scores, float):  # si un seul CV
        scores = [scores]
    scores = [max(0, min(sim*100, 100)) for sim in scores]

    return scores
