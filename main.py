from src.vector_updation import url_data_updation, load_store
from src.chat import chat, ragatouille_search

if __name__ == "__main__":
    vector_store = load_store()
    r = ragatouille_search(vector_store, "master", "What is embedding")
    print(r)
    exit()

    urls = [
        "https://huyenchip.com/2024/07/25/genai-platform.html",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
        "https://jina.ai/news/what-is-colbert-and-late-interaction-and-why-they-matter-in-search/",
        "https://quoraengineering.quora.com/Building-Embedding-Search-at-Quora",
    ]

    user_id = "sjain"
    print(url_data_updation(urls, user_id, vector_store))
    history = [{"role": "user", "content": "Explain embedding searching?"}]
    response = chat(
        history=history,
        user_id=user_id,
        vector_store=vector_store,
    )
    print(response)
    history += [
        {"role": "assistant", "content": response["response"]},
        {"role": "user", "content": "What is colbert?"},
    ]
    response = chat(
        history=history,
        user_id=user_id,
        vector_store=vector_store,
    )
    print(response)
    history += [
        {"role": "assistant", "content": response["response"]},
        {"role": "user", "content": "What is ColBERT?"},
    ]
    response = chat(
        history=history,
        user_id=user_id,
        vector_store=vector_store,
    )
    print(response)
    history += [
        {"role": "assistant", "content": response["response"]},
        {"role": "user", "content": "Who are you?"},
    ]
    response = chat(
        history=history,
        user_id=user_id,
        vector_store=vector_store,
    )
    print(response)
    history += [
        {"role": "assistant", "content": response["response"]},
        {"role": "user", "content": "Hi, How are you?"},
    ]
    response = chat(
        history=history,
        user_id=user_id,
        vector_store=vector_store,
    )
    print(response)

    # [{'role': 'user', 'content': 'Explain embedding searching?'}, {'role': 'assistant', 'content': 'Embedding searching is a retrieval method that involves generating embeddings for documents or data points and then searching for similar embeddings to find relevant information. It is computationally expensive but can be improved over time to outperform term-based retrieval.'}, {'role': 'user', 'content': 'What is colbert?'}, {'role': 'assistant', 'content': 'ColBERT represents a significant leap forward in the field of information retrieval. By enabling longer context lengths with Jina-ColBERT and maintaining compatibility with the ColBERT approach to late interaction, it offers a powerful alternative for developers looking to implement state-of-the-art search functionality. Coupled with the RAGatouille library, which simplifies the integration of complex retrieval models into RAG pipelines, developers can now harness the power of advanced retrieval with ease, streamlining their workflows and enhancing their applications. The synergy between Jina-ColBERT and RAGatouille illustrates a remarkable stride in making advanced AI search models accessible and efficient for practical use.'}, {'role': 'user', 'content': 'What is ColBERT?'}, {'role': 'assistant', 'content': 'ColBERT is a model that leverages the deep language understanding of BERT while introducing a novel interaction mechanism called late interaction, allowing for efficient and precise retrieval by processing queries and documents separately until the final stages of the retrieval process. It offers scalability and efficiency in handling large-scale document collections.'}, {'role': 'user', 'content': 'Who are you?'}, {'role': 'assistant', 'content': 'When was the last time Emily Doe bought something from us?'}, {'role': 'user', 'content': 'Hi, How are you?'}]
