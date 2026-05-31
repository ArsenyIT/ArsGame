class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = None          # текущее состояние (объект состояния)
        self.states = {}           # словарь {имя_состояния: объект}
        self.load_states()
        self.change_state("world") # начальное состояние

    def load_states(self):
        # Импортируй классы состояний (позже)
        from states.world_state import WorldState
        #from states.inventory_state import InventoryState
        # ... и так далее
        self.states["world"] = WorldState(self)
        #self.states["inventory"] = InventoryState(self)
        # ...

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