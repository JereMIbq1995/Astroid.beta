from genie.script.action import OutputAction
from genie.services.PygameScreenService import PygameScreenService

class DrawFrameAction(OutputAction):
    def __init__(self, priority, window_size):
        super().__init__(priority)
        self._window_size = window_size
        self._screen_service = PygameScreenService(window_size)

    def get_priority(self):
        return super().get_priority()
    
    def set_priority(self, priority):
        return super().set_priority(priority)

    def execute(self, actors, actions, clock, callback):
        self._screen_service.draw_frame(actors)