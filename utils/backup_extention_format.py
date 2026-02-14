

def get_format_extension(format_name: str) -> str:
    format_mapping = {
        "c": ".dump",
        "t": ".tar",
        "p": ".sql",
        "d": ""
    }
    ext = format_mapping.get(format_name)
    if ext is None:
        formats = ", ".join(format_mapping.keys())
        raise ValueError(f"Unsupported backup format: {format_name}. "
                         f"Supported formats are: {formats}.")
    return ext 