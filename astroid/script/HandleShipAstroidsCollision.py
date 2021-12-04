
from astroid.cast.astroid import Astroid
from astroid.cast.ship import Ship

from genie.script.action import UpdateAction

class HandleShipAstroidsCollision(UpdateAction):
    def __init__(self, priority, physics_service, audio_service):
        self._priority = priority
        self._ship = None
        self._physics_service = physics_service
        self._audio_service = audio_service               

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
            This action handles all collisions between the SHIP and the ASTROIDS
        """
        # First look for the ship
        self._ship = actors.get_first_actor("ship")

        # Only worry about collision if the ship actually exists
        if self._ship != None:
            # Look through all the astroids, see if any collides with ship
            for actor in actors.get_actors("astroids"):
                if self._physics_service.check_collision(self._ship, actor):
                    actors.remove_actor("ship", self._ship)
                    actors.remove_actor("astroids", actor)
                    self._audio_service.play_sound("astroid/assets/sound/explosion-01.wav", 0.1)
                    self._ship = None
                    break