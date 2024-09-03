import requests
import logging
import time
import sys
from datetime import datetime

log = logging.getLogger("pokelib")

class pokeLibError(Exception):
    """Custom exception class."""
    pass

class TouchScreen:
    maxX = 1000
    maxY = 2000

    def __init__(self, tcpPort, scaleX = 0.576, scaleY = 0.512):
        self.log = logging.getLogger("pokelib")
        self.log.info("Pokemat phone : {}".format(tcpPort))
        self.url = "http://localhost:{}/v1".format(tcpPort)
        self.scaleX = scaleX
        self.scaleY = scaleY

    def scaleXY(self, x, y):
        x = x * self.scaleX
        y = y * self.scaleY
        return int(x), int(y)
        
    def writeToPhone(self, cmd):
        log.debug("Send CMD - {}".format(cmd))
        return requests.get("{}/{}".format(self.url, cmd))
        
    def click(self, x, y, button = 1, duration = 50):
        log.info("click {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/click:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.writeToPhone("click:{},{},{},{}".format(x,y,button, duration))
        log.info("Response : {}".format(response))
        time.sleep(0.001 * duration)
    
    def getRGB(self, x, y):
        x, y = self.scaleXY(x, y)
        response = self.writeToPhone("color:{},{}".format(x,y))           
        self.writeToPhone("color:{},{}\n".format(x,y))
        log.info("Response : {}".format(response.status_code))
        log.info("Response : {}".format(response.json()))
        rgb = response.json()
        return int(rgb["red"]), rgb["green"], rgb["blue"],
    
    def matchColor(self, x, y, r, g, b, threshold=10):
        rr, gg, bb = self.getRGB(x, y)
        if rr > r + threshold or  rr < r - threshold or \
            gg > g + threshold or  gg < g - threshold or \
            bb > b + threshold or  bb < b - threshold:
            return False
        return True
    
    def waitMatchColor(self, x, y, r, g, b, threashold=10, time_out_ms=10000, freq_in_s = 1, match=True):
        log.info("waitMatchColor x{},y{},r{},g{},b{},t{},to{},f{},m{}".format(x, y, r, g, b, threashold, time_out_ms, freq_in_s, match))
        startTime = datetime.now()
        while True:
            if self.matchColor(x, y, r, g, b, threshold=threashold) == match:
                return True
                
            if ((datetime.now() - startTime).total_seconds() * 1000) > time_out_ms:
                log.warn("Timeout waiting {}ms for x:{},y{} r{},g{},b{}".format(time_out_ms, x, y, r, g, b))
                r, g, b = self.getRGB(x, y)
                raise pokeLibError("Timeout waiting {}ms for x:{},y{} r{},g{},b{}".format(time_out_ms, x, y, r, g, b))
            time.sleep(freq_in_s)
    
    def waitMatchColorAndClick(self, x, y, r, g, b, threashold=10, time_out_ms=10000, freq_in_s = 1, match=True, delay=0.8):
        log.info("waitMatchColorAndClick x{},y{},r{},g{},b{},t{},to{},f{},m{}".format(x, y, r, g, b, threashold, time_out_ms, freq_in_s, match))
        time.sleep(delay)
        self.waitMatchColor(x, y, r, g, b, threashold, time_out_ms, freq_in_s, match)
        # time.sleep(0.)
        self.click(x, y)
        
    def tabScreenBack(self):
        self.click(501, 1800)
        
    def tabExitMode(self):
        self.click(85,190)
        
    def tabConfirm(self):
        self.click(357, 1005)
        
    def tabAvatar(self):
        self.click(121, 1800)
        
    def tabOK(self):
        self.matchColor(623,1062,83,212,162)
        self.click(623,1062)
        return True
    def tabSearch(self):
        self.waitMatchColor(626, 457, 78, 208, 175,time_out_ms=2000)
        self.click(626, 457)
        self.waitMatchColor(92, 1228, 32, 39, 41)
        
    def tabFriends(self):
        log.debug("tabFriends")
        while self.isFriendScreen() == False:
            self.click(493, 193)
            time.sleep(0.2)
        
    def tabTextOK(self):
        self.waitMatchColorAndClick(871, 1082, 34, 34, 34)
        
    def tabTextOK(self):
        self.waitMatchColorAndClick(871, 1082, 34, 34, 34)
        
    def tabFirstFriend(self):
        time.sleep(0.2)
        self.waitMatchColorAndClick(147, 808, 255, 255,255, match=False)
        
    def tabBattle(self):
        self.waitMatchColorAndClick(510, 1664, 95, 166, 83)
    
    def typeString(self, text):
        log.debug("type string {}".format(text))
        i = 0
        
        while i < len(text):
            c = text[i]
            i += 1
            if c == "\\":
                c = c + text[i]
                i += 1       
            self.writeToPhone("key:{}".format(c))
    
    def getTimeNow(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def isHome(self):
        return self.matchColor(517,1802,255,55,72,10)
    
    def isFriendScreen(self):
        return self.matchColor(32, 91, 255, 255, 255)

    def goHome(self):
        log.info("Go to homescreen")
        while self.isHome() == False:
            log.warning("Wrong color")
            if self.matchColor(501, 1826, 30, 134, 149):
                self.tabScreenBack()                
            elif self.matchColor(500, 1796, 246, 254, 244):
                log.debug("light green press?")
                self.tabScreenBack()
            elif self.matchColor(500, 1832, 240, 242, 230):
                log.debug("whith like gym press?")
                self.tabScreenBack()
            elif self.matchColor(86, 187, 27, 134, 148):
                self.tabExitMode()
            elif self.matchColor(357, 1005, 150, 218, 151):
                self.tabConfirm()
            else:
                if self.matchColor(64, 156, 255, 255, 255):
                    self.click(64, 156)
                elif self.waitMatchColor(57, 361, 28, 135, 149):
                    self.click(57, 361)
                else:
                    raise
            time.sleep(1)

    def selectLeague(self, league):
        if league == "great":
            log.info("Great League selected")
            y = 951
        elif league == "ultra":
            log.info("Ultra League selected")
            y = 1301
        elif league == "master":
            log.info("Master League selected")
            y = 1650
        else:
            raise pokeLibError("Uknow leage {}".format(league))
        
        self.waitMatchColor(350, y, 255, 255, 255)
        time.sleep(3)
        self.click(350, y)
        # Lets battle
        self.waitMatchColorAndClick(305, 1230, 161, 221, 148)
        
    def friendScreen(self):
        self.goHome()
        self.tabAvatar()
        self.tabFriends()
        
        
    def searchFriend(self, name):
        self.friendScreen()
        self.tabSearch()
        self.typeString(name)
        self.tabTextOK()
        self.tabFirstFriend()
        
    def inviteFriend(self, name, league):
        log.warning("Invite friend")
        self.searchFriend(name)
        self.tabBattle()
        self.selectLeague(league)
        
    def acceptBattleInvite(self):
        self.waitMatchColorAndClick(309, 1275, 157, 218, 150)
        
    def useThisParty(self):
        self.waitMatchColorAndClick(329, 1775, 163, 220, 148, threashold=20)
