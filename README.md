# intent-classifier
Abei1uo的意图筛选器

# 模型下载：

````
pip install modelscope
````
````
python -c "from modelscope import snapshot_download; snapshot_download('AI-ModelScope/bge-small-zh-v1.5', cache_dir='./model_cache')"
````

## 启动
````
python -m uvicorn app.main:app --host 0.0.0.0 --port 8765 
````

