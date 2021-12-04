from genie.script.action import UpdateAction

class HandleBulletsAstroidsCollision(UpdateAction):
    def __init__(self, priority, physics_service, audio_service):
        self._priority = priority
        self._score = None
        self._physics_service = physics_service
        self._audio_service = audio_service

    def execute(self, actors, actions, clock, callback):
        """
            This action handles all collisions between the BULLETS and the ASTROIDS
        """
        # If we don't know who's the score actor, find it
        self._score = actors.get_first_actor("score")
        
        # First, get a list of bullets out of the cast
        bullets = actors.get_actors("bullets")
        
        # Next, loop through all the astroids to see which one collides with
        # any of the bullets
        for actor in actors.get_actors("astroids"):
            # if isinstance(actor, Astroid):
            collided_bullet = self._physics_service.check_collision_list(actor, bullets)
            if collided_bullet != -1:
                actors.remove_actor("bullets", collided_bullet)
                actor.take_damage(1)
                self._audio_service.play_sound("astroid/assets/sound/rock_cracking.wav", 0.1)

                # If the astroid's hp gets down to 0, remove it, give score to the player,
                if (actor.get_hp() <= 0):
                    actors.remove_actor("astroids", actor)
                    if (self._score != None):
                        self._score.add_score(actor.get_max_hp())
                    self._audio_service.play_sound("astroid/assets/sound/explosion-01.wav", 0.1)