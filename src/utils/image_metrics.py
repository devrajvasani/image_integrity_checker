import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr


def calculate_transfer_metrics(file1, file2):

    file1.seek(0)
    file2.seek(0)

    img1 = cv2.imdecode(np.frombuffer(file1.read(), np.uint8), cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(np.frombuffer(file2.read(), np.uint8), cv2.IMREAD_COLOR)

    if img1 is None or img2 is None:
        return {"error": "Invalid image format"}

    resolution_changed = img1.shape != img2.shape

    if resolution_changed:
        return {
            "resolution_changed": True,
            "message": "Resolution changed. Image was resized."
        }

    # Structural similarity
    ssim_score = ssim(img1, img2, channel_axis=2)

    # PSNR
    psnr_score = psnr(img1, img2)

    # Sharpness comparison
    sharp1 = cv2.Laplacian(img1, cv2.CV_64F).var()
    sharp2 = cv2.Laplacian(img2, cv2.CV_64F).var()

    sharpness_drop = ((sharp1 - sharp2) / sharp1) * 100 if sharp1 != 0 else 0

    return {
        "resolution_changed": False,
        "ssim": round(ssim_score, 6),
        "psnr_db": round(psnr_score, 2),
        "sharpness_original": round(sharp1, 2),
        "sharpness_transferred": round(sharp2, 2),
        "sharpness_drop_percent": round(sharpness_drop, 2)
    }
