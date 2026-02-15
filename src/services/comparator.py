from utils.file_utils import get_file_info
from utils.hash_utils import generate_hashes
from utils.metadata_utils import extract_metadata
from utils.image_metrics import calculate_metrics

def compare_images(file1, file2):

    file1_bytes = file1.getvalue()
    file2_bytes = file2.getvalue()

    result = {
        "Image 1 Info": get_file_info(file1),
        "Image 2 Info": get_file_info(file2),
        "Image 1 Hash": generate_hashes(file1_bytes),
        "Image 2 Hash": generate_hashes(file2_bytes),
        "Image 1 Metadata": extract_metadata(file1),
        "Image 2 Metadata": extract_metadata(file2),
        "Comparison Metrics": calculate_metrics(file1, file2)
    }

    return result
