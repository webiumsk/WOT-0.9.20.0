# 2017.08.29 21:48:19 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ProfileSectionMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ProfileSectionMeta(BaseDAAPIComponent):

    def setActive(self, value):
        self._printOverrideError('setActive')

    def requestData(self, vehicleId):
        self._printOverrideError('requestData')

    def requestDossier(self, type):
        self._printOverrideError('requestDossier')

    def as_updateS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_update(data)

    def as_setInitDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_responseDossierS(self, battlesType, data, frameLabel, emptyScreenLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_responseDossier(battlesType, data, frameLabel, emptyScreenLabel)
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\client\gui\Scaleform\daapi\view\meta\ProfileSectionMeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:48:19 St�edn� Evropa (letn� �as)
