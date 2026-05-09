def sanitize_input(text):
    blocked_patterns = [
        "ignore previous instructions",
        "system prompt",
        "reveal api key",
        "execute code",
        "delete database"
    ]

    cleaned = text.lower()

    for pattern in blocked_patterns:
        if pattern in cleaned:
            raise ValueError("Potential unsafe input detected.")

    return text