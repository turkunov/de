import json


def load_html(html_path: str) -> str:
    html_contents = None
    with open(html_path, 'r', encoding='utf-8') as f:
        html_contents = f.read()
    return html_contents


def load_json(config_path: str) -> dict:
    config_contents = None
    with open(config_path, 'r', encoding='utf-8') as f:
        config_contents = json.load(f)
    return config_contents