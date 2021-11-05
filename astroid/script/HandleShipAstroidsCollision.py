
from astroid.cast.astroid import Astroid
from astroid.cast.playerScore import PlayerScore
from astroid.cast.ship import Ship
from astroid.cast.bullet import Bullet

from genie.script.action import UpdateAction
from genie.services.PygamePhysicsService import PygamePhysicsService
from genie.services.PygameAudioService import PygameAudioService

class HandleShipAstroidsCollision(UpdateAction):
    def __init__(self, priority, physics_service, audio_service):
        self._priority = priority
        self._ship = None
        self._physics_service = physics_service
        self._audio_service = audio_service               

    def execute(self, actors, actions, clock, callback):
        """
            This action handles all collisions between the SHIP and the ASTROIDS
        """
        # First look for the ship
        if (self._ship == None):
            for actor in actors:
                if (isinstance(actor, Ship)):
                    self._ship = actor

        # Only worry about collision if the ship actually exists
        if self._ship != None:
            # Look through all the astroids, see if any collides with ship
            for actor in actors:
                if isinstance(actor, Astroid) and self._physics_service.check_collision(self._ship, actor):
                    callback.remove_actor(self._ship)
                    callback.remove_actor(actor)
                    self._audio_service.play_sound("astroid/assets/sound/explosion-01.wav", 0.1)
                    self._ship = None
                    break