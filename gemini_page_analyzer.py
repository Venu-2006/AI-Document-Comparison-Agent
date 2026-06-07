from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


def analyze_page(
    source_page,
    target_page
):

    img1 = Image.open(source_page)
    img2 = Image.open(target_page)

    prompt = """
You are a professional document comparison analyst.

Compare these two pages.

Ignore:
- Highlight boxes
- Rendering differences
- OCR mistakes
- Small spacing shifts

Focus on:

1. Added content
2. Removed content
3. Modified content
4. Moved content
5. Layout-only changes

Explain clearly.

Format:

Page Summary

Added:
...

Removed:
...

Modified:
...

Layout:
...

Overall Impact:
...
"""

    response = model.generate_content(
        [
            prompt,
            img1,
            img2
        ]
    )

    return response.text