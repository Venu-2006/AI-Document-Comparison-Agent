from compare_engine import *
from page_text_extractor import extract_page_text
from page_summary import generate_page_summary
from gemini_region_analyzer import analyze_region
from document_summary import generate_document_summary

import os
from PIL import Image
def run_comparison():

    results = []
    page_summaries = {}
    page_region_counts = {}

    source_pages = sorted(
        os.listdir("source_pages")
    )

    target_pages = sorted(
        os.listdir("target_pages")
    )

    scores = []

    total_pages = min(
        len(source_pages),
        len(target_pages)
    )

    # ==========================
    # Compare Pages
    # ==========================

    for page_num in range(total_pages):

        source_img = os.path.join(
            "source_pages",
            source_pages[page_num]
        )

        target_img = os.path.join(
            "target_pages",
            target_pages[page_num]
        )

        (
            contours,
            img1,
            img2,
            diff,
            score
        ) = compare_pages(
            source_img,
            target_img
        )

        scores.append(score)

        region_count = save_changes(
            contours,
            img1,
            img2,
            diff,
            page_num + 1
        )

        page_region_counts[
            page_num + 1
        ] = region_count

    # ==========================
    # Generate AI Summaries
    # ==========================

    for page_num in range(total_pages):

        page_no = page_num + 1

        source_original = (
            f"screenshots/page_{page_no}_source_original.png"
        )

        target_original = (
            f"screenshots/page_{page_no}_target_original.png"
        )

        source_marked = (
            f"screenshots/page_{page_no}_source_marked.png"
        )

        target_marked = (
            f"screenshots/page_{page_no}_target_marked.png"
        )

        if not (
            os.path.exists(source_original)
            and
            os.path.exists(target_original)
        ):
            continue

        try:

            source_text = extract_page_text(
                source_original
            )

            target_text = extract_page_text(
                target_original
            )

            summary = generate_page_summary(
                page_number=page_no,
                source_image_path=source_original,
                target_image_path=target_original,
                source_text=source_text,
                target_text=target_text,
                visual_region_count=page_region_counts.get(
                    page_no,
                    0
                )
            )

            # ==========================
            # Visual Region Analysis
            # ==========================

            region_summary = ""

            region_count = page_region_counts.get(
                page_no,
                0
            )

            for region in range(
                1,
                region_count + 1
            ):

                source_crop = (
                    f"screenshots/page_{page_no}_change_{region}_source.png"
                )

                target_crop = (
                    f"screenshots/page_{page_no}_change_{region}_target.png"
                )

                if (
                    os.path.exists(source_crop)
                    and
                    os.path.exists(target_crop)
                ):

                    try:

                        source_crop_text = extract_page_text(
                        source_crop
)

                        target_crop_text = extract_page_text(
                      target_crop
                        )

                        source_len = len(
                            source_crop_text.strip()
                        )
                        
                        target_len = len(
                            target_crop_text.strip()
                        )
                        
                        crop_width, crop_height = Image.open(
                            source_crop
                        ).size
                        
                        crop_area = (
                            crop_width
                            * crop_height
                        )
                        
                        # Large region (likely image/diagram)
                        
                        if crop_area > 150000:
                        
                            region_analysis = analyze_region(
                                source_crop,
                                target_crop
                            )
                        
                        # Large text block
                        
                        elif (
                            source_len > 20
                            and
                            target_len > 20
                        ):
                        
                            region_analysis = (
                                "Type: Layout Reflow / Text Change\n\n"
                                "Description: The detected region "
                                "contains primarily textual content. "
                                "The difference appears to be caused "
                                "by text insertion, removal, or "
                                "paragraph reflow.\n\n"
                                "Severity: Medium"
                            )
                        
                        # Small text edit
                        
                        elif (
                            source_len > 5
                            or
                            target_len > 5
                        ):
                        
                            region_analysis = (
                                "Type: Text Change\n\n"
                                "Description: A textual modification "
                                "was detected in this region.\n\n"
                                "Severity: Low"
                            )
                        
                        # Real visual comparison
                        
                        else:
                        
                            region_analysis = analyze_region(
                                source_crop,
                                target_crop
                            )

                        # Confidence estimation

                        if "Image Modified" in region_analysis:
                            confidence = 95
                        
                        elif "Text Change" in region_analysis:
                            confidence = 90
                        
                        elif "Layout Reflow" in region_analysis:
                            confidence = 85
                        
                        else:
                            confidence = 80
                        
                        region_summary += (
                            f"\n\nVisual Change {region}\n"
                            f"Confidence: {confidence}%\n\n"
                            f"{region_analysis}"
                        )

                    except Exception as e:

                        region_summary += (
                            f"\n\nVisual Change {region}\n"
                            f"Gemini Region Error: {str(e)}"
                        )

            full_summary = (
                summary
                + "\n\n"
                + region_summary
            )

            
            page_summaries[
                page_no
            ] = full_summary

        except Exception as e:

            full_summary = (
                f"Gemini Error: {str(e)}"
            )

            page_summaries[
                page_no
            ] = full_summary

        results.append({

            "page": page_no,

            "regions": page_region_counts.get(
                page_no,
                0
            ),

            "source": source_marked,

            "target": target_marked,

            "summary": page_summaries[
                page_no
            ]

        })

    avg_score = (
        sum(scores) / len(scores)
        if scores
        else 0
    )

    document_summary = (
        generate_document_summary(
            page_summaries
        )
    )

    return (

        results,

        avg_score,

        page_summaries,

        document_summary

    )
