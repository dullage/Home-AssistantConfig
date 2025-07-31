#!/usr/bin/env python3

# This script takes the contents of voice_assistant_config.yaml and converts it into two configuration
# files, one for the HomeKit integration and one for the Google Assistant integration. This serves
# two purposes:
#
#     1. There is only one place to configure the entites for both integrations. This could be done
#        by "including" the same file but this gives me the flexibility to differ the two configurations
#        in the future if needed.
#
#     2. The source file is in a more user friendly format (i.e. the names are declared alongside the
#        included entites).

import yaml
from os import path

ROOT_DIR = "./"

CONFIG_FILE = path.join(ROOT_DIR, "voice_assistant_config.yaml")
GOOGLE_FILE = path.join(ROOT_DIR, "google.yaml")
SIRI_FILE = path.join(ROOT_DIR, "siri.yaml")

WARNING = "# THIS FILE IS AUTO GENERATED, DO NOT DIRECTLY EDIT. SEE: voice_assistant_config.py\n\n"  # noqa

GOOGLE_EXCLUDED_ENTITIES = ["camera.front_door"]
SIRI_EXCLUDED_ENTITIES = []


def write_config(file, warning, config):
    with open(file, "w") as file_content:
        file_content.write(
            warning + yaml.dump(config, default_flow_style=False)
        )


def convert_structure(config):
    """Convert the structure of the config to the required format."""
    return {
        "filter": {"include_entities": [entity for entity in config.keys()]},
        "entity_config": config,
    }


# Read Source
with open(CONFIG_FILE, "r") as config_file_contents:
    config = yaml.safe_load(config_file_contents)

# Google
google_config = {
    entity: entity_config
    for entity, entity_config in config.items()
    if entity not in GOOGLE_EXCLUDED_ENTITIES
}

# Siri
siri_config = {
    entity: entity_config
    for entity, entity_config in config.items()
    if entity not in SIRI_EXCLUDED_ENTITIES
}

# Write Targets
write_config(GOOGLE_FILE, WARNING, convert_structure(google_config))
write_config(SIRI_FILE, WARNING, convert_structure(siri_config))
