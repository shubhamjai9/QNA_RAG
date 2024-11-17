from langchain.output_parsers import (
    ResponseSchema,
    StructuredOutputParser,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import os

curr_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(curr_path + "/.env", override=True)
response_schemas = [
    ResponseSchema(
        name="response",
        description="answer to the user's question",
    ),
    ResponseSchema(
        name="out_of_context",
        description="return True if user query is greeting else False",
    ),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
    max_retries=2,
)


def transform_past_messages_into_text(data: list[dict[str, str]], length: int = -1):
    if len(data) == 0:
        return ""
    data_len = 0 if length == -1 else len(data) - length
    text_format = ""
    for entry in data[data_len:-1]:  # ignoring the last one
        text_format += f"{entry['role']}: {entry['content']}\n"  # type: ignore
    return text_format


def ragatouille_search(vector_store, user_id, message):
    retriever = vector_store.as_langchain_retriever(k=20, index_name="RAG_Assignment")

    documents = retriever.invoke(message)
    i = 0
    for r in documents:
        print(i, r.metadata)
        i += 1
    # external filter on overall data
    return list(filter(lambda x: x.metadata["user_id"] == user_id, documents))[:2]


#    - If the user query is a greeting then answer appropriately and mark out_of_context to True.
def chat(history: list[str], user_id: str, vector_store):
    system_prompt = (
        """
    Your name is ZOLO developed by Shubham, you are an assistant for question-answering task. You have been provided with additional context to help you with the query. Please do not use prior knowledge
    user query: "{question} "
    Step:
    -  Look for the answer for the query in the context:"{context}" and return out_of_context to False.
    - If you don't have answer for the question, respond with "I don't have enough information to answer that question." and return out_of_context to True. 

    Here is the additional context to help answer the users query: "{context}".

    Here's a recap of your conversation with the user: 
    """
        + f"{transform_past_messages_into_text(history,4)}"
        + "Please output in {format_instructions}"
    )

    message = history[-1]["content"]
    filter_dict = {"user_id": {"$eq": user_id}}
    if os.getenv("MODEL") == "ColBERT":
        document = ragatouille_search(vector_store, user_id, message)
    else:

        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 1,
                "fetch_k": 10,
                "lambda_mult": 0.5,
                "score_threshold": 0.5,
                "pre_filter": filter_dict,
            },
        )
        document = retriever.invoke(message)
    print(len(document))

    # We include two documents to make it easier to find answers to the query only if both documents originate from the same link.
    if len(document) == 0:
        data = ""
        reference = ""
    elif len(document) == 1:
        data = document[0].page_content
        reference = document[0].metadata["link_id"]
        print(reference)
    else:
        data = document[0].page_content
        reference = document[0].metadata["link_id"]
        if document[0].metadata["link_id"] != document[1].metadata["link_id"]:
            reference += f" and {document[1].metadata['link_id']}"
        data = f"{data} \n {document[1].page_content}"
    prompt = PromptTemplate.from_template(
        template=system_prompt,
        # input_variables=["context", "question"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )
    try:
        response = (
            {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
            | prompt
            | model
            | output_parser
        ).invoke([data, message])
        print(response)
    except Exception as e:
        print(e)
        return {
            "response": "We had some issues",
            "reference": "",
        }
    return {
        "response": response["response"],
        "reference": (
            reference if response["out_of_context"] in [False, "False"] else ""
        ),
    }
