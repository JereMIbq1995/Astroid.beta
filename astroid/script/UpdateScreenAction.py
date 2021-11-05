from typing import Any
from genie.script.action import OutputAction

class UpdateScreenAction(OutputAction):
    def __init__(self, priority, screen_service):
        super().__init__(priority)
        self._score = None
        self._screen_service = screen_service

    def get_priority(self):
        return super().get_priority()
    
    def set_priority(self, priority):
        return super().set_priority(priority)

    def execute(self, actors, actions, clock, callback):
        self._screen_service.update_screen()