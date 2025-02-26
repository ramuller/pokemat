import requests
import logging
import threading
import time
import sys
import os
import signal
from datetime import datetime
from time import sleep
import random
import math
from ansible_collections.community.aws.plugins.modules import stepfunctions_state_machine
import matplotlib.pyplot as plt

log = logging.getLogger("pokelib")

class ExPokeLibError(Exception):
    """Custom exception class."""
    pass

class ExPokeLibFatal(Exception):
    """ Somthing fatal should not be ignored """
    pass

class WatchDog():
    def __init__(self, time_out, _callback = None):
        self.next_t = time.time()
        self.i = time_out
        self.done = False
        self.time_out = time_out
        self.callback = _callback
        self._run()

    def _run(self):
        print("WATCHDOG hello {}, done {}".format(self.i,self.done))
        self.next_t-=1
        self.i-=1
        time.sleep(1)
        if self.i < 0:
            print("WATCHDOG callback ")
            self.callback()
        if not self.done:
            # print("WATCHDOG  start thread ")
            threading.Timer( self.next_t - time.time(), self._run).start()
    
    def stop(self):
        self.done=True
    
    def reset(self):
        self.i = self.time_out
        
    def kill(self):
        print("WATCHDOG  end all ")
        os.kill(threading.main_thread().native_id, signal.SIGKILL)
        sys.exit(0)
    
class PixelVector:
    def __init__(self, phone, x_start, x_end, y_start, y_end, step, title = "none"):
        self.phone = phone
        print("Init PixelVector")
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.step = step
        self.title = title
        self.data = [tuple]
        self.coord = []
        self.len = 0
        self.__init_data()
        
    def __init_data(self):
        i = 0
        
        if self.x_start == self.x_end: # vertical
            for y in range(self.y_start, self.y_end, self.step):
                # print(self.phone.getRGB(self.x_start, y))
                self.data.append(self.phone.getRGB(self.x_start, y))
                self.coord.append(y)
            self.len = self.x_end - self.x_start
        elif self.y_start == self.y_end: # horizontal
            for x in range(self.x_start, self.x_end, self.step):
                self.data.append(self.phone.getRGB(self.x, y_start))
                self.coord.append(x)
        else:
            print("Only vertical and horizontal supported")
            raise ExPokeLibFatal("Only vertical and horizontal supported")
        
    def update(self):
        i = 0
        
        if self.x_start == self.x_end: # vertical
            for y in range(self.y_start, self.y_end, self.step):
                # print(self.phone.getRGB(self.x_start, y))
                self.data[i] = self.phone.getRGB(self.x_start, y)
                i += 1
            self.len = self.x_end - self.x_start
        elif self.y_start == self.y_end: # horizontal
            for x in range(self.x_start, self.x_end, self.step):
                self.data[i] = self.phone.getRGB(x, self.x_start)
                i += 1
                self.data.append(self.phone.getRGB(self.x, y_start))
        else:
            print("Only vertical and horizontal supported")
            raise ExPokeLibFatal("Cant find home")
        
    def x_start(self):
        return self.x_start
    def x_end(self):
        return self.x_end
    def y_start(self):
        return self.y_start
    def y_end(self):
        return self.y_end
        
    def plot_start(self):
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'r.-', label='Live Data')
        
    def get_r(self):
        return list(map(lambda tup: tup[0], self.data))
       
    
    
