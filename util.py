import streamlit as st
from pyzerox import zerox
import os

# Function for selecting LLM Model
def api_key_configuration():
    st.subheader('Configuration:')
    st.session_state.openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password",
                                                    value=st.session_state.openai_api_key,
                                                    help='Get API Key from: https://platform.openai.com/api-keys')

    if st.session_state.openai_api_key is None:
        st.warning('Set the API key to unlock application functionality.', icon=":material/warning:")
    else:
        os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key

# Function to perform OCR using zerox ocr engine
async def perform_ocr_zerox(source, model, auto_translate):
    markdown_format = ''
    translate = ""
    if auto_translate:
        translate = "If the markdown is in language other than English, translate the document to English"
    kwargs = {}  # Placeholder for additional model kwargs which might be required for some models
    # custom_system_prompt = None  # System prompt to use for the vision model

    custom_system_prompt = f"""Convert the following PDF page to markdown. Return only the markdown with no explanation
                              text. Do not exclude any content from the page. {translate}"""
    select_pages = None  ## None for all, but could be int or list(int) page numbers (1 indexed)

    result = await zerox(file_path=source, model=model,
                         custom_system_prompt=custom_system_prompt, select_pages=select_pages, **kwargs)

    # Get the content of all the pages
    for i in range(len(result.pages)):
        markdown_format += result.pages[i].content

    completion_time = result.completion_time / 1000

    return markdown_format, completion_time, result.input_tokens, result.output_tokens

def display_footer():
    footer = """
    <style>
    /* Ensures the footer stays at the bottom of the sidebar */
    [data-testid="stSidebar"] > div: nth-child(3) {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
    }

    .footer {
        color: grey;
        font-size: 15px;
        text-align: center;
        background-color: transparent;
    }
    </style>
    <div class="footer">
    Made with ❤️ by <a href="mailto:zeeshan.altaf@gmail.com">Zeeshan</a>.
    </div>
    """
    st.sidebar.markdown(footer, unsafe_allow_html=True)