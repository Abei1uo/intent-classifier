import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"
import numpy as np
import yaml
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings

class IntentClassifier:
    def __init__(self):
        self.model = SentenceTransformer(
            settings.model_name,
            #cache_folder=settings.model_cache_dir,
            local_files_only=True, #避免联网
        )
        self.intents_config = self._load_intents()
        self.anchor_vectors = self._precompute_anchors()

    def _load_intents(self) -> dict:
        with open(settings.intents_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data["intents"]

    def _precompute_anchors(self) -> dict[str, np.ndarray]:
        vectors = {}
        for intent, cfg in self.intents_config.items():
            vecs = self.model.encode(cfg["anchors"])
            vectors[intent] = np.mean(vecs, axis=0)
        return vectors

    def classify(self, text: str, threshold: float) -> dict:
        vec = self.model.encode([text])[0]

        scores = {
            intent: float(cosine_similarity([vec], [anchor])[0][0])
            for intent, anchor in self.anchor_vectors.items()
        }

        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        blocked = best_intent == "other" or best_score < threshold

        return {
            "intent": "other" if blocked else best_intent,
            "score": best_score,
            "scores": scores,
            "blocked": blocked,
        }

# 单例，避免重复加载模型
_classifier: IntentClassifier | None = None

def get_classifier() -> IntentClassifier:
    global _classifier
    if _classifier is None:
        _classifier = IntentClassifier()
    return _classifier