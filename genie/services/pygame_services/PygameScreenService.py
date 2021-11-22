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

    # def get_text_image(self):
    #     font = pygame.font.SysFont(font, font_size)
    #     text_image = font.render(text, antialias, color)

    def draw_text(self, text : str, font : str = None, font_size : int = 24, 
                    color : tuple = (0, 0, 0), position : tuple = (0, 0),
                    antialias : bool = True, position_center : bool = False):
        """
            Draw the input text (str).
            Inputs:
                - text: The text you want to draw
                - font: The font you want to use (try to find out what's
                        available on your system first)
                - font_size: default is 24
                - color: An RGB tuple. (0,0,0) is BLACK, and (255,255,255) is WHITE
                        You can also pass a 4 entries tuple. the 4th entry determines opacity
                - position: A tuple in the form of (x, y)
                - antialias: Boolean. Default is True
                - position_center: A boolean that tells whether the position given should be
                                    the center of the text image or the top-left corner.
                        + True: treats the position as the center of the text image
                        + False: treats the position as the top-left corner of the text image

        """
        font = pygame.font.SysFont(font, font_size)
        text_image = font.render(text, antialias, color)
        txt_img_position = position
        if (position_center):
            txt_img_position = (position[0] - text_image.get_width()/2, position[1] - text_image.get_height()/2)
        self._window.blit(text_image, txt_img_position)

    def draw_rectangle(self, center : Tuple, width : int, height: int, color : tuple = (0, 0, 0), 
                        border_width : int = 0, border_radius : int = 0, border_top_left_radius : int = -1,
                        border_top_right_radius : int = -1, border_bottom_left_radius : int = -1, 
                        border_bottom_right_radius : int = -1):
        """
            Draw a rectangle.

            Input:
                - center: An (x, y) tuple indicating the center of the rectangle
                - width: the width of the rectangle
                - height: the height of the rectangle
                - color: An RGB tuple. (0,0,0) is BLACK, and (255,255,255) is WHITE
                        You can also pass a 4 entries tuple. the 4th entry determines opacity
                - border_width: how many pixels you want the border to be
                
                - border_radius, border_..._radius: use these parameters if you want your rectangle
                                     to have rounded corners.
                                        + values < 1 means squared corners
                                        + values >= 1 means rounded corners. Increase this
                                            to increase the roundness
        """
        pygame.draw.rect(self._window, color, pygame.Rect(center[0] - width / 2, center[1] - height / 2, width, height),
                        border_width, border_radius, border_top_left_radius, border_top_right_radius, border_bottom_left_radius,
                        border_bottom_right_radius)
    
    def draw_circle(self, center, radius, color : tuple = (0, 0, 0), width : int = 0,
                    draw_top_right : bool = False, draw_top_left : bool = False, draw_bottom_left : bool = False, 
                    draw_bottom_right : bool = False):
        """
            Draw a circle.

            Input:
                - center: A tuple represents center of the circle (x, y)
                - radius: Well...
                - color: RGB tuple (0,0,0) is BLACK, (255,255,255) is WHITE.
                        Can also use 4th entry to specify opacity
                - width: How bold you want the border of the circle to be

                - draw_top_..., draw_bottom_...: Boolean. Use these parameters if want to draw
                    only parts of the circle (top left, top right, bottom left, bottom right)
        """
        pygame.draw.circle(self._window, color, center, radius, width, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)
    
    def draw_actors(self, actors : list, lerp : float = 0):
        """
            Draw all the actors in the "actors" list in order:
                    First thing in the list gets drawn first.

            actors: actors that need to be drawn
            lerp: linear interpolation
        """
        for actor in actors:
            actor_topleft = actor.get_top_left()
            path = actor.get_path()
            
            try:
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

                # The following lines of code when un-comment show the hit box of the actor AND the boundary of the image (the 2 are different)
                # pygame.draw.rect(self._window, (0,0,0), pygame.Rect(actor_topleft[0], actor_topleft[1], actor.get_width(), actor.get_height()), width = 5)
                # pygame.draw.rect(self._window, (0,0,0), pygame.Rect(image_topleft[0], image_topleft[1], transformed_image.get_width(), transformed_image.get_height()), width = 5)
            except:
                pass
        
        

    def release(self):
        pass