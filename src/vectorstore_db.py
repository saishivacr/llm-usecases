# =========================
#  Module: Vector DB Build
# =========================
import os
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, PDFMinerLoader
from langchain.embeddings import HuggingFaceEmbeddings
from utils.load_Vars import *
import time

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

knowledge_base_path = f"{project_root}/{DATA_PATH}"
db_path = f"{project_root}/{DB_FAISS_PATH}"

# Build vector database
def run_db_build():
    try:
        start_time = time.time()
        os.makedirs(db_path, exist_ok=True)
        loader = DirectoryLoader(knowledge_base_path,
                                glob='*.pdf',
                                loader_cls=PDFMinerLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=int(CHUNK_SIZE),
                                                    chunk_overlap=int(CHUNK_OVERLAP))
        docs = text_splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL,
                                        model_kwargs={'device': 'cpu'})

        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(db_path)
        end_time = time.time()
        return vectorstore, end_time-start_time
    except Exception as e:
        error_msg = f"An error occurred while reading files: {e}"
        print(error_msg)
        return None
if __name__ == "__main__":
    db = run_db_build()
    print(db)
