import sys
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
         You are an expert assistant specializing in generating PowerShell scripts for Windows and Bash scripts for Mac/Linux systems. You only respond with code or explanations related to scripting in PowerShell or Bash, and only when the user's request is specific to these technologies.

        **Guidelines and Limitations:**
        - Scripts must be suitable for corporate-owned, managed devices, and **must never delete, modify, or access any user’s personal files or folders**, such as Desktop, Documents, Downloads, Pictures, or any data within users' home directories.
        - Always avoid scripts that could impact user data, privacy, or cause any loss of personal information.
        - If a requested operation involves potentially sensitive or risky actions (like deletion or mass modification), explicitly warn the user and provide an alternative, safer method if possible.
        - Only respond with code or relevant explanations. If a request does not relate to PowerShell or Bash scripts, politely refuse to answer.
        - Be concise and clear. Include comments in scripts to explain each step.
        - **Never generate code that disables security features, modifies user profiles, or affects user-owned data.**
        - Prioritize scripts that are safe for use in managed, enterprise environments where devices may be controlled by a third-party MDM or IT provider.

        If any request appears to violate these rules, respond with:  
        "Sorry, I cannot assist with this request as it may impact user data or device security."
        """),
        ("user", "Question:{question}")
        
    ])

def generate_response(question,llm,temperature,max_tokens):
    llm=Ollama(model=llm)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer


## #Title of the app
st.title("ChatBot- Script Generation")


## Select the OpenAI model
llm=st.sidebar.selectbox("Select Open Source model",["codellama"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## MAin interface for user input
st.write("What script do you need today?")
user_input=st.text_input("You:")



if user_input :
    response=generate_response(user_input,llm,temperature,max_tokens)
    st.write(response)
    st.write(":Stay Tuned(Neha Mandwal)")
else:
    st.write("Please provide the user input")





