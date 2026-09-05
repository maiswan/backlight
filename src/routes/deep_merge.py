def deep_merge(source: dict, patch: dict) -> dict:
    merged = source.copy()
    for key, value in patch.items():
        if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged
