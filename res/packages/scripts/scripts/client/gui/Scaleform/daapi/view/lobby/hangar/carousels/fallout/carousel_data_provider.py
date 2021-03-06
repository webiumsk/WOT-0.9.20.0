# 2017.08.29 21:47:03 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/hangar/carousels/fallout/carousel_data_provider.py
from gui.Scaleform.locale.MENU import MENU
from gui.shared.gui_items.Vehicle import Vehicle
from gui.shared.formatters import text_styles
from gui.shared.utils.requesters import REQ_CRITERIA
from gui.Scaleform.daapi.view.lobby.hangar.carousels.basic.carousel_data_provider import HangarCarouselDataProvider
from gui.Scaleform.locale.FALLOUT import FALLOUT
from helpers import i18n

class FalloutCarouselDataProvider(HangarCarouselDataProvider):

    def __init__(self, carouselFilter, itemsCache, currentVehicle, falloutCtrl):
        super(FalloutCarouselDataProvider, self).__init__(carouselFilter, itemsCache, currentVehicle)
        self._baseCriteria = REQ_CRITERIA.INVENTORY
        self._falloutCtrl = falloutCtrl

    def _getVehicleDataVO(self, vehicle):
        vehicleData = super(FalloutCarouselDataProvider, self)._getVehicleDataVO(vehicle)
        if not self._falloutCtrl.isSuitableVeh(vehicle):
            infoText = i18n.makeString(MENU.tankcarousel_vehiclestates(Vehicle.VEHICLE_STATE.UNSUITABLE_TO_QUEUE))
            vehicleData.update({'infoText': text_styles.vehicleStatusInfoText(infoText)})
        if vehicle.isFalloutSelected:
            selectButtonLabel = FALLOUT.TANKCAROUSELSLOT_DEACTIVATEBUTTON
            selected = True
            selectable = True
            visible = True
            enabled = True
        else:
            selectButtonLabel = FALLOUT.TANKCAROUSELSLOT_ACTIVATEBUTTON
            selected = False
            selectable = vehicle.isFalloutAvailable and not vehicle.isDisabledInPremIGR
            visible = bool(self._falloutCtrl.getEmptySlots()) and self._falloutCtrl.getConfig().hasRequiredVehicles()
            enabled = self._falloutCtrl.canSelectVehicle(vehicle)
        vehicleData.update({'falloutCanBeSelected': selectable and visible,
         'falloutSelected': selected,
         'falloutButtonDisabled': not enabled,
         'selectButtonLabel': selectButtonLabel,
         'selectButtonTooltip': self._falloutCtrl.carouselSelectionButtonTooltip()})
        return vehicleData
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\client\gui\Scaleform\daapi\view\lobby\hangar\carousels\fallout\carousel_data_provider.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:47:03 St�edn� Evropa (letn� �as)
