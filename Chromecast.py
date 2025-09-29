import pychromecast
from time import sleep, strftime


TIME_STR_FORMAT = "[%d/%m/%y %H:%M:%S]"


class Queue:
    def __init__(self):
        self.queue = []

    def addFunc(self, func, args):
        if self.queue and self.queue[-1] == func:
            return
        else:
            self.queue.append([func, args])

    def tryExecute(self):  # doesnt have check if execution fails
        if self.queue:
            sleep(0.05)
            print(strftime(TIME_STR_FORMAT), "EXECUTING FROM QUEUE")
            func = self.queue.pop(0)
            if func[1] is None:
                func[0]()
            else:
                func[0](*func[1])

    def not_empty(self):
        return bool(self.queue)


class Listener:
    def __init__(self, mediaFunc=None, connectionFunc=None):
        self.mediaFunc = mediaFunc
        self.connectionFunc = connectionFunc

    def new_media_status(self, data):
        if self.mediaFunc is not None:
            self.mediaFunc(data)

    def new_connection_status(self, data):
        if self.connectionFunc is not None:
            self.connectionFunc(data)
    
    def load_media_failed(self, item, error_code):
        raise Exception(f"Failed loading media stream, item:{item}, code:{error_code}")


class Chromecast:
    def __init__(self, device):
        self.device = device
        self.cast = None
        self.mc = None
        self.chromecasts = None
        self.browser = None
        self.url = None
        self.newUrl = False
        self.isProcessing = False
        self.turnBackOn = False
        self.expectedStatus = "UNKNOWN"
        self.commandQueue = Queue()
        self.listener = Listener(
            self.new_media_status_handler, self.new_connection_status_handler
        )
        # self.connect() AFTER DEBUG DONE CAN BE REACTIVATED

    # RANDOM FUNCTIONS
    def waitUntilTrue(self, variable, timeout, period):
        while not eval(variable) and timeout > 0:
            timeout -= period
            sleep(period)

    # LISTENER HANDLER
    def new_media_status_handler(self, data):
        print(strftime(TIME_STR_FORMAT), "NEW MEDIA STATUS: ", data.player_state)

    def new_connection_status_handler(self, data):
        print(strftime(TIME_STR_FORMAT), "NEW CONNECTION STATUS: ", data)

        # Turn back on after disconnect
        if self.cast is not None:
            if self.turnBackOn and data.status == "CONNECTED":
                self.turnBackOn = False
                self.connect()
                self.play()

        if data.status == "LOST" and self.expectedStatus == "PLAYING":
            self.turnBackOn = True

    # CHROMECAST
    def connect(self, tries=0):
        if self.isProcessing:
            return

        self.processing(True)
        try:
            self.disconnect()
        except:
            print(strftime(TIME_STR_FORMAT), "Disconnect unsuccessful (or first connection)")
        chromecasts, self.browser = pychromecast.get_listed_chromecasts(
            friendly_names=[self.device]
        )
        #print(chromecasts)
        if not chromecasts:
            print(strftime(TIME_STR_FORMAT), f'No chromecast with name "{self.device}" discovered {tries + 1}')
            tries += 1
            if tries > 5:
                self.processing(False)
                return
            self.processing(False)
            self.connect(tries=tries)
            return

        self.cast = chromecasts[0]
        self.cast.wait()
        print(strftime(TIME_STR_FORMAT), "Chromecast ready")
        self.mc = self.cast.media_controller
        self.cast.socket_client.register_connection_listener(self.listener)
        self.mc.register_status_listener(self.listener)
        self.processing(False)

    def setMedia(self):
        if self.isProcessing:
            return

        if self.checkConnection() and self.url is not None:
            self.processing(True)
            self.newUrl = False

            self.mc.play_media(
                self.url, "audio/mp3", stream_type="LIVE", autoplay=False
            )
            self.mc.block_until_active()
            print(strftime(TIME_STR_FORMAT), "Trying to play: ", self.url)

            if self.mc.status.player_is_paused:
                self.waitUntilTrue("self.mc.status.player_is_idle", 15, 0.01)

            self.waitUntilTrue("self.mc.status.player_is_paused", 30, 0.01)
            print(strftime(TIME_STR_FORMAT), "Unblocked thread")
            self.processing(False)

    def processing(self, bool):
        if bool:
            self.isProcessing = True
        else:
            self.isProcessing = False

    def checkConnection(self):
        if self.cast is None:
            self.connect()
            if self.cast is None:
                return False

        if self.cast.socket_client.is_stopped:
            print(strftime(TIME_STR_FORMAT), "No chromecast connected, trying to connect")
            self.connect()
            if self.cast.socket_client.is_stopped:
                print(strftime(TIME_STR_FORMAT), "Connection unsuccessful")
                return False
        return True

    def checkMedia(self):
        if self.mc is None:
            return False

        print(strftime(TIME_STR_FORMAT), "Current state", self.mc.status.player_state)
        if (
            self.mc.status.player_state == "UNKNOWN"
            or self.mc.status.player_is_idle
            or self.newUrl
        ):
            print(strftime(TIME_STR_FORMAT), "No or new media, setting up")
            self.setMedia()
            if self.mc.status.player_state == "UNKNOWN":
                print(strftime(TIME_STR_FORMAT), "Media setup unsuccessful")
                return False
        return True

    def checkProcessing(self, command=None, args=None):
        if self.isProcessing:
            if command is not None:
                self.commandQueue.addFunc(command, args)
            return True
        return False

    def checkAll(self, command=None, args=None):
        processing = self.checkProcessing(command, args)
        if processing:
            return False

        return self.checkConnection() and self.checkMedia()

    def setUrl(self, url):
        if self.url != url:
            self.url = url
            self.newUrl = True

    # chromecast control functions
    def pause(self):
        if self.checkAll(self.pause):
            #print("pausing")
            self.mc.pause()
            self.expectedStatus = "PAUSED"
            self.commandQueue.tryExecute()
        return True

    def play(self):
        self.newUrl = True  # to always set new media and so radio is live
        if self.checkAll(self.play):
            self.mc.play()
            self.expectedStatus = "PLAYING"
            self.commandQueue.tryExecute()
        return True  # TODO temporary solution, mozno by sa zislo aj false vratit dakedy (aj pri volume a pause)

    def stop(self):
        if self.checkAll(self.stop):
            self.mc.stop()
            self.expectedStatus = "IDLE"
            self.commandQueue.tryExecute()

    def setVolume(self, value):
        if self.checkAll(self.setVolume, (value,)):
            # asi do queue treba pridat (zapnutie a hned zmenenie volume) (idk asi done)
            self.cast.set_volume(value / 100)
            self.commandQueue.tryExecute()
            # after disconnect doesnt resume playback (not implemented)
        return True
        

    def disconnect(self):
        self.cast.disconnect()

    def connectNew(self):
        self.connect()

    def is_playing(self):
        if self.checkConnection():
            self.waitUntilTrue('self.mc.status.player_state != "UNKNOWN"', 2, 0.01)
            if self.mc.status.player_is_playing:
                return True
        return False

    def get_url(self):
        return self.url

    def get_volume(self):
        if self.checkConnection():
            return self.cast.status.volume_level
        return -1
