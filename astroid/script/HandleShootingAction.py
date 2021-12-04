import time

from genie.script.action import InputAction
from genie.services import keys

from astroid.cast.bullet import Bullet

BULLET_VX = 0
BULLET_VY = -10
ATTACK_INTERVAL = 0.25   # seconds

class HandleShootingAction(InputAction):
    def __init__(self, priority, keyboard_service, audio_service):
        super().__init__(priority)
        self._ship = None
        self._last_bullet_spawn = time.time()  # seconds
        self._keyboard_service = keyboard_service
        self._audio_service = audio_service
    
    def _spawn_bullet(self, clock, actors):
        """
            Only spawn a bullet if:
                - The time from the last time bullet spawn until now is >= ATTACK_INTERVAL
                - The ship is still alive (not None)
        """
        time_since_last_shot = time.time() - self._last_bullet_spawn     #Measured in seconds
        if self._ship != None and time_since_last_shot >= ATTACK_INTERVAL:
            # Bullet's starting position should be right on top of the ship
            bullet_x = self._ship.get_x()
            bullet_y = self._ship.get_y() - (self._ship.get_height() / 2)
            
            # Spawn bullet
            bullet = Bullet("astroid/assets/bullet.png", 20, 30, x = bullet_x, y = bullet_y, vx = BULLET_VX, vy = BULLET_VY)
            actors.add_actor("bullets", bullet)

            # Play the shooting sound :)
            self._audio_service.play_sound("astroid/assets/sound/bullet_shot.wav", 0.1)

            # Record the time this bullet spawns
            self._last_bullet_spawn = time.time()

    def execute(self, actors, actions, clock, callback):
        """
            Handle the shooting when the user presses SPACE
        """
        # Look for the ship first to make sure it's still alive
        self._ship = actors.get_first_actor("ship")
        
        # If Space is pressed, spawn a bullet
        if self._keyboard_service.is_key_down(keys.SPACE):
            self._spawn_bullet(clock, actors)