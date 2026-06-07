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

        text = summary.lower()

        stats["critical"] += text.count(
            "removed content"
        )

        stats["high"] += text.count(
            "added content"
        )

        stats["medium"] += text.count(
            "layout / reflow"
        )

        stats["low"] += text.count(
            "text integrity issues"
        )

    stats["total"] = (
        stats["critical"]
        + stats["high"]
        + stats["medium"]
        + stats["low"]
    )

    return stats