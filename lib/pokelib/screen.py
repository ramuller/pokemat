#
# This class handle all screen navigations
#

from time import sleep
import logging
from datetime import datetime


class Screen:
    def __init__(self, ts):
        self.ts = ts
        self.specs = ts.specs

    '''
    Some buttons ar over the home screen but the pokeball is still visible
    check if for those buttons
    '''
    def _button_over_home(self):
        if self.ts.buttons.b_passanger_fast.search():
            print('Passanger')


    # Return the current screen by name
    # home - home screen
    # battle - battle screen
    # gym - gym battle screen
    # menu -
    def get_current_screen(self, verbose=0):
        if self.ts.buttons.i_pokeball.search(verbose=verbose):
            return 'home'
        else:
            return 'unknown'
        
    def go_gym(self):
        while not self.ts.buttons.i_gym_photo_disk.search(retries=1):
            print("Not in gym")
            self.ts.tap_screen(281, 339, scale=False)
            sleep(1)
        return True

    def is_in_gym(self):
        if not self.ts.buttons.i_gym_photo_disk.search(retries=1):
            return False
        else:
            return True

    def is_pokestop(self):
        if not self.ts.buttons.i_poke_stop_check.search(retries=1):
            return False
        else:
            return True

    def go_friends(self):
        if self.ts.buttons.text_only.press('.*IENDS.*', \
                                            xs=self.ts.rel_x(0.40), xe=self.ts.rel_x(0.60), \
                                            ys=self.ts.rel_y(0.05), ye=self.ts.rel_y(0.15), retries=1):
            return True
        self.go_home()
        sleep(1)
        self.ts.buttons.c_avatar()
        startTime = datetime.now()
        while (datetime.now() - startTime).total_seconds() < 30:
            self.ts.ocr.starty = int(self.ts.specs['max_y'] * 0.4)
            self.ts.ocr.starty = int(self.ts.specs['max_y'] * 0.7)
            t = self.ts.ocr.read()
            if len(t) > 5:
                sleep(1)
                return
        raise Exception('Trainer screen timeout!')

    def go_home(self):
        count = 1
        MAX_TRYS = 10
        while self.get_current_screen() != 'home':
            # self.color_show(300, 1803)
            # OK on green in the middle
            if self.ts.buttons.i_exits.press(retries=1):
                sleep(1)
                continue
            elif self.ts.color_match(357, 1005, 150, 218, 151, debug=False):
                # Not exit pokemon
                # t,_ = self.ts.ocr.find_regex('.*exit Pok.mon GO.*', verbose=0)
                mode = self.ts.ocr.mode
                self.ts.ocr.mode = "line"
                t,_ = self.ts.ocr.regex('.*Do you want to exit Pok.*', verbose=0)
                self.ts.ocr.mode = mode
                if not t:
                    self.ts.tap_confirm()
                else:
                    # return to home
                    self.ts.tap_screen(100, 100, button = 3)
            count += 1
            if count > MAX_TRYS:
                self.ts.tap_screen(100, 100, button = 3)
                self.ts.log.warn("No homescreen after {MAX_TRYS} atempts")
                print("Try egg")
                if self.ts.egg_handle():
                    break
                self.ts.buttons.dark('.*CANCEL.*', retries=1)

                # for y in range(100, self.ts.maxY - 100, 25):
                #     if self.ts.color_match(500, y, 116, 214, 156):
                #         print(f"Something green at {y}")
                #         b_text = self.ocr_read_line_center((500, y + 50), (100, 100))
                #         print(f"Button text {b_text}")
                #         if re.match(b_text, ".*CANCEL.*"):
                #             print("Found OK")
                #             self.tap_screen(b_text['center'])
                #             break
                count = 0
            if self.ts.buttons.dark('.*PASSENGER.*', retries=1):
                continue
            print('Passanger')
            sleep(0.5)

        if count == 0:
            self.ts.log.info("No homescreen found!")
            return False
        self.ts.log.info("Now we are on the home screen")
        return True
