import streamlit as st
import time
from langchain.chat_models import ChatOpenAI, ChatAnyscale
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_core.messages import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ['MISTRAL_API_KEY'] = st.secrets['MISTRAL_API_KEY']
os.environ['PERPLEXITY_API_KEY'] = st.secrets["PERPLEXITY_API_KEY"]
os.environ['PERPLEXITY_API_BASE'] = st.secrets["PERPLEXITY_API_BASE"]
os.environ["ANYSCALE_API_KEY"] = st.secrets["ANYSCALE_API_KEY"]


# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello!"}
    ]

# Define available models
models = {"gpt-3.5-turbo-1106" : "openai", "mistral-medium" : "mistralai", "pplx-70b-online" : "perplexity", "mixtral" : "anyscale"} # replace with your actual models
model_list = list(models.keys())

with st.sidebar:
    st.title("Build Fast with AI")
    st.write("Chat with multiple LLMs across API providers")
# Add dropdown for model selection
    model_name = st.selectbox("Select a model:", model_list)

# # Initialize ChatOpenAI and ConversationChain
# if models[model_name] == "mistralai":
#     llm = ChatMistralAI(llm=model_name, 
#                         mistral_api_key=os.getenv("MISTRAL_API_KEY")
#                         )
#     print(llm.predict("hello"))
#     # llm  = ChatOpenAI(model_name="mistral-medium", openai_api_base  ="https://api.mistral.ai/v1/chat/completions", openai_api_key=os.getenv("MISTRAL_API_KEY"))
# elif models[model_name] == "openai":
#     llm = ChatOpenAI(model_name=model_name)
# elif models[model_name] == "anyscale":
#     if model_name == "mixtral":
#         llm  = ChatOpenAI(model_name="mistralai/Mixtral-8x7B-Instruct-v0.1", 
#                           openai_api_base  ="https://api.endpoints.anyscale.com/v1", 
#                           openai_api_key=os.getenv("ANYSCALE_API_KEY"))
# elif models[model_name] == "perplexity":
#     llm = ChatOpenAI(model_name= model_name,
#                       openai_api_base="https://api.perplexity.ai",
#                       openai_api_key=os.getenv("PERPLEXITY_API_KEY"),
#                     #   streaming = True, 
#                     #   callbacks=[StreamingStdOutCallbackHandler()]
#                       )

llm = ChatMistralAI(llm=model_name, 
                        mistral_api_key=os.getenv("MISTRAL_API_KEY")
                        )
conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Create user interface
# st.title("Build Fast with AI - Chat")
st.subheader("You are now chatting with " + model_name)


if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# # If last message is not from assistant, generate a new response
# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             response = conversation.predict(input = prompt)
#             st.write(response)
#             message = {"role": "assistant", "content": response}
#             st.session_state.messages.append(message) # Add response to message history


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Placeholder for chatbot's response
        # with st.spinner("Thinking..."):
        full_response = ""
        for chunk in conversation.predict(input=prompt).split():
            full_response += chunk + " "
            time.sleep(0.01)  # Delay to simulate streaming
            message_placeholder.write(full_response + "▌")  # Add a blinking cursor to simulate typing
        message_placeholder.write(full_response)  # Display the full response
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)  # Add response to message history
