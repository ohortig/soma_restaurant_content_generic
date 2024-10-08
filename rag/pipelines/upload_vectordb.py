# useful libs
import logging
import os
from tqdm.auto import tqdm
from dotenv import load_dotenv
# custom libs
from load_documents import load_documents

# vector db
from llama_index.embeddings.openai import OpenAIEmbedding
from langchain_community.vectorstores.upstash import UpstashVectorStore
from upstash_vector import Vector
from upstash_vector import Index

load_dotenv()

logging.basicConfig(level=logging.INFO)

openai_embedding_model = "text-embedding-3-small"
embedder = OpenAIEmbedding(model=openai_embedding_model)

logging.info("model loaded")

# Load data
data_path=""
documents = load_documents(DATA_PATH=data_path)

vector_store = []
for i, doc in tqdm(enumerate(documents[:10])):
    if doc.page_content:
        embeddings = embedder.get_text_embedding(doc.page_content)
        v = Vector(id=f"id_{i}", vector=embeddings, metadata=doc.metadata, data=doc.page_content)
        vector_store.append(v)
print(vector_store)
logging.info("Documents loaded & embedded")


index = Index(url=os.environ["UPSTASH_VECTOR_REST_URL"],
              token=os.environ["UPSTASH_VECTOR_REST_TOKEN"]
              )
logging.info("index initiated")
collection_name="test"
index.upsert(
    vectors=vector_store,
    namespace=collection_name
)
logging.info("vectorstore loaded with info")
