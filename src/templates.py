def resolve_placeholders(text: str, variables: dict[str, str]) -> str:
    resolved = text

    for placeholder, value in variables.items():
        if placeholder in text:
            resolved = resolved.replace(placeholder, value)
    
    return resolved