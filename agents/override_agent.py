def apply_override(score_data, new_score, reason):
    score_data["overridden_score"] = new_score
    score_data["override_reason"] = reason
    score_data["recommendation"] = (
        "Strong Hire" if new_score >= 80
        else "Consider" if new_score >= 60
        else "Reject"
    )

    return score_data