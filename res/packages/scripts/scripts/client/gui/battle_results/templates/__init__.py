# 2017.08.29 21:44:48 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/client/gui/battle_results/templates/__init__.py
from gui.battle_results.components import base
from gui.battle_results.templates.cybersport import CYBER_SPORT_BLOCK
from gui.battle_results.templates.fallout import FALLOUT_COMMON_STATS_BLOCK
from gui.battle_results.templates.fortification import STRONGHOLD_BATTLE_COMMON_STATS_BLOCK
from gui.battle_results.templates.regular import MULTI_TEAM_TABS_BLOCK
from gui.battle_results.templates.regular import REGULAR_TABS_BLOCK
from gui.battle_results.templates.regular import VEHICLE_PROGRESS_STATS_BLOCK
from gui.battle_results.templates.regular import QUESTS_PROGRESS_STATS_BLOCK
from gui.battle_results.templates.regular import REGULAR_COMMON_STATS_BLOCK
from gui.battle_results.templates.regular import REGULAR_PERSONAL_STATS_BLOCK
from gui.battle_results.templates.regular import REGULAR_TEAMS_STATS_BLOCK
from gui.battle_results.templates.regular import REGULAR_TEXT_STATS_BLOCK
from gui.battle_results.templates.regular import CLAN_TEXT_STATS_BLOCK
from gui.battle_results.templates.sandbox import SANDBOX_PERSONAL_STATS_BLOCK
from gui.battle_results.templates.sandbox import SANDBOX_TEAM_ITEM_STATS_ENABLE
from gui.battle_results.templates.sandbox import SANDBOX_PERSONAL_ACCOUNT_DB_ID
from gui.battle_results.templates.ranked_battles import RANKED_COMMON_STATS_BLOCK
from gui.battle_results.templates.ranked_battles import RANKED_TEAMS_STATS_BLOCK
from gui.battle_results.templates.ranked_battles import RANKED_RESULTS_BLOCK
from gui.battle_results.templates.ranked_battles import RANKED_RESULTS_BLOCK_TITLE
from gui.battle_results.templates.ranked_battles import RANKED_RESULTS_TEAMS_STATS_BLOCK
__all__ = ('TOTAL_VO_META', 'MULTI_TEAM_TABS_BLOCK', 'REGULAR_TABS_BLOCK', 'VEHICLE_PROGRESS_STATS_BLOCK', 'QUESTS_PROGRESS_STATS_BLOCK', 'REGULAR_COMMON_STATS_BLOCK', 'REGULAR_PERSONAL_STATS_BLOCK', 'REGULAR_TEAMS_STATS_BLOCK', 'REGULAR_TEXT_STATS_BLOCK', 'CLAN_TEXT_STATS_BLOCK', 'STRONGHOLD_BATTLE_COMMON_STATS_BLOCK', 'FALLOUT_COMMON_STATS_BLOCK', 'CYBER_SPORT_BLOCK', 'SANDBOX_PERSONAL_STATS_BLOCK', 'SANDBOX_TEAM_ITEM_STATS_ENABLE', 'SANDBOX_PERSONAL_ACCOUNT_DB_ID', 'RANKED_COMMON_STATS_BLOCK', 'RANKED_TEAMS_STATS_BLOCK', 'RANKED_RESULTS_BLOCK', 'RANKED_RESULTS_BLOCK_TITLE')
TOTAL_VO_META = base.DictMeta({'personal': {},
 'common': {},
 'team1': [],
 'team2': [],
 'textData': {},
 'quests': None,
 'unlocks': [],
 'tabInfo': [],
 'cyberSport': None,
 'isFreeForAll': False,
 'closingTeamMemberStatsEnabled': True,
 'selectedTeamMemberId': -1})
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\client\gui\battle_results\templates\__init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:44:48 St�edn� Evropa (letn� �as)
