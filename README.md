# Chromecast Radio
Chromecast Radio is a web application that allows you to play online radio/music streams on chromecast devices. You are not limited to radio streams though. Any online audio or video file can be played and casted with this application. This app allows you to control multiple chromecast devices from any device with a web browser. You can also select between any number of files to play and control the volume of the chromecast device.

## Downloads
Download and extract the [latest release](https://github.com/staudyy/chromecast-radio/releases) or clone this repository.

## Getting Started
1. **Get Chromecast Names**  
If you know the name of your chromecast you can skip this step (the name that appears in every application that supports cast.) If not navigate to ```/tools/find_chromecasts``` and run ```find_chromecasts.py```. This script will print all available chromecast names in the console. We will refer to these names as **"friendly names"**.

2. **Add Chromecasts**  
You have to add one or more chromecast devices to the database. To do this navigate to ```/tools/add_chromecasts``` and open the text file ```add_chromecasts.txt```. Add your new chromecast **"display names"** (the names that will be displayed in the web UI) and chromecast **friendly names** to ```add_chromecasts.txt``` separated by **linebreaks**.
Empty lines are ignored, but there **CANNOT** be any empty lines between the display name and friendly name of one chromecast. When the display name AND friendly name are identical to an existing chromecast, it will not be added again.  
After writing your names in the file, run ```dump.py``` to add these entries to the database. For any other editing (like removing a chromecast or changing the order) you have to manually edit the json file located at ```/data/chromecasts.json```

3. **First Test**  
Now you are ready to run the web application. Run ```runServer.bat``` and open ```127.0.0.1:6900``` in a web browser. The UI should load and become accessible. You can now select one of the added chromecasts and play the sample audio files.

4. **Adding stations**  
First off turn off the server. Then delete the file ```/data/channels.json``` If you want to keep the sample audio tracks, do not delete it. Next navigate to ```/tools/add_channels``` and open ```add_channels.txt``` Add your new **display channel names** and **urls** to ```add_channels.txt``` separated by **linebreaks**. Empty lines are ignored, but there **CANNOT** be any empty lines between the name and the url of one channel When the name AND url is identical to an existing channel, it will not be added again. Make sure that the url links directly to the ```.mp3``` file or any other media file.
After writing your channels in the file, run ```dump.py``` to add these entries to the database. For any other editing (like removing a channel or changing the order) you have to manually edit the json file located at ```/data/channels.json```

## Other Instructions
- If you want to change the port, edit ```runServer.bat``` and change ```6900``` to any valid port number.

## Dependencies
Install with ```pip install -r requirements.txt```
- [Flask](https://pypi.org/project/Flask/)
- [pychromecast](https://github.com/home-assistant-libs/pychromecast)