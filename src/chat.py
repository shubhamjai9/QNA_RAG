from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import (
    ResponseSchema,
    StructuredOutputParser,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from src.vector_updation import load_store
from langchain_core.pydantic_v1 import BaseModel, Field
import os

curr_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(curr_path + "/.env", override=True)
# class Joke(BaseModel):
#     response: str = Field(description="The setup of the joke")
#     out_of_context: str = Field(description="The punchline to the joke"

response_schemas = [
    ResponseSchema(
        name="response",
        description="answer to the user's question",
    ),
    ResponseSchema(
        name="out_of_context",
        description="return True if user query is greeting else False",
        # type=bool,
    ),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

load_dotenv()

model = ChatOpenAI(
    temperature=0.0,
)

# def greeting(message:str):
#     system_prompt = """
#     Your name is ZOLO, a research assistant developed by Shubham, You look at user query and return True and False on basis
# """

# You are a knowledgeable DBT coach. You always talk about one options at at a time. you add greetings and you ask questions like real counsellor. Remember you are helpful and a good listener. You are concise and never ask multiple questions, or give long response. You response like a human counsellor accurately and correctly. consider the users as your client. and practice verbal cues only where needed. Remember you must be respectful and consider that the user may not be in a situation to deal with a wordy chatbot.  You Use DBT book to guide users through DBT exercises and provide helpful information. When needed only then you ask one follow up question at a time to guide the user to ask appropiate question. You avoid giving suggestion if any dangerous act is mentioned by the user and refer to call someone or emergency."


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


def chat(history: list[str], user_id: str, vector_store):
    system_prompt = (
        """
    Your name is ZOLO developed by Shubham, you are an assistant for question-answering task. You have been provided with additional context to help you with the query.
    Please respond to the user query and also return out_of_context to True if the user query is greeting or good bye or if it related to you or ZOLO else False.
    Greet user with "Hi I am ZOLO. How are you?" if it is a greeting message.   
    Here is the additional context to help answer the users query: {context}.
    ** Important Instruction: .
    * You must briefly answer the user query based on the additional context.
    * If you don't have answer for the question, respond with "I don't have enough information to answer that question." and return out_of_context to True. 
    * Do not mention that "my answer is based on the given context" in your replies
    * You avoid giving suggestion if any dangerous act is mentioned by the user and refer to call someone or emergency.
    **

    user query: {question}
    Here's a recap of your conversation with the user:
    
        
    """
        + f"{transform_past_messages_into_text(history,2)}"
        + "Please output in {format_instructions}"
    )

    message = history[-1]["content"]
    filter_dict = {"user_id": {"$eq": user_id}}
    # retriever = RetrievalQA.from_chain_type(
    #     llm=model,
    #     chain_type=self.chain_type,
    #     retriever=retriever,
    #     return_source_documents=True,
    #     chain_type_kwargs={"prompt": custom_prompt},
    # )
    if os.getenv("MODEL") == "ColBERT":
        document = ragatouille_search(vector_store, user_id, message)
    else:

        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 2,
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
    else:
        data = document[0].page_content
        reference = document[0].metadata["link_id"]
        if document[0].metadata["link_id"] == document[1].metadata["link_id"]:
            data = f"{data} \n {document[1].page_content}"
    prompt = PromptTemplate.from_template(
        template=system_prompt,
        # input_variables=["context", "question"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )

    response = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | model
        | output_parser
    ).invoke([data, message])
    return {
        "response": response["response"],
        "reference": reference if response["out_of_context"] == False else "",
    }
