from abstraction import Gamestate

# TODO: add some abstract classes for CA. Note: ABC is too abstract for our purposes
# TODO: Make some things private

# TODO: Draw out interaction diagram, create test suite, draw CA diagram
# TODO: Need to learn JavaScript with HTML for yummy visuals
######################################
# STATE ##


class Grid(Gamestate):
    """
    This represents the noughts and crosses game state. It keeps track of changes made and results of some of those
    changes
    """
    size: int
    fill: int
    grid_state: list

    def __init__(self, size: int = 3, fill: int = 0):
        self.size = size
        self.fill = fill
        self.grid_state = self.create_grid(size)    # initializer should not work if size is even and < 3 cos of
        # assert statements in create grid.

    def add_fill(self):
        """ every time a move is made, the fill of the grid increases by 1"""

        self.fill += 1

    def reset_fill(self):
        """For every new game, the fill should start back from zero"""
        self.fill = 0

    def get_size(self):
        """
        get size
        """
        return self.size

    def set_state(self, move: list[int, int, str]):
        """ set the state with new changes. I assume that move here is 3 things.
        [row, column, alias]
        """

        # row in which we want to update its column. We need to make a copy because lists are mutable.
        # if we don't, we get aliasing issues. NOTE: grid state is a list of LISTS (which are mutable)

        row_move = list(self.grid_state[move[0]])

        # next, update this copy with the new information at the column
        row_move[move[1]] = move[2]

        # finally, update the new row in the grid state
        self.grid_state[move[0]] = row_move

    def get_state(self) -> list:
        """ A getter useful for other classes"""

        return self.grid_state

    def grid_full(self) -> bool:
        """
        Check's if the grid is full. Every move made updates the fill parameter by 1 integer.
        i.e. given a 3 x 3 grid, ( size is 9, 3*3). if fill = 9, then the grid is full.
        """
        return self.fill == (self.size ** 2)        # 3^2

    def is_player1turn(self) -> bool:
        """
        todo: consider moving this to gameplay, you might also delete this
        """
        return False  ## TODO: come back and update this with a function call

    def reset_grid(self):
        """ reset grid for a fresh round"""

        self.grid_state = self.create_grid(self.size)

    def create_grid(self, size: int):
        """
        This is for the purposes of the initializer to create the grid state that reflects changes after every
        move made by the users. However, it should initially be a list of lists, with empty string place-holders.
        i.e for a 3 x 3 grid, we have [ [" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]


        precondition
        - size must be an odd number >= 3
        """
        assert size % 2 == 1 and size >= 3      # to check for oddness and "size" of size

        grid_start = []
        interior_grid = []

        for _ in range(size):
            interior_grid.append(" ")   # make a single list with [" ", " ", " "] for example assuming 3 x 3 grid

        for _ in range(size):
            grid_start.append(interior_grid)

        return grid_start


######################################
# INTERACTOR #


