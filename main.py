import streamlit as st
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.colored_header import colored_header
from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM
from scrape import (scrape_website, split_dom_content, clean_body_content, extract_body_content)
from parse import parse_with_ollama

st.sidebar.title("Dashboard")

# Sidebar
option = st.sidebar.selectbox("Select a dashboard option:", ['Data All in One', 'Details', 'Creator'])

if option == 'Data All in One':
    st.markdown("<h1 style='text-align: center; color: white;'>📊 Data All in One </h1>", unsafe_allow_html=True)
    add_vertical_space(5)

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
                with st.spinner("Parsing the content..."):

                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    st.write(parsed_result)
                    st.download_button('Download', parsed_result)

    add_vertical_space(5)

    #CSV File Uploader With Ollama Model
    model = LocalLLM(
        api_base="http://localhost:11434/v1",
        model="llama3"
    )

    uploaded_file = st.file_uploader("📄 Upload a File:", type={"csv", "txt"})

    if uploaded_file:
        #CSV Files
        if uploaded_file.type == "csv":
            file_results = pd.read_csv(uploaded_file)
            st.write(file_results)
            df = SmartDataframe(file_results, config={"llm":model})
            prompt = st.text_area("💬 Enter your prompt:")

            if st.button("Generate"):
                if prompt:
                    with st.spinner("Generating..."):
                        st.write(df.chat(prompt))

        else:
            #txt Files
            file_content = uploaded_file.read().decode("utf-8")
            st.session_state.content = file_content
            with st.expander("View File Content"):
                st.text_area('File Content', file_content, height=300)

            if "content" in st.session_state:
                my_prompt = st.text_area("💬 What would you like to know?")
            if st.button('Analyze'):
                if my_prompt:
                    with st.spinner("Analyzing"):
                        file_chunks = split_dom_content(st.session_state.content)
                        text_result = parse_with_ollama(file_chunks, my_prompt)
                        st.write(text_result)
                        st.download_button('Download', text_result)
                        

    
    add_vertical_space(10)
    
elif option == 'Details':
        colored_header(
        label="Details",
        description="",
        color_name="blue-70",
    )
        
        st.subheader("""
All in One Data (Work in Progress)

All in One Data is a developing application designed to streamline data scraping and analysis for businesses. Built for Infinite League, this AI-powered tool automates the collection of data from websites and analyzes CSV and TXT files, offering users an all-in-one solution for managing diverse data sources.

Current Features:
- AI Web Scraping: Automatically gathers data, and solves captcha problems from multiple websites using AI, simplifying the data extraction process.
- File Analysis: Processes CSV and TXT files to identify patterns and generate useful insights.
- Initial Reporting: Provides basic reports and visualizations with plans for more robust analytics in future updates.
- Secure Data Handling: Implements initial security measures with ongoing improvements planned as development continues.

All in One Data is an evolving platform, with future updates aimed at expanding its capabilities to offer more powerful data analytics and custom reporting features.
""")
        
else:
    colored_header(
        label="Creator",
        description="",
        color_name="blue-70",
    )
    add_vertical_space(2)
    linkedin_url = "https://www.linkedin.com/in/vir-chuy-darm-jr/"
    linkedin_logo = "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png"

    # GitHub URL
    github_url = "https://github.com/cottonbhudz"
    github_logo = "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg"

    st.markdown(
    """
    <style>
    .reportview-container .main footer {visibility: hidden;}
    .logo-container {
        position: absolute;
        bottom: 10px;
        left: 0px;
        display: flex;
        align-items: center;
    }
    .logo-container img {
        margin-right: 10px;
    }
    </style>
    """, 
    unsafe_allow_html=True
    )

    # Display the LinkedIn and GitHub logos in the same container
    st.markdown(
        f'''
        <div class="logo-container">
            <a href="{linkedin_url}" target="_blank">
                <img src="{linkedin_logo}" width="30">
            </a>
            <a href="{github_url}" target="_blank">
                <img src="{github_logo}" width="30">
            </a>
        </div>
        ''', 
        unsafe_allow_html=True
    )