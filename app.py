import streamlit as st
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

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

# Removed unused synchronous helper to favor streaming path


## #Title of the app
st.title("ChatBot- Script Generation")


## Select the Open Source model
selected_model = st.sidebar.selectbox("Select Open Source model", ["codellama"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## Main interface for user input (gated behind submit to reduce reruns)
st.write("What script do you need today?")

with st.form("gen_form"):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Generate")

if submitted and user_input:
    # Stream tokens for faster perceived latency
    placeholder = st.empty()
    streamed_text = ""
    llm = Ollama(model=selected_model, model_kwargs={"temperature": temperature, "num_predict": max_tokens})
    chain = (prompt | llm | StrOutputParser())
    for chunk in chain.stream({"question": user_input}):
        streamed_text += chunk
        placeholder.markdown(streamed_text)
    st.write(":Stay Tuned(Neha Mandwal)")
elif submitted and not user_input:
    st.write("Please provide the user input")





