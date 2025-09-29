import json
from flask import Flask, request, render_template
from pathlib import Path

from Chromecast import Chromecast


CHANNELS_PATH = Path(__file__).parent/"data"/"channels.json"
CHROMECASTS_PATH = Path(__file__).parent/"data"/"chromecasts.json"

# FLASK
app = Flask("ChromecastRadio")

# SETUP
chromecasts = {}
chromecast_list = []
with open(CHROMECASTS_PATH, "r") as f:
    chromecast_list = json.load(f)
    for chromecast in chromecast_list:
        chromecasts[chromecast["friendlyName"]] = Chromecast(chromecast["friendlyName"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chromecast", methods=["POST"])
def ajax():
    outputData = []
    
    castRequest = request.json.pop(0)
    if castRequest["action"] == "chromecast":
        chromecast = chromecasts[castRequest["value"]]
    else:
        return "NO CHROMECAST DEFINED"

    for req in request.json:
        action = req["action"]
        print(f"Command received: {action}")
        
        if action == "play":
            if chromecast.play():
                outputData.append("Play success")

        elif action == "url":
            chromecast.setUrl(req["value"])

        elif action == "pause":
            if chromecast.pause():
                outputData.append("Pause success")

        elif action == "stop":
            chromecast.stop()

        elif action == "volume":
            if chromecast.setVolume(float(req["value"])):
                outputData.append("Volume success")

        elif action == "disconnect":
            chromecast.disconnect()

        elif action == "connect":
            chromecast.connectNew()

        else:
            outputData.append("BAD DATA")

    print("")
    return outputData


@app.route("/getChannels", methods=["GET"])
def getChannels():
    with open(CHANNELS_PATH) as f:
        channels = json.load(f)
    return channels

@app.route("/getChromecasts", methods=["GET"])
def getChromecasts():
    return chromecast_list

@app.route("/setup", methods=["POST"])
def setup():
    try:
        chromecast = chromecasts[request.json["chromecast"]]
    except:
        return "NO CHROMECAST DEFINED"
    data = {
        "is_playing": chromecast.is_playing(),
        "url": chromecast.get_url(),
        "volume": round(chromecast.get_volume() * 100),
    }
    return data
