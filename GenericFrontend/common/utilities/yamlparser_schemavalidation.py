import yaml
import jsonschema
import logging
from json import load

logger = logging.getLogger(__name__)


def yaml_parser_prelogin(yml):
    """Function for parsing Yaml File functionality."""
    data = {}  # assign
    with open(yml) as f:
        try:
            data = yaml.safe_load(f)
            logger.info(data)
        except yaml.YAMLError as exc:
            logger.info(exc)
            print('daphne', exc)
    return data


def schema_validation(data, path):
    """Function for validating Json Schema functionality."""
    schema = load(path)
    print(type(schema))
    v = jsonschema.Draft4Validator(schema)
    errors = sorted(v.iter_errors(data), key=lambda e: e.path)
    for error in errors:
        print(error.message)
        logger.info('json validation failed')
    logger.info('schema validation done')

