FROM python:3.11-slim

WORKDIR /app

# 先装依赖，利用 Docker 缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 预下载模型（构建时下载，避免启动时拉取）
COPY scripts/preload_model.py .
RUN python preload_model.py

COPY . .

EXPOSE 8765

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8765"]