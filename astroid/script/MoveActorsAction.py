from genie.script.action import UpdateAction
from genie.services.PygamePhysicsService import PygamePhysicsService

class MoveActorsAction(UpdateAction):
    def __init__(self, priority, physics_service):
        super().__init__(priority=priority)
        self._physics_service = physics_service

    def execute(self, actors, actions, clock, callback):
        self._physics_service.move_actors(actors)
        self._physics_service.rotate_actors(actors)