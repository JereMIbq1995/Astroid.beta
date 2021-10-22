"""
Copyright 2021, BYU-Idaho.
Author(s): Matt Manley, Jacob Oliphant
Version: 1.0
Date: 27-01-2021
"""
from .clock import Clock
from .script.action import Action
from .script.action import InputAction
from .script.action import OutputAction
from .script.action import UpdateAction


class Director(Action.Callback):
    """The thing that controls the execution of an animation. 
    
    The responsibility of Director is to control the pacing of the animation by 
    sending cues to perform actions in the script at just the right time. 
    Director is the central class in the object model because it contains the 
    main animation loop.

    Attributes:
        _clock: Clock, The animation clock.
        _is_directing: boolm Whether or not it is currently directing a scene.
    """

    def __init__(self):
        """Initializes a new instance of Director.
        """
        self._actions = []
        self._removed_actions = []

        self._actors = []
        self._removed_actors = []

        self._clock = Clock()
        self._is_directing = True
        
    def direct_scene(self, actors : list, actions : list):
        """Starts the animation loop for the given scene. Cues input, update 
        and output actions in sequence.

        Args:
            cast: Cast, The cast to direct.
            script: Script, The script to use.
        """
        self._actors = actors
        self._actions = actions
        self._is_directing = True
        while self._is_directing:
            self._do_inputs()
            self._do_updates()
            self._do_outputs()
    
    def on_stop(self):
        """This Action.Callback override signals the animation to end."""
        self._is_directing = False

    def on_next(self, actors, actions):
        """This Action.Callback override transitions the current scene to the 
        next one.

        Args:
            cast: Cast, The cast for the next scene.
            script: Script, The script for the next scene.
        """
        # todo: we should exit the directing loop and then make these changes,
        # restarting the loop again after - need to think about this a bit
        self._actors = actors
        self._actions = actions
        
    def _do_inputs(self):
        """Cues the input actions for the given cast and script. This method 
        also ticks the animation clock forward since it is the beginning of the 
        animation frame.
        """
        self._clock.tick()
        for action in self._actions:
            if isinstance(action, InputAction):
                action.execute(self._actors, self._actions, self._clock, self)

    def _do_updates(self):
        """Cues the update actions for the given cast and script. This method 
        will execute the actions over and over until the animation time has 
        caught up with the real time.
        """
        while self._clock.is_lagging():
            for action in self._actions:
                if isinstance(action, UpdateAction):
                    action.execute(self._actors, self._actions, self._clock, self)
            self._clock.catch_up()
    
    def _do_outputs(self):
        """Cues the output actions for the given cast and script. This method 
        also clean's the cast of any removed actors since it is the end of the 
        animation frame.
        """
        for action in self._actions:
            if isinstance(action, OutputAction):
                action.execute(self._actors, self._actions, self._clock, self)
        self._apply_changes()
    
    def add_action(self, action):
        """Add the given action to the script.

        Args:
            action: Action, The action to add.
        """
        self._actions.append(action)

    def remove_action(self, action):
        """Removes the given action from the script.
        
        Args:
            action (Action): The action to remove.
        """
        self._removed_actions.append(action)
    
    def add_actor(self, actor):
        """Adds the given actor to the cast.

        Args:
            actors: Actor, The actor to add.
        """
        self._actors.append(actor)

    def remove_actor(self, actor):
        """Marks the given actor for removal from the cast. Clients must call clean_actors to permanently remove actors from the cast. 

        Args:
            actor: Actor, The actor to remove.
        """
        self._removed_actors.append(actor)

    def _apply_changes(self):
        """Permantely removes all of the dead actors and actions."""
        for actor in self._removed_actors:
            self._actors.remove(actor)
        self._removed_actors.clear()

        for action in self._removed_actions:
            self._actions.remove(action)
        self._removed_actions.clear()
