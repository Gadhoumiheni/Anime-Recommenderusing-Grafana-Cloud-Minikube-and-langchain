import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import getpass

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HuggingFace_API_Token")
MODEL_NAME = os.getenv("Model_Name", "llama-3.1-8b-instant")  

# Prompt for API key if not set
if not GROQ_API_KEY:
    GROQ_API_KEY = getpass.getpass("Enter your Groq API key: ")
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Load CSV data
loader = CSVLoader(
    file_path=r"C:\Users\user\Desktop\SelfProjects\AnimeRecommender\data\output.csv",
    csv_args={"delimiter": ","},
    encoding="utf-8"
)
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
docs = text_splitter.split_documents(documents)

# Create embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}  # optional: set device
)

# Build FAISS vector store
vectorstore = FAISS.from_documents(docs, embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Initialize LLM
llm = ChatGroq(
    model=MODEL_NAME,
    api_key=GROQ_API_KEY,
    temperature=0,
)

# Define prompt template
prompt_template = """
You are an anime recommendation assistant. Based on the following anime data, recommend the best anime for the user's request. if a user ask about a animie similar to one provided in his request, exclude it in the recommendation.
Provide a numbered list with name, genres, and a brief synopsis.

User Request: {question}

Anime Data:
{context}

Recommendation:
"""
PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Create RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
    input_key="question"
)

# Function to get anime recommendation
def get_anime_recommendation(query: str):
    print("Received query:", query)
    # Use .invoke() instead of deprecated __call__()
    result = qa_chain.invoke({"question": query})
    return result

if __name__ == "__main__":
    test_query = "I want to watch a fantasy anime with adventure and magic."
    recommendation = get_anime_recommendation(test_query)
    print("Recommendation:", recommendation['result'])
    print("Sources:", [doc.page_content for doc in recommendation['source_documents']])
