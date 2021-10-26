from typing import Tuple
import pygame

from genie.cast.actor import Actor

WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 0)

class PygameScreenService:
    """
        - add methods to the interface
            i.e. ScreenService.DrawImages(Actors)
            (this is in core)
        - create the trait Image
            i.e. image
        - Implement the methods in concrete class
            i.e. PygameScreenService
            A. Loop Through Actors
            If has Image trait:
                convert image data to what pygame needs
                use pygame to draw
    """
    def __init__(self, window_size):
        if not pygame.get_init():
            pygame.init()
        self._images_cache = {}
        self._window = pygame.display.set_mode(window_size)
    
    def initialize(self):
        pass
    
    def _load_image(self, actor : Actor, transform : bool = False):
        """
            Takes in an actor that has 2 traits: Body and Image
                and load the image of that Actor into the cache
        """
        image_path = actor.get_path()
        image = pygame.image.load(image_path)

        if transform:
            image = pygame.transform.rotate(
                pygame.transform.scale(image, (actor.get_width(), actor.get_height())), 
                actor.get_rotation())
        
        # put image in cache so we don't have to load again
        if (image_path not in self._images_cache.keys()):
            self._images_cache[image_path] = image

        return image

    def load_images(self, actors : list):
        """
            load all the images into a dictionary cache
        """
        for actor in actors:
            self._load_image(actor)

    def fill_screen(self, color = WHITE):
        """
            Fill the screen with a certain color
        """
        self._window.fill(color)

    def update_screen(self):
        """
            Actually putting whatever was drawn on to the screen
        """
        pygame.display.update()

    def draw_rectangle(self, center : Tuple, width : int, height: int, color : tuple = (0, 0, 0), 
                        border_width : int = 0, border_radius : int = 0, border_top_left_radius : int = -1,
                        border_top_right_radius : int = -1, border_bottom_left_radius : int = -1, 
                        border_bottom_right_radius : int = -1):
        """
            Draw a rectangle at the specified position
        """
        pygame.draw.rect(self._window, color, pygame.Rect(center[0] - width / 2, center[1] - height / 2, width, height),
                        border_width, border_radius, border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                        border_bottom_right_radius)
    
    def draw_circle(self, center, radius, color : tuple = (0, 0, 0), width : int = 0,
                    draw_top_right : bool = False, draw_top_left : bool = False, draw_bottom_left : bool = False, 
                    draw_bottom_right : bool = False):
        """
            Draw a circle at the specified position
        """
        pygame.draw.circle(self._window, color, center, radius, width, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)

    def draw_frame(self, actors, color = WHITE, background_image : Actor = None, lerp : float = 0):
        """
            Takes in a list of actors and a background image, then:
                - First, draw the background if it's given.
                    If background is not given, fill the screen the color given (default is WHITE)
                - Next, draw all the actors in the "actors" list on top of the background
                - Update display to show all the drawing.
        """
        self._draw_background(color, background_image)
        self._draw_images(actors, lerp)
        pygame.display.update()

    def _draw_background(self, color : tuple, background_image : Actor = None):
        """
            Simply draws the background
        """
        self._window.fill(color)
        if background_image != None:
            path = background_image.get_path()
            image = self._images_cache[path] if path in self._images_cache.keys() else self._load_image(background_image, True)
            self._window.blit(image, background_image.get_top_left())

    def _draw_images(self, actors : list, lerp : float = 0):
        """
            actors: actors that need to be drew
            lerp: linear interpolation
        """
        for actor in actors:
            actor_topleft = actor.get_top_left()
            path = actor.get_path()
            
            # Load image from cache or from file
            image = self._images_cache[path] if path in self._images_cache.keys() else self._load_image(actor)

            # Ensure that the image rotates when actor._rotation changes or when width and height change
            transformed_image = pygame.transform.rotate(
                    pygame.transform.scale(image, (actor.get_width(), actor.get_height())), 
                    actor.get_rotation())
            
            # Shift the image upward and to the left to account for pygame's way to do rotation
            offset_x = (transformed_image.get_width() - actor.get_width()) / 2
            offset_y = (transformed_image.get_height() - actor.get_height()) / 2
            image_topleft = (actor_topleft[0] - offset_x, actor_topleft[1] - offset_y)

            # Draw the image with pygame
            self._window.blit(transformed_image, image_topleft)

            # pygame.draw.rect(self._window, (0,0,0), actor, width = 5)

    def release(self):
        pass