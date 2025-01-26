import os
import streamlit as st
from PIL import Image
import fitz
import os


def run():
    st.title("PDF Compressor")
    st.markdown("### Compress your PDFs with adjustable quality settings!")
    st.markdown("---")

    # Sidebar settings
    st.sidebar.title("Settings")
    compression_level = st.sidebar.slider("Compression Level", 10, 100, 70)
    st.sidebar.markdown("Use the slider to adjust the compression quality.")

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        input_path = f"temp_{uploaded_file.name}"
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Compress PDF"):
            output_path = "compressed_" + uploaded_file.name

            # Function to compress PDF
            def compress_pdf(input_path, output_path, compression_level):
                pdf = fitz.open(input_path)
                temp_images = []
                new_pdf = fitz.open()

                for page_num in range(len(pdf)):
                    page = pdf.load_page(page_num)
                    pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), alpha=False)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    temp_img_path = f"temp_page_{page_num}.jpg"
                    img.save(temp_img_path, "JPEG", quality=compression_level)
                    temp_images.append(temp_img_path)
                    img_page = new_pdf.new_page(width=page.rect.width, height=page.rect.height)
                    img_page.insert_image(page.rect, filename=temp_img_path)

                new_pdf.save(output_path)
                for temp_img in temp_images:
                    os.remove(temp_img)

                pdf.close()
                new_pdf.close()

            compress_pdf(input_path, output_path, compression_level)

            st.success("PDF compressed successfully!")
            with open(output_path, "rb") as f:
                st.download_button(
                    "Download Compressed PDF", data=f, file_name=output_path, mime="application/pdf"
                )
