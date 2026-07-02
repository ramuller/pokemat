#
# This class handle all screen navigations
#

import re
from time import sleep
import logging
from datetime import datetime
from .structs import ScreenRegion
from .timeout_with_default import timeout_with_default


class Screen:
    def __init__(self, ts):
        self.ts = ts
        self.specs = ts.specs

    '''
    Some buttons ar over the home screen but the pokeball is still visible
    check if for those buttons
    '''
    def _button_over_home(self):
        if self.ts.buttons.b_passenger_fast.search():
            print('Passanger')


    # Return the current screen by name
    # home - home screen
    # battle - battle screen
    # gym - gym battle screen
    # menu -
    def get_current_screen(self, verbose=0, retries=1):
        if self.ts.buttons.i_pokeball.search(verbose=verbose, retries=retries):
            return 'home'
        elif self.is_in_items(verbose=0, retries=1):
            return 'items'
        elif self.is_in_gym():
            return 'gym'
        elif self.is_in_lobby():
            return 'lobby'
        elif self.is_in_pokestop():
            return 'pokestop'
        else:
            return 'unknown'
    
    def is_home(self, verbose=0, retries=1):
        if self.ts.buttons.i_pokeball.search(verbose=verbose, retries=retries):
            return True
        else:
            return False

    def is_in_items(self,verbose=0, retries=1):
        reg = ScreenRegion(self.ts, 
                           xs=self.ts.rel_x(0.35),
                           xe=self.ts.rel_x(0.65),
                           ys=self.ts.rel_y(0.03),
                           ye=self.ts.rel_y(0.10))
        if not self.ts.ocr.regex('.*ITEMS.*', reg, verbose=verbose, retries=retries):
            return False
        else:
            return True
        
    def is_in_pokemon(self,verbose=0, retries=1):
        reg = ScreenRegion(self.ts, 
                           ys=self.ts.rel_y(0.00),
                           ye=self.ts.rel_y(0.10),
                           process=True)
        if not self.ts.ocr.regex('.*POK.MON.*', reg, verbose=verbose, retries=retries):
            return False
        else:
            return True
        
    def is_in_gym(self):
        if not self.ts.buttons.i_gym_photo_disk.search(retries=1):
            return False
        else:
            return True

    def is_in_lobby(self):
        reg = ScreenRegion(self.ts, ys=self.ts.rel_y(0.03), \
                           ye=self.ts.rel_y(0.20), \
                           invert=True)
        lines = self.ts.ocr.read(reg)
        for l in lines:
            if l['text'] in ['QUIT','ITEMS', 'GROUP','CODE']:
                return True
        return False

       
    def is_in_pokestop(self):
        if not self.ts.buttons.i_poke_stop_check.search(retries=1):
            return False
        else:
            return True

    def go_pokemon(self):
        b = self.ts.buttons.t_pokemon_pokemon.press(retries=1, verbose=0)
        if b:
            print('Already on pogo screen')            
            return True
        self.go_home()
        sleep(1)
        if not self.ts.buttons.i_pokeball.press(retries=3):
            return False
        if not self.ts.buttons.t_menu_pokemon.press(where='under', 
                                                retries=3,
                                                verbose=0):
            return False
        return True


    def go_friends(self):
        b = self.ts.buttons.t_friends.press(retries=1)
        if not b:
            self.go_home()
            sleep(1)
            self.ts.buttons.c_avatar()
        reg = ScreenRegion(self.ts, xs=self.ts.rel_x(0.75))
        self.ts.buttons.i_x_clear_text.press(retries=1)
        if self.ts.buttons.t_friends.press(retries=10, verbose=0):
            startTime = datetime.now()
            reg = ScreenRegion(self, xs=self.ts.rel_x(0.25), xe=self.ts.rel_x(0.5), ys=self.ts.rel_y(0.3)) 
            reg_center = ScreenRegion(self.ts,
                        xs=self.ts.specs['max_x'] * 0.5,
                        xe=(self.ts.specs['max_x'] * 0.5),
                        ys=self.ts.specs['max_y'] * 0.37,
                        ye=self.ts.specs['max_y'] * 0.60)
            while (datetime.now() - startTime).total_seconds() < 30:
                if len(self.ts.ocr.regex('.*.....*', reg, retries=1)) > 0:
                    return True
                npa = self.ts.image.scan_region(reg_center)
                if npa.min() == npa.max():
                    print('Empty screen')
                    return True
                print(f'Time elapsed {(datetime.now() - startTime).total_seconds()}')
                sleep(1)
        self.go_home()
        raise Exception('Trainer screen timeout!')

    def go_gym(self):
        while not self.ts.buttons.i_gym_photo_disk.search(retries=1):
            print("Not in gym")
            self.ts.tap_screen(281, 339, scale=False)
            sleep(1)
        return True

    def go_battle(self):
        if self.ts.buttons.i_menu_battle.search(retries=1) is None:
            self.go_home()
            sleep(1)
            self.ts.buttons.i_pokeball.press(retries=3)
        b = self.ts.buttons.i_menu_battle.press(retries=5)
        return b

    def go_items(self):
        if self.ts.buttons.i_menu_items.search(retries=1) is None:
            self.go_home()
            sleep(1)
            self.ts.buttons.i_pokeball.press(retries=3)
        b = self.ts.buttons.i_menu_items.press(retries=5)
        return b

    @timeout_with_default(30, default=False, raise_on_timeout=False)    
    def go_eggs(self):
        b = self.ts.buttons.i_egg_select.search(retries=1)
        if b:
            return True
        else:
            self.go_home()
            sleep(1)
            self.ts.buttons.c_avatar()

        self.ts.buttons.i_exits.search(retries=10)
        while self.ts.buttons.b_me_egg.press(retries=1) is None:
            print("Not in egg screen")
            self.ts.scroll(0, 
                           self.ts.rel_y(-0.8),
                           sx=self.ts.rel_x(0.05),
                           sy=self.ts.rel_y(0.9))
            sleep(2)
        return True

    def deep_exit(self):
        self.ts.tap_screen(100, 100, button = 3)
        # Remove traced from screen debug
        self.ts.tap_screen(2, 2)
        sleep(1)
        self.ts.log.warn("No homescreen after {MAX_TRYS} atempts")
        print("Try egg")
        if self.ts.egg_handle():
            return
        print('Try rescue')
        if self.ts.buttons.b_lucky_egg.search(retries=1):
            self.ts.buttone.i_exits.press(retries=1)
            return
        if self.ts.buttons.b_grunt_rescue.press(retries=1):
            return
        print('Try passenger')
        if self.ts.buttons.b_passenger.press(retries=1):
            return
        # Abit tricke because the button is below the detected
        if self.ts.buttons.b_grunt_rematch.search(retries=1):
            b = self.ts.buttons.b_grunt_rematch.search(retries=1)
            print(f'Rematch text found {b}')
            ys = b['center'][1] + self.ts.rel_y(0.1)
            for y in range(ys, self.ts.rel_y(0.9), 5):
                self.ts.tap_screen(self.ts.rel_x(0.5), y, scale=False)
                sleep(0.1)
                if self.ts.screen.is_home():
                    print("Back home")
                    return
            return

        self.ts.buttons.t_cancel.press(retries=1)
        self.ts.buttons.b_yes.press(retries=1)

    def go_home(self):
        count = 1
        MAX_TRYS = 5
        print('screen go home')
        while self.get_current_screen() != 'home':
            # self.color_show(300, 1803)
            # OK on green in the middle
            count += 1
            if count > MAX_TRYS:
                self.deep_exit()
                count = 0
            
            if self.ts.buttons.i_exits.press(retries=1,verbose=0) or \
                        self.ts.buttons.i_button_ok.press() \
                        or self.ts.buttons.i_exit_man.press():
                sleep(1)
                continue
            elif self.ts.ocr.regex('exit'):
                self.ts.tap_screen(100, 100, button = 3)
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
            sleep(0.5)

        if count == 0:
            self.ts.log.info("No homescreen found!")
            return False
        self.ts.log.info("Now we are on the home screen")
        return True
