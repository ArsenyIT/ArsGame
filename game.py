from player import Player
from resource_manager import ResourceManager
from utils import resource_path

class Game:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.resources = ResourceManager()
        self.resources.load_all()
        self.player = Player()
        self.state = None          # Текущее состояние
        self.states = {}           # Словарь {имя_состояния: объект}
        self.load_states()
        self.change_state("world") # Начальное состояние
        self.selected_character_index = 0

    def load_states(self):
        from states.world_state import WorldState
        from states.inventory_state import InventoryState
        from states.character_state import CharacterState
        from states.map_state import MapState
        from states.quest_state import QuestState
        from states.tutorials_state import TutorialsState
        from states.party_state import PartyState
        from states.events_state import EventsState
        from states.battlepass_state import BattlepassState
        from states.gacha_state import GachaState
        from states.passport_state import PassportState
        from states.dialog_state import DialogState
        from states.shop_state import ShopState
        from states.settings_state import SettingsState
        from states.battle_state import BattleState
        from states.weapon_state import WeaponState
        from states.weapon_upgrade_state import WeaponUpgradeState
        from states.artifact_state import ArtifactState
        from states.artifact_upgrade_state import ArtifactUpgradeState
        from states.level_up_state import LevelUpState
        from states.talents_state import TalentsState
        from states.symbolism_state import SymbolismState

        self.states["world"] = WorldState(self)
        self.states["inventory"] = InventoryState(self)
        self.states["character"] = CharacterState(self)
        self.states["map"] = MapState(self)
        self.states["quest_log"] = QuestState(self)
        self.states["tutorials"] = TutorialsState(self)
        self.states["party"] = PartyState(self)
        self.states["events"] = EventsState(self)
        self.states["battlepass"] = BattlepassState(self)
        self.states["gacha"] = GachaState(self)
        self.states["passport"] = PassportState(self)
        self.states["dialog"] = DialogState(self)
        self.states["shop"] = ShopState(self)
        self.states["settings"] = SettingsState(self)
        self.states["battle"] = BattleState(self)
        self.states["weapon"] = WeaponState(self)
        self.states["weapon_upgrade"] = WeaponUpgradeState(self)
        self.states["artifact"] = ArtifactState(self)
        self.states["artifact_upgrade"] = ArtifactUpgradeState(self)
        self.states["level_up"] = LevelUpState(self)
        self.states["talents"] = TalentsState(self)
        self.states["symbolism"] = SymbolismState(self)

    def change_state(self, new_state_name):
        if self.state:
            self.state.on_exit()
        self.state = self.states[new_state_name]
        self.state.on_enter()

    def update(self, dt, events):
        if self.state:
            self.state.update(dt, events)

    def draw(self, screen):
        if self.state:
            self.state.draw(screen)

    def save_all(self):
        saved = False
        if self.player.inventory.modified:
            self.player.inventory.save(resource_path("assets/data/inventory.json"))
            saved = True
        if self.player.modified:
            self.player.save_party(resource_path("assets/data/party_save.json"))
            saved = True
        if saved:
            print("Всё сохранено")