import cv2
from pyzbar.pyzbar import decode

def read_qr(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Không đọc được ảnh")

    qr_codes = decode(img)

    results = []
    for qr in qr_codes:
        results.append(qr.data.decode("utf-8"))
    return results

if __name__ == "__main__":
    print(read_qr("./image.jpg"))