import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from app.classifier import IntentClassifier, get_classifier
from app.models.schema import ClassifyRequest, IntentScore
from app.config import settings

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时预加载模型
    logger.info("Loading intent classifier model...")
    get_classifier()
    logger.info("Model loaded successfully")
    yield

app = FastAPI(title="Intent Classifier", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/classify", response_model=IntentScore)
def classify(
    req: ClassifyRequest,
    classifier: IntentClassifier = Depends(get_classifier),
):
    threshold = req.threshold if req.threshold is not None else settings.default_threshold
    result = classifier.classify(req.text, threshold)
    logger.info(f"classify | text={req.text!r} intent={result['intent']} score={result['score']:.3f}")
    return result