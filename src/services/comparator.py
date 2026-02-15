from utils.file_utils import get_file_info
from utils.hash_utils import generate_hashes
from utils.metadata_utils import extract_metadata
from utils.image_metrics import calculate_transfer_metrics


def classify_quality(score):
    if score >= 99:
        return "Identical"
    elif score >= 95:
        return "Very Minor Compression"
    elif score >= 85:
        return "Noticeable Degradation"
    else:
        return "Significant Quality Loss"


def compare_images(file1, file2):

    info1 = get_file_info(file1)
    info2 = get_file_info(file2)

    # ---------- File Size ----------
    size1 = info1["file_size_kb"]
    size2 = info2["file_size_kb"]

    size_diff_kb = round(size2 - size1, 2)
    size_diff_percent = round(((size2 - size1) / size1) * 100, 2) if size1 != 0 else 0

    # ---------- Hash ----------
    hash1 = generate_hashes(file1.getvalue())
    hash2 = generate_hashes(file2.getvalue())
    identical_file = hash1["md5"] == hash2["md5"]

    # ---------- Metadata ----------
    metadata1 = extract_metadata(file1)
    metadata2 = extract_metadata(file2)
    metadata_stripped = len(metadata2) < len(metadata1)

    # ---------- Quality Metrics ----------
    metrics = calculate_transfer_metrics(file1, file2)

    if metrics.get("resolution_changed"):
        final_score = 70
        status = "Resolution Changed (Image Resized)"
    else:
        normalized_psnr = min(metrics["psnr_db"] / 50, 1)
        final_score = (metrics["ssim"] * 0.6 + normalized_psnr * 0.4) * 100
        status = classify_quality(final_score)

    return {
        "Original Image": info1,
        "Transferred Image": info2,
        "Size Difference (KB)": size_diff_kb,
        "Size Difference (%)": size_diff_percent,
        "Resolution Changed": metrics.get("resolution_changed", False),
        "Metadata Stripped": metadata_stripped,
        "Files Identical": identical_file,
        "Quality Metrics": metrics,
        "Final Quality Score (%)": round(final_score, 2),
        "Quality Status": status
    }
