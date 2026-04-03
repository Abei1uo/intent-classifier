from sentence_transformers import SentenceTransformer
print("Downloading model...")
SentenceTransformer("BAAI/bge-small-zh-v1.5", cache_folder="./model_cache")
print("Done")