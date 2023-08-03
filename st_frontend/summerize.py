import os
import sys
import streamlit as st

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.insert(0, src_path)

temp_docs = f"{project_root}/temp_docs"


def execute_summerization(text: str, auth: bool):
    is_text_empty = len(text.strip()) == 0
    if st.button("Summerize", disabled=is_text_empty):
        if auth:
            st.write("Summerized text is:")
            st.write(text)
            # Insert the logic to summerize.
        else:
            st.error("Please Login to use this feature")


def summerize():
    st.write("Paste your own content or provide an URL to get the summerized context.")

    input_option = st.selectbox(label="Choose input mode", options=["Paste Text", "from URL", "Upload a document"])

    if input_option == "Paste Text":
        text_input = st.text_area(label="Text to summerize 🗒️",
                                  value='''The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.''', 
                                  height=300,
                                  max_chars=2048)
        execute_summerization(text_input, st.session_state.auth_status)
    elif input_option == "from URL":
        url_input = st.text_input(label="Paste URL to summerize 🔗",
                                  value='''https://en.wikipedia.org/wiki/Eiffel_Tower''')
        # Insert extracting text from url logic here.
        # execute_summerization(url_input)
        st.error("Extracting from web pages is under development! Please visit us later!")
    else:
        uploaded_file = st.file_uploader(label="Upload a document", type=["pdf", "txt", "docx"])
        if uploaded_file is not None:
            os.makedirs(temp_docs, exist_ok=True)
            # Logic to extract content from documents
            # execute_summerization(text_input)
            st.error("This feature is under development! Please visit us later!")