class Player:
    """
    The players of the game. Position is in the structure, row column. So, [0,1] in a 3 x 3 grid is
    row 1, column 2.

    """
    name: str
    position: list      # Todo: consider turning it into a tuple if that works
    is_myturn: bool
    game_state: Gamestate       # We need this to check position but this is an abstraction! yay
    alias: str
    num_moves: int = 0  # keep track of the moves for documentation purposes # make getter and setter for interactor

    def __init__(self, name: str, turn: bool, alias: str, gamestate: Gamestate):

        assert alias in ("X", "O")

        self.name = name
        self.position = []
        self.is_myturn = turn
        self.alias = alias
        self.game_state = gamestate

    def positionis_empty(self):
        """
        todo: delete this maybe
        returns if self.position is empty
        """
        return self.current_position() == []

    def valid_position(self, position: list) -> bool:
        """
        returns true if position is valid. that is, the position doesn't exceed the grid size. Our grid is ALWAYS a
        square.

        empty position is still valid, because we start off empty
        """

        size = self.game_state.get_size()
        if not position:  # position == [ ]
            return True
        else:
            return len(position) == 2 and position[0] < size and position[1] < size

    def get_name(self):
        """
        Get player's name
        """
        return self.name

    def change_position(self, position: list):
        """
        When a player makes a move, update their position.

        From the controller, the player clicks first. That click becomes their current position. Hence, when they click,
        current position is changed (i.e from [] so [num, num] assuming first move of the game).

        """
        assert len(position) == 2
        self.position = position

    def current_position(self):
        """
        This getter will be used for the logic of the game to check if the player has won. (By checking all directions
        of the current position)
        """
        return self.position

    def corner_or_middle(self, position: list) -> bool:
        """check if a position is placed in the corner or middle of a given grid. There are always 5 posistions
        for corner or middle for ANY size of grid. Because our grid is a SQUARE.

        i.e for a 3 X 3 grid our 5 positions are: [ [0,0] , [0,2], [2,0] , [1,1] , [2,2] ]
        """

        assert position != []       # can't be empty

        size = self.game_state.get_size()
        middle = size//2
        edge = size - 1
        valid_set = ((0, 0), (edge, edge), (0, edge), (edge, 0), (middle, middle))

        return tuple(position) in valid_set

    def specify_diagonal_direction(self, position: list) -> int:
        """ If we know a move is a corner or centre-piece, we want to know specifically its position, because
        that will help with calculating our win. Which is different for diagonal and off diagonal

        for simplicity
        0 == diagonal
        1 == off-diagonal
        2 == middle-piece
        """

        edge = self.game_state.get_size() - 1
        move = tuple(position)

        if move in ((0, 0), (edge, edge)):
            return 0
        elif move in ((0, edge), (edge, 0)):
            return 1
        else:
            return 2

    def check_win(self) -> bool:
        """
        The player, just like in a physical game, should be able to know if they've won or not. This isn't
        something the player directly has to do. However, it is done indirectly throught the system. (i.e me)

        This is also the main logic of the game
        """
        size = self.game_state.get_size()
        current_move = self.current_position()  # this is the move they just played it cannot be empty
        state = self.game_state.get_state()

        # you need at least the number of moves as rows or columns to have won, this is
        # to prevent redundant calls but is not necessary

        # if grid is full, that is after they have played a move. you have to report grid full!

        if self.num_moves < size:
            return False
        elif self.corner_or_middle(current_move):
            return self.check_diagonals(state, current_move) or self.check_non_diagonals(state, current_move)
        else:
            return self.check_non_diagonals(state, current_move)

    def check_non_diagonals(self, state: list[list], position: list) -> bool:
        """ This checks the non diagonals given the current position to find out if a win has been found.

        Strategy: always check right for horizontal direction, and down for vertical direction. If during check we see
        a different alias or " " ,STOP. Then check the other non-diagonal direction. If both have no winner, there is no
        winner """

        size = self.game_state.get_size()
        consecutives = 1        # if we get to size, we have won, however count YOURSELF as a consecutive so 1.

        # HORIZONTAL DIRECTION

        # i.e assume [2,0].  i = 0 + 1 =1. i needs to go round at most 5 times for a 5 X 5 grid which is equivalent
        # to checking again that i is not 0. we want to stop when we get to our given position

        i = (position[1] + 1) % size        # could be an end piece
        while i <= size and i != position[1]:
            if state[position[0]][i % size] == self.alias:
                consecutives += 1
            else:
                consecutives = 1    # set it to 1 again so next direction can accumulate
                break   # exit this loop prematurely. Then go to next direction

            i += 1

        # VERTICAL DIRECTION

        j = (position[0] + 1) % size  # could be an end piece
        while j <= size and j != position[0]:
            if state[j % size][position[1]] == self.alias:
                consecutives += 1
            else:
                break

            j += 1

        # we only do one check for consecutives because I cannot have a win in mutiple directions. Only one

        return consecutives == size

    def check_diagonals(self, state: list[list], position: list) -> bool:
        """ Checks the diagonal routes in the game stae given a position.

        Strategy: We always check "right" for diagonal directions. However, calculating right is different for
        diagonal and off-diagonal"""

        def diagonal() -> bool:
            """ Returns True if there are game_state.size consecutive alias names along the diagonal and False
            otherwise
            """

            size = self.game_state.get_size()

            consecutives = 1  # if we get to size, we have won however count YOURSELF as a consecutive so 1.

            i = (position[0] + 1) % size
            j = (position[1] + 1) % size

            while j <= size and [i, j] != position:
                if state[i % size][j % size] == self.alias:
                    consecutives += 1
                else:
                    break

                i += 1
                j += 1

            return consecutives == size

        def off_diagonal() -> bool:
            """ Returns True if there are game_state.size consecutive alias names along the off diagonal and False
            otherwise
            """

            size = self.game_state.get_size()

            consecutives = 1  # if we get to size, we have won, however count YOURSELF as a consecutive so 1.

            i = (position[0] - 1) % size
            j = (position[1] + 1) % size

            while j <= size and [i, j] != position:     # because j is always increasing. easier to check
                if state[i % size][j % size] == self.alias:
                    consecutives += 1
                else:
                    break

                i -= 1
                j += 1

            return consecutives == size

        if self.specify_diagonal_direction(position) == 0:
            return diagonal()
        elif self.specify_diagonal_direction(position) == 1:
            return off_diagonal()
        else:
            return diagonal() or off_diagonal()     # middle point

    def my_turn(self):
        """
        Players keep track of their turn in the game just like how a physical game would be. This is a function useful
        for logic of game. The control flow of the game. This is a getter

        """

        return self.is_myturn

    def update_turn(self, turn: bool):
        """
        When a player has played, their is_myturn parameter should be changed to False for example. This is a setter
        """

        self.is_myturn = turn

    def make_move(self, move: list):        # they shouldn't have access to the grid. but the grid should be updated
        """
        When a player makes a move, the following should be updated.
        1. Their move position should NOT exceed the grid size. If not raise error
        2. Their CURRENT POSITION MUST CHANGE!
        3. The grid state should change to reflect the move just made
        4. Their turn parameter should be false after the move
        5. Move is 2 things! player adds their alias by default so set state can use it [row, column, alias].
        The person acting as the player is not concerned of adding their alias.

        make_move and check_win are the main logic of the game.
        """

        # add an extra guard for if its the players turn to make a move

        if self.valid_position(move):       # checks len 2 and validity of sizes
            self.change_position(move)
            self.game_state.set_state(move + [self.alias])      # game state needs alias
            self.num_moves += 1
            self.game_state.add_fill()  # every move fills up the grid
            self.update_turn(False)
        else:
            print("invalid move")
            raise ValueError        # not valid position todo: make custom error


