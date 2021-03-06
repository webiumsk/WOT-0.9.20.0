# 2017.08.29 21:46:08 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/shared/ribbons_aggregator.py
import Event
import BattleReplay
from ids_generators import SequenceIDGenerator
from debug_utils import LOG_UNEXPECTED
from collections import defaultdict
from gui.Scaleform.genConsts.BATTLE_EFFICIENCY_TYPES import BATTLE_EFFICIENCY_TYPES
from BattleFeedbackCommon import BATTLE_EVENT_TYPE as _BET
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

class _Ribbon(object):
    __slots__ = ('_id',)

    def __init__(self, ribbonID):
        """
        Constructor. Creates a new ribbon from the given event feedback.
        
        :param ribbonID: Ribbon ID.
        """
        super(_Ribbon, self).__init__()
        self._id = ribbonID

    @classmethod
    def createFromFeedbackEvent(cls, ribbonID, event):
        raise NotImplementedError

    def getType(self):
        """
        Returns efficiency type (see BATTLE_EFFICIENCY_TYPES)
        """
        raise NotImplementedError

    def getID(self):
        """
        Returns ribbon's ID.
        """
        return self._id

    def aggregate(self, ribbon):
        if self._canAggregate(ribbon):
            self._aggregate(ribbon)
            return True
        return False

    def _aggregate(self, ribbon):
        pass

    def _canAggregate(self, ribbon):
        """
        Returns True if ribbon can aggregated data from the given one. False - otherwise.
        :param ribbon: An instance of _Ribbon derived class
        """
        return self.getType() == ribbon.getType()


class _BasePointsRibbon(_Ribbon):
    __slots__ = ('_points',)

    def __init__(self, ribbonID, points):
        super(_BasePointsRibbon, self).__init__(ribbonID)
        self._points = points

    @classmethod
    def createFromFeedbackEvent(cls, ribbonID, event):
        return cls(ribbonID, event.getExtra())

    def getType(self):
        raise NotImplementedError

    def getPoints(self):
        """
        Returns base points represented by int.
        """
        return self._points

    def _aggregate(self, ribbon):
        self._points += ribbon.getPoints()


class _BaseCaptureRibbon(_BasePointsRibbon):
    __slots__ = ('_sessionID',)

    def __init__(self, ribbonID, points, sessionID):
        super(_BaseCaptureRibbon, self).__init__(ribbonID, points)
        self._sessionID = sessionID

    @classmethod
    def createFromFeedbackEvent(cls, ribbonID, event):
        return cls(ribbonID, event.getExtra(), event.getTargetID())

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.CAPTURE

    def getSessionID(self):
        return self._sessionID

    def _canAggregate(self, ribbon):
        return super(_BaseCaptureRibbon, self)._canAggregate(ribbon) and self._sessionID == ribbon.getSessionID()


