"""
---HOW TO USE---
Add your new chromecast display names and chromecast "friendly names" to "add_chromecasts.txt" separated by newlines.
Empty lines are ignored, but there cannot be any blank lines between the display name and chromecast friendly name of one chromecast
When the display name AND chromecast "friendly name" is identical to an existing chromecast, it will not be added again.

You can find "friendly names" of available chromecasts by running find_chromecasts.py
Example syntax:

Chomecast 1
FRIENDLY NAME

Chomecast 2
OTHER FRIENDLY NAME
"""

import json
from pathlib import Path

INPUT_PATH = Path(__file__).parent/"add_chromecasts.txt"
TARGET_PATH = Path(__file__).parent.parent.parent/"data"/"chromecasts.json"

formatedChromecasts = []
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    newName = ""
    for line in f:
        line = line.rstrip()
        if line and not newName:
            newName = line
        elif newName:
            if not line:
                print(f'WARNING: Missing a friendly name to "{newName}"')
                newName = ""
                continue
            formatedChromecasts.append({"displayName": newName, "friendlyName": line})
            newName = ""

print(formatedChromecasts)

chromecasts = []
try:
    with open(TARGET_PATH, "r") as f:
        chromecasts = json.load(f)
except:
    pass

for chromecast in formatedChromecasts:
    if chromecast not in chromecasts:
        chromecasts.append(chromecast)

with open(TARGET_PATH, "w") as f:
    json.dump(chromecasts, f, indent=4)
    



