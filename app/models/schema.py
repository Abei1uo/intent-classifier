from pydantic import BaseModel

class ClassifyRequest(BaseModel):
    text: str
    threshold: float | None = None  # 不传则用配置默认值

class IntentScore(BaseModel):
    intent: str
    score: float
    scores: dict[str, float]
    blocked: bool