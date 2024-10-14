import requests
import logging
import time
import sys
from datetime import datetime
from ansible_collections.community.aws.plugins.modules.directconnect_gateway import dx_gateway_info
from ansible_collections.cisco.ise.plugins.action import sxp_connections
import random
log = logging.getLogger("pokelib")

class ExPokeLibError(Exception):
    """Custom exception class."""
    pass

class ExPokeLibFatal(Exception):
    """ Somthing fatal should not be ignored """
    pass

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
        
    def tapScreen(self, x, y, button = 1, duration = 50):
        self.log.info("tap {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/tapScreen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.writeToPhone("click:{},{},{},{}".format(x,y,button, duration))
        self.log.debug("Response : {}".format(response))
        time.sleep(0.001 * duration)
    
    def tapDown(self, x, y, button = 1, duration = 0):
        self.log.info("tapDown {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/tapScreen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.writeToPhone("button_down:{},{},{},{}".format(x,y,button, duration))
        self.log.debug("Response : {}".format(response))
        time.sleep(0.001 * duration)
    
    def tapUp(self, x, y, button = 1, duration = 50):
        self.log.info("tapUp {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/tapScreen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.writeToPhone("button_up:{},{},{},{}".format(x,y,button, duration))
        self.log.debug("Response : {}".format(response))
        time.sleep(0.001 * duration)
        
    def moveCursor(self, x, y, dx, dy):
        self.log.info("move {},{}".format(x,y))
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
            log.info("matchColor : False")
        if      rr > (r + threashold) or rr < (r - threashold) or \
                gg > (g + threashold) or gg < (g - threashold) or \
                bb > (b + threashold) or bb < (b - threashold):
            if debug:
                log.info("matchColor : False")           
            return False
        if debug:
            log.info("matchColor : True")           
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
        self.waitMatchColorAndClick(366, 1103, 149, 216, 150)
        return True

    def tapSearch(self):
        self.waitMatchColor(626, 457, 78, 208, 175,time_out_ms=2000)
        self.tapScreen(626, 457)
        # Wait for light grey fromkeyboard
        # self.waitMatchColor(46, 1480, 37, 50, 55)
        self.waitMatchColor(46, 1480, 255,255,255, same=False)
        

    def scroll(self, dx, dy):
        self.log.info("Scroll")
        # x = maxX / 2
        x = float(self.maxX / 2)
        y = float(self.maxY / 2)
        sx = float(dx / 20.0)
        sy = float(dy / 20.0)
        self.tapDown(int(x), int(y), duration = 0)
        for s in range(0,20):
            x = x + sx
            y = y + sy
            self.moveCursor(int(x), int(y), int(sx), int(sy))
            print("sy={}".format(int(sy)))
            # self.moveCursor(int(sx), int(sy))
            time.sleep(0.01)
            # self.tapDown(int(x), int(y), int(sx), int(sy))
        self.tapUp(int(x), int(y))

    def tapOpen(self):
        self.log.debug("tapOpen")
        time.sleep(1)
        self.waitMatchColorAndClick(406, 1654, 137, 218, 154)
                
    def tapFriends(self):
        self.log.debug("tapFriends")
        while self.isFriendScreen() == False:
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
        self.waitMatchColorAndClick(147, 808, 255, 255,255, same=False)
        
    def selectFirstPokemon(self):
        time.sleep(0.2)
        self.waitMatchColor(79, 179, 255, 255, 255)
        time.sleep(0.2)
        self.tapScreen(177, 751)
        
    def evolvePokemon(self):
        self.waitMatchColor(135, 1001, 255, 255, 255)
        time.sleep(1.5)
        # self.scroll(0, 200)
        # sys.exit(0)
        for y in range(self.maxY - 2, self.maxY - 200, -10):
            print("Search in {}".format(y))
            if self.matchColor(116, y, 163, 220, 148):
                print("Match at {}".format(y))
                self.tapScreen(114, y)
                break
        time.sleep(0.8)
        for y in range(1200, 1400, 10):
            if self.matchColor(319, y, 151, 218, 147):
                self.tapScreen(319, y)
                break
        time.sleep(5)
        self.waitMatchColor(135, 1388, 255, 255, 255, time_out_ms=20000)
        self.waitMatchColor(135, 1388, 255, 255, 255, time_out_ms=20000)
        time.sleep(0.8)
        self.tapScreenBack()
        
    def tapBattle(self):
        self.waitMatchColorAndClick(496, 1681, 95, 166, 83, delay=3)
    
    def tapTrade(self):
        self.log.info("Tap Trade")
        self.waitMatchColorAndClick(826, 1683, 20, 150, 200, threashold=20, debug=True)
    
    def typeString(self, text):
        self.log.debug("type string {}".format(text))
        i = 0
        
        while i < len(text):
            c = text[i]
            i += 1
            if c == "&":
                c = "\\&"
            elif c == "\\":
                print("RALF : backslash {}".format(text))
                print("RALF : backslash {}".format(text[i]))
                c = "\\" + text[i]
                i += 1
            print("RALF string '{}'".format(c))
            self.writeToPhone("key:{}".format(c))

    def selectAll(self):
        self.typeString("\\a")
    
    def getTimeNow(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def isHome(self):
        return self.matchColor(501,1802,255,55,72,10)
    
    def isFriendScreen(self):
        return self.matchColor(32, 91, 255, 255, 255)

    def goHome(self):
        self.log.info("Go to homescreen")
        count = 10 # Try count time
        while self.isHome() == False and count > 0:
            self.log.warning("Wrong color")
            if self.matchColor(501, 1826, 30, 134, 149):
                self.tapScreenBack()                
            # Upper left exit
            elif self.matchColor(109, 185, 234, 247, 240):
                self.tapScreen(109, 185)
                self.tapYES()
            elif self.matchColor(500, 1822, 246, 254, 244):
                self.log.debug("light green press?")
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
            else:
                if self.matchColor(64, 156, 255, 255, 255):
                    self.tapScreen(64, 156)
                elif self.matchColor(57, 361, 28, 135, 149):
                    self.tapScreen(57, 361)
                else:
                    if count == 0:
                        raise ExPokeLibError("Cant find home")
                    count = count -1
            time.sleep(1)
        log.info("Now we are on the home screen {}".format(self.isHome()))

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
        sx = float(x1)
        sy = float(y1)
        dx = (float(x2) - float(x1)) / 15.0
        dy = (float(y2) - float(y1)) / 15.0
        self.tapDown(x1, y1, duration = 0)
        for s in range(0,15):
            self.moveCursor(int(sx), int(sy), int(sx + dx), int(sy + dy))
            sx = sx + dx
            sy = sy + dy
            # print("sx={},sy={}".format(int(sx),int(sy)))
            # self.moveCursor(int(sx), int(sy))
            time.sleep(0.005)
        self.tapUp(int(sx), int(sy))
    
    def catchPokemon(self):
        print("Try to catch pokemon")
        while self.matchColor(881, 1742, 238, 56, 56):
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
                self.waitMatchColorAndClick(200 + i * 120, 1603, 254, 178, 81, time_out_ms = 1000)
                try:
                    print("Check if pokemon")
                    self.waitMatchColor(881, 1742, 238, 56, 56, time_out_ms = 5000)
                    print("Try to catch pokemon")
                    self.catchPokemon()
                    sys.exit(0)
                except:
                    sys.exit(0)
                    pass
            except:
                pass
        self.waitMatchColorAndClick(187, 1919, 255, 180, 82)
        
    def attack(self, time_out_ms = 6000):
        startTime = datetime.now()
        # while ((datetime.now() - startTime).total_seconds() * 1000) < time_out_ms:
            # and \
        while not self.matchColor(164, 222, 246, 14, 29) and \
                not self.matchColor(100, 100, 10, 10, 10):
                # and self.matchColor(213, 177, 255, 255, 255) \
                # and self.matchColor(722, 177, 255, 255, 255):
            # self.swipe(150, 700, 800, 1750)
            # self.swipe(800, 700, 150, 1750)
            # for x in range(50,990, 120):
            #    self.swipe(x, 700, 900 - x, 1950)
            # Use shield for what ever
            self.tapScreen(498, 1500)
            for y in range(800, 1801, 100):
               self.swipe(10, y, self.maxX - 10, 800 + 1800 - y)
            
    
    def goBattle(self):
        print("Tap pokeball")
        self.tapPokeBall()
        self.waitMatchColorAndClick(734, 1041, 240, 252, 239)
        time.sleep(0.5)
        count = 30
        while not self.matchColor(366, 1939, 154, 218, 149) and \
                not self.matchColor(361, 1878, 229, 246, 227):
            count = count -1
            if count == 0:
                return
            self.scroll(0, -22)
            time.sleep(0.5)
        time.sleep(0.5)
        if self.matchColor(361, 1878, 229, 246, 227):
            self.collectRewards()
            time.sleep(30)
        if self.matchColor(312, 1835, 149, 217, 148):
            self.tapScreen(312, 1835)
        next_battle = True
        self.waitMatchColorAndClick(366, 1939, 154, 218, 149)
        while next_battle:
            self.waitMatchColorAndClick(328, 939, 255, 255, 255)
            self.waitMatchColorAndClick(322, 1781, 163, 220, 148)
            try:
                time.sleep(1)
                self.waitMatchColor(81, 998, 255, 254, 255, same=False, time_out_ms=20000)
            except:
                pass
            
            while not self.matchColor(100, 100, 10, 10, 10):
                self.tapScreen(498, 1500)
                for x in range(150,800,75):
                    # print("tapScreen : {},{}".format(x,1850))
                    
                    # Check for attack and use shield
                    if self.matchColor(545, 195, 108, 121, 126, threashold=20) and False:
                    # if self.matchColor(498, 1500, 237, 122, 241):
                        print("Use shield")
                        self.tapScreen(498, 1500)
                        # time.sleep(1)
                    # if self.matchColor(505, 658, 245, 245, 245):
                    # if self.matchColor(394, 630, 252, 255, 255):
                    # if self.matchColor(505, 660, 245, 245, 245) and \
                    if    not self.matchColor(161, 218, 251, 38, 14):
                        self.attack()
                        
                    self.tapScreen(x, 1790)
                self.tapScreen(498, 1500)
                time.sleep(0.01)
            try:
                next_battle = self.waitMatchColorAndClick(315, 1535, 153, 219, 149, time_out_ms=20000)
                next_battle = True
                time.sleep(1)
                # next_battle = self.waitMatchColor(690, 1539, 72, 209, 163)
            except:
                next_battle = False
        
    def hasGift(self):
        xs = 402
        ys = 1144
        # self.waitMatchColor(76, 1970, 240, 240, 240, threashold = 14, debug=True)
        time.sleep(2)
        for x in range(xs, xs + 40, 4):
            print("Check {},{}".format(x, ys))
            if self.matchColor(x, ys, 223, 15, 206):
                print("Has gift")
                time.sleep(1)
                return True
            time.sleep(0.5)
        return False
    
    def openGift(self):
        self.log.info("tap gift")
        self.tapScreen(500, 1164)
        self.log.info("openGilft")
        self.tapOpen()
        while self.matchColor(85, 1960, 255, 255, 255) == False:
            # if ping_limit:
            #     return False
            self.tapScreen(85, 1960)
            time.sleep(0.5)
        return True
    
    def sendGift(self):
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
    
    def changeSortGift(self):
        self.waitMatchColorAndClick(857, 1798, 28, 135, 149)
        self.waitMatchColorAndClick(796, 1431, 44, 113, 119)

    def friendSortHasGift(self, hasGift = False):
        self.friendScreen()
        self.changeSortGift()
        self.waitMatchColor(838, 220, 255, 255, 255)
        if self.matchColor(922, 1850, 124, 236, 229) == False:
            self.changeSortGift()
        else:
            print("Order is OK")
        
