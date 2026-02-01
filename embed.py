import utils as Utils
import os as OS
import requests
import fitz  # PyMuPDF
from tqdm import tqdm

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


# ---------------- PDF TO TEXT ----------------
def pdf_to_text(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    document = fitz.open(stream=response.content, filetype="pdf")
    text = ""

    for page in document:
        text += page.get_text()

    return text


# ---------------- TEXT SPLITTING ----------------
def split_text_into_sections(text: str, min_chars_per_section: int = 1000):
    paragraphs = text.split("\n")
    sections = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) <= min_chars_per_section:
            current += para + "\n"
        else:
            sections.append(current.strip())
            current = para + "\n"

    if current:
        sections.append(current.strip())

    return sections


# ---------------- EMBEDDING ----------------
def embed_text_in_chromadb(text, document_name, document_description):
    openai_key = OS.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not set")

    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_key,
        model="text-embedding-ada-002"
    )

    documents = split_text_into_sections(text)

    metadatas = [
        {
            "name": document_name,
            "description": document_description
        }
        for _ in documents
    ]

    vectordb = Chroma(
        persist_directory=Utils.DB_FOLDER,
        embedding_function=embeddings,
        collection_name="collection_1"
    )

    for i in tqdm(range(0, len(documents), 100), desc="Embedding"):
        vectordb.add_texts(
            texts=documents[i:i + 100],
            metadatas=metadatas[i:i + 100]
        )

    vectordb.persist()
    print(f"✅ Embedded {len(documents)} chunks successfully.")


# ---------------- RUN DIRECTLY ----------------
if __name__ == "__main__":
    document_name = "Artificial Intelligence Act"
    document_description = "Artificial Intelligence Act"

    text = pdf_to_text(Utils.EUROPEAN_ACT_URL)
    embed_text_in_chromadb(text, document_name, document_description)
