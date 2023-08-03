import os
import sys
import shutil
import requests
from bs4 import BeautifulSoup
import streamlit as st



# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, src_path)


knowledge_base_path = f"{project_root}/knowledge_base"


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

def ingest(documents):
    pass

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
                db = run_db_build()
                print(db)
            if db:
                st.success("Sucecssfully digested the content of the documents ✔️. You can proceed to interact with with your docuemnts.")
                st.session_state.db_loaded = True
        
        query = st.text_input(label="Ask queries from your documents",
                        placeholder="Type your query....",
                        disabled=not st.session_state.db_loaded)
        if len(query)>0:
            st.write("Implementing logic to get completion.")


                
            

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
