import random


def game_setup():
    game_prepped = 0

    human_hand = []
    computer_hand = []
    domino_bag = []

    # generate full set of dominos
    domino_stock = []

    for first in range(0, 7):
        for second in range(first, 7):
            domino_stock.append([first, second])

    while game_prepped == 0:
        # shuffle the 'bag' of dominos
        random.shuffle(domino_stock)

        # distribute dominos between computer, human player and the 'bag'
        computer_hand = domino_stock[0:7]
        human_hand = domino_stock[7:14]
        domino_bag = domino_stock[14:]

        # check to ensure either player has at least one 'double' domino
        # if no doubles are detected, reshuffle the bag and start again
        doubles = [[0, 0], [1, 1], [3, 3], [2, 2], [5, 5], [4, 4], [6, 6]]

        for domino in doubles:
            if domino in computer_hand or domino in human_hand:
                game_prepped = 1

    # determine which player has the starting piece (the highest value domino)
    # start by sorting the players' hands to make it easier to jump to the highest value domino
    computer_hand_sorted = computer_hand  # this allows us to sort without changing the original hand order
    computer_hand_sorted.sort()

    human_hand_sorted = human_hand
    human_hand_sorted.sort()

    if computer_hand_sorted[6][0] > human_hand_sorted[6][0]:
        starting_player = 'player'
        snake = [computer_hand_sorted[6]]
    else:
        starting_player = 'computer'
        snake = [human_hand_sorted[6]]

    # remove starting piece from the appropriate hand
    if starting_player == 'player':
        computer_hand.remove(snake[0])
    else:
        human_hand.remove(snake[0])

    return computer_hand, human_hand, domino_bag, snake, starting_player


def display_game_state(domino_bag, computer_hand, human_hand, snake):
    print('=' * 70)
    print(f"Stock size: {len(domino_bag)}")
    print(f"Computer pieces: {len(computer_hand)}\n")

    if len(snake) > 6:  # display snake, truncating if over 6 tiles long
        print(f"{''.join(map(str, snake[:3]))}...{''.join(map(str, snake[-3:]))}\n")
    else:
        print(f"{''.join(map(str, snake))}\n")

    print('Your pieces:')  # display all human players' tiles
    for each in range(0, len(human_hand)):
        print(f"{each + 1}: {human_hand[each]}")


def process_turn_human(domino_bag, human_hand, snake):
    turn_processed = 0

    # prompt human user to make a turn
    move = input("\nStatus: It's your turn to make a move. Enter your command.")

    while turn_processed == 0:
        if not str(move).replace('-', '').isnumeric():  # if move is not numeric request new move
            move = input('Invalid input. Please try again. (not numeric)')
        elif abs(int(move)) > len(human_hand):  # if move doesn't reference a tile in hand request new move
            move = input('Invalid input. Please try again. (out of range)')
        else:
            move = int(move)

            if move == 0:  # draw from bag and skip turn, if bag is empty skip turn
                if len(domino_bag) > 0:  # bag is not empty
                    tile = random.choice(domino_bag)  # randomly select a tile from the bag

                    domino_bag.remove(tile)  # remove the tile from the bag
                    human_hand.append(tile)  # add tile to the players' hand

                    turn_processed = 1

            elif move > 0:  # add tile to the right of the snake
                tile = human_hand[move - 1]

                # check a side of the chosen tile matches the right-most number on the snake
                if tile[0] == snake[-1][1]:
                    snake.append(tile)
                    human_hand.remove(tile)

                    turn_processed = 1
                elif tile[1] == snake[-1][1]:
                    snake.append(tile[::-1])
                    human_hand.remove(tile)

                    turn_processed = 1
                else:
                    move = input('Illegal move. Please try again.')
            elif move < 0:  # add tile to the left of the snake
                tile = human_hand[abs(move) - 1]

                # check a side of the chosen tile matches the left-most number on the snake
                if tile[1] == snake[0][0]:
                    snake.insert(0, tile)
                    human_hand.remove(tile)

                    turn_processed = 1  # complete turn
                elif tile[0] == snake[0][0]:
                    snake.insert(0, tile[::-1])
                    human_hand.remove(tile)

                    turn_processed = 1  # complete turn
                else:
                    move = input('Illegal move. Please try again.')


