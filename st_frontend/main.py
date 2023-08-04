import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
#from train import train
from llm_page import llm_app
from summerize import summerize
from qna_content import qna_docs, qna_web


with open('st_frontend/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Streamlit configuration
st.set_page_config(
    page_title="Private LLM",
    page_icon="❇️",
    layout="wide",
    menu_items={
        "About": "A Simple Web interface for conversation chatbot trained on your data powered by LLMs"
    },
)
st.markdown(
    """ <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
                    padding-top: 1rem;
                }
    </style> """,
    unsafe_allow_html=True,
)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


with st.sidebar:
    st.image(
        "https://www.criticalriver.com/wp-content/uploads/2022/04/cr-logo-updated.png"
    )
    name, authentication_status, username = authenticator.login('Login', 'main')

if "model_name" not in st.state:
    st.session_state.model_name = ''

# Header
st.header("PRIVATE GPT")
st.empty().markdown("&nbsp;")


def base():
    models = ["LLAMA2-13B", "LaMini-Flan-T5-783M"]
    selected = st.sidebar.selectbox(label="Select a model", options=models)
    if selected == "LLAMA2-13B":
        st.write(f"Selected model is **{selected}**")
        st.session_state.model_name = "LLAMA2"
    else:
        st.write(f"Selected model is **{selected}**")
        st.session_state.model_name = "LaMini-Flan-T5"
    
    action = st.sidebar.radio(label="Select an Action", options=["Explore UseCases", "Chat UI"], label_visibility="hidden")

    if action == "Explore UseCases":
        if 'auth_status' not in st.session_state:
            st.session_state.auth_status = False
            st.session_state.db_loaded = False
            st.session_state.db_loaded = False
        
        tab1, tab2, tab3 = st.tabs(["Summerize", "Chat with WebContents", "QnA from Documents"])
        with tab1:
            summerize()
        with tab2:
            qna_web()
        with tab3:
            qna_docs()
    else:
        llm_app()



if authentication_status:
    st.session_state.auth_status = True
    
    with st.sidebar:
        authenticator.logout('Logout', 'main')
        st.sidebar.write(f'Welcome, **{name}**')
    if username == 'admin':
        base()
    elif username == 'user':
        base()
elif authentication_status == False:
    st.session_state.auth_status = False
    st.sidebar.error('Username/password is incorrect')
    base()
elif authentication_status == None:
    st.session_state.auth_status = False
    st.sidebar.warning('Please enter your username and password')
    base()