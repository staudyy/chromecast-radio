'''
This script tries to find all available chromecast devices and prints their friendly names to the console.
'''

import time
import pychromecast
import zeroconf

# Create a browser which prints the friendly name of found chromecast devices
zconf = zeroconf.Zeroconf()
browser = pychromecast.CastBrowser(pychromecast.SimpleCastListener(lambda uuid, service: print(browser.devices[uuid].friendly_name)), zconf)
browser.start_discovery()
# Shut down discovery
time.sleep(10)
pychromecast.discovery.stop_discovery(browser)