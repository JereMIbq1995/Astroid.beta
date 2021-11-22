from genie.script.action import InputAction
from genie.services import keys

from astroid.cast.ship import Ship

VEL = 4

class HandleShipMovementAction(InputAction):
    def __init__(self, priority, keyboard_service):
        super().__init__(priority)
        self._keyboard_service = keyboard_service
        self._ship = None
    
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
            This action handles the movement of the ship
        """
        # Look for the ship among the actors if we haven't already known it
        self._ship = self._get_ship(actors)
        
        # Don't worry about it if ship doesn't exist
        if (self._ship != None):
            # Check which keys are pressed and update the ship's velocity accordingly
            keys_state = self._keyboard_service.get_keys_state(keys.LEFT, keys.RIGHT, keys.DOWN, keys.UP)
            if keys_state[keys.LEFT]:
                self._ship.set_vx(-VEL)
            if keys_state[keys.RIGHT]:
                self._ship.set_vx(VEL)
            if keys_state[keys.DOWN]:
                self._ship.set_vy(VEL)
            if keys_state[keys.UP]:
                self._ship.set_vy(-VEL)
            
            # If keys in either dirrection are not pressed, set velocity of that direction to 0
            if not keys_state[keys.LEFT] and not keys_state[keys.RIGHT]:
                self._ship.set_vx(0)
            if not keys_state[keys.UP] and not keys_state[keys.DOWN]:
                self._ship.set_vy(0)