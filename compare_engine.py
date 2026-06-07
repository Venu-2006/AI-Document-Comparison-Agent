import cv2
import os
from skimage.metrics import structural_similarity as ssim


def compare_pages(source_img, target_img):

    img1 = cv2.imread(source_img)
    img2 = cv2.imread(target_img)

    if img1 is None:
        raise Exception(f"Cannot read {source_img}")

    if img2 is None:
        raise Exception(f"Cannot read {target_img}")

    # Resize images to same size
    h = min(img1.shape[0], img2.shape[0])
    w = min(img1.shape[1], img2.shape[1])

    img1 = cv2.resize(
        img1,
        (w, h)
    )

    img2 = cv2.resize(
        img2,
        (w, h)
    )

    gray1 = cv2.cvtColor(
        img1,
        cv2.COLOR_BGR2GRAY
    )

    gray2 = cv2.cvtColor(
        img2,
        cv2.COLOR_BGR2GRAY
    )

    # SSIM Comparison
    score, diff = ssim(
        gray1,
        gray2,
        full=True
    )

    print(
        f"Similarity Score: {score}"
    )

    diff = (
        diff * 255
    ).astype(
        "uint8"
    )

    thresh = cv2.threshold(
        diff,
        0,
        255,
        cv2.THRESH_BINARY_INV |
        cv2.THRESH_OTSU
    )[1]

    # ==================================
    # NEW: Merge nearby text differences
    # ==================================

    kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (15, 15)
)

    thresh = cv2.dilate(
    thresh,
    kernel,
    iterations=1
)

    # Optional cleanup
    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    print(
        f"Contours Found: {len(contours)}"
    )

    return (
        contours,
        img1,
        img2,
        diff,
        score
    )
def merge_boxes(
    boxes,
    distance=50
):

    merged = []

    for box in boxes:

        x, y, w, h = box

        merged_flag = False

        for i, (
            mx,
            my,
            mw,
            mh
        ) in enumerate(merged):

            if (
                abs(x - mx) < distance
                and
                abs(y - my) < distance
            ):

                nx = min(
                    x,
                    mx
                )

                ny = min(
                    y,
                    my
                )

                nw = max(
                    x + w,
                    mx + mw
                ) - nx

                nh = max(
                    y + h,
                    my + mh
                ) - ny

                merged[i] = (
                    nx,
                    ny,
                    nw,
                    nh
                )

                merged_flag = True

                break

        if not merged_flag:

            merged.append(
                box
            )

    return merged
def save_changes(
    contours,
    img1,
    img2,
    diff,
    page_num
):

    os.makedirs(
        "screenshots",
        exist_ok=True
    )

    source_marked = img1.copy()
    target_marked = img2.copy()

    cv2.imwrite(
        f"screenshots/page_{page_num}_source_original.png",
        img1
    )

    cv2.imwrite(
        f"screenshots/page_{page_num}_target_original.png",
        img2
    )

    boxes = []

    for contour in contours:

        area = cv2.contourArea(
            contour
        )

        if area < 5000:
            continue

        boxes.append(
            cv2.boundingRect(
                contour
            )
        )

    

    count = 0

    for (
        x,
        y,
        w,
        h
    ) in boxes:

        cv2.rectangle(
            source_marked,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            3
        )

        cv2.rectangle(
            target_marked,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            3
        )

        source_crop = img1[
            y:y+h,
            x:x+w
        ]

        target_crop = img2[
            y:y+h,
            x:x+w
        ]

        count += 1

        cv2.imwrite(
            f"screenshots/page_{page_num}_change_{count}_source.png",
            source_crop
        )

        cv2.imwrite(
            f"screenshots/page_{page_num}_change_{count}_target.png",
            target_crop
        )

    cv2.imwrite(
        f"screenshots/page_{page_num}_source_marked.png",
        source_marked
    )

    cv2.imwrite(
        f"screenshots/page_{page_num}_target_marked.png",
        target_marked
    )

    print(
        f"Page {page_num}: {count} merged regions"
    )

    return count
def clear_screenshots():

    if not os.path.exists("screenshots"):
        return

    for file in os.listdir("screenshots"):

        path = os.path.join(
            "screenshots",
            file
        )

        if os.path.isfile(path):
            os.remove(path)