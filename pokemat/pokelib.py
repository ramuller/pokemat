class TouchScreen:
    def __init__(self, fifoName, scaleX = 0.576, scaleY = 0.512):
        log.info("Pokemat phone : {}".format(fifoName))
        fd = os.open("{}.sh".format(fifoName), os.O_RDWR|os.O_CREAT)
        self.fi = os.fdopen(fd, "r")
        self.fi.seek(0, 2)            
        self.fo = fifoName
        self.scaleX = scaleX
        self.scaleY = scaleY

    def scaleXY(self, x, y):
        x = x * self.scaleX
        y = y * self.scaleY
        return int(x), int(y)
        
    def writeToTouch(self, cmd):
        log.debug("Send CMD - {}".format(cmd))
        with open(self.fo, 'w') as fo:
            fo.write(cmd)
    
    def click(self, x, y, button = 1, duration = 20):
        x, y = self.scaleXY(x, y)
        self.writeToTouch("click:{},{},{},{}\n".format(x,y,button, duration))
        time.sleep(0.001 * duration)
    
    def getRGB(self, x, y):
        x, y = self.scaleXY(x, y)
        self.fi.seek(0, 2)            
        self.writeToTouch("color:{},{}\n".format(x,y))
        # time.sleep(1)
        l = ""
        while not "color" in l:
            l = self.fi.readline().rstrip()
            time.sleep(0.005)
        # Create a list
        ll = l.split(":")
        # create value list
        vl = ll[2].split(",")
        # print(vl)
        r,g,b = int(vl[2]), int(vl[3]), int(vl[4])
        log.debug("getRGB : x:{} y{}. r{} g{}, b{}".format(x, y, r, g,b))
        return r, g, b
    
    def matchColor(self, x, y, r, g, b, threshold=10):
        rr, gg, bb = self.getRGB(x, y)
        if rr > r + threshold or  rr < r - threshold or \
            gg > g + threshold or  gg < g - threshold or \
            bb > b + threshold or  bb < b - threshold:
            return False
        return True 
    
    def cancel(self):
        self.click(501, 1857)
        
    def exitMode(self):
        self.click(85,190)
        
    def home(self):
        log.info("Go to homescreen")
        while self.matchColor(517,1802,255,55,72,5) == False:
            if self.matchColor(468,1853,30,134,148):
                self.cancel()
            elif self.matchColor(85,190,28,135,150):
                self.cancel()
            else:
                raise Exception('home : Unknow situation!')
            sleep(1)
    
    def trainerScreen(self):
        pass
    