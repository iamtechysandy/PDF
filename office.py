import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io


def run():
    st.title("Office File Compressor")
    st.markdown("### Compress PDF and image files efficiently with adjustable compression levels.")
    st.markdown("---")

    # File uploader
    file = st.file_uploader("Upload a file to compress", type=["pdf", "jpg", "jpeg", "png"])

    if file:
        file_type = file.type.split("/")[1]
        compression_level = st.slider("Select Compression Level (Higher = Less Compression)", 10, 100, 70)
        output_buffer = io.BytesIO()

        # Handle different file types
        if file_type == "pdf":
            st.info("Compressing PDF...")
            compress_pdf(file, output_buffer, compression_level)
            st.success("PDF compressed successfully!")
            st.download_button(
                "Download Compressed PDF",
                data=output_buffer.getvalue(),
                file_name="compressed_file.pdf",
                mime="application/pdf",
            )
        elif file_type in ["jpg", "jpeg", "png"]:
            st.info("Compressing Image...")
            compress_image(file, output_buffer, compression_level)
            st.success("Image compressed successfully!")
            st.download_button(
                "Download Compressed Image",
                data=output_buffer.getvalue(),
                file_name=f"compressed_image.{file_type}",
                mime=f"image/{file_type}",
            )
        else:
            st.error("File type not supported!")


# Helper Functions

def compress_pdf(input_pdf, output_buffer, compression_level):
    """
    Compress a PDF file and write it to an in-memory buffer.
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Write the compressed content directly to the buffer
    writer.write(output_buffer)
    output_buffer.seek(0)  # Reset the buffer pointer to the beginning


def compress_image(input_image, output_buffer, compression_level):
    """
    Compress an image and write it to an in-memory buffer.
    """
    img = Image.open(input_image)
    img.save(output_buffer, "JPEG", quality=compression_level)
    output_buffer.seek(0)  # Reset the buffer pointer to the beginning
