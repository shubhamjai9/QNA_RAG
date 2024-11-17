# QNA_RAG

An application used to answer user queries on basis of the data provided through urls. It uses RAG Approach to filter document and provide sufficient response.

### Models
User can choose between mxbai, ColBERT and OpenAI Embeddings for RAG.

## Project Screen Shot(s)

#### Example:   

[ PRETEND SCREEN SHOT IS HERE ]

[ PRETEND OTHER SCREE SHOT IS HERE ]

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the dependencies.

```bash
pip install -r requirement.txt
```

## Usage
After Completing the installation of dependency. Please provide the `.env` file and  `user_password_info.csv` in the folder. Please do ensure that the `.env` file have `MODEL` and `OPENAI_API_KEY` values.

### API Usage 

```bash
python app.py
```
To Visit API:

`http://0.0.0.0:8001/docs`  

### FOR UI (Gradio) Usage
```bash
python app_ui.py
```
To Visit UI:

`http://127.0.0.1:8002/` 


## Discussion

Happy to discuss if anything else is required or any issue you are facing while running the program

## License

[MIT](https://choosealicense.com/licenses/mit/)
