# 2017.08.29 21:49:47 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/client/gui/shared/gui_items/dossier/achievements/SoldierOfFortuneAchievement.py
from dossiers2.ui.achievements import ACHIEVEMENT_BLOCK as _AB
from abstract import ClassProgressAchievement
from abstract.mixins import Fortification

class SoldierOfFortuneAchievement(Fortification, ClassProgressAchievement):

    def __init__(self, dossier, value = None):
        ClassProgressAchievement.__init__(self, 'soldierOfFortune', _AB.FORT, dossier, value)

    def getNextLevelInfo(self):
        return ('winsLeft', self._lvlUpValue)

    def _readProgressValue(self, dossier):
        return dossier.getRecordValue(_AB.FORT, 'soldierOfFortune')

    def _readCurrentProgressValue(self, dossier):
        return dossier.getFortSortiesStats().getWinsCount()
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\client\gui\shared\gui_items\dossier\achievements\SoldierOfFortuneAchievement.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:49:47 St�edn� Evropa (letn� �as)
