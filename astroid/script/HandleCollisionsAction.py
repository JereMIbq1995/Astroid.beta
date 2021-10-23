
from astroid.cast.astroid import Astroid
from astroid.cast.ship import Ship
from astroid.cast.bullet import Bullet

from genie.script.action import UpdateAction
from genie.services.PygamePhysicsService import PygamePhysicsService

class HandleCollisionAction(UpdateAction):
    def __init__(self):
        pass
    
    def _handle_bullet_astroid_col(self, actors):
        # for actor in actors:
        #     if isinstance(Bullet):
        #         for a in actors:
        #             if a != actor:
        #                 actor.colliderect()
        pass
    
    def _handle_ship_astroid_col(self, actors):
        pass

    def execute(self, actors, actions, clock, callback):
        self._handle_bullet_astroid_col(actors)
        self._handle_ship_astroid_col(actors)
        pass