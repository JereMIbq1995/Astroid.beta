import time

from genie.script.action import InputAction
from genie.services.PygameKeyboardService import PygameKeyboardService
from genie.services.PygameAudioService import PygameAudioService
from genie.services.constants import keys

from astroid.cast.ship import Ship
from astroid.cast.bullet import Bullet

VEL = 4
BULLET_VX = 0
BULLET_VY = -10
ATTACK_INTERVAL = 0.25   # seconds

class HandleShootingAction(InputAction):
    def __init__(self, priority, keyboard_service):
        super().__init__(priority)
        self._ship = None
        self._last_bullet_spawn = time.time()  # seconds
        self._keyboard_service = keyboard_service
        self._audio_service = PygameAudioService()
    
    def _spawn_bullet(self, clock, callback):
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
            callback.add_actor(bullet)

            # Play the shooting sound :)
            self._audio_service.play_sound("astroid/assets/sound/bullet_shot.wav", 0.1)

            # Record the time this bullet spawns
            self._last_bullet_spawn = time.time()

    def _get_ship(self, actors):
        """
            Look through the actors and return the ship.
            Returns None if Ship is not in the list.
        """
        for actor in actors:
            if(isinstance(actor, Ship)):
                return actor
        return None

    def execute(self, actors, actions, clock, callback):
        """
            Handle the shooting when the user presses SPACE
        """
        # Look for the ship first to make sure it's still alive
        self._ship = self._get_ship(actors)
        
        # If Space is pressed, spawn a bullet
        if self._keyboard_service.is_key_pressed(keys.SPACE):
            self._spawn_bullet(clock, callback)