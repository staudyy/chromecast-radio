"""
---HOW TO USE---
Add your new channel names and urls to "add_channels.txt" separated by newlines.
Empty lines are ignored, but there cannot be any blank lines between the name and the url of one channel
When the name AND url is identical to an existing channel, it will not be added again
Example syntax:

24/7 Royalty Free Music
https://ec3.yesstreaming.net:3585/stream

Butterflies - Zane Little
https://files.freemusicarchive.org/storage-freemusicarchive-org/tracks/z4CDjchx1oLrTs1OjOtupGZpO0w9SilxK0o5ECiZ.mp3

C'est La Vie
https://files.freemusicarchive.org/storage-freemusicarchive-org/tracks/3RahChJRrtlnO9m1xoBAKPvuvxr6aR99sh4JIUwf.mp3
"""

import json
from pathlib import Path

INPUT_PATH = Path(__file__).parent/"add_channels.txt"
TARGET_PATH = Path(__file__).parent.parent.parent/"data"/"channels.json"

formatedChannels = []
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    newName = ""
    for line in f:
        line = line.rstrip()
        if line and not newName:
            newName = line
        elif newName:
            if not line:
                print(f'WARNING: Missing a link to "{newName}"')
                newName = ""
                continue
            formatedChannels.append({"name": newName, "url": line})
            newName = ""

print(formatedChannels)

channels = []
try:
    with open(TARGET_PATH, "r") as f:
        channels = json.load(f)
except:
    pass

for channel in formatedChannels:
    if channel not in channels:
        channels.append(channel)

with open(TARGET_PATH, "w") as f:
    json.dump(channels, f, indent=4)
