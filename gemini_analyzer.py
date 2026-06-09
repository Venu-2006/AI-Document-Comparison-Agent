import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash-latest"
)


def analyze_page(
    source_page,
    target_page
):

    print(
        f"Analyzing page: {source_page}"
    )

    source_img = Image.open(
        source_page
    )

    target_img = Image.open(
        target_page
    )

    prompt = """
You are a professional document comparison analyst.

A difference has already been detected
between SOURCE and TARGET.

Your task is to explain the detected difference.

Rules:

- Focus only on observable evidence.
- Do not speculate.
- Do not infer intent.
- Do not infer business impact.
- Do not infer reasons for changes.
- Report only what is visibly different.

IMPORTANT:
Ignore punctuation-only changes unless
they alter the meaning of the sentence.
A change definitely exists.

Do NOT determine whether a change exists.

Your job is to describe the change.

Analyze:

1. Text changes
2. Image changes
3. Logo changes
4. Diagram changes
5. Chart changes
6. Signature changes
7. Stamp changes
8. Icon changes
9. Formatting changes
10. Layout changes
11. Position changes

For visual changes:

- Identify if an image was added.
- Identify if an image was removed.
- Identify if an image was modified.
- Identify if a logo changed.
- Identify if a chart changed.
- Identify if a diagram changed.
- Identify if a signature changed.
- Identify if a stamp changed.

IMPORTANT PRIORITY ORDER

Always report the most significant change first.

Priority:

1. Text Added
2. Text Removed
3. Text Modified
4. Image Added
5. Image Removed
6. Image Modified
7. Logo Changed
8. Diagram Changed
9. Chart Changed
10. Structural/Layout Changes
11. Formatting Changes
12. Alignment Changes
13. Spacing Changes
14. Pixel-only Differences

If meaningful text changes exist:

- Do NOT report spacing changes.
- Do NOT report punctuation changes.
- Do NOT report alignment changes.

Only report those if no meaningful content change exists.

OCR UNCERTAINTY RULES

If text appears truncated,
partially recognized,
or potentially corrupted:

Report:

OCR / Extraction Uncertainty

Do NOT automatically classify it as
a document change.

Examples:

domains → domai
learners → lents

may be OCR uncertainty.

Output Format:

Type:
Description:
Location:
Impact:

Impact must describe only the
observable effect on document content.

Do NOT describe business impact.
Do NOT speculate.
"""

    response = model.generate_content(
        [
            prompt,
            source_img,
            target_img
        ]
    )

    return response.text
