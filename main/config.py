import os
import site
import sys

os.environ.setdefault("USE_TF", "0")
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")

user_site = site.getusersitepackages()
if user_site not in sys.path:
    site.addsitedir(user_site)

DB_DIR = "chroma_db"
COLLECTION_NAME = "pm_documents"
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
TOP_K = 4

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"