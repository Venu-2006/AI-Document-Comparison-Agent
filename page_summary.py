import difflib
from PIL import Image
from gemini_analyzer import model


def _clip_text(text: str, limit: int = 6000) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated]..."


def _build_line_diff_notes(source_text: str, target_text: str, max_items: int = 12) -> str:
    source_lines = [line.strip() for line in source_text.splitlines() if line.strip()]
    target_lines = [line.strip() for line in target_text.splitlines() if line.strip()]

    diff = list(difflib.ndiff(source_lines, target_lines))

    removed = []
    added = []

    for item in diff:
        if item.startswith("- "):
            line = item[2:].strip()
            if line and line not in removed:
                removed.append(line)
        elif item.startswith("+ "):
            line = item[2:].strip()
            if line and line not in added:
                added.append(line)

        if len(removed) >= max_items and len(added) >= max_items:
            break

    parts = []

    if removed:
        parts.append(
            "Removed lines:\n" + "\n".join(f"- {x}" for x in removed[:max_items])
        )

    if added:
        parts.append(
            "Added lines:\n" + "\n".join(f"- {x}" for x in added[:max_items])
        )

    if not parts:
        return "No strong line-level text diff detected."

    return "\n\n".join(parts)


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
Rules:

- Never infer intent.
- Never infer strategy.
- Never infer business goals.
- Never infer user motivation.
- Never infer editorial decisions.

- Report only observable document changes.

- If content appears moved:
  classify as Relocated Content.

- Do not report moved content as both Added and Removed.

- If a word appears truncated:
  determine whether it is:

  1. Actual document change
  2. OCR extraction artifact

- If uncertain:
  classify as:

  OCR / Extraction Uncertainty

- Do not make assumptions beyond the evidence.

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

OCR SOURCE TEXT:
{_clip_text(source_text)}

OCR TARGET TEXT:
{_clip_text(target_text)}

OCR LINE DIFF NOTES:
{diff_notes}

Return this format exactly:

Page {page_number} Summary

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
- ...

Business Impact Rules:

- Report only observable document changes.

- Do not infer:
  * business consequences
  * user consequences
  * strategic intent
  * marketing impact
  * organizational impact

- Never speculate.

- If impact cannot be directly observed:

  Output exactly:

  Business Impact:

  Unable to determine impact
  from observable document changes.
"""

    response = model.generate_content([prompt, source_img, target_img])
    return response.text.strip()