class TouchScreen:

    def __init__(self, tcpPort, name = "unknown", scaleX = 0.576, scaleY = 0.512):
        self.log = logging.getLogger(name)
        self.log.info("Pokemat phone : {}".format(tcpPort))
        self.url = "http://localhost:{}/v1".format(tcpPort)
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.httpErrorCount = 0
        self.maxX = 1000
        self.maxY = 2000

    # def checkConnetionState(self):

    def scaleXY(self, x, y):
        x = x * self.scaleX
        y = y * self.scaleY
        return int(x), int(y)
        
    def writeToPhone(self, cmd):
        self.log.debug("Send CMD - {}".format(cmd))
        try:
            return requests.get("{}/{}".format(self.url, cmd))
        except Exception as e:
            raise ExPokeLibFatal("No connection")
            # self.log.fatal("No connection")
        
    def tapScreen(self, x, y, button = 1, duration = 30):
        self.log.debug("tap {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/tapScreen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.writeToPhone("click:{},{},{},{}".format(x,y,button, duration))
        self.log.debug("Response : {}".format(response))
        time.sleep(0.001 * duration)
    
    def tapDown(self, x, y, button = 1, duration = 0):
        self.log.debug("tapDown {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/tapScreen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.writeToPhone("button_down:{},{},{},{}".format(x,y,button, duration))
        self.log.debug("Response : {}".format(response))
        time.sleep(0.001 * duration)
    
    def tapUp(self, x, y, button = 1, duration = 50):
        self.log.debug("tapUp {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/tapScreen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.writeToPhone("button_up:{},{},{},{}".format(x,y,button, duration))
        self.log.debug("Response : {}".format(response))
        time.sleep(0.001 * duration)
        
    def moveCursor(self, x, y, dx, dy):
        self.log.debug("move {},{}".format(x,y))
        x, y = self.scaleXY(x, y)
        dx, dy = self.scaleXY(dx, dy)
        # response = requests.get("{}/tapScreen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.writeToPhone("move:{},{},{},{}".format(x,y,dx,dy))
        self.log.debug("Response : {}".format(response))
        # time.sleep(0.1)
    
    def getRGB(self, x, y):
        x, y = self.scaleXY(x, y)
        response = self.writeToPhone("color:{},{}".format(x,y))           
        self.writeToPhone("color:{},{}\n".format(x,y))
        self.log.debug("Response : {}".format(response.status_code))
        self.log.debug("Response : {}".format(response.json()))
        rgb = response.json()
        return int(rgb["red"]), int(rgb["green"]), int(rgb["blue"])
    
    def matchColor(self, x, y, r, g, b, threashold=10, debug=False):
        rr, gg, bb = self.getRGB(x, y)
        if debug:
            self.log.info("matchColor x{},y{},r{},g{},b{},t{}".format(x, y, r, g, b,threashold))
            self.log.info("matchColor x{},y{},r{},g{},b{},t{}".format(x, y, rr, gg, bb, threashold))
        if gg > (g + threashold) or gg < (g - threashold):
            log.debug("matchColor : False")
        if      rr > (r + threashold) or rr < (r - threashold) or \
                gg > (g + threashold) or gg < (g - threashold) or \
                bb > (b + threashold) or bb < (b - threashold):
            if debug:
                log.debug("matchColor : False")           
            return False
        if debug:
            log.debug("matchColor : True")           
        return True
    
    def waitMatchColor(self, x, y, r, g, b, threashold=10, time_out_ms=10000, 
                       freq_in_s = 1, same=True,
                       debug=False):

        self.log.info("waitMatchColor x{},y{},r{},g{},b{},t{},to{},f{},m{}".format(x, y, r, g, b, threashold, time_out_ms, freq_in_s, same))
        startTime = datetime.now()
        while True:
            if self.matchColor(x, y, r, g, b, threashold=threashold, debug=debug) == same:
                return True
                
            if ((datetime.now() - startTime).total_seconds() * 1000) > time_out_ms:
                self.log.warn("Timeout waiting {}ms for x:{},y{} r{},g{},b{}".format(time_out_ms, x, y, r, g, b))
                r, g, b = self.getRGB(x, y)
                raise ExPokeLibError("Timeout waiting {}ms for x:{},y{} r{},g{},b{}".format(time_out_ms, x, y, r, g, b))
            time.sleep(freq_in_s)
    
    def waitMatchColorAndClick(self, x, y, r, g, b, threashold=10, time_out_ms=10000, 
                               freq_in_s = 1, same=True, delay=0.8,
                               debug=False):
        self.log.info("waitMatchColorAndClick x{},y{},r{},g{},b{},t{},to{},f{},m{}".format(x, y, r, g, b, threashold, time_out_ms, freq_in_s, same))
        time.sleep(delay)
        self.waitMatchColor(x, y, r, g, b, threashold, time_out_ms, freq_in_s, 
                            same=same, debug=debug)
        # time.sleep(0.)
        self.tapScreen(x, y)
    
    def tapScreenBack(self):
        self.log.info("Tap Screen back")
        # self.waitMatchColorAndClick(501, 1826, 30, 134, 149)
        self.tapScreen(501, 1800)
        
    def tapExitMode(self):
        self.tapScreen(85,190)
        
    def tapConfirm(self):
        self.tapScreen(357, 1005)
        
    def tapAvatar(self):
        self.tapScreen(121, 1800)
        
    def tapOK(self):
        self.matchColor(623,1062,83,212,162)
        self.tapScreen(623,1062)
        return True
    
    def tapYES(self):
        try:
            self.waitMatchColorAndClick(366, 1103, 149, 216, 150, time_out_ms=1000)
        except:
            pass
        return True

    def tapSearch(self):
        self.waitMatchColor(626, 457, 78, 208, 175,time_out_ms=2000)
        self.tapScreen(626, 457)
        # Wait for light grey fromkeyboard
        # self.waitMatchColor(46, 1480, 37, 50, 55)
        self.waitMatchColor(46, 1480, 255,255,255, same=False)
    
    def screen_get_type(self):
        return("unknow")

    def screen_is_catch_pokemon(self):
        y = 1792
        y = 1791
        delta_max = delta_min = 0
        for x in range(854,904,2):
            r,_,_ = self.getRGB(x,y)
            r2,_,_ = self.getRGB(x + 2,y)
            d = r2 -r
            if d < delta_min:
                delta_min = d
            if d > delta_max:
                delta_max = d
        # return True
        return (delta_max - delta_min) > 150

    def scroll(self, dx, dy, start_x = 100, start_y = 1000, tap_time = 0.1, stop_to = 0.6):
        # self.log.info("Scroll")
        # x = maxX / 2
        x = float(start_x)
        y = float(start_y)
        sx = float(dx / 20.0)
        sy = float(dy / 20.0)
        self.tapDown(int(x), int(y), tap_time)
        for s in range(0,20):
            x = x + sx
            y = y + sy
            self.moveCursor(int(x), int(y), int(sx), int(sy))
            # print("sy={}".format(int(sy)))
            # self.moveCursor(int(sx), int(sy))
            time.sleep(0.01)
            # self.tapDown(int(x), int(y), int(sx), int(sy))
        time.sleep(stop_to)
        self.tapUp(int(x + dx), int(y + dy))

    def tapOpen(self):
        self.log.debug("tapOpen")
        # time.sleep(1)
        # self.waitMatchColorAndClick(406, 1654, 137, 218, 154)
        self.waitMatchColor(406, 1600, 137, 218, 154)
        # Pin
        if 1 == 1:
            print("Postit")
            time.sleep(0.5)
            self.tapScreen(876, 1652, duration = 300)
            time.sleep(0.5)
            self.tapScreen(876, 1652, duration = 300)
            time.sleep(1)
        while self.matchColor(406, 1600, 137, 218, 154):
            print("tapOpen")
            self.tapScreen(406, 1654)
            time.sleep(0.2)
                
    def tapBack(self):
        self.waitMatchColorAndClick(498, 1822, 28, 135, 149)
        
    def tapFriends(self):
        self.log.debug("tapFriends")
        for timeout in reversed(range(0,100)):
            if self.isFriendScreen() == True:
                break
            self.tapScreen(493, 193)
            time.sleep(0.2)

    def tapPokeBall(self):
        self.waitMatchColorAndClick(500, 1798, 255, 57, 69)
        
    def tapPokeSearch(self):
        self.waitMatchColorAndClick(187, 371, 233, 243, 223)
        
    def menuPokemon(self):
        self.waitMatchColorAndClick(180, 1599, 241, 255, 242)
        
    def tapTextOK(self):
        # self.waitMatchColorAndClick(871, 1082, 34, 34, 34)
        time.sleep(1)
        # self.waitMatchColorAndClick(871, 1152, 34, 34, 34)
        self.tapScreen(871, 1152)
        
    def selectFirstFriend(self):
        time.sleep(0.2)
        try:
            self.waitMatchColorAndClick(147, 808, 255, 255,255, same=False, time_out_ms=4000)
        except:
            return False
        return True
        
    def selectFirstPokemon(self):
        time.sleep(0.2)
        self.waitMatchColor(79, 179, 255, 255, 255)
        time.sleep(0.2)
        if self.matchColor(184, 777, 251, 254, 249) and \
           self.matchColor(184, 750, 255, 255, 255) and \
           self.matchColor(178, 730, 255, 255, 255) and \
           self.matchColor(184, 710,255, 255, 255):
            print("No more pokemons with this filter")
            return False
        print("Tao 177, 751")
        self.tapScreen(177, 751)
        return True
    
    def showColor(self, x, y):
            r, g, b = self.getRGB(x, y)
            print("Pixel color {},{},{},{},{}".format(x, y, r, g ,b))
       
    def evolvePokemon(self):
        self.waitMatchColor(135, 1001, 255, 255, 255)
        time.sleep(1)
        # self.scroll(0, 200)
        # sys.exit(0)
        print("Scroll up")
        self.scroll(0,-400)
         # Search and tap evolve
        for y in range(self.maxY - 2, self.maxY - 400, -10):
            self.log.debug("Search in {}".format(y))
            if self.matchColor(116, y, 163, 220, 148):
                print("Match at {}".format(y))
                self.tapScreen(130, y -10)
                break
        time.sleep(1.2)
         # Search and tap yes
        for i in range(0, 2):
            print("Wait for yes")
            for y in range(1200, 1400, 10):
                if self.matchColor(319, y, 151, 218, 147):
                    self.tapScreen(319, y)
                    break
        time.sleep(3)
        # 72, 476, 255, 255, 255
        print("Wait for evolve ready")
        self.waitMatchColor(505, 1832, 28, 135, 149, time_out_ms=20000)
        # self.waitMatchColor(72, 476, 255, 255, 255, time_out_ms=20000)
        # self.waitMatchColor(135, 1388, 255, 255, 255, time_out_ms=20000)
        # self.waitMatchColor(135, 1388, 255, 255, 255, time_out_ms=20000)
        print("Evolve ready")
        time.sleep(0.8)
        self.tapScreenBack()
        
    def tapBattle(self):
        self.waitMatchColorAndClick(496, 1681, 95, 166, 83, delay=3)
    
    def tapTrade(self):
        self.log.info("Tap Trade")
        # self.waitMatchColorAndClick(826, 1683, 20, 150, 200, threashold=20, debug=True)
        self.waitMatchColorAndClick(826, 1900, 20, 200, 240, threashold=20, debug=True)
    
    def typeString(self, text):
        time.sleep(0.1)
        # self.log.debug("type string {}".format(text))
        i = 0
        
        while i < len(text):
            c = text[i]
            i += 1
            if c == "&":
                c = "\\&"
            elif c == "\\":
                # print("RALF : backslash {}".format(text))
                # print("RALF : backslash {}".format(text[i]))
                c = "\\" + text[i]
                i += 1
            # print("RALF string '{}'".format(c))
            self.writeToPhone("key:{}".format(c))
            time.sleep(0.001)

    def selectAll(self):
        self.typeString("\\a")
    
    def getTimeNow(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def is_home(self):
        return self.matchColor(501,1802,255,55,72,10)
    
    def button_has_exit(self):
        for y in range(1835,1880,4):
            self.showColor(500,y)
        if      self.matchColor(500, 1835, 235, 245, 242, threashold=15, debug=True) \
            and self.matchColor(500, 1875, 235, 245, 246, threashold=15, debug=True):
            return True
        return False
    
    def button_tap_exit(self):
        self.tapScreen(500,1850)
    
    def isFriendScreen(self):
        if self.matchColor(319, 843, 0, 0, 0) \
            and self.matchColor(319, 1246, 0, 0, 0) \
            and self.matchColor(678, 843, 0, 0, 0):
            self.tapBack()
            time.sleep(0.5)
        return self.matchColor(32, 91, 255, 255, 255)

    def spinDisk(self):
        self.scroll(600, 0, start_x = 150, start_y = 1000)
    
    def goHome(self):
        self.log.info("Go to homescreen")
        print("Go Home")
        count = 10 # Try count time
        while self.is_home() == False and count > 0:
            self.log.warning("Wrong color")
            if self.matchColor(501, 1826, 30, 134, 149):
                self.tapScreenBack()                
            # Upper left exit
            # elif self.matchColor(500, 1822, 246, 245, 245, threashold=15):
            #    self.log.debug("light green press?")
            #     self.tapScreenBack()
            elif self.matchColor(498, 1832, 231, 235, 227):
                self.log.debug("Almost white?")
                print("AlmostWhite")
                self.tapScreenBack()
            elif self.matchColor(500, 1832, 240, 242, 230):
                self.log.debug("whith like gym press?")
                self.tapScreenBack()
            elif self.matchColor(86, 187, 27, 134, 148):
                self.tapExitMode()
            elif self.matchColor(357, 1005, 150, 218, 151):
                self.tapConfirm()
            elif self.matchColor(357, 1138, 150, 218, 151):
                self.tapScreen(357, 1138)
            elif self.matchColor(357, 1000, 143, 215, 150):
                self.tapScreen(357, 1000)                
            elif self.matchColor(847, 1849, 27, 134, 150):
                self.tapScreen(847, 1849)
            elif self.matchColor(109, 185, 234, 247, 240) or \
                 self.matchColor(97, 166, 250, 250, 250):
                print("Tap somthing")
                self.tapScreen(109, 185)
                self.tapYES()
                count = count -1 
            else:
                count = count -1
                if self.matchColor(64, 156, 255, 255, 255):
                    self.tapScreen(64, 156)
                elif self.matchColor(57, 361, 28, 135, 149):
                    self.tapScreen(57, 361)
                elif count == 6:
                    for y in [1750, 1850]:
                        self.tapScreen(500,y)                    
                    self.tapScreen(100, 100, button = 3)
                else:
                    print("Not found")
                    if count == 0:
                        raise ExPokeLibError("Cant find home")
            print("count = {}".format(count))
            if count == 4:
                self.tapScreen(100, 100, button = 3)
            time.sleep(1)
        log.info("Now we are on the home screen {}".format(self.is_home()))

    def selectLeague(self, league):
        if league == "great":
            self.log.info("Great League selected")
            y = 951
        elif league == "ultra":
            self.log.info("Ultra League selected")
            y = 1301
        elif league == "master":
            self.log.info("Master League selected")
            y = 1650
        else:
            raise ExPokeLibError("Uknow leage {}".format(league))
        
        self.waitMatchColor(350, y, 255, 255, 255)
        time.sleep(3)
        self.tapScreen(350, y)
        # Lets battle
        self.waitMatchColorAndClick(305, 1230, 161, 221, 148)
        
    def friendScreen(self):
        self.goHome()
        self.tapAvatar()
        self.tapFriends()

    def pokeScreen(self):
        self.goHome()
        self.tapPokeBall()
        self.menuPokemon()
        
    def selectPokemon(self, filter):
        self.pokeScreen()
        self.tapPokeSearch()
        self.waitMatchColor(121, 1154, 255, 255, 255)
        time.sleep(0.4)
        self.typeString(filter)
        time.sleep(1)        
        self.tapTextOK()
        
    def searchFriend(self, name):
        self.friendScreen()
        self.tapSearch()
        print("done")
        self.typeString(name)
        self.tapTextOK()
        self.selectFirstFriend()

    def searchPokemon(self, filter):
        self.waitMatchColorAndClick(500, 345, 233, 233, 223, threashold=14, time_out_ms=30000,debug=True)
        time.sleep(1)
        self.selectAll()
        time.sleep(0.2)
        self.typeString(filter)
        self.tapTextOK()
    
    def swipe(self, x1, y1, x2, y2):
        steps = 5
        sx = float(x1)
        sy = float(y1)
        dx = (float(x2) - float(x1)) / float(steps)
        dy = (float(y2) - float(y1)) / float(steps)
        self.tapDown(x1, y1, duration = 0)
        for s in range(0, steps):
            self.moveCursor(int(sx), int(sy), int(sx + dx), int(sy + dy))
            sx = sx + dx
            sy = sy + dy
            # print("sx={},sy={}".format(int(sx),int(sy)))
            # self.moveCursor(int(sx), int(sy))
            # time.sleep(0.005)
        self.tapUp(int(sx), int(sy))
    
    def catchPokemon(self):
        print("Try to catch pokemon")
        while self.matchColor(881, 1742, 238, 56, 56) or \
                self.matchColor(881, 1742, 255, 255, 255):
            v = random.randint(0,300)
            print("Throug {}".format(v))
            self.swipe(506, 1820, 506, 950 + v)
            try:
                self.waitMatchColor(364, 1326, 146, 216, 149, time_out_ms = 20000)
                self.tapScreen(364, 1326)
            except:
                pass
    
    def collectRewards(self):
        for i in range(0,5):
            try:
                print("Collect award {}".format(i))
                for x in range( 100,800,40):
                    self.showColor(x, 1630)
                    if self.matchColor(x, 1630, 254, 183, 86):
                        self.tapScreen(x, 1630)
                        time.sleep(3)
                        try:
                            print("Check if pokemon")
                            # time.sleep(1.5)
                            if not self.matchColor(166, 1171, 250, 251, 246):
                                print("Try to catch pokemon")
                                self.catch_pokemon()
                                self.waitMatchColorAndClick(418, 1365, 137, 218, 154, time_out_ms=3500)
                                self.waitMatchColorAndClick(508, 1869, 26, 136, 151, time_out_ms=3500)
                        except:
                            sys.exit(0)
                            pass
            except:
                pass
        if self.matchColor(187, 1919, 255, 180, 82):
            selt.tapScreen(187, 1919)
        
    def goItem(self):
        self.goHome()
        print("wait")
        self.tapPokeBall()
        self.waitMatchColorAndClick(795, 1542, 240, 254, 238)
        
        
    def goBattle(self):
        print("Tap pokeball")
        self.tapPokeBall()
        self.waitMatchColorAndClick(734, 1041, 240, 252, 239)
        
    def healAll(self):
        print("Heal all")
        self.goItem()
        # Revive
        for y in [960, 550]:
            # for x in [750, 455, 150]
            
            time.sleep(1)
            for x in range(900,100, -20):
                # self.showColor(x, y)
                if self.matchColor(x, y, 220, 220, 110, threashold=35):
                    print("Found revive at {},{}".format(x,y))
                    self.tapScreen(x, y)
                    time.sleep(0.5)
                    if self.matchColor(67, 205, 141, 205, 145):
                        self.tapScreen(328, 1648)
                        time.sleep(1)
                        if self.matchColor(525, 1850, 28, 135, 149):
                            self.tapScreen(525, 1850)
                            break
        time.sleep(1)
        # Potion
        for x in [250, 500, 750]:
            self.tapScreen(x, 550)
            time.sleep(1)
            if self.matchColor(67, 205, 141, 205, 145):
                self.tapScreen(328, 1648)
                time.sleep(1)
                if self.matchColor(525, 1850, 28, 135, 149):
                    self.tapScreen(525, 1850)
        self.goHome()

    
    def battleLeague(self):
        time.sleep(2)
        self.showColor(200, 1900)
        if self.matchColor(200, 1900, 255, 180, 82):
            print("Claim rewards")
            self.tapScreen(200, 1900)
            time.sleep(1)
            return

        count = 10
        while not self.matchColor(366, 1939, 154, 218, 149) and \
                not self.matchColor(361, 1878, 229, 246, 227):
            count = count -1
            if count == 0:
                return
            self.scroll(0, -60)
            time.sleep(0.5)
        time.sleep(0.5)
        if self.matchColor(361, 1878, 229, 246, 227):
            self.collectRewards()
            time.sleep(30)
        if self.matchColor(312, 1835, 149, 217, 148):
            self.tapScreen(312, 1835)
            return
        self.waitMatchColorAndClick(366, 1939, 154, 218, 149)
        next_battle = True
        while next_battle:
            if self.matchColor(288, 1806, 151, 217, 147):
                self.tapScreen(288, 1806)
            for to in range(1,10):
                if self.matchColor(328, 939, 255, 255, 255):
                    self.tapScreen(328, 939)
                    break
                if self.matchColor(347, 1812, 144, 218, 152):
                    self.tapScreen(347, 1812)
                time.sleep(1)
            self.waitMatchColorAndClick(322, 1781, 163, 220, 148)
            try:
                time.sleep(1)
                self.waitMatchColor(81, 998, 255, 254, 255, same=False, time_out_ms=20000)
            except:
                pass
            self.doBattle()
            try:
                next_battle = self.waitMatchColorAndClick(315, 1535, 153, 219, 149, time_out_ms=20000)
                next_battle = True
                time.sleep(1)
                # next_battle = self.waitMatchColor(690, 1539, 72, 209, 163)
            except:
                next_battle = False
        
    def battleTrainer(self, trainer, league):
        for i in range(0,6):
            self.scroll(0,-1000)
            
        time.sleep(1)
        
        cont = True
        while cont:
            self.tapScreen(250 + ((trainer - 1) * 250), 1634)
            # Press battle
            self.waitMatchColorAndClick(362, 1552, 149, 217, 148)
            if league == "great":
                self.waitMatchColorAndClick(338, 850, 255, 255, 255)
            elif league == "ultra":
                self.waitMatchColorAndClick(333, 1300, 255, 255, 255)
            elif league == "master":
                self.waitMatchColor(345, 1640, 255, 255, 255)
            else:
                self.log.error("Unknow trainer league {}".format(league))
                
            self.waitMatchColorAndClick(501, 1742, 113, 213, 157)
            self.doBattle()
            self.waitMatchColorAndClick(500, 1826, 28, 135, 149)
            time.sleep(0.5)
        
    def attack(self, time_out_ms = 12000):
        startTime = datetime.now()
        # while ((datetime.now() - startTime).total_seconds() * 1000) < time_out_ms:
            # and \
        step = 100
        self.tapDown(10, 800, duration = 0)
        x = self.maxX / 2
        y = self.maxY / 2
        while   ((datetime.now() - startTime).total_seconds() * 1000) < time_out_ms and \
                not self.matchColor(164, 222, 246, 14, 29) and \
                not self.matchColor(100, 100, 10, 10, 10) and \
                not self.matchColor(500, 1826, 28, 135, 149):
                # and self.matchColor(213, 177, 255, 255, 255) \
                # and self.matchColor(722, 177, 255, 255, 255):
            
            self.tapUp(498, 1500, duration = 0)
            time.sleep(0.05)
            # Tap shield
            self.tapScreen(498, 1500)
            self.tapDown(498, 1500, duration = 0)

            # self.swipe(150, 700, 800, 1750)
            # self.swipe(800, 700, 150, 1750)
            # for x in range(50,990, 120):
            #    self.swipe(x, 700, 900 - x, 1950)
            # Use shield for what ever
            # self.tapScreen(498, 1500)
            if False:
                for y in range(800, 1900, 100):
                    self.swipe(10, y, self.maxX - 200, y)

            if False:
                for y in range(0, 100, 25):
                    for ya in range(800, 1900, 100):
                        self.swipe(10, y + ya, self.maxX - 200, y + ya)
                    
                    
            if False:
                self.swipe(10, 800, self.maxX - 10, self.maxY - 10)
                self.swipe(self.maxX - 10, 800, 10, self.maxY - 10)
    
                self.swipe(self.maxX / 4, self.maxY - 10, self.maxX - ( self.maxX / 4), 800)
                self.swipe(self.maxX - ( self.maxX / 4), self.maxY - 10, self.maxX / 4, 800)
              
            if False:  
                cx = self.maxX / 2
                cy = 800 + self.maxX / 2
                for a in range(0, 180,10):
                    dx = int(math.sin(math.radians(a)) * (self.maxX / 2 - 2))
                    dy = int(math.cos(math.radians(a)) * 698) # (self.maxX / 2 - 2))
                    log.debug("x1 {}, y1 {}, x2 {}, y2 {}".format(cx + dx, cy + dy, cx - dx, cy - dy))
                    # self.swipe(cx + dx, cy + dy, cx - dx, cy - dy)
                    # self.swipe(cx - dx, cy + dy, cx + dx, cy - dy)
                    self.moveCursor(cx + dx, cy + dy, cx - dx, cy - dy)
                    self.moveCursor(cx - dx, cy - dy, cx + dx, cy + dy)
                    
            if False:
                # self.tapDown(10, 800, duration = 0)
                for y in range(800, 1800, step):
                    self.moveCursor(10, y, self.maxX - 200, y)
                    time.sleep(0.01)
                    self.moveCursor(self.maxX - 200, y ,10 , y + step)
                    time.sleep(0.01)
                   
                for x in range(10, self.maxX - 200, step):
                    self.moveCursor(x, 800, x, 1900)
                    time.sleep(0.01)
                    self.moveCursor(x, 800, x + step, 1900)
                    time.sleep(0.01)

            if False:
                xn = random.randint(10, self.maxX - 200)
                yn = random.randint(800, 1900)
                self.moveCursor(x, y, xn, yn)
                x = xn
                y = yn
                
            if True:
                x = ox = 200
                y = oy = 1300
                t = 0.05
                step = 30
                max_degrees = 180
                t = 0.03
                step = 45
                max_degrees = 360
                for a in range(0,max_degrees, step):
                    dx = ox + ( a * ( 600.0 / max_degrees))
                    dy = oy + (int(math.sin(math.radians(a)) * 350))
                    self.moveCursor(x, y, dx, dy)
                    x = dx
                    y = dy
                    time.sleep(t)
                for a in range(max_degrees,0, -step):
                    dx = ox + ( a * ( 600.0 / max_degrees))
                    dy = oy + (int(math.sin(math.radians(a)) * 350)) 
                    self.moveCursor(x, y, dx, dy)
                    x = dx
                    y = dy
                    time.sleep(t)           
        self.tapUp(x, y + step, duration = 0)
                
    def catch_pokemon(self, distance = 6, right = True, berry = "a"):
        while not self.matchColor(90, 1414, 245, 254, 242):
            try:
                self.waitMatchColor(420, 1923, 220, 220, 220, threashold = 35)
            except:
              print("Catch over")
              break
            self.tapScreen(114, 1757)
            time.sleep(1)
            no_berry = True
            if berry == "a":
                if self.matchColor(814, 1373, 236, 227, 19):
                    self.tapScreen(815, 1375)
                    sleep(0.5)
                    self.tapScreen(486, 1748)
                    sleep(1)
                    no_berry = False
                elif self.matchColor(772, 1767, 248, 246, 76):
                    self.tapScreen(772, 1767)
                    sleep(0.5)
                    self.tapScreen(486, 1748)
                    sleep(1)
                    no_berry = False
                elif self.matchColor(182, 1718, 238, 232, 27):
                    self.tapScreen(182, 1718)
                    sleep(0.5)
                    self.tapScreen(486, 1748)
                    sleep(1)
                    no_berry = False
            elif berry == "g":
                self.scroll(600,0, start_y = 1750, tap_time = 1)
                time.sleep(0.5)
                if self.matchColor(454, 1732, 255, 143, 9):
                    self.tapScreen(454, 1718)
                    sleep(0.5)
                    self.tapScreen(486, 1748)
                    sleep(1)
                    no_berry = False
            if no_berry:
                time.sleep(1)
                print("Remove screen")
                self.tapScreen(795, 191)
                sleep(2)
            sleep(0.5)
            print("distance {}".format(distance))
            self.catch_move(distance = distance)
            sleep(5)
       
        
    
#     def catch_move(self, right = True, start = -90, end = 60, off_y = 900, radius = 250, delay = 0.012, step = 5, distance = 15):
    def catch_move(self, right = True, start = -180, end = 90 + 720, off_x = 500, off_y = 1300, \
                   radius = [80, 250], delay = 0.015, step = 5, distance = 5, tilt = -1.0):
        def getX(d, r, offset=0, tilt = 0.0):
            return math.sin(math.radians(d)) * float(r) + float(offset) + float(tilt)
        
        def getY(d, r, offset=0, tilt = 0.0):
            return math.cos(math.radians(d)) * float(r) + float(offset) + float(tilt)
        
        attempt = 1 
        # off_x = 500
        # off_y = 1250
        # off_y = 900
        y = getY(start, radius[1])
        x = getX(start, radius[0], tilt = y * tilt) 
        self.tapDown(x + off_x, y + off_y)
        top = 10
        while top < 0:
            for probe in range(750,900,2):
                if self.matchColor(500, probe, 240,240,240):
                    top = probe
        button = -1
        while top < 0:
            for probe in range(750,850,-2):
                if self.matchColor(500, probe, 240,240,240):
                    top = probe
        # print("Top = {}".format(top))
        # return
        a  = start + step
        b = 0.0
        if attempt % 2:
            right = False
        else:
            right = True
            
        while a < end + step:
            a = a + step + int(a / 60)
            b = b + 0.2
            # t = radius + int(b)
            # radius = t
            # for a in range(start + step, end + step, step):
            sx = x
            sy = y
            
            y = getY(a, radius[1]) # - a * 2
            x = getX(a, radius[0] , tilt = y * tilt)
            attempt = attempt + 1
            # print("radius {}".format(radius))
            # print("XY {} {}".format(x, y))
            # print("x = {}".format(x))
            self.moveCursor(int(sx) + off_x, int(sy) + off_y, int(x) + off_x, int(y) + off_y)
            # dx = x - sx
            # dy = y - sy
            # d = math.sqrt(dx * dx + dy * dy)
            # print("Delta {}".format(d))
            # canvas.create_line(sx, sy, x, y)
            # canvas.update()
            time.sleep(delay)
        ys = int(y)
        xs = x
        dx = x - sx
        dy = y - sy
        d = math.sqrt(dx * dx + dy * dy)
        print("Delta {}".format(d))
        accel=0.0
        #for y2 in range(int(y) - 10 , int(y) - 100, -10):
        for i in range(distance):        
            accel = accel + 5.0
            ye = ys - ( d + accel)
            xe = xs + dx # distance - i
            self.moveCursor(int(xs) + off_x, int(ys) + off_y, int(xe) + off_x, int(ye) + off_y)
            xs = xe
            ys = ye
            time.sleep(delay)
        # return
        self.tapUp(x, y)
        # 750

    def black_screen(self):
        for xy in range(100, 600, 100):
            if not self.matchColor(xy, xy, 1, 1, 1, threashold=1):
                return False
        return True
            

    def doBattle(self):
            def still_in_battle():
                in_battle = False
                if not self.matchColor(100, 100, 10, 10, 10) and \
                        not self.matchColor(500, 1826, 28, 135, 149):
                    print("Found trainer screen")
                    # return False
                # Check black screen    
                        
               # Check white screen
                if not in_battle:
                    for d in range(0, 320, 80):
                        if not self.matchColor(200 + d, 1150 + d, 241, 241, 241, threashold=15):
                        # if not self.matchColor(200 + d, 1250, 241, 241, 241, threashold=15):
                            print("no white screen")
                            in_battle = True
                            break
                
                return in_battle
            
            # while not self.matchColor(79, 357, 212, 227, 217) \
            #     and not self.matchColor(76, 360, 240, 240, 240):
            #     time.sleep(0.1)
            print("Start battle")
            
            while still_in_battle():
                for x in [270, 500, 730]:
                    # print("tapScreen : {},{}".format(x,1850))
                    
                    # Check for attack and use shield
                    if self.matchColor(545, 195, 108, 121, 126, threashold=20) and False:
                    # if self.matchColor(498, 1500, 237, 122, 241):
                        print("Use shield")
                        self.tapScreen(498, 1500)
                        # time.sleep(1)
                    if False:
                        print("")
                        for i in range(0, 80,2):
                            xx = 400 + i
                            yy = 660 + i
                            r,g,b =self.getRGB(xx, yy)
                            print("{},{},{},{},{}".format(xx, yy, r, g, b))
                    time.sleep(0.015)
                    self.tapScreen(x, 1790)
                    time.sleep(0.015)
                    self.tapScreen(x, 1790)
                    # self.tapScreen(x, 1810)
                    # wait for ready of last red ball disappear
                    p = {}
                    if self.black_screen():
                        return
                    # for x in range(400, 420, 4):
                    #    print("DEBUG X({}):{}".format(x,self.getRGB(x, 665)))
                    # if self.matchColor(405, 665, 220, 220, 220, threashold=20) \
                    #    or self.matchColor(48, 670, 220, 220, 220, threashold=20):
                    # if self.matchColor(394, 630, 252, 255, 255):
                    # if self.matchColor(505, 660, 245, 245, 245) and \
                    # for xx in range(0,8,2):
                    #     for yy in range(0,8,2):
                    #         self.showColor(158 + xx,216 + yy)
                if not self.matchColor(164, 222, 246, 14, 29) \
                    and not self.matchColor(161, 218, 240, 38, 20):
                        self.attack()
                        # print("Exit")
                        # sys.exit(0)
                        
                # self.tapScreen(498, 1500)
                time.sleep(0.01)
                self.tapScreen(498, 1500)
         
    def hasGift(self):
        xs = 402
        ys = 1144
        # self.waitMatchColor(76, 1970, 240, 240, 240, threashold = 14, debug=True)
        time.sleep(2)
        for x in range(xs, xs + 40, 4):
            print("Check if gift {},{}".format(x, ys))
            if self.matchColor(x, ys, 223, 15, 206, debug=True):
                print("Friend has already gift")
                time.sleep(1)
                return True
            time.sleep(0.1)
        print("Friend has no gift yet.")
        return False
    
    def openGift(self):
        self.log.info("tap gift")
        try:
            self.waitMatchColor(496, 1000, 230, 51, 198, time_out_ms = 2000, threashold=50)
        except:
            pass
        self.tapScreen(500, 1164)
        self.log.info("openGift")
        self.tapOpen()
        while self.matchColor(85, 1960, 255, 255, 255) == False:
            # if ping_limit:
            #     return False
            if self.matchColor(376, 1630, 144, 217, 149):
                print("Daily limit reached")
                self.tapScreen(500, 1850)
                return False
            self.tapScreen(85, 1960)
            time.sleep(0.5)
        return True
    
    def sendGift(self, has_gift = False):
        print("Send gift")
        # if self.hasGift():
        #    self.tapScreen(500, 1850)
        time.sleep(2)
        if has_gift:
            self.tapScreen(500, 1850)
        # if self.matchColor(175, 1919, 243, 243, 243, threashold=13):
        # if self.matchColor(237, 1900, 172, 172, 172):
        #     print("Friend has a gift")
        #     return False
        timeout = 50
        # while self.matchColor(800, 857, 255, 255, 255,threashold=1) == False:
        # Check for post card
        while self.matchColor(700, 857, 255, 255, 255,threashold=1) == False \
                and self.matchColor(750, 1110, 255, 255, 255,threashold=1) == False:
            
            time.sleep(0.2)
            self.tapScreen(170, 1919)
            timeout = timeout - 1
            # Timout or send already
            if timeout == 0 or \
                self.matchColor(95, 1000, 232, 128, 181):
                return False
        time.sleep(1)
        self.tapScreen(750, 857)
        try:
            self.waitMatchColorAndClick(407, 1638, 140, 216, 152)
        except:
            print("Gift not sent !?!?")
        sleep(0.5)
        if self.matchColor(105, 1000, 232, 128, 181):
            print("No gifts")   
        # self.waitMatchColorAndClick(503, 1820, 30, 134, 149)
        return True
    
    def sendGift2(self):
        if self.matchColor(195, 1630, 222, 60, 190):
            self.log.debug("Click send")
            # sys.exit(0)
            self.tapScreen(204, 1703)
            return True
        return False

    def inviteFriend(self, name, league):
        self.log.warning("Invite friend")
        self.searchFriend(name)
        time.sleep(1)
        if self.hasGift():
            self.tapScreenBack()
        self.tapBattle()
        self.selectLeague(league)
        
    def acceptBattleInvite(self):
        self.waitMatchColorAndClick(309, 1275, 157, 218, 150)
        
    def useThisParty(self):
        print("useThisParty start")
        self.waitMatchColorAndClick(329, 1775, 163, 220, 148, threashold=20,time_out_ms=10000)
        print("useThisParty end")
    
    def changeSortGift(self, hasGift = True):
        self.waitMatchColorAndClick(857, 1798, 28, 135, 149)
        if hasGift == True:
            self.waitMatchColorAndClick(796, 1431, 44, 113, 119)
        else:
            self.waitMatchColorAndClick(913, 1644, 41, 105, 120)

    def friendSortHasGift(self, noGift = False):
        self.friendScreen()
        self.changeSortGift()
        self.waitMatchColor(838, 220, 255, 255, 255)
        # for x in range(912, 935, 2):
        #    r, g, b = self.getRGB(x, 1860)
        #    print("X {},{},{},{}".format(x, r, g ,b))
        # sys.exit(0)
        while self.matchColor(929, 1860, 170, 245, 205, threashold=20) == noGift:            
            self.changeSortGift()
            self.waitMatchColor(838, 220, 255, 255, 255)
        else:
            print("Order is OK")
            
    def friendSortCanReceive(self, noGift = False):
        self.friendScreen()
        self.changeSortGift(hasGift = False)
        self.waitMatchColor(838, 220, 255, 255, 255)
        # for x in range(912, 935, 2):
        #    r, g, b = self.getRGB(x, 1860)
        #    print("X {},{},{},{}".format(x, r, g ,b))
        # sys.exit(0)
        while self.matchColor(929, 1860, 170, 245, 205, threashold=20) == noGift:            
            self.changeSortGift(hasGift = False)
            self.waitMatchColor(838, 220, 255, 255, 255)
        else:
            print("Order is OK")
            

