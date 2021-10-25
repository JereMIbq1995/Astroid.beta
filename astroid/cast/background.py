from genie.cast.actor import Actor

class Background(Actor):
    def __init__(self, path: str, 
                scale: float = 1, 
                width: int = 0, 
                height: int = 0, 
                
                x: float = 0, 
                y: float = 0, 
                
                vx: float = 0, 
                vy: float = 0, 
                
                rotation: float = 0, 
                rotation_vel: float = 0, 
                player_controlled: bool = False):

        super().__init__(path, 
                        scale=scale, 
                        width=width, 
                        height=height, 
                        
                        x=x, 
                        y=y, 
                        
                        vx=vx, 
                        vy=vy, 
                        
                        rotation=rotation, 
                        rotation_vel=rotation_vel, 
                        player_controlled=player_controlled)