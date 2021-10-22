from genie.director import Director
from genie.services.PygameKeyboardService import PygameKeyboardService
from genie.services.PygamePhysicsService import PygamePhysicsService

from genie.cast.actor import Actor
from genie.script.action import Action


from astroid.cast.ship import Ship

from astroid.script.DrawFrameAction import DrawFrameAction
from astroid.script.HandleInputAction import HandleInputAction
from astroid.script.MoveActorsAction import MoveActorsAction
from astroid.script.SpawnAstroidsAction import SpawnAstroidsAction

W_SIZE = (500, 700)
START_POSITION = 200, 250
SHIP_WIDTH = 40
SHIP_LENGTH = 55

def main():

    # Create a director
    director = Director()

    # Create all the actors, including the player
    cast = []

    # Create the player
    player = Ship(path="astroid/assets/spaceship/spaceship_yellow.png", 
                    scale= 0.12,
                    x = W_SIZE[0]/2,
                    y = W_SIZE[1]/10 * 9,
                    rotation=180,
                    player_controlled=True)

    # Give actor(s) to the cast
    cast.append(player)

    # Create all the actions
    script = []

    # Create input actions
    handle_input = HandleInputAction(1, PygameKeyboardService())

    # Create update actions
    move_bodies = MoveActorsAction(1, PygamePhysicsService())
    spawn_astroid = SpawnAstroidsAction(1, W_SIZE)

    # Create output actions
    draw_frame = DrawFrameAction(1, W_SIZE)

    # Give action(s) to the script
    script.append(handle_input)
    script.append(move_bodies)
    script.append(spawn_astroid)
    script.append(draw_frame)

    # Give the cast and script to the dirrector by calling direct_scene.
    # direct_scene then runs the main game loop:
    director.direct_scene(cast, script)

if __name__ == "__main__":
    main()