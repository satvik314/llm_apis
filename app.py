import streamlit as st
import random
import string

# List of options for the dropdowns
providers = ["Anyscale", "Perplexity", "Together", "Fireworks"]
llm_apis = ["Langchain", "LlamaIndex", "LiteLLM",  "OpenAI Client"]

# Function to generate a random code
def generate_random_code(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Create the form
with st.form("LLM APIs"):
    # Dropdown 1
    provider = st.selectbox("Provider", providers)

    # Dropdown 2
    llm_api = st.selectbox("LLM API", llm_apis)

    # Submit button
    submitted = st.form_submit_button("Submit")

    # If the submit button is clicked
    if submitted:
        # Generate a random code
        code = generate_random_code()

        # Display the code
        st.code("Your code is: " + code)