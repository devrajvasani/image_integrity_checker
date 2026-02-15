import streamlit as st
from services.comparator import compare_images
import json

st.set_page_config(page_title="Deep Image Comparator", layout="wide")

st.title("🔍 Deep Image Comparison Tool")

st.write("Upload two images to compare size, quality, metadata and internal metrics.")

col1, col2 = st.columns(2)

with col1:
    image1 = st.file_uploader("Upload Image 1", type=["jpg", "jpeg", "png", "webp"])

with col2:
    image2 = st.file_uploader("Upload Image 2", type=["jpg", "jpeg", "png", "webp"])

if image1 and image2:
    st.success("Images uploaded successfully!")

    if st.button("Compare Images"):

        result = compare_images(image1, image2)

        st.subheader("📊 Comparison Report")

        st.json(result)

        # Download report
        report_text = json.dumps(result, indent=4)

        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name="image_comparison_report.txt",
            mime="text/plain"
        )
