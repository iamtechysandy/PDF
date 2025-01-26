import streamlit as st
from streamlit_option_menu import option_menu
import comparison_tool
import excel
import office
import pdf
import time

# Set page configuration
st.set_page_config(page_title="Multi-App Dashboard", layout="wide")


# Centralized footer
def display_footer():
    footer = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f5f5f5;
            color: black;
            text-align: center;
            padding: 10px;
            font-size: 12px;
        }
    </style>
    <div class="footer">
        Techysandy.com - 2025 Made under Streamlit. https://techysandy.com
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)


# Centralized spinner with estimated time
def with_spinner_and_timer(func, *args, **kwargs):
    with st.spinner("Processing..."):
        start_time = time.time()
        result = func(*args, **kwargs)  # Call the function
        elapsed_time = time.time() - start_time
        st.success(f"Completed in {elapsed_time:.2f} seconds!")
        return result


# Sidebar navigation
with st.sidebar:
    theme = st.radio("Select Theme", options=["Light", "Dark"])
    selected = option_menu(
        "Navigation",
        ["Compare Files", "Compare Excel", "Compress Office Documents", "Compress PDF"],
        icons=["file-earmark-diff", "file-earmark-excel", "file-zip", "file-earmark-pdf"],
        menu_icon="grid",
        default_index=0,
    )


# Apply the selected theme
def apply_theme(theme):
    if theme == "Light":
        st.markdown(
            """
            <style>
                body {
                    background-color: #ffffff;
                    color: #000000;
                }
                .stApp {
                    background-color: #f9f9f9;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    elif theme == "Dark":
        st.markdown(
            """
            <style>
                body {
                    background-color: #333333;
                    color: #ffffff;
                }
                .stApp {
                    background-color: #444444;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )


apply_theme(theme)

# Display logo and header
col1, col2 = st.columns([1, 8])
with col1:
    st.image("logo.png", width=100)
with col2:
    st.markdown(
        """
        <h1 style="font-family: Arial, sans-serif; color: #333;">Multi-App Dashboard</h1>
        <p style="font-size: 16px; color: #555;">Seamlessly switch between tools for document and file management.</p>
        """,
        unsafe_allow_html=True,
    )

# Load selected app and apply spinner + timer
if selected == "Compare Files":
    with_spinner_and_timer(comparison_tool.run)
elif selected == "Compare Excel":
    with_spinner_and_timer(excel.run)
elif selected == "Compress Office Documents":
    with_spinner_and_timer(office.run)
elif selected == "Compress PDF":
    with_spinner_and_timer(pdf.run)

# Display footer
display_footer()
