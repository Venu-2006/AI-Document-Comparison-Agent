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
You are a professional visual document analyst.

A visual difference has already been detected.

IMPORTANT:

Do not determine whether a change exists.

Assume a change exists.

Analyze BOTH images visually.

Do not rely only on OCR text.

Identify:

1. Image Added
2. Image Removed
3. Image Modified
4. Photograph Changed
5. Diagram Changed
6. Workflow Changed
7. Chart Changed
8. Logo Changed
9. Screenshot Changed
10. Graphic Changed

Examples:

Bird photo → Workflow diagram

Report:

Type: Image Modified

Description:
A bird photograph was replaced
by a workflow/process diagram.

Observable Effect:

*IMPORTANT*
Do not infer:
- purpose
- intent
- meaning
- business impact
- user impact
- informational significance

Only describe visible differences.
Describe only observable differences.

Output Format:

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
