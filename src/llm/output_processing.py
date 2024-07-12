import re

# Pipable


def pipable__extract_query(text):
    pattern = re.compile(r"<sql>\s*(.*?)\s*</sql>", re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    else:
        return "select 'Query not generated'"


def pipable__extract_answer(text):
    return text.split("Answer:")[-1].split("\n")[0]


def get_extractors(model_type):
    if model_type == "pipable":
        return pipable__extract_query, pipable__extract_answer
    elif model_type == "google":
        return lambda text: text, lambda text: text
    else:
        return lambda text: text, lambda text: text
