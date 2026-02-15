import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim, peak_signal_noise_ratio as psnr

def calculate_metrics(file1, file2):

    file1.seek(0)
    file2.seek(0)

    img1 = cv2.imdecode(np.frombuffer(file1.read(), np.uint8), cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(np.frombuffer(file2.read(), np.uint8), cv2.IMREAD_COLOR)

    if img1.shape != img2.shape:
        return {"error": "Images have different resolutions. Cannot compute structural metrics."}

    ssim_score = ssim(img1, img2, channel_axis=2)
    psnr_score = psnr(img1, img2)

    pixel_diff = int(np.sum(img1 != img2))

    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    hist_corr = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    sharp1 = cv2.Laplacian(img1, cv2.CV_64F).var()
    sharp2 = cv2.Laplacian(img2, cv2.CV_64F).var()

    noise1 = np.std(img1)
    noise2 = np.std(img2)

    return {
        "SSIM": ssim_score,
        "PSNR": psnr_score,
        "Pixel Difference": pixel_diff,
        "Histogram Correlation": hist_corr,
        "Sharpness Image 1": sharp1,
        "Sharpness Image 2": sharp2,
        "Noise Image 1": noise1,
        "Noise Image 2": noise2
    }
