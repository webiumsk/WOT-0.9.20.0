# 2017.08.29 21:48:04 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCOutroVideoPageMeta.py
from gui.Scaleform.framework.entities.View import View

class BCOutroVideoPageMeta(View):

    def videoFinished(self):
        self._printOverrideError('videoFinished')

    def handleError(self, data):
        self._printOverrideError('handleError')

    def as_playVideoS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_playVideo(data)
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\client\gui\Scaleform\daapi\view\meta\BCOutroVideoPageMeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:48:04 St�edn� Evropa (letn� �as)
