from genie.script.action import InputAction
from genie.services.PygameKeyboardService import PygameKeyboardService
from genie.services.constants import keys

VEL = 4

class HandleInputAction(InputAction):
    def __init__(self, priority, keyboard_service):
        super().__init__(priority)
        self._keyboard_service = keyboard_service
    
    def execute(self, actors, actions, clock, callback):
        if self._keyboard_service.is_quit():
            callback.on_stop()

        for actor in actors:
            if actor.player_controlled():
                keys_state = self._keyboard_service.get_keys_state(keys.LEFT, keys.RIGHT, keys.DOWN, keys.UP)
                if keys_state[keys.LEFT]:
                    actor.set_vx(-VEL)
                if keys_state[keys.RIGHT]:
                    actor.set_vx(VEL)
                if keys_state[keys.DOWN]:
                    actor.set_vy(VEL)
                if keys_state[keys.UP]:
                    actor.set_vy(-VEL)
                
                if not keys_state[keys.LEFT] and not keys_state[keys.RIGHT]:
                    actor.set_vx(0)
                if not keys_state[keys.UP] and not keys_state[keys.DOWN]:
                    actor.set_vy(0)