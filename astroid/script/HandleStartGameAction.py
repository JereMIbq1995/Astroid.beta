from genie.script.action import InputAction
from genie.services import mouse

from astroid.cast.startGameButton import StartGameButton

class HandleStartGameAction(InputAction):
    def __init__(self, priority, mouse_service, physics_service, actions):
        super().__init__(priority)
        self._mouse_service = mouse_service
        self._physics_service = physics_service
        self._actions = actions

    def _get_start_button(self, actors):
        for actor in actors:
            if isinstance(actor, StartGameButton):
                return actor
        return None

    def execute(self, actors, actions, clock, callback):
        """
            When left mouse is clicked:
                - check to see if the mouse coordinate collides with the start game button
                - if the mouse collides with the button:
                    + remove the button (or switch it to the "clicked" state)
                    + add handleShipMovementAction to the script
                    + add spawnAstroidAction to the script
        """
        start_button = self._get_start_button(actors)
        mouse_pos = self._mouse_service.get_current_coordinates()

        if start_button != None \
            and self._mouse_service.is_button_down(mouse.LEFT) \
            and self._physics_service.check_collision_point(start_button, mouse_pos):
                callback.remove_actor(start_button)
                callback.remove_action(self)
                for action in self._actions:
                    callback.add_action(action)