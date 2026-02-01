import os
from langchain_community.vectorstores import FAISS
from app.core import logger
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

class MemoryService:
    def __init__(self, embeddings: HuggingFaceEmbeddings):
        self.embeddings = embeddings
        self.db_path = "memory_store"
        self.vector_db = self._load_or_create_db()

    def _load_or_create_db(self):
        if os.path.exists(self.db_path):
            return FAISS.load_local(
                self.db_path, self.embeddings, allow_dangerous_deserialization=True
            )
        return FAISS.from_texts(["Initial memory"], self.embeddings)

    def save_memory(self, text: str):
        self.vector_db.add_texts([text])
        self.vector_db.save_local(self.db_path)
        logger.info(f"Memory stored: {text}")

    def search_memory(self, query: str, k: int = 3):
        docs = self.vector_db.similarity_search(query, k=k)
        logger.debug(docs)
        return [
            doc.page_content for doc in docs if doc.page_content != "Initial memory"
        ]
