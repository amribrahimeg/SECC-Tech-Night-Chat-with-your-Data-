# replace the followijg iwth your own Azure OpenAI key and base URL
OPENAI_API_KEY = "..."
OPENAI_BASE_URL = "..."

import streamlit as st
import openai
openai.api_type = "azure"
openai.api_base = OPENAI_BASE_URL
openai.api_version = "2022-12-01"
openai.api_key = OPENAI_API_KEY

def call_openai(prompt, temperature=0.9, max_tokens=100):

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].text

# initialize streamlit app
st.title("GPT-3 Playground")
st.write("This is a playground for GPT-3. You can try out different prompts and see what the model outputs.")

# add a text input field
prompt = st.text_area("Enter a prompt", "Once upon a time")

# add a slider for temperature
temperature = st.slider("Temperature", 0.0, 1.0, 0.9, 0.1)

# add a slider for max tokens
max_tokens = st.slider("Max Tokens", 1, 3000, 100, 1)

# add a button to call the API
if st.button("Call GPT-3"):
    with st.spinner("Calling the OpenAI API..."):
        response = call_openai(prompt, temperature, max_tokens)
        st.write(response)
        # st.code(response)
    
