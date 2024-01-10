from game_classes import Gameplay, Player


def play_game():
    """
    This function is going to be used to test the game before the UI. This is to help me have a structure to
    follow.

    This is the structure:
    1. The game template is set. That is how much grid we want, rounds and all that.
    2. The user which for now is me puts in the names and that also sets the game template.
    3. We then print "Round 1!"
    4. By default, player 1 is X. However this can be changed in game play settings. Still player 1 goes first.
    (so their turn parameter is initially True)
    5. We print "Player 1 Turn"
    6. Player 1 makes a move. Once anybody makes a move, their X or O is placed in the position specified
    (in the grid/game state). This cannot be reversed.

    (If there was a UI, I click, it shows up on the computer for whoever turn is current. X or O.
    This position is used in make_move to update/ set the game state. So once there is a click
    a casscade of other information is stored)

    7. After as many turns as grid size, a player checks if they've won.

    8. If player1 has not won, it is player 2's turn (player 1 turn is false). Then we repeat 5-8 but for player 2.

    9. if player1 has won, then we announce, "player 1 wins!" then announce "round 2!" (if there is a round 2 as
    specified by user)

    10. For a new round, player's wins statuses must be set to default. We then repeat previous steps

    11. Once we have exhausted rounds. We need to check if there's a tie. Then prompt the user to decide
    if they want a tiebreaker round or not.
    "result : tie!"
    "tiebreak round? Y/N"

    12. If user wants a tie breaker, make_tiebreak returns true. If this is so print "Tiebreak Round!". This updates
    our extra round parameter. We play again as normal.

    13. If there's another tie but extra round is already filled. End game. If step 11 is rejected and user
    picks No, end game.

    14. Game end is as follows: The winner is announced. Then shortly after the bubble buttons appear for,
    play again or back to main menu. (play again just takes you to clear grid and main menu to main menu)

    """

    player_1_name = "player 1"
    player_2_name = "player 2"

    input("X and O's!")  # user will press enter

    while True:
        user_choice = input("Is Player 1 X? (Y/N): ")
        if user_choice.upper() == 'Y':
            player_1_alias = "X"
            player_2_alias = "O"
            print("Player 1 is X.")
            break
        elif user_choice.upper() == 'N':
            player_1_alias = "O"
            player_2_alias = "X"
            print("Player 1 is O.")
            break
        else:
            print("Invalid choice. Please enter 'Y' or 'N'.")

            input()

    input()

    while True:
        choice_2 = input("You can only go up to 5 rounds for this game. How many rounds do you want?: ")
        try:
            int(choice_2)
        except ValueError:
            choice_2 = 0

        if int(choice_2) > 5:
            print("Too many rounds, try again")
            input()
        if int(choice_2) <= 0:
            print("Too few rounds, try again")
            input()
        else:
            rounds = int(choice_2)
            print("For this game we have " + choice_2 + " round(s)!")
            break

    input()

    while True:
        choice_3 = input("It's time for grid size! Grid size must be an odd number that is at least 3 and at most 11:")
        try:
            int(choice_3)
        except ValueError:
            choice_3 = 0

        if int(choice_3) < 3:
            print("Size is too small!")
            input()
        elif int(choice_3) % 2 == 0:
            print("Not an even number!")
            input()
        else:
            grid_size = int(choice_3)
            print("Our grid size is " + choice_3 + "!")
            break

    input()

    input("Put in your names! If you leave them blank, I will refer to you as Player 1 and Player 2. Okay? ")

    choice_4 = input("Player 1 name: ")

    if choice_4 != "":
        player_1_name = choice_4

    input()

    print("Player 1's name is " + player_1_name + "!")

    input()

    choice_5 = input("Player 2 name: ")

    if choice_5 != "":
        player_2_name = choice_5

    input()

    print("Player 2's name is " + player_2_name + "!")

    input()

    input("For some ground rules. For every round you will give me numbers that is >= 0 and < grid size.")

    input("For example, if your grid size is 3, 0 1, is a valid move. This is row 0 and column 1")

    input("Anything else is not valid. So enter 2 numbers separated by a space for your moves.")

    input("Great! That wasn't too bad huh. Let's play!")

    game = Gameplay((player_1_name, player_1_alias), (player_2_name, player_2_alias), rounds, grid_size)
    player1 = game.player1
    player2 = game.player2

    game_over = False
    while not game_over:
        if not game.rounds_complete():

            # Round_added starts off true
            if game.get_round_added():      # if true

                # needs to be off by 1 to meet stopping condition
                print("Round " + str(game.current_round + 1) + " !")
                input()
                game.set_round_added(False)     # this only resets if someone wins or there is no winner for the round

                # rounds added is true is someone has won OR if no one has won
                # however win_status is set to True if someone has WON, we need to reset it to false
                # in case we meet a tie round
                game.set_win_status(False)

            # No winner, round not complete. However, extra round should be true if tiebreaker was done.
            if game.grid.grid_full() and not game.get_win_status():
                message = "No winner for Round " + str(game.current_round + 1) + " !"
                no_winner(message, game)
                continue        # go to beginning of loop. by now rounds are completed

            if player1.my_turn() and not game.grid.grid_full():
                regular_move(player1, player2, game, grid_size)

            if player2.my_turn() and not game.grid.grid_full():
                regular_move(player2, player1, game, grid_size)

        elif game.rounds_complete() and game.theres_tie():
            while True:
                choice_7 = input("Our rounds are completed, but there is a tie! Request tiebreak? (Y/N): ")
                if choice_7.upper() == 'Y':
                    game.add_round_tiebreak()       # adds a new round
                    while True:
                        if not game.rounds_complete():
                            if game.get_round_added():  # should start off true cos last round someone won/no one won
                                print("Tiebreak Round, Round " + str(game.current_round + 1) + " !")
                                input()
                                game.set_round_added(False)     # should not reset.

                            # No winner and tie break has been exhausted
                            if game.grid.grid_full() and not game.get_win_status() and game.get_extra_round():
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

                            if player1.my_turn() and not game.grid.grid_full() and not game.grid.grid_full():
                                tie_break_move(player1, player2, game, grid_size)

                            if player2.my_turn() and not game.grid.grid_full() and not game.grid.grid_full():
                                tie_break_move(player2, player1, game, grid_size)
                        else:
                            break       # break out of tiebreak loop

                    return  # come out of the entire game.

                elif choice_7.upper() == 'N':
                    message = "You have proceeded with tie!"
                    normal_end(message, game)
                    game_over = True
                    break
                else:
                    print("Invalid choice. Please enter 'Y' or 'N'.")
                    input()

        else:
            message = "There is no tie and we have reached " + str(game.current_round) + " out of " + \
                      str(game.rounds) + " rounds!"
            normal_end(message, game)
            game_over = True


