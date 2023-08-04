import os
import sys
import time
import shutil
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.abspath(os.path.join(project_root, "src"))
sys.path.insert(0, src_path)

from utils.load_Vars import *


knowledge_base_path = f"{project_root}/knowledge_base"
db_path = f"{project_root}/{DB_FAISS_PATH}"


def delete_folder_contents(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Delete the folder and its contents
        shutil.rmtree(folder_path)
        print(f"Deleted everything in '{folder_path}'.")
    else:
        print(f"Folder '{folder_path}' does not exist.")


def extract_webpages(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        st.error("Failed to fetch the page.")
        return None
    
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all div tags with class "mw-parser-output"
    # Works only with wikipedia
    article_divs = soup.find_all("div", class_="mw-parser-output")

    # Concatenate text from all divs to get the entire article content
    article_text = ""
    for div in article_divs:
        article_text += div.get_text()
    
    return article_text


def qna_docs():
    st.write("Upload your documents and type a query to get responses from the document.")
    os.makedirs(knowledge_base_path, exist_ok=True)
    # Display the file uploader
    uploaded_files = st.file_uploader(
        "Upload your knowledge base 📚", type=["pdf", "txt", "docx"], accept_multiple_files=True
    )
    # Clean the existing knowledge base
    if not st.session_state.auth_status:
        st.session_state.upload_docs_qna = False
        delete_folder_contents(knowledge_base_path)
        delete_folder_contents(db_path)
    len_uploaded_files = len(uploaded_files)

    # Validate files and copy to new_files directory
    if len_uploaded_files != 0:
        try:         
            if st.session_state.auth_status:
                # Create directory if not exists
                os.makedirs(knowledge_base_path, exist_ok=True)
                file_count = 0
                msg = st.toast(f"Uploading {len_uploaded_files} files...")
                for file in uploaded_files:
                    # Save the file to new_files directory
                    file_path = os.path.join(knowledge_base_path, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.read())
                    file_count += 1
                    # Display a success message after upload is done
                    msg.toast(f"Uploaded {file_count}/{len_uploaded_files}: {file.name}")

                if file_count == len_uploaded_files:
                    st.success("All files uploaded and validated successfully.")
                    msg.toast(f"Upload Complete.", icon="✔️")
                    st.session_state.upload_docs_qna = True
                elif file_count > 0 and file_count <= len_uploaded_files:
                    st.warning(f"Only {file_count} out of {len_uploaded_files} files are uploaded.")
                    msg.toast(f"Upload Complete.", icon="⚠️")
                else:
                    st.error("No files are uploaded.")
                    msg.toast(f"Upload Error.", icon="❌")
            else:
                st.error("Please Login to use this feature")
                st.session_state.db_loaded = False
        except Exception as e:
            error_msg = f"An error occurred while uploading files: {e}"
            st.exception(error_msg)

        if st.button("Digest Documents", disabled=not st.session_state.upload_docs_qna):
            st.session_state.db_loaded = False
            with st.spinner("Reading contents of documents..."):
                from vectorstore_db import run_db_build
                
                if os.path.exists(db_path) and os.path.isdir(db_path): 
                    delete_folder_contents(db_path)
                
                db, exec_time = run_db_build()
            if db:
                st.success(f"Sucecssfully digested the content of the documents ✔️. You can proceed to interact with with your docuemnts.\
                           Executed in {exec_time:.4f} seconds")
                st.session_state.db_loaded = True
        
        query = st.text_input(label="Ask queries from your documents",
                        placeholder="Type your query....",
                        disabled=not st.session_state.db_loaded)
        if len(query)>0:
            API_URL = "http://localhost:8000/queryllama"
            headers = {'Content-Type': 'application/json'}
            payload = {
                "query": query
            }
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                response_json = response.json()
                reply_dbqa = response_json['answer_dbqa']
                reply_genqa = response_json['answer_genqa']
                source = str(response_json['source_documents'])
                time = response_json['time_taken']
                col1, col2 = st.columns([3,2])
                with col1:
                    st.markdown("<h4 color: green>Answer from uploaded knowledge_base:</h4>", unsafe_allow_html=True)
                    st.markdown(reply_dbqa)
                    st.markdown(f"<p style='font-size: smaller; color: green;'>Source documents: {source}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: smaller; color: green;'>Time to retrieve response: {time:.4f} seconds", unsafe_allow_html=True)
                with col2:
                    st.markdown("<h4 color: green>Answer from known knowledge:</h4>", unsafe_allow_html=True)
                    st.markdown(reply_genqa)

            else:
                reply = f"Request error: {response.status_code} - {response.text}"
                st.markdown(reply)


                
            

def qna_web():
    st.write("Patse a Web Page URL, to chat with content of it.")
    st.info("Currently, this works best with wikipedia articles.")

    web_url = st.text_input(label="Paste URL to Chat with it 🔗",
                                  value='''https://en.wikipedia.org/wiki/Eiffel_Tower''')
    if len(web_url)>0:
        with st.spinner("Extracting Web Page contents..."):
            page_content = extract_webpages(web_url)
            if st.session_state.auth_status:
                if len(page_content) > 0 and len(page_content) < 3000:
                    st.success("Working!")
                else:
                    st.error("Context length is too long! We are working to support longer context.")
            else:
                st.error("Please Login to use this feature")
    else:
        st.error("Please input a web page URL")
