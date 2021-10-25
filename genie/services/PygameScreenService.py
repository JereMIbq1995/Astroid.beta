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
        

        # rotation = actor.get_rotation()

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

    def draw_frame(self, actors, color = WHITE, background_image : Actor = None, lerp : float = 0):
        self.draw_background(color, background_image)
        self.draw_images(actors, lerp)
        pygame.display.update()


    def draw_background(self, color : tuple, background_image : Actor = None):
        self._window.fill(color)
        if background_image != None:
            topleft = background_image.get_top_left()
            path = background_image.get_path()
            image : pygame.Surface = None

            if path not in self._images_cache.keys():
                image = self._load_image(background_image, True)
            else:
                image = self._images_cache[path]
            
            assert(image != None)
            
            self._window.blit(image, topleft)
        
        # pygame.display.update()

    def draw_images(self, actors : list, lerp : float = 0):
        """
            actors: actors that need to be drew
            lerp: linear interpolation
        """
        for actor in actors:
            actor_topleft = actor.get_top_left()
            image_path = actor.get_path()
            image : pygame.Surface = None

            if image_path in self._images_cache.keys():
                image = self._images_cache[image_path]
            else:
                image = self._load_image(actor)
            
            assert(image != None)
            transformed_image = pygame.transform.rotate(
                    pygame.transform.scale(image, (actor.get_width(), actor.get_height())), 
                    actor.get_rotation())
            
            offset_x = (transformed_image.get_width() - actor.get_width()) / 2
            offset_y = (transformed_image.get_height() - actor.get_height()) / 2

            image_topleft = (actor_topleft[0] - offset_x, actor_topleft[1] - offset_y)
            self._window.blit(transformed_image, image_topleft)
            # pygame.draw.rect(self._window, (0,0,0), actor, width = 5)

        
        # pygame.display.update()

    def release(self):
        pass