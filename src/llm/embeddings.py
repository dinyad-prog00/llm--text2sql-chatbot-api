from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings(emdedding_type="hf"):

    if emdedding_type == "google":
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    elif emdedding_type == "openai":
        return OpenAIEmbeddings()
    else:
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            encode_kwargs={'normalize_embeddings': False}
        )
