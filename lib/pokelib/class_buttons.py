from .buttons import TextButton, TextFlat, IconButton
from .screen import ScreenRegion

class CButtFriendTrade(TextFlat):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.05),
            xe=ts.rel_x(.5),
            ys=ts.rel_y(0.8),
            ye=ts.rel_y(1)),
            'LOCAL')

class CButtYes(TextButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=True,
            blur=1,
            # color='red',
            threshold=100,
            xs=ts.rel_x(0.00),
            xe=ts.rel_x(0.99),
            ys=ts.rel_y(0.30),
            ye=ts.rel_y(0.80)),
            'YES')

class CButtTradeConfirm(TextFlat):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=True,
            xs=ts.rel_x(0.0),
            xe=ts.rel_x(.5),
            ys=ts.rel_y(0.2),
            ye=ts.rel_y(0.8),
            ),  
            'CONFIRM')

class CButtCatchBerrie(TextFlat):
    def __init__(self, ts, threshold=0):
        super().__init__(
            ScreenRegion(ts,
            threshold=threshold,
            ys=ts.rel_y(0.40),
            ye=ts.rel_y(0.72)), 
            'Berry')


class CButtTradeNext(TextButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=True,
            xs=ts.rel_x(0),
            xe=ts.rel_x(1),
            ys=ts.rel_y(0.5),
            ye=ts.rel_y(1)),
            'NEXT')

class CButtRaidChallange(TextButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=True,
            xs=ts.rel_x(0),
            xe=ts.rel_x(1),
            ys=ts.rel_y(0.5),
            ye=ts.rel_y(1)),
            'CHALLENGE')

class CButtRaidRescue(TextButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=True,
            xs=ts.rel_x(0),
            xe=ts.rel_x(1),
            ys=ts.rel_y(0.5),
            ye=ts.rel_y(1)),
            'RESCUE')

class CButtRaidGoToSummary(TextButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=True,
            xs=ts.rel_x(0),
            xe=ts.rel_x(1),
            ys=ts.rel_y(0.5),
            ye=ts.rel_y(1)),
            'SUMMARY')

class CButtRaidInvite10(TextButton):
    def __init__(self, ts, threshold=50, verbose=0):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=True,
            threshold=threshold,
            xs=ts.rel_x(0),
            xe=ts.rel_x(1),
            ys=ts.rel_y(0.20),
            ye=ts.rel_y(0.80)),
            'INVITE')

class CButtRaidInvite(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.60),
            xe=ts.rel_x(0.99),
            ys=ts.rel_y(0.10),
            ye=ts.rel_y(0.50)),
            'raid_invite')