##############################################
# kind of like a controller or main


class Gameplay:

    # We only have ONE tie breaker which i believe is reasonable.

    grid: Grid
    player1: Player
    player2: Player
    rounds: int
    tally: dict
    current_round: int
    grid_size: int
    extra_round: bool          # keep track of tie break round!
    round_added: bool       # to keep track of new rounds
    win_status: bool    # to avoid calling check win everytime

    def __init__(self, player1: tuple[str, str], player2: tuple[str, str], rounds: int,
                 size: int, current_round: int = 0):

        # player 1 information should be gotten from UI. like the settings but default is ("player1","X")
        # ("player 2", "O"). so, ("name", "alias") todo: check here to change to list maybe

        gamestate = Grid(size)  # fill is automatically 0
        self.grid = gamestate   # referred to for testing purposes
        self.player1 = Player(player1[0], True, player1[1], gamestate)   # player 1 always goes first
        self.player2 = Player(player2[0], False, player2[1], gamestate)  # might need to add abstractions here
        self.rounds = rounds
        self.current_round = current_round
        self.tally = self.create_tally()    # this dict has {"player 1" : 0 , "player 2": 0} by default
        self.round_added = True
        self.extra_round = False
        self.win_status = False     # nobody has won yet

    def print_state(self):
        """
        print state
        """
        return str(self.grid.get_state())

    def get_tally(self):
        """
        get tally
        """

        return self.tally

    def create_tally(self):
        """
        creates the default tally which will be updated as the game goes.
        Default is {"player 1" : 0 , "player 2": 0}.
        However, player 1 and player 2 could be a different name by choice of the user.

        todo: convert the numbers to actual tallies when you figure out the ui
        """

        dum_tally = {self.player1.get_name(): 0, self.player2.get_name(): 0}

        return dum_tally

    def update_tally(self, player: Player):
        """
        Tally keeps track of the status of game play.
        - For every turn, the player is responsible of letting the game know if they've won or not. The
        game always asks the player, have you won?
        - There can only be one or no winner per round.
        - For each round, who ever wins will have a number added to their tally.
        - This function is used assuming the placed player has won.

        - I could check that this player has won using this function. However, check_win() could slow down the system.
        I think someone else should be responsible.

        todo: draw a diagram of dependencies to create abstractions and clarify responsibility

        """
        self.tally[player.get_name()] += 1

        # you might use this:

        # if self.player1.check_win():    # if this is true
        #     self.tally[self.player1.get_name()] += 1        # increase their count in the tally.
        # if self.player2.check_win():                    # 2 ifs because both could be true acyually no
        #     self.tally[self.player2.get_name()] += 1

    def get_currentround(self):
        """
        todo: unsure of how to utilise function in presenter
        We need the current round to be used in presenter
        """
        # if self.extra_round:    # if it is true
        #     print("extra")      # todo: adequately handle this for presenter views or change things
        # else:

        return self.current_round  # todo: adequately handle this for presenter views or change things. this is a
        # number. I want to convert it to a string at some point

    def game_end(self):     # game ends when rounds are over or when
        """
        todo: unsure of this function
        If this is true, then the presenter for a new view would need to be updated differently than in regular
        gameplay.


        We want game_end state to show us the final winner and reset our game to original before we ever played.
        Possibly we can add a metrics to it.
        """
        if self.rounds_complete():
            self.final_winner()     # todo: change the view with this information
            self.reset_game()       # reset game
            # once we click anywhere, we go back to set up screen

    def theres_tie(self) -> bool:
        """
        if there is a tie, we should know so we can ask the user if they want a tie breaker round.
        """
        return self.tally[self.player1.get_name()] == self.tally[self.player2.get_name()]

    def make_tiebreak(self, decision: int) -> bool:
        """
        todo: you might delete this function
        todo: unsure of this function
        if the decision is YES from the UI or whatever, then we need to add 1 more round. After which we have a
        decision of a final winner.
        YES == 1
        NO == 0

        if the tiebreak should be made and was made, it should return True. If it returns False,
        we proceed as normal with rounds.
        If it returns True we can do something a bit special like "Tiebreak round!" instead of round (insert number).
        """

        if decision == 1 and self.add_round_tiebreak():
            self.extra_round += 1   # change this, we are making it true or false now
            return True
        else:
            return False

    def add_round(self):
        """ add round after we have found a winner for the round. Finding winner isn't this method's
        responsibility
        """

        if not self.extra_round:
            self.current_round += 1
            self.set_round_added(True)
        else:
            print("Tie break round already done!")
            raise AttributeError

    def rounds_complete(self):
        """
        check if we've reached our total rounds
        """
        # the second case is there in case for some reason i have a current round > set rounds
        # if rounds is 2 and current round is 1. This will fail. Only thing that will pass is 2.

        return self.current_round == self.rounds and self.current_round <= self.rounds

    def add_round_tiebreak(self):
        """
        We only have 1 tiebreaker round for this software. Then we declare winner.
        This is basically like adding an extra round. But only 1!
        """
        if not self.extra_round:
            self.rounds += 1
            self.set_round_added(True)
            return True
        else:
            print("Tie break round already done!")
            raise AttributeError

    def get_extra_round(self):
        """ get extra round is true or false"""

        return self.extra_round

    def extra_round_added(self):
        """ set that an extra round has been added. Once set, it can't be reset"""
        self.extra_round = True

    def set_round_added(self, added: bool):
        """
        after a new round has started, round added is false. Once someone has won, we add a round
        so round added is true
        """
        self.round_added = added

    def get_round_added(self):
        """
        return that a round was added. Used to check if we are in a new round
        """

        return self.round_added

    def final_winner(self) -> str:
        """
        If all the rounds are complete. (That is including additional rounds for tiebreakers as per players'
        request). Then we check who had the most tallies. That is the final winner
        """
        if self.rounds == self.current_round:
            if self.tally[self.player1.get_name()] == self.tally[self.player2.get_name()]:
                return "You both win the game!"  # this is if they don't want to tiebreak
            if (self.tally[self.player1.get_name()] == 0) and (self.tally[self.player2.get_name()] == 0):
                return "No winner for this game!"   # they could both just not win
            else:
                tally = self.tally
                return "The winner of the game is " + max(tally, key=tally.get) + " !"
                # this returns the player with the most wins

    def get_win_status(self):
        """
        Getter for win status
        :return:
        """
        return self.win_status

    def set_win_status(self, status: bool):
        """

        :return:
        """
        self.win_status = status

    def found_winner(self, player: Player) -> bool:
        """
        Game asks the player, have you won?
        If so, our win status is set to True. Else it is kept as False
        """
        a_win = player.check_win()
        if a_win:
            self.set_win_status(True)
            # update win attribute, set it here
        return a_win

    def soft_reset(self):
        """ Prepare the game for a new round. That is,
        1. Players should have their initial turn like they first started
        2. We get a fresh grid"""

        self.player1.update_turn(True)      # player 1 always starts
        self.player2.update_turn(False)
        self.set_win_status(False)
        self.grid.reset_grid()  # fresh grid!
        self.grid.reset_fill() # start fill from beginning

    def reset_game(self):
        """ reset game to original state and change screen.

        To reset a game, the inits for this class should be changed to default.

        """
