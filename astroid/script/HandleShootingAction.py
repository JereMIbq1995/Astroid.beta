from genie.script.action import InputAction
from genie.services.PygameKeyboardService import PygameKeyboardService
from genie.services.constants import keys

from astroid.cast.ship import Ship
from astroid.cast.bullet import Bullet

VEL = 4
BULLET_VX = 0
BULLET_VY = -10
ATTACK_INTERVAL = 20

class HandleShootingAction(InputAction):
    def __init__(self, priority, keyboard_service):
        super().__init__(priority)
        self._ship = None
        self._last_bullet_spawn = 0
        self._keyboard_service = keyboard_service
    
    def _spawn_bullet(self, clock, callback):
        time_since_last_shot = clock._frames - self._last_bullet_spawn
        if self._ship != None and time_since_last_shot >= ATTACK_INTERVAL:
            bullet_x = self._ship.get_x()
            bullet_y = self._ship.get_y() - (self._ship.get_height() / 2)
            
            bullet = Bullet("astroid/assets/bullet.png", 0.7, x = bullet_x, y = bullet_y, vx = BULLET_VX, vy = BULLET_VY)
            callback.add_actor(bullet)
            self._last_bullet_spawn = clock._frames

    def _get_ship(self, actors):
        for actor in actors:
            if(isinstance(actor, Ship)):
                self._ship = actor
                return
        self._ship = None

    def execute(self, actors, actions, clock, callback):        
        self._get_ship(actors)
        if self._keyboard_service.is_key_pressed(keys.SPACE):
            self._spawn_bullet(clock, callback)