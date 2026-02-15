import streamlit as st
import json
from services.comparator import compare_images

st.set_page_config(page_title="Pixel Integrity", layout="wide")

st.title("🔍 Pixel Integrity Checker")

st.write("Upload original image and transferred image to check quality degradation.")

col1, col2 = st.columns(2)

with col1:
    image1 = st.file_uploader("Upload Original Image", type=["jpg", "jpeg", "png", "webp"])

with col2:
    image2 = st.file_uploader("Upload Transferred Image", type=["jpg", "jpeg", "png", "webp"])

# ✅ This must come AFTER file_uploader
if image1 is not None and image2 is not None:

    if st.button("Check Transfer Quality"):

        result = compare_images(image1, image2)

        st.subheader("📊 Transfer Integrity Report")

        st.metric("Final Quality Score (%)", result["Final Quality Score (%)"])
        st.success(f"Status: {result['Quality Status']}")

        st.write("### File Size Change (%)")
        st.write(result["File Size Change (%)"])

        st.write("### Metadata Stripped")
        st.write(result["Metadata Stripped"])

        st.write("### Detailed Metrics")
        st.json(result["Quality Metrics"])

        report_text = json.dumps(result, indent=4)

        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name="transfer_quality_report.txt",
            mime="text/plain"
        )
