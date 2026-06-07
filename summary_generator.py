def generate_summary(diff):

    removed = []
    added = []

    for item in diff:

        item = item.strip()

        if item.startswith("- "):

            word = item[2:].strip()

            if len(word) > 1:
                removed.append(word)

        elif item.startswith("+ "):

            word = item[2:].strip()

            # Ignore OCR garbage like > , | , _
            if (
                len(word) > 2
                and word.replace(".", "").isalnum()
            ):
                added.append(word)

    if removed and not added:

        return (
            "Text removed: "
            + ", ".join(removed)
        )

    elif added and not removed:

        return (
            "Text added: "
            + ", ".join(added)
        )

    elif removed and added:

        return (
            "Text changed.\n"
            f"Removed: {', '.join(removed)}\n"
            f"Added: {', '.join(added)}"
        )

    return "Visual change detected."