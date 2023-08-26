import os
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdf(pdf_path: str):
  loader = PyPDFLoader(pdf_path)
  pages = loader.load_and_split()
  return pages


def init_vectordb(pdf_path):
  pages = load_pdf(pdf_path)
  embeddings = OpenAIEmbeddings()
  vectordb = Chroma.from_documents(pages, embedding=embeddings,
                                   persist_directory=".")
  vectordb.persist()
  return vectordb

from langchain.document_loaders import UnstructuredWordDocumentLoader

document_path = "/Users/sailana/ML_projects/LawyerAssistantProd/data/2. Трудовой Кодекс РК.txt"
#
# # Specify the custom delimiter
# delimiter = "Next"

# Read the content of the Word document
# with open(document_path, "rb") as file:
#     document_content = file.read().decode("utf-8")

from langchain.document_loaders import TextLoader
#
loader = TextLoader(document_path)
documents = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
  chunk_size=1000,
  chunk_overlap=100,
  keep_separator=False
)

split_documents = text_splitter.split_documents(documents)
for document in split_documents:
    document.metadata = {"source": "Трудовой Кодекс РК"}
#
os.environ["OPENAI_API_KEY"] = "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"
embeddings = OpenAIEmbeddings()
vectorstore_name = "prod_chroma"
vectordb = Chroma.from_documents(split_documents, embedding=embeddings,
                                 persist_directory=vectorstore_name)
vectordb.persist()
#

#
# splitter = CharacterTextSplitter(separator=delimiter, keep_separator=False, chunk_overlap=0,
#                                  chunk_size=0)
# split_documents = splitter.split_documents(documents)
#
# for document in split_documents:
#     document.metadata = {"source": "КОДЕКС РЕСПУБЛИКИ КАЗАХСТАН ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ"}
#
#
# # save document to chroma_db
# os.environ["OPENAI_API_KEY"] = "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"
# # # folder = "/Users/sailana/ML_projects/LawyerAssitantLLMBot/data_raw/"
# embeddings = OpenAIEmbeddings()
# vectorstore_name = "KOAP_cleaned"
# # file_path = "/Users/sailana/ML_projects/LawyerAssitantLLMBot/data_raw/КОАП_РК.pdf"
# # file_path = "/Users/sailana/ML_projects/LawyerAssitantLLMBot/data_raw/КОАП_РК.pdf"
# # loader_file = PyPDFLoader(file_path)
# # documents = loader_file.load_and_split()
# # print(documents)
# vectordb = Chroma.from_documents(split_documents, embedding=embeddings,
#                                  persist_directory=vectorstore_name)
# vectordb.persist()

# for file in os.listdir(folder):
#     file_path = folder+file
#     print(file_path)
#     loader_file = PyPDFLoader(file_path)
#     documents = loader_file.load_and_split()
#     vectordb = Chroma.from_documents(documents, embedding=embeddings,
#                                      persist_directory=vectorstore_name)
#     vectordb.persist()
# print(os.listdir("/Users/sailana/ML_projects/LawyerAssitantLLMBot/data_raw/"))
# loader = PyPDFLoader(
#     "/Users/sailana/ML_projects/LawyerAssitantLLMBot/data/VAT.pdf")
# documents = loader.load_and_split()
# embeddings = OpenAIEmbeddings()
# vectordb = Chroma.from_documents(documents, embedding=embeddings,
#                                  persist_directory="chroma_db_full_kaz_adm")
# vectordb.persist()
