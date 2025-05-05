def flatten_candidate_for_embedding(candidate) -> str:
    lines = [
        candidate.name,
        f"Email: {candidate.email}",
        f"Phone: {candidate.phone}",
        f"Location: {candidate.location}",
        "Skills: " + ", ".join(candidate.skills or []),
    ]

    # Handle certifications as list of strings or dicts
    certifications = candidate.certifications or []
    cert_line = "Certifications: " + ", ".join(
        cert if isinstance(cert, str)
        else f"{cert.get('certification') or cert.get('FINRA Licenses', 'Unknown')} ({cert.get('date') or cert.get('dates', 'Unknown')})"
        for cert in certifications
    )
    lines.append(cert_line)

    lines.append("Experience:")
    for exp in candidate.experience:
        resp = exp.responsibilities
        if isinstance(resp, list):
            resp = "; ".join(resp)
        lines.append(f"- {exp.title} at {exp.company}, {exp.dates} ({exp.location}) — {resp}")

    lines.append("Education:")
    education_items = candidate.education
    if isinstance(education_items, dict):
        education_items = [education_items]
    for edu in education_items:
        lines.append(f"- {edu.degree} in {edu.field}, {edu.school} ({edu.dates})")

    return "\n".join(lines)
