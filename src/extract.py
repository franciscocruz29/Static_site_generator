def extract_title(markdown):
    for line in markdown.split("\n"):
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            return stripped_line[2:]
        raise Exception("No title heading found in markdown")
