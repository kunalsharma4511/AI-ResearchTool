from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from langchain_core.prompts import PromptTemplate
import json
import sys

load_dotenv()

try:
    _ctx = get_script_run_ctx()
except Exception:
    _ctx = None

if __name__ == "__main__" and _ctx is None:
    print("This is a Streamlit app. Run it with:")
    print("    streamlit run prompt_ui.py")
    sys.exit(0)

model = ChatGoogleGenerativeAI(model="gemini-2.5-pro")


st.header("Research Tool")
# user_input = st.text_input("Enter your prompt:")

paper_input = st.selectbox(" Select a research paper:",
                           ("Paper 1: AI in Healthcare", 
                            "Paper 2: Quantum Computing",
                            "Paper 3: Climate Change Models",
                            "Paper 4: Renewable Energy Technologies",
                            "Paper 5: Advances in AI Ethics",
                            "Paper 6: Space Exploration Technologies",
                            "Paper 7: Attention Mechanisms in Neural Networks"
                            ))
style_input = st.selectbox(" Select a writing style:",
                           ("Formal", "Informal", "Technical", "Conversational"))
length_input = st.selectbox(" Select response length:",
                            ("Short", "Medium", "Long"))

with open("template.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Expect data to have keys like "template" and optional "input_variables"
template = PromptTemplate(
    input_variables=["query", "style", "length"],
    template="answer this {paper} in a {style} style with {length} length."
)

#fill the placeholders
prompt = template.format(
    paper = paper_input,
    style = style_input,
    length = length_input
)
if st.button("Summarize"):
    chain = template | model
    result = chain.invoke({
        "paper": paper_input,
        "style": style_input,
        "length": length_input
    })
    st.write(result.content)
    # response = ChatGoogleGenerativeAI().generate(user_input)
    # st.text(response)