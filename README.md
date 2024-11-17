# QNA_RAG

An application used to answer user queries on basis of the data provided through urls. It uses RAG Approach to filter document and provide sufficient response.

### Models
You can choose between mxbai, ColBERT and OpenAI Embeddings for RAG from `.env`.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the dependencies. Tested on :`Python==3.12.6`

```bash
pip install -r requirements.txt
```

## Usage
After Completing the installation of dependency. Please provide the `.env` file and  `user_password_info.csv` in the folder. Please do ensure that the `.env` file have `MODEL` and `OPENAI_API_KEY` values.

### API Usage 

```bash
python app.py
```
To Visit API:

`http://0.0.0.0:8001/docs`  

Dummy Request Format for Uploading Links(Curl)
```bash
curl -X 'POST' \
  'http://0.0.0.0:8001/api/v1/index' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "urls": [
        "https://huyenchip.com/2024/07/25/genai-platform.html",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination/"
    ],
  "user_id": "string"
}'
```
Returns a stringify json object
```json
{
    "status": "success",
    "indexed_url": [
        "https://huyenchip.com/2024/07/25/genai-platform.html",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
        "https://jina.ai/news/what-is-colbert-and-late-interaction-and-why-they-matter-in-search/",
        "https://quoraengineering.quora.com/Building-Embedding-Search-at-Quora"
    ],
    "failed_url": []
}
```
Dummy Request Format for Chat(Curl)
```bash
curl -X 'POST' \
  'http://0.0.0.0:8001/api/v1/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "string",
    "messages": [
        {
            "role": "user",
            "content": "Explain embedding searching?"
        },
        {
            "role": "assistant",
            "content": "Embedding searching is a retrieval method that involves generating embeddings for documents or data points and then searching for similar embeddings to find relevant information. It is computationally expensive but can be improved over time to outperform term-based retrieval."
        },
        {
            "role": "user",
            "content": "What is ColBert?"
        }
    ]
}'
```
Returns a stringify json object
```json
{
    "response": [
        {
            "content": "ColBERT is a model that achieves significant efficiency gains by reducing computational costs (FLOPs) and latency compared to traditional BERT-based ranking models. It matches or exceeds the effectiveness of BERT-based models with much lower computational demands.",
            "role": "assistant",
            "citation": "https://jina.ai/news/what-is-colbert-and-late-interaction-and-why-they-matter-in-search/"
        }
    ]
}
```


### FOR UI (Gradio) Usage
```bash
python app_ui.py
```
To Visit UI:

`http://127.0.0.1:8002/` 

First Login to the Link using user_id and Password provided in `user_password_info.csv`. After Login, you can send urls to update the vector data base. The urls Should be in list od string format as shown below:
<img width="626" alt="Screenshot 2024-11-17 at 6 04 56 PM" src="https://github.com/user-attachments/assets/610700cc-a944-44c3-abbf-8229015e2cb8">



You can directly converse with the Chatbot.

## Issues
1. There might be chances that Ratatoille won't work correctly as there is very less document and support for the library. 
2. While using ColBERT on CPU could slow up system.

## Future Work
1. Provide support for semantic router to improve chat response on greetings and personal questions.
2. Improve RAG structure for ColBert.
3. 

## Discussion

Happy to discuss if anything else is required or any issue you are facing while running the program

## License

[MIT](https://choosealicense.com/licenses/mit/)
