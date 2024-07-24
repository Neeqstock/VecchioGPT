def fix_codeblocks(text):
    """
    Removes markdown code blocks delimiters from the input text.
    """
    result = []
    for line in text.splitlines():
        if not line.startswith("```"):
            result.append(line)
    return "\n".join(result)
