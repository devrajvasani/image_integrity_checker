import streamlit as st
import json
from services.comparator import compare_images

st.set_page_config(page_title="Image Integrity", layout="wide")

st.title("🔍 Image Integrity Checker")

# ----------------------------------------------------
# SESSION STATE (ONLY FOR RESULT)
# ----------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None


def reset_app():
    # Clear entire session safely
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# ----------------------------------------------------
# MAIN HORIZONTAL LAYOUT
# ----------------------------------------------------
left_col, right_col = st.columns([1, 1.2])

# ====================================================
# LEFT SIDE → UPLOAD + PREVIEW
# ====================================================
with left_col:

    st.subheader("📂 Upload Images")

    image1 = st.file_uploader(
        "Original Image",
        type=["jpg", "jpeg", "png", "webp"],
        key="original"
    )

    image2 = st.file_uploader(
        "Transferred Image",
        type=["jpg", "jpeg", "png", "webp"],
        key="transferred"
    )

    st.markdown("### 🖼 Preview")

    preview_col1, preview_col2 = st.columns(2)

    with preview_col1:
        if image1 is not None:
            st.image(image1, width=220)
        else:
            st.info("No Original Image")

    with preview_col2:
        if image2 is not None:
            st.image(image2, width=220)
        else:
            st.info("No Transferred Image")

    st.markdown("---")

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if image1 is not None and image2 is not None:
            if st.button("🔍 Compare"):
                st.session_state.result = compare_images(image1, image2)

    with btn_col2:
        if st.button("🔄 Reset"):
            reset_app()
            st.rerun()


# ====================================================
# RIGHT SIDE → REPORT
# ====================================================
with right_col:

    st.subheader("📊 Transfer Report")

    if st.session_state.get("result"):

        result = st.session_state.result

        # Final Score
        st.metric("Quality Score (%)", result["Final Quality Score (%)"])
        st.success(result["Quality Status"])

        st.markdown("### 📦 File Size Comparison")
        st.write(f"Original: {result['Original Image']['file_size_kb']} KB")
        st.write(f"Transferred: {result['Transferred Image']['file_size_kb']} KB")
        st.write(
            f"Difference: {result['Size Difference (KB)']} KB "
            f"({result['Size Difference (%)']}%)"
        )

        st.markdown("### 📏 Resolution Comparison")
        st.write(f"Original: {result['Original Image']['resolution']}")
        st.write(f"Transferred: {result['Transferred Image']['resolution']}")
        st.write(f"Resolution Changed: {result['Resolution Changed']}")

        st.markdown("### 🧾 Metadata")
        st.write(f"Metadata Stripped: {result['Metadata Stripped']}")

        if not result["Resolution Changed"]:
            metrics = result["Quality Metrics"]

            st.markdown("### 🔬 Quality Metrics")
            st.write(f"SSIM: {metrics['ssim']}")
            st.write(f"PSNR (dB): {metrics['psnr_db']}")
            st.write(f"Sharpness Drop (%): {metrics['sharpness_drop_percent']}")

        # Download Report
        report_text = json.dumps(result, indent=4)

        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name="transfer_quality_report.txt",
            mime="text/plain"
        )

    else:
        st.info("Upload both images and click Compare to generate report.")
