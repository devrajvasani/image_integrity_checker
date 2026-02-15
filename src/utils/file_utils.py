from PIL import Image
import os
import io

def get_file_info(uploaded_file):
    image = Image.open(uploaded_file)
    file_bytes = uploaded_file.getvalue()

    return {
        "filename": uploaded_file.name,
        "format": image.format,
        "mode": image.mode,
        "resolution": image.size,
        "file_size_kb": round(len(file_bytes) / 1024, 2)
    }
