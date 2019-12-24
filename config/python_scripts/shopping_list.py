import json
import os
import sys

import requests
import yaml

CONFIG_PATH = "/config"

SHOPPING_LIST_FILE = os.path.join(CONFIG_PATH, ".shopping_list.json")
SECRETS_FILE = os.path.join(CONFIG_PATH, "secrets.yaml")
VALID_MODES = ("ENTER", "EXIT", "CLEAR")

# Get the mode from arguments
MODE = sys.argv[1]
if MODE not in VALID_MODES:
    exit(1)


def load_shopping_list():
    with open(SHOPPING_LIST_FILE, "r") as file:
        return json.load(file)


def get_incomplete_item_list():
    shopping_list = load_shopping_list()

    shopping_list_items = []
    for item in shopping_list:
        if not item["complete"]:
            shopping_list_items.append(item["name"].title())

    return shopping_list_items


def get_secrets():
    with open(SECRETS_FILE, "r") as file:
        return yaml.load(file)


secrets = get_secrets()
auth_header = {
    "content-type": "application/json",
    "Authorization": "Bearer {}".format(secrets["shopping_list_script_token"]),
}


def send_notification(notify_entity, data):
    requests.post(
        "{}/api/services/notify/{}".format(
            secrets["shopping_list_base_url"], NOTIFY_ENTITY
        ),
        headers=auth_header,
        data=json.dumps(data),
    )


def complete_item(item_name):
    data = {"name": item_name}

    requests.post(
        "{}/api/services/shopping_list/complete_item".format(
            secrets["shopping_list_base_url"]
        ),
        headers=auth_header,
        data=json.dumps(data),
    )


if MODE == "CLEAR":
    shopping_list = load_shopping_list()
    for item in shopping_list:
        complete_item(item["name"])
    exit(0)

if MODE == "ENTER":
    NOTIFY_ENTITY = sys.argv[2]
    incomplete_items = get_incomplete_item_list()

    if incomplete_items:
        data = {"message": "Shopping List:\n" + "\n".join(incomplete_items)}
        send_notification(NOTIFY_ENTITY, data)
    exit(0)

if MODE == "EXIT":
    NOTIFY_ENTITY = sys.argv[2]
    incomplete_items = get_incomplete_item_list()

    if incomplete_items:
        data = {
            "message": "Do you want to clear the shopping list?",
            "data": {"push": {"category": "clear_shopping_list"}},
        }
        send_notification(NOTIFY_ENTITY, data)
    exit(0)
