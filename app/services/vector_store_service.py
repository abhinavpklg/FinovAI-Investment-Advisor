import pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone

class VectorStoreService:
    def __init__(self):
        pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="YOUR_PINECONE_ENVIRONMENT")
        self.embeddings = HuggingFaceEmbeddings()
        self.index_name = "financial-knowledge"
        self.vectorstore = Pinecone.from_existing_index(self.index_name, self.embeddings)

    def query_vectorstore(self, query, k=3):
        results = self.vectorstore.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in results])