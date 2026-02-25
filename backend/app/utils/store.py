from app.utils.vector_store import VectorStore

vector_store = VectorStore()
if vector_store.load_index():
    print("Index loaded successfully")
else:
    print("No existing index found")