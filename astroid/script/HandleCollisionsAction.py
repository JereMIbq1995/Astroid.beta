
from astroid.cast.astroid import Astroid
from astroid.cast.ship import Ship
from astroid.cast.bullet import Bullet

from genie.script.action import UpdateAction
from genie.services.PygamePhysicsService import PygamePhysicsService

class HandleCollisionAction(UpdateAction):
    def __init__(self, priority):
        self._priority = priority
        self._ship = None
        self._physics_service = PygamePhysicsService()
    
    def _handle_bullet_astroid_col(self, actors, callback):
        bullets = []
        astroids = []
        for actor in actors:
            if isinstance(actor, Bullet):
                bullets.append(actor)
            elif isinstance(actor, Astroid):
                astroids.append(actor)
        
        for bullet in bullets:
            for astroid in astroids:
                if self._physics_service.check_collision(bullet, astroid):
                    callback.remove_actor(bullet)
                    callback.remove_actor(astroid)
    
    def _handle_ship_astroid_col(self, actors, callback):
        for actor in actors:
            if (isinstance(actor, Ship)):
                self._ship = actor
                break

        if self._ship != None:
            for actor in actors:
                if isinstance(actor, Astroid):
                    if self._physics_service.check_collision(self._ship, actor):
                        callback.remove_actor(self._ship)
                        callback.remove_actor(actor)
                        self._ship = None
                        break

    def execute(self, actors, actions, clock, callback):
        self._handle_bullet_astroid_col(actors, callback)
        self._handle_ship_astroid_col(actors, callback)
        pass