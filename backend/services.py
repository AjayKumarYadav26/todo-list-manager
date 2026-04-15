def normalize_tags(tags):
    if not tags:
        return []
    if isinstance(tags, str):
        tags = [tags]
    normalized = []
    seen = set()
    for tag in tags:
        value = str(tag).strip().lower()
        if value and value not in seen:
            seen.add(value)
            normalized.append(value)
    return normalized


def get_popular_tags(todos):
    counts = {}
    for todo in todos:
        for tag in todo.get('tags', []) or []:
            normalized = str(tag).strip().lower()
            if not normalized:
                continue
            counts[normalized] = counts.get(normalized, 0) + 1
    return [{'tag': tag, 'count': count} for tag, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]
