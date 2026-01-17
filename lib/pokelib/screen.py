#
# This class handle all screen navigations
#

class Screen:
    def __init__(self, ts):
        self.ts = ts
        self.specs = ts.specs


    # Return the current screen by name
    # home - home screen
    # battle - battle screen
    # gym - gym battle screen
    # menu -
    def get_current_screen(self, verbose=0):
        if self.ts.buttons.pokeball.search(verbose=verbose):
            return 'home'
        else:
            return 'unknown'
    
    def go_home(self):

        while self.get_current_screen() != 'home':
            # self.color_show(300, 1803)
            # OK on green in the middle
            log.debug(f"Go home atempt {count}")
            if self.color_match(300, 1805, 150, 218, 151, debug=False):
                self.tap_screen(500, 1800)
            elif self.color_match(300, 1705, 150, 218, 151, debug=False):
                self.tap_screen(500, 1800)            
            elif self.color_match(500, 1828, 28, 135, 151, debug=False):
                self.tap_screen(500, 1828)            
            elif self.color_match(57, 365, 28, 135, 149, debug=False):
                self.tap_screen(57, 365)
            elif self.color_match(357, 1005, 150, 218, 151, debug=False):
                # Not exit pokemon
                # t,_ = self.pocr.find_regex('.*exit Pok.mon GO.*', verbose=0)
                mode = self.pocr.mode
                self.pocr.mode = "line"
                t,_ = self.pocr.regex('.*Do you want to exit Pok.*', verbose=0)
                self.pocr.mode = mode
                if not t:
                    self.tap_confirm()
                else:
                    # return to home
                    self.tap_screen(100, 100, button = 3)
            else:
                self.tap_screen(100, 100, button = 3)
            count += 1
            if count > MAX_TRYS:
                log.warn("No homescreen after {MAX_TRYS} atempts")
                print("Try egg")
                if self.egg_handle():
                    break
                self.buttons.dark('.*CANCEL.*', retries=1)

                # for y in range(100, self.maxY - 100, 25):
                #     if self.color_match(500, y, 116, 214, 156):
                #         print(f"Something green at {y}")
                #         b_text = self.pocr_read_line_center((500, y + 50), (100, 100))
                #         print(f"Button text {b_text}")
                #         if re.match(b_text, ".*CANCEL.*"):
                #             print("Found OK")
                #             self.tap_screen(b_text['center'])
                #             break
                count = 0
            sleep(1)

        if count == 0:
            log.info("No homescreen found!")
            return False
        log.info("Now we are on the home screen {}".format(self.is_home()))
        return True
