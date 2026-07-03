import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config import DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL

embedding_function = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)