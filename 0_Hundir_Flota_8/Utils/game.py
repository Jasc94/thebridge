def game():
    import os
    import time

    import classes as c
    import functions as f

    # ---------------------------- Game preparation ----------------------------
    # >>> Function for the beginning of the game
    def beginning_of_game(new_or_old_game):
        # If new game...
        if new_or_old_game == 'new':

            # 2) Ask players for the coordenates
            print('Player 1, please place your ships:\n')
            p1_ships = f.ask_coordenates(board1)

            # Clear the output and ask the next player
            os.system('clear')

            print('Player 2, please place your ships:\n')
            p2_ships = f.ask_coordenates(board2)

            # 3) Update the boards' lifes situation
            board1.board_lifes()
            board2.board_lifes()

        # If old game...
        else:
            try:
                f.show_saved_games()
                game_name = input('Enter the name of the game you want to load:\n')

                # This is how they are laoded: [board1_backend, board2_backend]
                board1.backend, board2.backend = f.load_old_game(game_name)

                # Update the lifes
                board1.board_lifes()
                board2.board_lifes()

            except Exception:
                print("\nYou don't have any saved game. You'll start a new one.\n")
                beginning_of_game("new")


    # 1.A ) Create empty boards for each player
    name1 = input('Please enter your alias for the game: ')
    name2 = input('Please enter your alias for the game: ')

    board1 = c.board(name1)
    board2 = c.board(name2)

    # 1.B) New game or old game?
    new_or_old_game = input('Do you want to start a new game(new) or load an old one(old)?\n').lower()

    # 2) Call the function created for the beginning of the game
    beginning_of_game(new_or_old_game)



    # ---------------------------- Beginning of the game ----------------------------

    # Clear the output
    os.system('clear')

    # Set the turn to 1
    turn = 1
    keep_playing = 'yes'

    # Start the game
    while board1.life > 28 and board2.life > 28:
    
        if keep_playing == 'no':
            # Ask for the game name
            game_name = input('Please enter a name to save the game:\n')
            # Pack the backends into a list
            dfs = [board1.backend, board2.backend]
            # Save the game
            f.save_game(dfs, game_name)
            # Confirmation message
            print('The game was succesfully saved as:', game_name)
            print('Status summary:\n')
            print('Player 1 remaining lifes: ', board1.life, '\n')
            print('Player 2 remaining lifes: ', board2.life, '\n')
            break

        # Show the full board
        f.full_boards(board1, board2, turn)

        # 1) PLAYER 1 TURN

        # Show the player 2 (front)board
        board2.frontend_creator()

        # Then ask the player 1 to guess
        print('\nPlayer 1, its your turn:\n')
        p1_guess = f.ship_coordenates()

        # Update the situation after the attack
        board2.pointer(p1_guess)
        board2.board_lifes()

        # Show the result
        board2.frontend_creator()

        print('-' * 80)

        # 2) PLAYER 2 TURN

        # Show the player 1 (front)board
        board1.frontend_creator()

        # Then ask the player 2 to guess
        print('\nPlayer 2, its your turn:\n')
        p2_guess = f.ship_coordenates()

        # Update the situation after the attack
        board1.pointer(p2_guess)
        board1.board_lifes()

        # Show the result
        board1.frontend_creator()

        # Clear the turn output
        os.system('clear')

        # Update turn
        turn += 1

        # Keep playing or save the game?
        keep_playing = input('Do you want to keep playing(yes) or save the game(no)?\n').lower()
    


    # ---------------------------- End of the game ----------------------------
    # print('End of the game:\n')

    # print('Player 1 - remaining lifes:', board1.life)
    # print('Player 2 - remaining lifes', board2.life)
    # Show the full board
    if keep_playing == 'yes':
        winner = f.winner(board1, board2)
        f.full_boards(board1, board2, turn, winner)