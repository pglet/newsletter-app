from dataclasses import dataclass, field
from typing import Dict, List
import json

settings_path = "newsletters/config.json"

@dataclass
class Settings():
    mailgunApiKey: str

def load():
    j = '{ "mailgunApiKey": "123!" }'
    j_dict = json.loads(j)
    return Settings(**j_dict)

def save(config):
    print("Saving settings")