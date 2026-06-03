from player import Player

class Game:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.state = None          # текущее состояние (объект состояния)
        self.states = {}           # словарь {имя_состояния: объект}
        self.load_states()
        self.change_state("world") # начальное состояние
        self.player = Player()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

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