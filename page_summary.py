import difflib
from PIL import Image
from gemini_analyzer import model


def _clip_text(text: str, limit: int = 6000) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated]..."
def is_noise(text: str) -> bool:

    text = text.strip()

    if not text:
        return True

    # Very short fragments
    if len(text) < 5:
        return True

    # Count alphabetic characters
    alpha_count = sum(
        c.isalpha()
        for c in text
    )

    if alpha_count < 3:
        return True

    return False

def _build_line_diff_notes(
    source_text: str,
    target_text: str,
    max_items: int = 12
) -> str:

    source_lines = [
        line.strip()
        for line in source_text.splitlines()
        if line.strip()
    ]

    target_lines = [
        line.strip()
        for line in target_text.splitlines()
        if line.strip()
    ]

    diff = list(
        difflib.ndiff(
            source_lines,
            target_lines
        )
    )
    removed_words, added_words = detect_word_changes(
    source_text,
    target_text
)

    removed = []
    added = []

    for item in diff:

        if item.startswith("- "):

            line = item[2:].strip()

            if (
                line
                and
                not is_noise(line)
                and
                line not in removed
            ):
                removed.append(line)

        elif item.startswith("+ "):

            line = item[2:].strip()

            if (
                line
                and
                not is_noise(line)
                and
                line not in added
            ):
                added.append(line)

        if (
            len(removed) >= max_items
            and
            len(added) >= max_items
        ):
            break

    parts = []

    if removed:

        parts.append(
            "Removed lines:\n"
            + "\n".join(
                f"- {x}"
                for x in removed[:max_items]
            )
        )

    if added:

        parts.append(
            "Added lines:\n"
            + "\n".join(
                f"- {x}"
                for x in added[:max_items]
            )
        )

    if not parts:

        return (
            "No meaningful OCR text changes detected."
        )

    return "\n\n".join(parts)
def detect_word_changes(
    source_text,
    target_text
):

    source_words = source_text.split()
    target_words = target_text.split()

    diff = list(
        difflib.ndiff(
            source_words,
            target_words
        )
    )

    removed = []
    added = []

    for item in diff:

        if item.startswith("- "):
            removed.append(item[2:])

        elif item.startswith("+ "):
            added.append(item[2:])

    return removed[:20], added[:20]
def generate_page_summary(
    page_number: int,
    source_image_path: str,
    target_image_path: str,
    source_text: str,
    target_text: str,
    visual_region_count: int
) -> str:

    source_img = Image.open(source_image_path)
    target_img = Image.open(target_image_path)

    diff_notes = _build_line_diff_notes(source_text, target_text)

    prompt = f"""
You are a senior document comparison analyst.

STRICT RULES

Report only observable document changes.

Do NOT infer:

- intent
- purpose
- strategy
- business goals
- user motivation
- editorial decisions
- business impact

OCR NOISE RULES

Ignore completely:

- isolated symbols
- OCR fragments
- clipped characters
- random character strings

Examples:

ae,
+
:
~ s #4
ye”

Do not report them under:

- Added Content
- Removed Content
- Modified Content

VISUAL PRIORITY RULE

If a major image replacement,
diagram replacement,
workflow replacement,
chart replacement,
logo replacement,
or screenshot replacement exists:

Prioritize the visual change.

Do not allow OCR artifacts
to dominate the report.

Page number: {page_number}
Visual regions detected by SSIM: {visual_region_count}

You are given:
1. Source page image
2. Target page image
3. OCR text extracted from both pages
4. A compact line-level OCR diff

Rules:
- Use the OCR text as the primary source of truth.
- Use the images to confirm layout, formatting, alignment, and reflow.
- Do NOT invent replacements between unrelated lines or list items.
- If text moved because content above was removed, report it as Layout / Reflow.
- If text is actually removed or added, report that first.
- If only punctuation, spacing, or font style changed, report that only when no stronger content change exists.
- Do not ignore truncated words, clipped line endings, or partial OCR text.
- Report those under a separate section called "Text Integrity Issues".
- Keep the summary concise but complete.
- Modernize the wording so the summary is useful and not vague.
If added or removed text is shorter than 5 characters
or contains mostly symbols,
classify it only under:
OCR / Extraction Uncertainty
Do NOT place it under
Added Content
or
Removed Content.

OCR SOURCE TEXT:
{_clip_text(source_text)}

OCR TARGET TEXT:
{_clip_text(target_text)}

OCR LINE DIFF NOTES:
{diff_notes}

WORD LEVEL CHANGES:

Removed Words:
{removed_words}

Added Words:
{added_words}
Return this format exactly:

Page {page_number} Summary

Severity:
- Critical | High | Medium | Low

Added Content:
- ...

Removed Content:
- ...

Modified Content:
- ...

Layout / Reflow:
- ...

Formatting / Spacing:
- ...

Text Integrity Issues:
- None

Observable Effect:
- ...

Rules:

If no findings exist:

Output:

None

Do not speculate.
Keep descriptions concise.
"""

    response = model.generate_content([prompt, source_img, target_img])
    return response.text.strip()
