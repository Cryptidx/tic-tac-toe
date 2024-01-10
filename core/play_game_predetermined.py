from game_classes import Gameplay, Player

# todo: fill in the moves such that it will behave according to function docstring

# THIS IS A SUITE OF FUNCTIONS THAT I CAN RUN TO SHOW WORKING BEHAVIOUR OF GAME AND ISOLATE FOR BUGS
# check player moves for some moves to use if interested.


def playgame_predet(player1_moves: list[list], player2_moves: list[list], rounds: int, grid_size: int,
                    decision: int):
    """ Give a set of moves for a game of X and O's that will suffice for as many rounds and grid size given.

    You can decide to put a tiebreak round or not.
    0 == no tiebreak
    1 == tiebreak

    To simplify, I have removed the initilaization of gameplay. I don't care about the names.

    I have stored some moves in a txt file that you can copy and paste into the function.
    """

    player_1_alias = "X"
    player_2_alias = "O"
    player_1_name = "player 1"
    player_2_name = "player 2"

    game = Gameplay((player_1_name, player_1_alias), (player_2_name, player_2_alias), rounds, grid_size)

    # this is popping from behind, so take that into account. Order sould be from back to front
    play_game(game.player1, game.player2, player1_moves, player2_moves, game, decision)


####################################################
# HELPER FUNCTIONS

def play_game(player1: Player, player2: Player, player1_move: list[list], player2_move: list[list], game: Gameplay,
              tie_break: int):
    """
    Play the game using a predetermined set of moves from player 1 and 2.

    Preconditions:
    - These are valid moves
    - If moves are exhausted, either nobody won or someone won. Else moves are not enough
    """

    game_over = False
    while not game_over:
        if not game.rounds_complete():
            if game.get_round_added():  # if true
                print("Round " + str(game.current_round + 1) + " !")
                input()
                game.set_round_added(False)  # this only resets if someone wins or there is no winner for the round
                game.set_win_status(False)

            if game.grid.grid_full() and not game.get_win_status():  # No winner, round not complete
                message = "No winner for Round " + str(game.current_round + 1) + " !"
                no_winner(message, game)
                continue

            if player1.my_turn() and not game.grid.grid_full():     # and not game.rounds_complete():
                assert player1_move != []
                regular_move(player1, player2, game, player1_move.pop())

            if player2.my_turn() and not game.grid.grid_full():     # and not game.rounds_complete():
                assert player2_move != []
                regular_move(player2, player1, game, player2_move.pop())

        elif game.rounds_complete() and game.theres_tie():
            while True:
                if tie_break == 1:
                    game.add_round_tiebreak()
                    while True:
                        if not game.rounds_complete():
                            if game.get_round_added():  # should start off true cos last round someone won/no one won
                                print("Tiebreak Round, Round " + str(game.current_round + 1) + " !")
                                input()
                                game.set_round_added(False)  # should not reset.

                            if game.grid.grid_full() and not game.get_win_status() and game.extra_round:
                                print("Tie Remains!")
                                print("No winner for Round " + str(game.current_round + 1) + " !")

                                game.add_round()
                                game.extra_round_added()  # set to true

                                # final winner
                                print(game.final_winner())

                                input()

                                print("Current gamestate: " + game.print_state())
                                print("Final record: " + str(game.get_tally()))

                                input("Game Over!")

                                game.soft_reset()
                                break  # break out of tiebreak loop

                            if player1.my_turn() and not game.grid.grid_full():
                                tie_break_move(player1, player2, game, player1_move.pop())

                            if player2.my_turn() and not game.grid.grid_full():
                                tie_break_move(player2, player1, game, player2_move.pop())
                        else:
                            break  # break out of tiebreak loop

                    return  # come out of the entire game.

                else:
                    message = "You have proceeded with tie!"
                    normal_end(message, game)
                    game_over = True
                    break

        else:
            message = "There is no tie and we have reached " + str(game.current_round) + " out of " + \
                      str(game.rounds) + " rounds!"
            normal_end(message, game)
            game_over = True


def no_winner(message: str, game: Gameplay):
    """blah"""

    print(message)
    print("Current gamestate: " + game.print_state())
    print("Current tally: " + str(game.get_tally()))
    input()

    game.add_round()
    game.soft_reset()
    return


def normal_end(message: str, game: Gameplay):
    """ Two branches end similarly, so I'm lumping the result into a function"""

    input(message)
    print(game.final_winner())

    input()

    # we shouldn't need to print the game status by now, we just announce the winner and game tally because there is
    # no game after.

    print("Final record: " + str(game.get_tally()))
    input("Game Over!")

    # add a hard reset maybe
    return


def regular_move(current_player: Player, other_player: Player, game: Gameplay, move: list[int, int]):
    """
    Helper Function to reduce redundant code
    """
    input(current_player.get_name() + " 's " + "turn!")
    current_player.make_move(move)  # their turn is now false

    if game.found_winner(current_player):  # game win_status becomes true!
        print(current_player.get_name() + " made move " + str(move[0]) + ", " + str(move[1]))

        input()
        print("Current gamestate: " + game.print_state())

        input()

        print(current_player.get_name() + " won round " + str(game.get_currentround() + 1))
        game.update_tally(current_player)
        print("Current tally: " + str(game.get_tally()))

        input()

        game.add_round()
        game.soft_reset()
        return
    else:
        other_player.update_turn(True)
        print(current_player.get_name() + " made move " + str(move[0]) + ", " + str(move[1]))
        print("Current gamestate: " + game.print_state())
        input()
        return


def tie_break_move(current_player: Player, other_player: Player, game: Gameplay, move: list[int, int]):
    """
    tie break move
    """

    input(current_player.get_name() + " 's " + "turn!")

    current_player.make_move(move)  # their turn is now false

    if game.found_winner(current_player):  # win status becomes true!
        game.update_tally(current_player)

        print(current_player.get_name() + " made move " + str(move[0]) + ", " + str(move[1]))
        print("Current gamestate: " + game.print_state())

        input()

        print("Tie Broken!")

        input()

        print(current_player.get_name() + " won round " + str(game.get_currentround() + 1))
        game.add_round()  # to make if condition of outer loop false
        game.set_round_added(False)  # so the first if condition doesn't print
        game.extra_round_added()  # make it true
        print(game.final_winner())

        input()

        print("Final Record: " + str(game.get_tally()))

        input("Game Over!")

        game.soft_reset()  # shouldn't matter, but should start on clean slate, todo: possibly make hard reset
        return
    else:
        other_player.update_turn(True)  # next turn will be other player
        print(current_player.get_name() + " made move " + str(move[0]) + ", " + str(move[1]))
        print("Current gamestate: " + game.print_state())
        input()
        return
