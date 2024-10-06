import streamlit as st
import pandas as pd
from streamlit_extras.mention import mention
from pandasai import SmartDataframe
from langchain_ollama import OllamaLLM
from pandasai.llm.local_llm import LocalLLM
from scrape import (scrape_website, split_dom_content, clean_body_content, extract_body_content)
from parse import parse_with_ollama

st.sidebar.title("Dashboard")
st.sidebar.write("This is a sliding dashboard.")

# Sidebar input controls
option = st.sidebar.selectbox("Select a dashboard option:", ['Overview', 'Details', 'Settings'])

# Based on the selection, show different content on the main page
if option == 'Overview':
    st.write("This is the Overview page.")
elif option == 'Details':
    st.write("This is the Details page.")
else:
    st.write("This is the Settings page.")

#Page Title
st.markdown("<h1 style='text-align: center; color: white;'>📊 Data All in One </h1>", unsafe_allow_html=True)
st.subheader("")

#Web Scaper
url = st.text_input("🌐 Enter a Website URL:")

if st.button("Scrape Site"):
    with st.spinner("Scraping the website"):
    
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)


    st.session_state.dom_content = cleaned_content

    with st.expander("View Dom Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("💬 Describe what you want to parse?")

    if st.button("Parse"):
        if parse_description:
            with st.spinner("Parsing the content"):

                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)
                st.write(parsed_result)
                st.download_button('Download', parsed_result)

st.subheader("")

#CSV File Uploader With Ollama Model
model = LocalLLM(
    api_base="http://localhost:11434/v1",
    model="llama3"
)

uploaded_file = st.file_uploader("📄 Upload a File:", type={"csv", "txt"})

if uploaded_file:
    
    if uploaded_file.type == "text/csv":
        file_results = pd.read_csv(uploaded_file)
        st.write(file_results)
        df = SmartDataframe(file_results, config={"llm":model})
        prompt = st.text_area("💬 Enter your prompt:")

        if st.button("Generate"):
            if prompt:
                with st.spinner("Generating..."):
                    st.write(df.chat(prompt))

    else:
        file_results = pd.read_excel(uploaded_file)
        st.write(file_results)

#LinkedIn Link
linkedin_url = "https://www.linkedin.com/in/vir-chuy-darm-jr/"
linkedin_logo = "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png"

st.markdown(
    """
    <style>
    .reportview-container .main footer {visibility: hidden;}
    .linkedin-logo {
        position: flexible;
        bottom: 10px;
        left: 10px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
st.title("")
st.title("")
st.title("")
st.markdown(f'<a href="{linkedin_url}" target="_blank"><img src="{linkedin_logo}" width="30"></a>', unsafe_allow_html=True)
