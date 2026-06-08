import pytesseract
import difflib
import cv2
import os
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


def extract_text(image_path):

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.resize(
        gray,
        None,
        fx=5,
        fy=5,
        interpolation=cv2.INTER_CUBIC
    )

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    text = pytesseract.image_to_string(
        thresh,
        config="--psm 7"
    )

    return text.strip()


def compare_text(source_img, target_img):

    source_text = extract_text(source_img)
    target_text = extract_text(target_img)

    print("\nSOURCE OCR:")
    print(source_text)

    print("\nTARGET OCR:")
    print(target_text)

    diff = list(
        difflib.ndiff(
            source_text.split(),
            target_text.split()
        )
    )

    return source_text, target_text, diff