from PIL import Image
from gemini_analyzer import model


def analyze_region(
    source_image,
    target_image
):

    print(
        f"Analyzing region: {source_image}"
    )

    img1 = Image.open(
        source_image
    )

    img2 = Image.open(
        target_image
    )

    prompt = """
You are a forensic document comparison expert.

A visual difference has already been detected.

Do NOT determine whether a difference exists.

Explain the difference.

Priority:

1. Text Added
2. Text Removed
3. Text Modified
4. Layout Change
5. Formatting Change
6. Alignment Change
7. Spacing Change

Output:

Type:
Description:
Impact:
"""

    response = model.generate_content(
        [
            prompt,
            img1,
            img2
        ]
    )

    return response.text