import os
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"]="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"

def llm_is_greeting(user_input, llm=None):
  if llm is None:
    llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo-16k", max_tokens=100)

  prompt = f"""
  You are given a Human's prompt below. You task is determine whether the Human prompt is greeting.
  Return True if it is greeting, False otherwise.
  Here is the Human's prompt delimited by the triple backticks:
  ```
  {user_input}
  ```
  """
  result = llm.predict(text=prompt)
  return result



def pdf_qa(chroma_db_path):
  embeddings = OpenAIEmbeddings()
  vectordb = Chroma(persist_directory=chroma_db_path,
                    embedding_function=embeddings)
  memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)
  pdf_qa = ConversationalRetrievalChain.from_llm(OpenAI(
    temperature=0.1, model_name="gpt-3.5-turbo-16k"), vectordb.as_retriever(), memory=memory)
  return pdf_qa


def pdf_qa_template(chroma_db_path):
  template = """
    Act as lawyer in the Republic of Kazakhstan, expert in Labor Code. Use information from the context.
    If there is no answer in context, try to answer it yourself.
    Use the following context (delimited by <ctx></ctx>) to answer the question, delimeted by triple dashes.
    ------
    <ctx>
    {context}
    </ctx>
    ------
    {question}
    ---
    Don't make up facts. Write which article (статья) you used if needed.
    If in your answer you use Месячный Расчетный показатель (МРП), additionally add info in tenge, given 1 МРП = 3450 tenge.
    Important! Reply in the same language as used in this sentence: ''' {question} '''. 
    If you cannot answer, then write you cannot answer in the same language as the question.
    """
  prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
  )

  embeddings = OpenAIEmbeddings()
  vectordb = Chroma(persist_directory=chroma_db_path,
                    embedding_function=embeddings)

  qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0.1, model_name="gpt-4"),
    chain_type='stuff',
    retriever=vectordb.as_retriever(search_kwargs={"k": 8}),
    verbose=True,
    chain_type_kwargs={
      "verbose": True,
      "prompt": prompt
    }
  )
  return qa



print(llm_is_greeting("Привет, как твои дела?"))