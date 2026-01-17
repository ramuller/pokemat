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
    def get_current_screen(self):
        if self.ts.buttons.pokeball.search():
            return 'home'
        else:
            return 'unknown'
    