def computer_move_dictionary(computer_hand, snake):
    # determine the value of each tile in the computers' hand based on pip-count frequency
    pips = [0, 0, 0, 0, 0, 0, 0]

    # count each instance of identical pips across tiles in computers' hand
    for domino in computer_hand:
        for each in range(0, 7):
            if domino[0] == each:
                pips[each] = pips[each] + 1
            if domino[1] == each:
                pips[each] = pips[each] + 1

    # count each instance of identical pips across tiles in the snake
    for domino in snake:
        for each in range(0, 7):
            if domino[0] == each:
                pips[each] = pips[each] + 1
            if domino[1] == each:
                pips[each] = pips[each] + 1

    # calculate the value of each tile in the computers' hand
    computer_hand_values = {}
    computer_hand_values_sorted = {}

    for domino in computer_hand:
        value = pips[domino[0]] + pips[domino[1]]
        computer_hand_values.update({str(domino): value})  # tabulate the values in a dictionary

    # sort the dictionary by value, lowest to highest
    sorted_values = sorted(computer_hand_values.values())

    for item in sorted_values:
        for key in computer_hand_values.keys():
            if computer_hand_values[key] == item:
                computer_hand_values_sorted[key] = computer_hand_values[key]

    # convert sorted dictionary keys into a list
    move_list = list(computer_hand_values_sorted.keys())

    # above method return strings instead of a list, the below cleans up the strings and converts them back into a list
    # this allows the list to be used by process_turn_computer()
    count = 0
    for _ in move_list:
        move_list[count] = move_list[count].replace("[", '')
        move_list[count] = move_list[count].replace("]", '')
        move_list[count] = move_list[count].replace(", ", '')
        move_list[count] = list(move_list[count])
        move_list[count][0] = int(move_list[count][0])
        move_list[count][1] = int(move_list[count][1])
        count += 1

    return move_list


def process_turn_computer(domino_bag, computer_hand, snake):
    input("Status: Computer is about to make a move. Press Enter to continue...")

    # determine the move order of priority (best to worst)
    move_order = computer_move_dictionary(computer_hand, snake)

    available_moves = len(move_order)  # how many moves to attempt before drawing from the bag

    turn_processed = 0
    while turn_processed == 0:
        if available_moves > 0:
            tile = move_order[available_moves - 1]

            # check whether tile fits on either end of the snake
            if tile[0] == snake[-1][1]:
                snake.append(tile)
                computer_hand.remove(tile)

                turn_processed = 1  # complete turn
            elif tile[1] == snake[-1][1]:
                snake.append(tile[::-1])
                computer_hand.remove(tile)

                turn_processed = 1  # complete turn
            elif tile[1] == snake[0][0]:
                snake.insert(0, tile)
                computer_hand.remove(tile)

                turn_processed = 1  # complete turn
            elif tile[0] == snake[0][0]:
                snake.insert(0, tile[::-1])
                computer_hand.remove(tile)

                turn_processed = 1  # complete turn
            else:  # if tile does not fit reduce the number of available moves
                available_moves -= 1
        # if no better moves are available draw a tile from the bag
        else:  # draw from bag and skip turn, if bag is empty skip turn
            if len(domino_bag) > 0:  # bag is not empty
                tile = random.choice(domino_bag)  # randomly select a tile from the bag

                domino_bag.remove(tile)  # remove the tile from the bag
                computer_hand.append(tile)  # add tile to the players' hand

                turn_processed = 1  # complete turn


def game_end_check(computer_hand, human_hand, snake):
    if len(computer_hand) == 0 or len(human_hand) == 0:  # check whether a player has emptied their hand
        return 2  # 2: win state

    elif snake[0][0] == snake[-1][1]:
        count = 0
        instance = 0
        for _ in snake:
            instance += snake[count].count(snake[0][0])
            count += 1

        if instance >= 8:
            return 0  # draw state
        else:
            return 1  # game continues

    else:
        return 1  # game continues


def game():
    computer_hand, human_hand, domino_bag, snake, status = game_setup()

    game_running = 1  # 0: draw, 1: ongoing, 2: win state

    while game_running == 1:
        # display game board
        display_game_state(domino_bag, computer_hand, human_hand, snake)

        # request user input and ensure a legal move occurs
        if status == 'computer':
            process_turn_computer(domino_bag, computer_hand, snake)
        else:
            process_turn_human(domino_bag, human_hand, snake)

        # check to see whether a game end condition has been met
        game_running = game_end_check(computer_hand, human_hand, snake)

        if game_running != 1:  # if game has ended display game state for last time, else switch players
            display_game_state(domino_bag, computer_hand, human_hand, snake)
            if game_running == 0:
                print("\nStatus: The game is over. It's a draw!")
                exit()
            elif game_running == 2:
                if status == 'computer':
                    print("\nStatus: The game is over. The computer won!")
                    exit()
                else:
                    print("\nStatus: The game is over. You won!")
                    exit()
        else:
            if status == 'computer':
                status = 'player'
            else:
                status = 'computer'


if __name__ == '__main__':
    game()
