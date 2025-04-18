import streamlit as st
import asyncio
from streamlit_pdf_viewer import pdf_viewer
from datetime import datetime
from util import *

# Page title of the application
page_title = "ScanLingua"
page_icon = "✨"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None
if "markdown_zerox" not in st.session_state:
    st.session_state.markdown_zerox = None
    st.session_state.input_tokens = None
    st.session_state.output_tokens = None
    st.session_state.zerox_ocr_time = None

# Application Title and description
st.title(f'{page_title}{page_icon}')
st.write('***:blue[From Scan to Clarity – OCR, Convert, Translate! ✨🔍📝]***')
st.write("""
ScanLingua is your smart document assistant! 📄➡️📝 Simply upload a scanned PDF, and let our app do the rest:

✅ Optical Character Recognition (OCR) to extract text

✅ Convert to clean Markdown for easy editing & sharing

✅ Auto-translate to English 🌍 if needed

Perfect for digitizing notes, reports, or multilingual documents—effortlessly! 🚀

""")

st.info("This application is powered by [Zerox OCR](https://github.com/getomni-ai/zerox). "
        "Popular toolkit for document OCR'ing.", icon=':material/info:')

# Display footer in the sidebar
display_footer()

api_key_configuration()
auto_translate = st.toggle('Auto Translate to English', value=False)

# File uploader
st.subheader("Upload a PDF file:", divider='gray')
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], label_visibility="collapsed", disabled=not st.session_state.openai_api_key)

# If pdf file is not none then save the contents of the pdf file into temp file
if uploaded_pdf is not None:
    # Save the contents of the uploaded file into temp file
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
        file.write(uploaded_pdf.getvalue())

    col1, col2 = st.columns([1, 1], vertical_alignment="top")

    # OCR with Zerox toolkit
    with col1:
        st.subheader('OCR with Zerox:', divider='gray')
        model_name = 'gpt-4o-mini'
        ocr_zerox = st.button("Run OCR", type="primary", key="run_ocr_zerox", disabled=not uploaded_pdf)
        if ocr_zerox:
            with st.spinner('Processing ...'):
                st.session_state.markdown_zerox, st.session_state.zerox_ocr_time, st.session_state.input_tokens,\
                st.session_state.output_tokens = asyncio.run(perform_ocr_zerox(temp_file, model_name, auto_translate))

        # Display the markdown response and statistics of Zerox
        if st.session_state.markdown_zerox is not None:
            st.subheader('Statistics:', divider='gray')
            col3, col4, col5 = st.columns(3)
            col3.metric('Time Taken (sec)', f'{st.session_state.zerox_ocr_time:.2f}')
            col4.metric('Input Tokens', f"{st.session_state.input_tokens:,}")
            col5.metric('Output Tokens', f"{st.session_state.output_tokens:,}")
            st.subheader('Response:', divider='gray')

            with st.expander('Markdown Response', expanded=True, icon=':material/markdown:'):
                zerox_container = st.container(height=1000, key='zerox-container')
                zerox_container.markdown(st.session_state.markdown_zerox, unsafe_allow_html=True)

                # Create a unique file name based on current date & time for download
                file_name = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                st.download_button("Download", data=st.session_state.markdown_zerox,file_name=f"{file_name}_zerox.md",
                                   type='primary', icon=':material/markdown:', help='Download the Markdown Response')

    # Display PDF Previewer
    with col2:
        st.subheader('PDF Previewer:', divider='gray')
        with st.expander(':blue[***Preview PDF***]', expanded=False, icon=':material/preview:'):
            pdf_viewer(uploaded_pdf.getvalue(), height=1000, render_text=True)



