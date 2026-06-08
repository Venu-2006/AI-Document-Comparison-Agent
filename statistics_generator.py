import re

def calculate_statistics(
    page_summaries
):

    stats = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for summary in page_summaries.values():

        stats["critical"] += len(
            re.findall(
                r"Removed Content:",
                summary
            )
        )

        stats["high"] += len(
            re.findall(
                r"Added Content:",
                summary
            )
        )

        stats["medium"] += len(
            re.findall(
                r"Modified Content:",
                summary
            )
        )

        stats["low"] += len(
            re.findall(
                r"Text Integrity",
                summary
            )
        )

    stats["total"] = sum(
        stats.values()
    )

    return stats