class _BaseDefenceRibbon(_BasePointsRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.DEFENCE


class _SingleVehicleRibbon(_Ribbon):
    __slots__ = ('_extraValue', '_targetVehID')

    def __init__(self, ribbonID, vehID, extraValue):
        super(_SingleVehicleRibbon, self).__init__(ribbonID)
        self._extraValue = extraValue
        self._targetVehID = vehID

    @classmethod
    def createFromFeedbackEvent(cls, ribbonID, event):
        return cls(ribbonID, event.getTargetID(), cls._extractExtraValue(event))

    def getType(self):
        raise NotImplementedError

    def getExtraValue(self):
        return self._extraValue

    def setExtraValue(self, value):
        self._extraValue = value

    def getVehicleID(self):
        return self._targetVehID

    @classmethod
    def _extractExtraValue(cls, event):
        """
        Extracts extra data from the given event. Note that the type of returned value
        should support operation +. Otherwise required to override _aggregate method.
        
        :param event:
        :return: An object supporting + operation.
        """
        raise NotImplementedError

    def _canAggregate(self, ribbon):
        return super(_SingleVehicleRibbon, self)._canAggregate(ribbon) and self.getVehicleID() == ribbon.getVehicleID()

    def _aggregate(self, ribbon):
        self._extraValue += ribbon.getExtraValue()


class _SingleVehicleDamageRibbon(_SingleVehicleRibbon):
    __slots__ = ()

    def getType(self):
        raise NotImplementedError

    @classmethod
    def _extractExtraValue(cls, event):
        return event.getExtra().getDamage()


class _CriticalHitRibbon(_SingleVehicleRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.CRITS

    @classmethod
    def _extractExtraValue(cls, event):
        return event.getExtra().getCritsCount()


class _TrackAssistRibbon(_SingleVehicleDamageRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.ASSIST_TRACK


class _RadioAssistRibbon(_SingleVehicleDamageRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.ASSIST_SPOT


class _EnemyKillRibbon(_SingleVehicleDamageRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.DESTRUCTION

    @classmethod
    def _extractExtraValue(cls, event):
        return 0


class _BlockedDamageRibbon(_SingleVehicleDamageRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.ARMOR


class _CausedDamageRibbon(_SingleVehicleDamageRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.DAMAGE


class _FireHitRibbon(_SingleVehicleDamageRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.BURN


class _RamHitRibbon(_SingleVehicleDamageRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.RAM


class _WorldCollisionHitRibbon(_SingleVehicleDamageRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.WORLD_COLLISION


class _ReceivedCriticalHitRibbon(_CriticalHitRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.RECEIVED_CRITS


class _SingleVehicleReceivedHitRibbon(_SingleVehicleRibbon):
    __slots__ = ()

    def getType(self):
        raise NotImplementedError

    @classmethod
    def _extractExtraValue(cls, event):
        return event.getExtra().getDamage()


class _ReceivedDamageHitRibbon(_SingleVehicleReceivedHitRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.RECEIVED_DAMAGE


class _ReceivedFireHitRibbon(_SingleVehicleReceivedHitRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.RECEIVED_BURN


class _ReceivedRamHitRibbon(_SingleVehicleReceivedHitRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.RECEIVED_RAM


class _ReceivedWorldCollisionHitRibbon(_SingleVehicleReceivedHitRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.RECEIVED_WORLD_COLLISION


class _StunAssistRibbon(_SingleVehicleDamageRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.STUN


class _MultiVehicleRibbon(_Ribbon):
    __slots__ = ('_hits',)

    def __init__(self, ribbonID, vehID, extraValue):
        super(_MultiVehicleRibbon, self).__init__(ribbonID)
        self._hits = defaultdict(int)
        self._hits[vehID] = extraValue

    @classmethod
    def createFromFeedbackEvent(cls, ribbonID, event):
        return cls(ribbonID, event.getTargetID(), cls._extractExtraValue(event))

    @classmethod
    def _extractExtraValue(cls, event):
        raise NotImplementedError

    def getVehIDs(self):
        return self._hits.keys()

    def getCount(self):
        return len(self._hits)

    def getExtraValue(self):
        return sum(self._hits.itervalues())

    def _aggregate(self, ribbon):
        for targetID, extra in ribbon._hits.iteritems():
            self._hits[targetID] += extra


class _EnemyDetectionRibbon(_MultiVehicleRibbon):
    __slots__ = ()

    def getType(self):
        return BATTLE_EFFICIENCY_TYPES.DETECTION

    @classmethod
    def _extractExtraValue(cls, event):
        return 0


class _RibbonClassFactory(object):
    __slots__ = ()

    def getRibbonClass(self, event):
        return None


class _RibbonSingleClassFactory(_RibbonClassFactory):
    __slots__ = ('__cls',)

    def __init__(self, ribbonCls):
        super(_RibbonSingleClassFactory, self).__init__()
        self.__cls = ribbonCls

    def getRibbonClass(self, event):
        return self.__cls


class _DamageRibbonClassFactory(_RibbonClassFactory):
    __slots__ = ('__damageCls', '__fireCls', '__ramCls', '__wcCls')

    def __init__(self, damageCls, fireCls, ramCls, wcCls):
        super(_DamageRibbonClassFactory, self).__init__()
        self.__damageCls = damageCls
        self.__fireCls = fireCls
        self.__ramCls = ramCls
        self.__wcCls = wcCls

    def getRibbonClass(self, event):
        damageExtra = event.getExtra()
        if damageExtra.isShot():
            ribbonCls = self.__damageCls
        elif damageExtra.isFire():
            ribbonCls = self.__fireCls
        elif damageExtra.isWorldCollision():
            ribbonCls = self.__wcCls
        else:
            ribbonCls = self.__ramCls
        return ribbonCls


class _AssistRibbonClassFactory(_RibbonClassFactory):
    __slots__ = ('__trackAssistCls', '__radioAssistCls', '__stunAssistCls')

    def __init__(self, trackAssistCls, radioAssistCls, stunAssistCls):
        super(_AssistRibbonClassFactory, self).__init__()
        self.__trackAssistCls = trackAssistCls
        self.__radioAssistCls = radioAssistCls
        self.__stunAssistCls = stunAssistCls

    def getRibbonClass(self, event):
        if event.getBattleEventType() == _BET.TRACK_ASSIST:
            return self.__trackAssistCls
        elif event.getBattleEventType() == _BET.RADIO_ASSIST:
            return self.__radioAssistCls
        elif event.getBattleEventType() == _BET.STUN_ASSIST:
            return self.__stunAssistCls
        else:
            return None


_RIBBON_TYPES_AGGREGATED_WITH_KILL_RIBBON = (BATTLE_EFFICIENCY_TYPES.DAMAGE,
 BATTLE_EFFICIENCY_TYPES.BURN,
 BATTLE_EFFICIENCY_TYPES.RAM,
 BATTLE_EFFICIENCY_TYPES.WORLD_COLLISION)
_RIBBON_TYPES_EXCLUDED_IF_KILL_RIBBON = (BATTLE_EFFICIENCY_TYPES.CRITS,)
_RIBBON_TYPES_EXCLUDED_IN_POSTMORTEM = (BATTLE_EFFICIENCY_TYPES.RECEIVED_CRITS,)
_NOT_CACHED_RIBBON_TYPES = (BATTLE_EFFICIENCY_TYPES.DETECTION, BATTLE_EFFICIENCY_TYPES.DEFENCE)
_ACCUMULATED_RIBBON_TYPES = (BATTLE_EFFICIENCY_TYPES.CAPTURE,)
_FEEDBACK_EVENT_TO_RIBBON_CLS_FACTORY = {FEEDBACK_EVENT_ID.PLAYER_CAPTURED_BASE: _RibbonSingleClassFactory(_BaseCaptureRibbon),
 FEEDBACK_EVENT_ID.PLAYER_DROPPED_CAPTURE: _RibbonSingleClassFactory(_BaseDefenceRibbon),
 FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY: _RibbonSingleClassFactory(_EnemyDetectionRibbon),
 FEEDBACK_EVENT_ID.PLAYER_USED_ARMOR: _RibbonSingleClassFactory(_BlockedDamageRibbon),
 FEEDBACK_EVENT_ID.PLAYER_DAMAGED_DEVICE_ENEMY: _RibbonSingleClassFactory(_CriticalHitRibbon),
 FEEDBACK_EVENT_ID.PLAYER_KILLED_ENEMY: _RibbonSingleClassFactory(_EnemyKillRibbon),
 FEEDBACK_EVENT_ID.ENEMY_DAMAGED_DEVICE_PLAYER: _RibbonSingleClassFactory(_ReceivedCriticalHitRibbon),
 FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY: _DamageRibbonClassFactory(damageCls=_CausedDamageRibbon, fireCls=_FireHitRibbon, ramCls=_RamHitRibbon, wcCls=_WorldCollisionHitRibbon),
 FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER: _DamageRibbonClassFactory(damageCls=_ReceivedDamageHitRibbon, fireCls=_ReceivedFireHitRibbon, ramCls=_ReceivedRamHitRibbon, wcCls=_ReceivedWorldCollisionHitRibbon),
 FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_KILL_ENEMY: _AssistRibbonClassFactory(trackAssistCls=_TrackAssistRibbon, radioAssistCls=_RadioAssistRibbon, stunAssistCls=_StunAssistRibbon),
 FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY: _AssistRibbonClassFactory(trackAssistCls=_TrackAssistRibbon, radioAssistCls=_RadioAssistRibbon, stunAssistCls=_StunAssistRibbon)}

def _createRibbonFromPlayerFeedbackEvent(ribbonID, event):
    etype = event.getType()
    if etype in _FEEDBACK_EVENT_TO_RIBBON_CLS_FACTORY:
        factory = _FEEDBACK_EVENT_TO_RIBBON_CLS_FACTORY[etype]
        ribbonCls = factory.getRibbonClass(event)
        if ribbonCls is not None:
            return ribbonCls.createFromFeedbackEvent(ribbonID, event)
    LOG_UNEXPECTED('Could not find a proper ribbon class associated with the given feedback event', event)
    return


class ATTACK_REASON(object):
    SHOT = 'shot'
    FIRE = 'fire'
    RAM = 'ramming'
    WORLD_COLLISION = 'world_collision'
    DEATH_ZONE = 'death_zone'
    DROWNING = 'drowning'
    GAS_ATTACK = 'gas_attack'
    OVERTURN = 'overturn'


class _RibbonsCache(object):
    __slots__ = ('__ribbons', '__typeToIDs')

    def __init__(self):
        super(_RibbonsCache, self).__init__()
        self.__ribbons = {}
        self.__typeToIDs = defaultdict(set)

    def clear(self):
        self.__ribbons.clear()
        self.__typeToIDs.clear()

    def get(self, ribbonID, default):
        return self.__ribbons.get(ribbonID, default)

    def pop(self, ribbonID):
        if ribbonID in self:
            ribbon = self.__ribbons.pop(ribbonID)
            self.__typeToIDs[ribbon.getType()].remove(ribbonID)
            return ribbon
        else:
            return None

    def add(self, ribbon):
        self[ribbon.getID()] = ribbon
        self.__typeToIDs[ribbon.getType()].add(ribbon.getID())

    def iterByType(self, ribbonType):
        for ribbonID in self.__typeToIDs[ribbonType]:
            yield self[ribbonID]

    def __contains__(self, ribbonID):
        return self.__ribbons.__contains__(ribbonID)

    def __iter__(self):
        return self.__ribbons.__iter__()

    def __len__(self):
        return self.__ribbons.__len__()

    def __getitem__(self, index):
        return self.__ribbons.__getitem__(index)

    def __setitem__(self, ribbonID, ribbon):
        return self.__ribbons.__setitem__(ribbonID, ribbon)


class RibbonsAggregator(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        super(RibbonsAggregator, self).__init__()
        self.__feedbackProvider = None
        self.__vehicleStateCtrl = None
        self.__cache = _RibbonsCache()
        self.__accumulatedRibbons = _RibbonsCache()
        self.__rules = {}
        self.__idGenerator = SequenceIDGenerator()
        self.onRibbonAdded = Event.Event()
        self.onRibbonUpdated = Event.Event()
        self.__isStarted = False
        self.__isSuspended = False
        self.__isInPostmortemMode = False
        return

    def start(self):
        self.__isStarted = True
        if self.__feedbackProvider is None:
            self.__feedbackProvider = self.sessionProvider.shared.feedback
            self.__feedbackProvider.onPlayerFeedbackReceived += self._onPlayerFeedbackReceived
        if self.__vehicleStateCtrl is None:
            self.__vehicleStateCtrl = self.sessionProvider.shared.vehicleState
            self.__vehicleStateCtrl.onPostMortemSwitched += self._onPostMortemSwitched
        return

    def suspend(self):
        if self.__isStarted:
            self.__isSuspended = True

    def resume(self):
        if self.__isSuspended:
            self.__isSuspended = False

    def stop(self):
        self.__isStarted = False
        self.__isSuspended = False
        self.clearRibbonsData()
        if self.__feedbackProvider is not None:
            self.__feedbackProvider.onPlayerFeedbackReceived -= self._onPlayerFeedbackReceived
            self.__feedbackProvider = None
        if self.__vehicleStateCtrl is None:
            self.__vehicleStateCtrl.onPostMortemSwitched -= self._onPostMortemSwitched
            self.__vehicleStateCtrl = None
        return

    def getRibbon(self, ribbonID):
        """
        Gets ribbon by the given ID.
        :param ribbonID: Ribbon ID.
        :return: ribbon or None.
        """
        return self.__cache.get(ribbonID, None)

    def resetRibbonData(self, ribbonID):
        """
        Reset ribbon's data by the given ID.
        :param ribbonID: ribbon ID
        """
        ribbon = self.__cache.pop(ribbonID)
        if ribbon is not None and ribbon.getType() in _ACCUMULATED_RIBBON_TYPES:
            self.__accumulatedRibbons.add(ribbon)
        return

    def clearRibbonsData(self):
        """
        Clears all cached ribbons.
        """
        self.__cache.clear()
        self.__accumulatedRibbons.clear()

    def _onPostMortemSwitched(self):
        """
        Callback on switching to the postmortem mode  (see VehicleStateController).
        """
        self.__isInPostmortemMode = True

    def _onPlayerFeedbackReceived(self, events):
        """
        Callback on player feedback event (see BattleFeedbackAdaptor).
        
        :param events: list of PlayerFeedbackEvent
        """

        def _ribbonsGenerator(events):
            for e in events:
                r = _createRibbonFromPlayerFeedbackEvent(self.__idGenerator.next(), e)
                if r is not None:
                    yield r

            return

        self._aggregateRibbons(_ribbonsGenerator(events))

    def _aggregateRibbons(self, ribbons):
        """
        Aggregates ribbons according to some rules and converts them to appropriate battle
        efficiency events (see _FEEDBACK_EVENT_TO_RIBBON_CLS). Puts ribbons to the inner cache
        and triggers appropriate RibbonsAggregator events.
        
        Note that knowledge about aggregation is kept in each ribbon type/class (see canAggregate
        method).
        
        :param ribbons: list of Ribbon derived instances
        """
        aggregatedRibbons = {}
        for ribbon in ribbons:
            if self.__isSuspended and ribbon.getType() not in _ACCUMULATED_RIBBON_TYPES:
                continue
            if ribbon.getType() in aggregatedRibbons:
                temporaryRibbons = aggregatedRibbons[ribbon.getType()]
                for temporaryRibbon in temporaryRibbons:
                    if temporaryRibbon.aggregate(ribbon):
                        break
                else:
                    temporaryRibbons.append(ribbon)

            else:
                aggregatedRibbons[ribbon.getType()] = [ribbon]

        filteredRibbons = self.__filterRibbons(aggregatedRibbons)
        sortedRibbons = self.__getSortedList(filteredRibbons)
        for ribbon in sortedRibbons:
            etype = ribbon.getType()
            if etype in _NOT_CACHED_RIBBON_TYPES:
                self.__cache.add(ribbon)
                self.onRibbonAdded(ribbon)
            else:
                for cachedRibbon in self.__cache.iterByType(etype):
                    if cachedRibbon.aggregate(ribbon):
                        if not self.__isSuspended:
                            self.onRibbonUpdated(cachedRibbon)
                        break
                else:
                    if etype in _ACCUMULATED_RIBBON_TYPES:
                        for accumulatedRibbon in self.__accumulatedRibbons.iterByType(etype):
                            if accumulatedRibbon.aggregate(ribbon):
                                if not self.__isSuspended:
                                    self.__accumulatedRibbons.pop(accumulatedRibbon.getID())
                                    self.__cache.add(accumulatedRibbon)
                                    self.onRibbonAdded(accumulatedRibbon)
                                break
                        else:
                            if self.__isSuspended:
                                self.__accumulatedRibbons.add(ribbon)
                            else:
                                self.__cache.add(ribbon)
                                self.onRibbonAdded(ribbon)
                    elif not self.__isSuspended:
                        self.__cache.add(ribbon)
                        self.onRibbonAdded(ribbon)

    def __filterRibbons(self, ribbons):
        if self.__isInPostmortemMode:
            for rType in _RIBBON_TYPES_EXCLUDED_IN_POSTMORTEM:
                if rType in ribbons:
                    del ribbons[rType]

        if BATTLE_EFFICIENCY_TYPES.DESTRUCTION in ribbons:
            killRibbons = dict(((r.getVehicleID(), r) for r in ribbons[BATTLE_EFFICIENCY_TYPES.DESTRUCTION]))
            damageRibbons = dict(((t, ribbons[t]) for t in _RIBBON_TYPES_AGGREGATED_WITH_KILL_RIBBON if t in ribbons))
            for rType, tmpRibbons in damageRibbons.iteritems():
                filteredRibbons = []
                for tmpRibbon in tmpRibbons:
                    if tmpRibbon.getVehicleID() in killRibbons:
                        killRibbon = killRibbons[tmpRibbon.getVehicleID()]
                        killRibbon.setExtraValue(killRibbon.getExtraValue() + tmpRibbon.getExtraValue())
                    else:
                        filteredRibbons.append(tmpRibbon)

                ribbons[rType] = filteredRibbons

            excludedRibbons = dict(((t, ribbons[t]) for t in _RIBBON_TYPES_EXCLUDED_IF_KILL_RIBBON if t in ribbons))
            for rType, tmpRibbons in excludedRibbons.iteritems():
                filteredRibbons = [ r for r in tmpRibbons if r.getVehicleID() not in killRibbons ]
                ribbons[rType] = filteredRibbons

        return ribbons

    def __getSortedList(self, ribbons):
        """
        Sort events according to the following rules:
        1. Enemy kill ribbon should appear at the end of the list.
        2. Enemy detection ribbon should appear at the top of the list.
        
        NOTE: according to aggregation rules, the output ribbons don't contain duplicates of
        ribbons with the same type). If there are a few ribbons with the same type in the
        server response, use the last one.
        
        :param ribbons: dict of ribbons to be resorted according to rules described above
                        and converted to the list without duplicates.
        
        :return: Sorted ribbons list.
        """

        def _sortKey(ribbon):
            """
            Routine to be used for sorting ribbons by time. Ribbon ID is used for comparing because
            it grows with time.
            :param ribbon: _Ribbon derived instance.
            """
            return ribbon.getID()

        sortedRibons = []
        if ribbons:
            killRibbons = ribbons.pop(BATTLE_EFFICIENCY_TYPES.DESTRUCTION, None)
            detectionRibbons = ribbons.pop(BATTLE_EFFICIENCY_TYPES.DETECTION, None)
            if detectionRibbons is not None:
                sortedRibons.extend(sorted(detectionRibbons, key=_sortKey))
            remaningRibbons = []
            for newRibbons in ribbons.itervalues():
                remaningRibbons.extend(newRibbons)

            sortedRibons.extend(sorted(remaningRibbons, key=_sortKey))
            if killRibbons is not None:
                sortedRibons.extend(sorted(killRibbons, key=_sortKey))
        return sortedRibons


class RibbonsAggregatorPlayer(RibbonsAggregator):

    def _onPlayerFeedbackReceived(self, events):
        if BattleReplay.g_replayCtrl.isTimeWarpInProgress:
            return
        super(RibbonsAggregatorPlayer, self)._onPlayerFeedbackReceived(events)


def createRibbonsAggregator():
    if BattleReplay.g_replayCtrl.isPlaying:
        return RibbonsAggregatorPlayer()
    else:
        return RibbonsAggregator()
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\client\gui\Scaleform\daapi\view\battle\shared\ribbons_aggregator.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:46:08 St�edn� Evropa (letn� �as)
