import json
import os
from typing import Optional


DB_FILE_PATH: str = f"{os.path.dirname(__file__)}/../users-db.json"


def read_item(item_id: str) -> Optional[dict]:
    with open(DB_FILE_PATH) as file:
        items: dict = json.loads(file.read())
        return items.get(item_id)


def save_item(item: dict):
    with open(DB_FILE_PATH, "r+") as file:
        items: dict = json.loads(file.read())
        items[item["id"]] = item
        file.seek(0)
        json.dump(items, file)


def delete_item(item_id: str):
    with open(DB_FILE_PATH, "r+") as file:
        items: dict = json.loads(file.read())
        items.pop(item_id, None)
        file.seek(0)
        json.dump(items, file)
