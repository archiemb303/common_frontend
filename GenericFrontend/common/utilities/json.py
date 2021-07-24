import json
from pathlib import Path


def load(schema_path):
    """
    :param schema_path:
    :return:
    """
    schema = Path(schema_path)

    with schema.open() as f:
        return json.load(f)
