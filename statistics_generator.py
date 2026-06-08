def calculate_statistics(page_summaries):

    stats = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for summary in page_summaries.values():

        text = summary.lower()

        # Critical
        if "removed content" in text:
            stats["critical"] += 1

        # High
        if "added content" in text:
            stats["high"] += 1

        # Medium
        if (
            "modified content" in text
            or "layout / reflow" in text
        ):
            stats["medium"] += 1

        # Low
        if (
            "text integrity issues" in text
            or "formatting" in text
            or "spacing" in text
        ):
            stats["low"] += 1

    stats["total"] = (
        stats["critical"]
        + stats["high"]
        + stats["medium"]
        + stats["low"]
    )

    return stats
