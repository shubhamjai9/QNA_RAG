import gradio as gr
import pandas as pd
from fastapi.responses import RedirectResponse
from src.vector_updation import url_data_updation, load_store
from src.chat import chat
import os
import json
import ast
from dotenv import load_dotenv


curr_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv(override=True)
vector_store = load_store()
print(os.getenv("OPENAI_API_KEY"))


def authenticate(username, password):
    user_info = pd.read_csv(f"{curr_path}/user_password_info.csv", index_col=0)
    print(user_info)
    if username in user_info.index:
        if user_info.loc[username, "password"] == password:
            return True
    return False


def logout(request: gr.Request):

    # demo.launch(auth=authenticate, share=True)
    response = RedirectResponse(url="/", status_code=302)
    # response.delete_cookie(key=f"access-token-{app.cookie_id}")
    # response.delete_cookie(key=f"access-token-unsecure-{app.cookie_id}")
    return response


def grad_url_update(request: gr.Request, urls: str):
    try:
        urls = ast.literal_eval(urls)
        resp = url_data_updation(urls, request.username, vector_store)
        return {
            output_col: gr.Column(visible=True),
            status: resp["status"],
            indexed_url: resp["indexed_url"],
            failed_url: resp["failed_url"],
            error: resp.get("error", ""),
        }

    except Exception as e:
        resp = "Error:" + str(e)
        return {
            output_col: gr.Column(visible=True),
            status: False,
            indexed_url: [],
            failed_url: [],
            error: "Error:" + str(e),
        }


def responder(request: gr.Request, message: str, chatbox: list):
    history.append({"role": "user", "content": message})
    print(message, chatbox, request.username)
    output = chat(history, request.username, vector_store)
    chatbox.append(
        (
            history[-1]["content"],
            f"{output['response']} \n reference: {output['reference']}",
        )
    )
    return "", chatbox


history = []
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            urls = gr.Textbox(
                lines=10,
                label="List of urls",
                placeholder="Please provide strictly list of urls",
            )
            # response = gr.Textbox(label="response", visible=False)
            submit = gr.Button("Submit")
            status = gr.Textbox(label="Status")
            with gr.Column(visible=False) as output_col:
                indexed_url = gr.TextArea(label="Indexed Urls")
                failed_url = gr.Textbox(label="Failed Urls")
                error = gr.Textbox(label="Error")

            submit.click(
                grad_url_update,
                inputs=[urls],
                outputs=[output_col, status, indexed_url, failed_url, error],
            )

        with gr.Column(scale=2, min_width=300):
            chatbot = gr.Chatbot(label="Ask Query regarding DB")
            message = gr.Textbox(label="Message", placeholder="Write your message here")
            send = gr.Button("Send")

            clear = gr.ClearButton([message, chatbot])
            # logout_button = gr.Button(value="Logout")
            # logout_button.click(logout)

    send.click(responder, inputs=[message, chatbot], outputs=[message, chatbot])

    # # logout_button = gr.LogoutButton()
    # def respond(message, chat_history):
    #     bot_message = random.choice(["How are you?", "I'm very hungry"])
    #     chat_history.append((message, bot_message))
    #     time.sleep(2)
    #     return "", chat_history

    message.submit(responder, [message, chatbot], [message, chatbot])


if __name__ == "__main__":
    demo.launch(auth=authenticate, server_port=8002)
