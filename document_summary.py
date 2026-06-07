from gemini_analyzer import model


def generate_document_summary(
    page_summaries
):

    combined_summary = ""

    for page_num in sorted(
        page_summaries.keys()
    ):

        combined_summary += (
            f"\n\nPAGE {page_num}\n"
        )

        combined_summary += (
            page_summaries[page_num]
        )

    prompt = f"""
You are a professional document auditor.
Rules:

- Never infer intent.
- Never infer strategy.
- Never infer editorial direction.
- Never infer author decisions.

- Report only observable findings.

- If evidence is insufficient:
  state:

  "Unable to determine intent from document changes."

- If content moved between pages:
  classify as:

  Relocated Content

- Do not classify moved content as both
  Added and Removed.
- Do not classify content as relocated unless the same text
  clearly appears in another page.

- If uncertain, classify separately as:
  Possible Relocation

- If text may be OCR damage:
  classify as:

  OCR / Extraction Uncertainty
Below are page-level comparison summaries.

Create a document-level executive summary.

Requirements:

1. Count major changes.
2. Group similar changes.
3. Ignore duplicate findings.
4. Highlight critical removals.
5. Highlight major additions.
6. Mention layout changes.
7. Mention text integrity issues separately.
8. Write in professional business language.

Rules:
- Never assume content was relocated.

- Only classify content as "Relocated Content"
  if the same text clearly appears
  in another location.

- If evidence is insufficient:

  Use:

  Possible Relocation

  instead of

  Relocated Content

- Do not infer document intent.

- Do not infer author decisions.

- Do not infer editorial strategy.

- Report only observable changes.
If content appears to move from one page
to another page:

Do NOT report it as both
Added and Removed.

Report it as:
Relocated Content
Also generate:

Change Statistics

Critical:
High:
Medium:
Low:
Additional Rules:

- Never infer business intent.
- Never infer editorial decisions.
- Never infer strategic direction.
- Never infer author motivations.
- Report only observable changes.
- If evidence is insufficient, state:
  "Unable to determine intent from document changes."

Return format:

Executive Summary

Pages Compared:
...

Major Changes:
...

Text Integrity Issues:
...

Business Impact Rules:

- Never speculate.

- Never infer intent.

- Never infer consequences.

- Report only evidence.

- If impact is not explicitly visible:

  Output:

  Business Impact:

  Unable to determine impact
  from observable document changes.

PAGE SUMMARIES:

{combined_summary}
"""

    response = model.generate_content(
        prompt
    )

    return response.text