from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from datetime import datetime
from zoneinfo import ZoneInfo
import os


def generate_pdf_report(
    similarity_score,
    executive_summary,
    page_summaries,
    source_name,
    target_name,
    stats
):

    pdf_path = "Comparison_Report.pdf"

    doc = SimpleDocTemplate(
        pdf_path
    )

    styles = getSampleStyleSheet()

    content = []

    generated_time = datetime.now(
    ZoneInfo("Asia/Kolkata")
    ).strftime(
    "%d-%b-%Y %H:%M:%S IST"
    )
    # ==========================================
    # REPORT HEADER
    # ==========================================

    content.append(
        Paragraph(
            "AI Document Comparison Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"<b>Generated On:</b> {generated_time}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Source Document:</b> {source_name}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Target Document:</b> {target_name}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Pages Compared:</b> {len(page_summaries)}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Similarity Score:</b> {similarity_score:.4f}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ==========================================
    # CHANGE STATISTICS
    # ==========================================

    content.append(
        Paragraph(
            "Change Statistics",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
        f"""
        Critical Changes: {stats['critical']}<br/>
        High Changes: {stats['high']}<br/>
        Medium Changes: {stats['medium']}<br/>
        Low Changes: {stats['low']}<br/>
        Total Changes: {stats['total']}
        """,
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    content.append(
        Paragraph(
            "Executive Summary",
            styles["Heading1"]
        )
    )

    content.append(
        Spacer(1, 10)
    )

    clean_summary = executive_summary

    if clean_summary.startswith(
        "Executive Summary"
    ):
        clean_summary = clean_summary.replace(
            "Executive Summary",
            "",
            1
        ).strip()

    content.append(
        Paragraph(
            clean_summary.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    content.append(
        PageBreak()
    )

    # ==========================================
    # PAGE SUMMARIES
    # ==========================================

    for page_num in sorted(
        page_summaries.keys()
    ):

        content.append(
            Paragraph(
                f"Page {page_num} Summary",
                styles["Heading1"]
            )
        )

        page_text = page_summaries[
            page_num
        ]

        if page_text.startswith(
            f"Page {page_num} Summary"
        ):
            page_text = page_text.replace(
                f"Page {page_num} Summary",
                "",
                1
            ).strip()

        content.append(
            Paragraph(
                page_text.replace(
                    "\n",
                    "<br/>"
                ),
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

        source_img = (
            f"screenshots/page_{page_num}_source_marked.png"
        )

        target_img = (
            f"screenshots/page_{page_num}_target_marked.png"
        )

        if os.path.exists(
            source_img
        ):

            content.append(
                Paragraph(
                    "Source Marked",
                    styles["Heading3"]
                )
            )

            content.append(
                Image(
                    source_img,
                    width=250,
                    height=350
                )
            )

        if os.path.exists(
            target_img
        ):

            content.append(
                Paragraph(
                    "Target Marked",
                    styles["Heading3"]
                )
            )

            content.append(
                Image(
                    target_img,
                    width=250,
                    height=350
                )
            )

        content.append(
            PageBreak()
        )

    doc.build(
        content
    )

    return pdf_path
