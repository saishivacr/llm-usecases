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

# Header
st.header("PRIVATE GPT")
st.empty().markdown("&nbsp;")


def base():
    models = ["LLAMA2-7B", "LaMini-Flan-T5-783M"]
    selected = st.sidebar.selectbox(label="Select a model", options=models)
    if selected == "LLAMA2-7B":
        st.write(f"Selected model is **{selected}**")
    else:
        st.write(f"Selected model is **{selected}**")
    
    action = st.sidebar.radio(label="Select an Action", options=["Explore UseCases", "Chat UI"], label_visibility="hidden")

    if action == "Explore UseCases":
        tab1, tab2, tab3 = st.tabs(["Summerize", "Chat with WebContents", "QnA from Documents"])
        with tab1:
            summerize()
        with tab2:
            qna_web()
        with tab3:
            qna_docs()
    else:
        llm_app()

if 'auth_status' not in st.session_state:
    st.session_state.auth_status = False

if authentication_status:
    st.session_state.auth_status = True
    
    with st.sidebar:
        authenticator.logout('Logout', 'main')
        st.sidebar.write(f'Welcome, **{name}**')
    if username == 'admin':
        
        pages =  {
            #'Train LLM': train,
            'Try LLM': llm_app
        }  

        # Add a sidebar to display the page selector
        selection = st.sidebar.radio("Go to", list(pages.keys()), label_visibility="hidden")

        # Display the selected page content
        pages[selection]()
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