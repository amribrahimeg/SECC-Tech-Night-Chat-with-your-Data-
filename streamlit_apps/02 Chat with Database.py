import streamlit as st

from langchain.sql_database import SQLDatabase
from langchain.llms import AzureOpenAI


#replace with your own values
openai_api_base="...."
openai_api_key="...."
db_user = "...."
db_password = "...."
db_host = "...."
db_name = "...."

llm = AzureOpenAI(deployment_name="text-davinci-003", 
                  model_name= "text-davinci-003", 
                  openai_api_base=openai_api_base,
                  openai_api_key=openai_api_key,
                  temperature=0.1,
                  openai_api_version="2022-12-01"
                  )


db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

from langchain import SQLDatabaseChain

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, top_k=100)

st.title("Chat with your database!🤖")

st.text('Welcome')

user_input = st.text_area("Write your question here:")
import json

if user_input:
    with st.spinner('Talking with the database. Please wait...'):
        lang = llm("What's the language of this phrase? Give only the name of the language. Phrase: " + user_input)

        # st.write(lang)
        if lang != "English":
            english_question = llm("Translate the following from " + lang + " to English:" + user_input)
        else:
            english_question = user_input
        
        response = db_chain.run(english_question + ". Always include table names before field names when writing the SQL commands. Use nested queries when needed. If the database doesn't contain the answer, return 'No answer found' and never make up an answer. When searching for a subject, always use the like operator rather than the equal operator and search in the module title rather than the subject column")

        if lang=="English":
            st.success(response)
        else:
            st.success(llm("Translate the following statement into " + lang + ". Statement: " + response + "."))
