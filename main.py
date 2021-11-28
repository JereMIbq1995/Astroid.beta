from genie.director import Director
from genie.services import *

from astroid.cast.ship import Ship
from astroid.cast.background import Background
from astroid.cast.startGameButton import StartGameButton

from astroid.script.HandleQuitAction import HandleQuitAction
from astroid.script.HandleShipMovementAction import HandleShipMovementAction
from astroid.script.HandleShootingAction import HandleShootingAction
from astroid.script.HandleStartGameAction import HandleStartGameAction

from astroid.script.MoveActorsAction import MoveActorsAction
from astroid.script.SpawnAstroidsAction import SpawnAstroidsAction
from astroid.script.HandleOffscreenAction import HandleOffscreenAction
from astroid.script.HandleShipAstroidsCollision import HandleShipAstroidsCollision
from astroid.script.HandleBulletsAstroidsCollision import HandleBulletsAstroidsCollision

from astroid.script.DrawActorsAction import DrawActorsAction
from astroid.script.UpdateScreenAction import UpdateScreenAction


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
                    width = 70,
                    height = 50,
                    x = W_SIZE[0]/2,
                    y = W_SIZE[1]/10 * 9,
                    # y = mother_ship.get_top_left()[1] - 30,
                    rotation=180)

    # Scale the background to have the same dimensions as the Window,
    # then position it at the center of the screen
    background_image = Background("astroid/assets/space.png", 
                                    width=W_SIZE[0],
                                    height=W_SIZE[1],
                                    x = W_SIZE[0]/2,
                                    y = W_SIZE[1]/2)

    # Start game button
    start_button = StartGameButton(path="astroid/assets/others/start_button.png",
                                    width = 305,
                                    height = 113,
                                    x = W_SIZE[0]/2,
                                    y = W_SIZE[1]/2)

    # Give actor(s) to the cast
    cast.append(background_image)
    cast.append(player)
    cast.append(start_button)

    # Initialize all services:
    # Initialize all services:
    service_code = 0
    while not (int(service_code) == 1 or int(service_code) == 2):
        service_code = str(input("What service would you like to use? (Input 1 for Pygame or 2 for Raylib): ")).strip()
        if not (int(service_code) == 1 or int(service_code) == 2):
            print (service_code)
            print("Incorrect input! Please try again!")

    if int(service_code) == 1:
        keyboard_service = PygameKeyboardService()
        physics_service = PygamePhysicsService()
        screen_service = PygameScreenService(W_SIZE)
        audio_service = PygameAudioService()
        mouse_service = PygameMouseService()
    elif int(service_code) == 2:
        keyboard_service = RaylibKeyboardService()
        physics_service = RaylibPhysicsService()
        screen_service = RaylibScreenService(W_SIZE)
        audio_service = RaylibAudioService()
        mouse_service = RaylibMouseService()

    # Create all the actions
    script = []

    # Create input actions
    script.append(HandleQuitAction(1, keyboard_service))

    # Add actions that must be added to the script when the game starts
    startgame_actions = []
    startgame_actions.append(HandleShootingAction(1, keyboard_service, audio_service))
    startgame_actions.append(HandleShipMovementAction(2, keyboard_service))
    startgame_actions.append(SpawnAstroidsAction(1, W_SIZE))
    script.append(HandleStartGameAction(2, mouse_service, physics_service, startgame_actions))

    # script.append(HandleShipMovementAction(2, keyboard_service))
    # script.append(HandleShootingAction(1, keyboard_service, audio_service))


    # Create update actions
    script.append(MoveActorsAction(1, physics_service))
    script.append(HandleOffscreenAction(1, W_SIZE))
    script.append(HandleShipAstroidsCollision(1, physics_service, audio_service))
    script.append(HandleBulletsAstroidsCollision(1, physics_service, audio_service))
    # script.append(SpawnAstroidsAction(1, W_SIZE))

    # Create output actions
    script.append(DrawActorsAction(1, screen_service))
    script.append(UpdateScreenAction(2, screen_service))

    # Give the cast and script to the dirrector by calling direct_scene.
    # direct_scene then runs the main game loop:
    director.direct_scene(cast, script)

if __name__ == "__main__":
    main()