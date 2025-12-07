import uuid


def generate_filename(original_name: str) -> str:
    ext = original_name.split(".")[-1]
    return f"{uuid.uuid4().hex}.{ext}"
