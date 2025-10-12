from langchain_community.embeddings import OllamaEmbeddings
import chromadb

class RAG:
    def __init__(self, model_name: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        self.embeddings = OllamaEmbeddings(model=model_name, base_url=base_url)
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name="moderation_data", embedding_function=self.embeddings.embed_query)