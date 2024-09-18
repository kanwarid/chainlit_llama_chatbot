import pprint
import ollama
import chainlit as cl
from chainlit import Message
from src.sys_config import system_prompt
from chainlit.input_widget import Select


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", []) #Start with blank
    cl.user_session.set("chat_history", [{"role": "system",
                         "content": system_prompt}])


@cl.on_message
async def generate_response(query: cl.Message):
    chat_history = cl.user_session.get("chat_history")
    print("Query:", query.content)
    chat_history.append({"role": "user", "content": query.content})
    
    response = cl.Message(content="")
    ###Start: Model API Specific Part ###
    answer = ollama.chat(model="llama3.1:latest", messages=chat_history, stream=True)
    #pprint.pp(answer)
    
    complete_answer = ""
    for token_dict in answer:
        token = token_dict["message"]["content"]
        complete_answer += token
        await response.stream_token(token)
    
    ###End: Model API Specific Part ###
    chat_history.append({"role": "assistant", "content": complete_answer})    
    cl.user_session.set("chat_history", chat_history)
    pprint.pp(chat_history)

    await response.send()

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="List Top Financial Books",
            message="Can you help me with  top three financial books to study.",
            #icon="/public/idea.svg",
            ),

        cl.Starter(
            label="Tell me a Finance Joke",
            message="Give me tow liner funny joke with finanance learning",
            #icon="/public/learn.svg",
            ),
        cl.Starter(
            label="Quotes from Finance Guru/s",
            message="Tell me one great quote from Warren Buffer or Charlie Munger on Finance or Stock Market",
            #icon="/public/terminal.svg",
            ),
        cl.Starter(
            label="Best Financial Education Podcasts",
            message="Tell me three podcast series on financial education.",
            #icon="/public/write.svg",
            )
        ]
    
@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")

@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")
    
