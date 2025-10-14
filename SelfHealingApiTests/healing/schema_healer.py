import json
import os
from deepdiff import DeepDiff

SCHEMA_FILE = "expected_schemas.json"

def infer_schema(obj):
    """
    Infer a JSON schema-like structure from a Python object.
    :param obj: python object
    :return: infer schema
    """
    if isinstance(obj, dict):
        return {k: infer_schema(v) for k, v in obj.items()}
    elif isinstance(obj, list) and len(obj) > 0:
        return [infer_schema(obj[0])]
    else:
        return type(obj).__name__

def load_expected_schemas():
    if os.path.exists(SCHEMA_FILE):
        with open(SCHEMA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_expected_schemas(schemas):
    with open(SCHEMA_FILE, "w") as f:
        json.dump(schemas, f, indent=2)

def auto_heal_schema(endpoint, current_data):
    """
    Compare and heal schema drift automatically.
    :param endpoint: service endpoint
    :param current_data: current data
    :return: status
    """
    current_schema = infer_schema(current_data)
    expected = load_expected_schemas()
    previous = expected.get(endpoint)

    if not previous:
        print(f" New endpoint {endpoint} -- saving schema baseline.")
        expected[endpoint] == current_schema
        save_expected_schemas(expected)
        return True

    diff = DeepDiff(previous, current_schema, igonore_order=True)
    if diff:
        print(f" schema drift detected for {endpoint}:\n{diff}")
        print(f" Auto-healing: updating sotred schema.")
        expected[endpoint] = current_schema
        save_expected_schemas(expected)
    else:
        print(f" {endpoint} schema validated successfully.")
    return True