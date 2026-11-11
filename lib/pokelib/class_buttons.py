from .buttons import TextButton, TextFlat, IconButton
from .screen import ScreenRegion

class CButtAutoCatchConnect(TextFlat):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=False,
            threshold=180,
            xs=ts.rel_x(0.0),
            xe=ts.rel_x(0.5),
            ys=ts.rel_y(0.10),
            ye=ts.rel_y(0.35),
            ),  
            'connect')

class CButtAutoCatchPair(TextFlat):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=False,
            threshold=180,
            xs=ts.rel_x(0.6),
            xe=ts.rel_x(1.0),
            ys=ts.rel_y(0.30),
            ye=ts.rel_y(0.70),
            ),  
            'Pair')

class CButtCommonOK(TextButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=True,
            process=True,
            xs=ts.rel_x(0.1),
            xe=ts.rel_x(0.9),
            ys=ts.rel_y(0.1),
            ye=ts.rel_y(0.9),
            ),  
            'IENDS')

class CButtExit(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.38),
            xe=ts.rel_x(0.62),
            ys=ts.rel_y(0.85),
            ye=ts.rel_y(0.97)),
            'exits')

class CButtCatchBall(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.35),
            xe=ts.rel_x(0.65),
            ys=ts.rel_y(0.85),
            ye=ts.rel_y(1)),
            'catch_ball')

class CButtMeFriends(TextFlat):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            invert=False,
            process=False,
            threshold=180,
            xs=ts.rel_x(0.2),
            xe=ts.rel_x(0.8),
            ys=ts.rel_y(0.05),
            ye=ts.rel_y(0.25),
            ),  
            'IENDS')

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

class CButtTradeSelect(TextFlat):
    def __init__(self, ts, threshold=0):
        super().__init__(
            ScreenRegion(ts,
            process=True,
            threshold=threshold,
            xs=ts.rel_x(0.40),
            xe=ts.rel_x(0.80),
            ys=ts.rel_y(0.01), 
            ye=ts.rel_y(0.20)), 
            '.*POK.*MON')

class CButtSelectFirstPM(TextFlat):
    def __init__(self, ts, threshold=0):
        super().__init__(
            ScreenRegion(ts,
            process=True,
            threshold=220,
            xs=ts.rel_x(0.1),
            xe=ts.rel_x(0.90),
            ys=ts.rel_y(0.1), 
            ye=ts.rel_y(0.75)), 
            r'.*\d\d$')

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

class CButtRaidInvite(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.60),
            xe=ts.rel_x(0.99),
            ys=ts.rel_y(0.10),
            ye=ts.rel_y(0.50)),
            'raid_invite')

class CButtRaidInvite(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.60),
            xe=ts.rel_x(0.99),
            ys=ts.rel_y(0.10),
            ye=ts.rel_y(0.50)),
            'raid_invite')

class CButtGymPhotoDisc(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.8),
            xe=ts.rel_x(1),
            ys=ts.rel_y(0.85),
            ye=ts.rel_y(1.0)),
            'gym_photo_disk')

class CButtGymDefeat(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.8),
            xe=int(ts.specs['max_x']),
            ys=ts.rel_y(0.75),
            ye=ts.rel_y(0.90)),
            'gym_defeat')

class CButtGymDefeatInBattle(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.8),
            xe=ts.rel_x(1.0),
            ys=ts.rel_y(0.85),
            ye=ts.rel_y(0.95)),
            'gym_defeat_in_battle')

class CButtGymMyTeam(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.8),
            xe=ts.rel_x(1),
            ys=ts.rel_y(0.70),
            ye=ts.rel_y(0.90)),
            'gym_mine')

class CButtGymFeed(IconButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            xs=ts.rel_x(0.1),
            xe=ts.rel_x(0.9),
            ys=ts.rel_y(0.05),
            ye=ts.rel_y(0.20)),
            'gym_feed')

class CButtHealAll(TextButton):
    def __init__(self, ts):
        super().__init__(
            ScreenRegion(ts,
            process=True,
            invert=True,
            blur=0,
            xs=ts.rel_x(0),
            xe=ts.rel_x(1),
            ys=ts.rel_y(0.5
                        ),
            ye=ts.rel_y(1)),
            'HEAL|REVIVE|ALL')