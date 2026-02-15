from PIL import Image, ExifTags
import io

def extract_metadata(uploaded_file):
    metadata = {}
    try:
        image = Image.open(uploaded_file)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                metadata[tag_name] = str(value)
        else:
            metadata["info"] = "No EXIF metadata found"
    except:
        metadata["info"] = "Metadata not available"

    return metadata
