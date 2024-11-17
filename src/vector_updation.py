from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings, OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from ragatouille import RAGPretrainedModel
from dotenv import load_dotenv
import os
import shutil
from src.scrap import get_processed_text, url_extract

curr_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHROMA_PATH = curr_path + "/database/"
COLBERT_PATH = curr_path + "/.ragatouille/colbert/indexes/RAG_Assignment"

load_dotenv(curr_path + "/.env", override=True)

print(curr_path, os.getenv("OPENAI_API_KEY"))


def split_text(document: str):
    """
    Split the text content of the given list of Document objects into smaller chunks.
    Args:
      document (str): Document representing text chunks to split.
    Returns:
      list[Document]: List of Document objects representing the split text chunks.
    """
    # Initialize text splitter with specified parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Size of each chunk in characters
        chunk_overlap=100,  # Overlap between consecutive chunks
        length_function=len,
        add_start_index=True,  # Flag to add start index to each chunk
    )

    # Split documents into smaller chunks using text splitter
    chunks = text_splitter.split_text(document)
    print(f"Split {len(document)} documents into {len(chunks)} chunks.")

    return chunks  # Return the list of split text chunks


def load_store(embed: str = os.getenv("MODEL")):
    if embed == "mxbai":
        vector_store = Chroma(
            persist_directory=f"{CHROMA_PATH}/mxbai",
            collection_name="test",
            embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"),
        )
    elif embed == "ColBERT":
        try:
            vector_store = RAGPretrainedModel.from_index(COLBERT_PATH)
        except Exception as e:
            print("ERROR Ragatouille", e)
            vector_store = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
            vector_store.index(
                collection=["temp temp " * 1000],
                document_ids=["temp_link_id"],
                document_metadatas=[{"user_id": "temp", "link_id": "link_id"}],
                index_name="RAG_Assignment",
                max_document_length=512,
                split_documents=True,
            )

    else:
        vector_store = Chroma(
            persist_directory=f"{CHROMA_PATH}/openai",
            collection_name="test",
            embedding_function=OpenAIEmbeddings(),
        )
    return vector_store


def save_to_chroma(chunks: list[str], user_id: str, link_id: str, vector_store):
    """
    Save the given list of Document objects to a Chroma database.
    Args:
    document (str): Document representing text chunks to save.
    Returns:
    None
    """

    # chunks = split_text(document)
    metadata = []
    ids = []
    c = 0
    for chunk in chunks:
        metadata.append({"user_id": user_id, "link_id": link_id})
        ids.append(user_id + link_id + str(c))
        c += 1
    vector_store.add_texts(
        chunks,
        metadatas=metadata,
        ids=ids,
    )

    # Persist the database to disk
    vector_store.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    return vector_store


def save_to_ragatouille(collection, metadata, vector_store):

    vector_store.add_to_index(
        new_collection=[collection],
        new_document_ids=None,
        new_document_metadatas=[metadata],
        index_name="RAG_Assignment",
        split_documents=True,
    )


def url_data_updation(urls: list[str], user_id: str, vector_store):
    success_url = []
    failed_url = []
    if type(urls) != list or len(urls) < 1:
        return {
            "status": "Failure",
            "indexed_url": [],
            "failed_url": [],
            "error": "Please provide valid list of urls",
        }
    for url in urls:
        try:
            text = get_processed_text(url_extract(url), url)
            if os.getenv("MODEL") == "ColBERT":
                save_to_ragatouille(
                    text, {"user_id": user_id, "link_id": url}, vector_store
                )
            else:
                documents = split_text(text)
                save_to_chroma(documents, user_id, url, vector_store)
            success_url.append(url)
        except Exception as e:
            print("Error at url extraction", e)
            failed_url.append(url)
    return {"status": "success", "indexed_url": success_url, "failed_url": failed_url}
    # except Exception as e:
    #     return {}


if __name__ == "__main__":
    urls = urls = [
        "https://huyenchip.com/2024/07/25/genai-platform.html",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    ]
    user_id = "sjain"
    vector_store = load_store()
    print(vector_store)
    print(url_data_updation(urls, user_id, vector_store))
