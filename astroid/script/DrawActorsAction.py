from genie.script.action import OutputAction

class DrawActorsAction(OutputAction):
    def __init__(self, priority, screen_service):
        super().__init__(priority)
        self._screen_service = screen_service

    def get_priority(self):
        return super().get_priority()
    
    def set_priority(self, priority):
        return super().set_priority(priority)

    def execute(self, actors, actions, clock, callback):
        """
            Take advantage of the screen_service's draw_actors function
        """
        self._screen_service.draw_actors(actors.get_all_actors())
        # self._screen_service.draw_actors(actors.get_actors("background_image"))
        # self._screen_service.draw_actors(actors.get_actors("score"))
        # self._screen_service.draw_actors(actors.get_actors("ship"))
        # self._screen_service.draw_actors(actors.get_actors("mother_ship"))
        # self._screen_service.draw_actors(actors.get_actors("start_button"))
        # self._screen_service.draw_actors(actors.get_actors("astroids"))
        # self._screen_service.draw_actors(actors.get_actors("bullets"))