##############################################
#  HELPER FUNCTIONS

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
    """ Two branches end similarly, so I'm lumping the reseult into a function"""

    input(message)
    print(game.final_winner())

    input()

    # we shouldn't need to print the game status by now, we just announce the winner and game tally because there is
    # no game after.

    print("Final record: " + str(game.get_tally()))
    input("Game Over!")

    # add a hard reset maybe
    return


def regular_move(current_player: Player, other_player: Player, game: Gameplay, grid_size: int):

    """
    Helper Function to reduce redundant code
    """
    input(current_player.get_name() + " 's " + "turn!")
    while True:
        choice_6 = input("What's your move?: ")
        input_parts = choice_6.split()
        row, column = input_parts

        if len(input_parts) != 2 or (not (row.isdigit() and column.isdigit())):
            print("Invalid input. Please enter TWO INTEGERS separated by a SPACE.")
            input()
        if int(row) > grid_size or int(column) > grid_size:
            print("Invalid move!")
            input()
        else:
            # once you make a move, current position changes.  (mimicing clicking)
            current_player.make_move([int(row), int(column)])       # their turn is now false

            # if grid is full and player 1 is not winner, print no one won!

            if game.found_winner(current_player):   # game win_status becomes true!
                game.update_tally(current_player)
                print(current_player.get_name() + " made move " + row + ", " + column)

                input()

                print("Current gamestate: " + game.print_state())

                input()

                print(current_player.get_name() + " won round " + str(game.get_currentround() + 1))
                print("Current tally: " + str(game.get_tally()))

                input()

                game.add_round()
                game.soft_reset()
                return
            else:
                #   win status remains false because it started out false
                other_player.update_turn(True)  # next turn will be other player
                print(current_player.get_name() + " made move " + row + ", " + column)
                print("Current gamestate: " + game.print_state())
                input()
                return


def tie_break_move(current_player: Player, other_player: Player, game: Gameplay, grid_size: int):
    """

    :param current_player:
    :param other_player:
    :param game:
    :param grid_size:
    :return:
    """

    input(current_player.get_name() + " 's " + "turn!")
    while True:
        choice_6 = input("What's your move?: ")
        input_parts = choice_6.split()
        row, column = input_parts

        if len(input_parts) != 2 or (not (row.isdigit() and column.isdigit())):
            print("Invalid input. Please enter TWO INTEGERS separated by a SPACE.")
            input()
        if int(row) > grid_size or int(column) > grid_size:
            print("Invalid move!")
            input()
        else:
            # once you make a move, current position changes.  (mimicing clicking)
            current_player.make_move([int(row), int(column)])  # their turn is now false

            if game.found_winner(current_player):  # win status becomes true!
                game.update_tally(current_player)
                print(current_player.get_name() + " made move " + row + ", " + column)

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
                print(current_player.get_name() + " made move " + row + ", " + column)
                print("Current gamestate: " + game.print_state())
                input()
                return



# TODAY:
# create test suite for entities

# Try later to draw dependencies for UI tomorrow


# todo: things i need to test:
# test game for grid 5. I want to see the speed.

# are attributes being correctly updated. test this

# todo:write tests for code using analog game as a guide
# todo: draw out the game UI and abstract dependencies. Update dependencies and run test again (so we can run new test)
# todo: if tests pass, delete old todos
# todo: write test for UI to back end. By now, unit tests are done. so write integration and end to end tests
# todo: create blueprint for UI and connect it to back end. (html and java script)
# todo: bring it all together in like vs code or something then run it
