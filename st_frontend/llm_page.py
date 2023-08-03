import os
import streamlit as st
import requests

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

knowledge_base_path = f"{project_root}/knowledge_base"


def llm_app():

    os.makedirs(knowledge_base_path, exist_ok=True)
    # Display the file uploader
    uploaded_files = st.file_uploader(
        "Upload your knowledge base", type=["pdf", "txt", "docx"], accept_multiple_files=True
    )
    len_uploaded_files = len(uploaded_files)

    # Validate files and copy to new_files directory
    if len_uploaded_files != 0:
        try:
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
                upload_success = True
            elif file_count > 0 and file_count <= len_uploaded_files:
                st.warning(f"Only {file_count} out of {len_uploaded_files} files are uploaded.")
                msg.toast(f"Upload Complete.", icon="⚠️")
            else:
                st.error("No files are uploaded.")
                msg.toast(f"Upload Error.", icon="❌")
        except Exception as e:
            error_msg = f"An error occurred while uploading files: {e}"
            st.exception(error_msg)


    #if upload_file is not None:
    #    ingest():

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["domain"] == selected:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        if not authentication_status:
                st.error("Please login to use the LLM functionality")
        # Display user message in chat message container
        st.chat_message("user", avatar="🧑").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"domain": selected, "role": "user", "content": prompt})

        # API_URL = "http://localhost:8000/queryinput"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "query": prompt
        }


        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            # Display assistant response in chat message container
            with st.chat_message("assistant", avatar="🤖"):
                response_json = response.json()
                reply = response_json['answer']
                source = str(response_json['source_documents'])
                st.markdown(reply)
                st.markdown(f"<p style='font-size: smaller; color: green;'>Source documents: {source}</p>", unsafe_allow_html=True)
            # Add assistant response to chat history
            st.session_state.messages.append({"domain": selected, "role": "assistant", "content": reply})
        else:
            with st.chat_message("assistant", avatar="🤖"):
                reply = f"Request error: {response.status_code} - {response.text}"
                st.markdown(reply)
            # Add assistant response to chat history
            st.session_state.messages.append({"domain": selected, "role": "assistant", "content": reply})