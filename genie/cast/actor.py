from typing import overload
import pygame

class Actor(pygame.Rect):
    """
        A thing that participates in an animation. Anything that either MOVES, can be DRAWN
        on the screen, or BOTH is an actor.
        For the purpose of collision checking, all actors are represented with the shape of a RECTANGLE.
        
        Attributes:
            _x : the x coordinate of the center of the rectangle
            _y : the y coordinate of the position
            _vx : the horizontal velocity
            _vy : the vertical velocity
            _height : 
    """
    def __init__(self, path : str,
                    scale : float = 1,
                    width : int = 0,
                    height : int = 0,

                    x : float = 0, 
                    y : float = 0,
                    
                    vx : float = 0,
                    vy : float = 0,

                    rotation : float = 0,
                    rotation_vel : float = 0,
                    player_controlled : bool = False):
        """
            Initialize the actor using the image and
            a scaling factor, or width and height
        """

        self._path = path
        self._scale = scale

        self._vx = vx
        self._vy = vy

        self._rotation = rotation
        self._rotation_vel = rotation_vel
        self._player_controlled = player_controlled

        # If both the height and width are provided, use
        # it to initialize the triangle
        if (height != 0 and width != 0):
            left = int(x - width / 2)
            top = int(y - height / 2)
            super().__init__(left, top, width, height)
        
        # If either height and with are 0, use the scale
        else:
            wh = self._get_width_height()
            left = int(x - wh[0] / 2)
            top = int(y - wh[1] / 2)
            super().__init__(left, top, wh[0], wh[1])
    
    def _get_width_height(self):
        """
            Use the size of the image provided by the path and
            the scaling to figure out the size of the rectangular actor
        """
        image = pygame.image.load(self._path)
        width = int(self._scale * image.get_width())
        height = int(self._scale * image.get_height())
        return (width, height)
    
    # Path
    def get_path(self):
        return self._path
    
    def set_path(self, path):
        self._path = path
    
    # Getters and setters for width and height
    def get_width(self):
        return super().width
    
    def set_width(self, width):
        super().width = width
    
    def get_height(self):
        return super().height
    
    def set_height(self, height):
        super().height = height

    # Getters and setters for x and y
    def get_x(self):
        return super().centerx
    
    def set_x(self, x):
        vx = x - super().centerx
        super().move(vx, 0)
    
    def get_y(self):
        return super().centery
    
    def set_y(self, y):
        vy = y - super().centery
        super().move(0, vy)
    
    # Getters and setters for position
    def get_position(self):
        return (self.get_x(), self.get_y())
    
    def set_position(self, x, y):
        self.set_x(x)
        self.set_y(y)
    
    # Getters for top-left corner of the rectangle
    def get_top_left(self):
        return super().topleft
    
    # Getters and setters for velocity
    def get_vx(self):
        return self._vx
    
    def set_vx(self, vx):
        self._vx = vx
    
    def get_vy(self):
        return self._vy
    
    def set_vy(self, vy):
        self._vy = vy
    
    # Getters and setters for rotation and rotation velocity
    def get_rotation(self):
        return self._rotation
    
    def set_rotation(self, rotation):
        self._rotation = rotation

    def get_rotation_vel(self):
        return self._rotation_vel
    
    def set_rotation_vel(self, rotation_vel):
        self._rotation_vel = rotation_vel
    
    # Getter and setter for the player_controlled bool
    def player_controlled(self):
        return self._player_controlled
    
    def set_player_controlled(self, player_controlled):
        self._player_controlled = player_controlled

    # Move function
    def move_with_vel(self):
        """
            Simply add vx and vy onto x and y respectively
        """
        super().update(super().left + self._vx, super().top + self._vy, super().width, super().height)
    
    def rotate(self):
        self._rotation += self._rotation_vel
        
    # # In case the hit box needs to be updated
    # def update_hitbox(self, image : pygame.Surface):
    #     super().width = image.get_width()
    #     super().height = image.get_height()
