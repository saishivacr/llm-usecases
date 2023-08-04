from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from utils.prompts import llama_qa_template
from utils.llm import build_llm
from utils.load_Vars import *
import os

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

db_path = f"{project_root}/{DB_FAISS_PATH}"


def set_qa_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=llama_qa_template,
                            input_variables=['context', 'question'])
    return prompt

def build_retrieval_qa(llm, prompt, vectordb):
    dbqa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=vectordb.as_retriever(search_kwargs={'k': int(VECTOR_COUNT)}),
                                       return_source_documents=bool(RETURN_SOURCE_DOCUMENTS),
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return dbqa

def llama_dbqa():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL,
                                       model_kwargs={'device': 'cpu'})
    vectordb = FAISS.load_local(db_path, embeddings)
    llm = build_llm("LLAMA2")
    qa_prompt = set_qa_prompt()
    dbqa = build_retrieval_qa(llm, qa_prompt, vectordb)

    return dbqa
