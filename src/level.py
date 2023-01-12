from player import Player


class Level:
    """
    Level performs the heavy lifting and general gameplay loop.
    """
    def __init__(self, lvl_num: int, player: Player):
        self.turns = 0
        self.player = player
        self.enemies = generate_enemy_list(lvl_num)
        self.score = 0

    def start(self):
        """
        Keep this as reference, will not work for the actual game.
        You need to pass the score back up to the GameManager after each turn.
        Consider a get_turn action called by the GameManager during the main loop which passes in player input
        when it is received to prevent hanging while waiting.
        :return:
        """
        while self.player.earned_multiplier > 0:
            # wait for player input
            # parse input
            # perform inputted action
            if not len(self.enemies) > 0:
                self.score += max(self.player.earned_mulitplier * (64 - self.turns), 0)
                return self.score

            for enemy in self.enemies:
                # perform an action
                pass

            self.turns += 1
        else:
            return -1
