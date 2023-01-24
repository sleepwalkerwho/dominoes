# Write your code here
import random


def generate_set():
    set = []
    pair = []
    start = 0
    for i in range(start, 7):
        for j in range(start, 7):
            pair.append(i)
            pair.append(j)
            set.append(pair)
            pair = []
        start += 1
    random.shuffle(set)
    return set


def generate_stock_computer_player():
    set = generate_set()
    stock = set[:14]
    computer = set[14:21]
    player = set[21:]
    return stock, computer, player


def find_snake(computer, player):
    domino = []
    player_max = max(player)
    computer_max = max(computer)
    if player_max > computer_max:
        domino.append(player_max)
        player_turn = 'computer'
        player.remove(player_max)
    else:
        domino.append(computer_max)
        player_turn = 'player'
        computer.remove(computer_max)
    return player_turn, domino


def print_invalid_input(stock, domino, computer, player):
    print("Invalid input. Please try again.")
    print_all(stock, domino, computer, player)


def player_move(domino, computer, player, stock):
    flag = True
    move = input()
    # 0 -incorrenct, 1 - plus, 2 - minus, 3 - 0, 4 - comp
    result = check_input(move)
    if result == 0:
        print_invalid_input(stock, domino, computer, player)
        print("\nStatus: It's your turn to make a move. Enter your command.")
        domino, computer, player, stock, flag = player_move(domino, computer, player, stock)
    elif result == 1:
        move = int(move)
        if move <= len(player):
            domino.append(player[move - 1])
            player.remove(player[move - 1])
        else:
            print_invalid_input(stock, domino, computer, player)
            print("\nStatus: It's your turn to make a move. Enter your command.")
            domino, computer, player, stock, flag = player_move(domino, computer, player, stock)
    elif result == 2:
        move = -int(move)
        if move <= len(player):
            domino.insert(0, player[move - 1])
            player.remove(player[move - 1])
        else:
            print("Invalid input. Please try again.")
            print_all(stock, domino, computer, player)
            print("\nStatus: It's your turn to make a move. Enter your command.")
            domino, computer, player, stock, flag = player_move(domino, computer, player, stock)
    elif result == 3:
        if len(stock) > 0:
            stock, player = take_from_stock(stock, player)
        elif len(stock) <= 0:
            flag = check_win(computer, player, domino, stock)

    elif result == 4:
        flag = True
        if len(computer) > 0:
            move = random.randint(0, len(computer) - 1)
            domino.append(computer[move])
            computer.remove(computer[move])
        if len(computer) == 0:
            flag = check_win(computer, player, domino, stock)
    return domino, computer, player, stock, flag


def check_input(move):
    '''try:
        move = int(move)
    except ValueError or IndexError:
        print("Invalid input. Please try again.")'''
    result = 0
    if move.isdigit():
        move = int(move)
        if move > 0:
            result = 1
        elif move == 0:
            result = 3
        else:
            result = 2
    elif move.isalpha():
        result = 0
    elif move == "" and len(move) == 0:
        result = 4
    return result


def take_from_stock(stock, pieces):
    elem = random.choice(stock)
    stock.remove(elem)
    pieces.append(elem)
    return stock, pieces


def check_win(computer, player, snake, stock):
    draw = is_draw(snake)
    if draw == 1:
        print("\nStatus: The game is over. It's a draw!")
        flag = False
        return flag
    elif draw == 0:
        if len(computer) == 0:
            print_all(stock, snake, computer, player)
            print("\nSStatus: The game is over. The computer won!")
            flag = False
        elif len(player) == 0:
            print("\nStatus: The game is over. You won!")
            flag = False
        else:
            flag = True
        return flag


def is_draw(snake):
    counter = 0
    if snake[0][0] == snake[-1][1]:
        a = snake[0][0]
        for i in range(len(snake)):
            if snake[i][0] == a or snake[i][-1] == a:
                counter += 1
    if counter >= 8:
        return 1
    else:
        return 0


def print_all(stock, domino, computer, player):
    print("======================================================================")
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}")
    print("")

    print_snake(domino)
    print("")
    player_count = 1
    print("Your pieces: ")

    if len(player) > 0:
        for i in player:
            print(f"{player_count}:{i}")
            player_count += 1


def print_snake(domino_snake):
    snake = ""
    for i in range(len(domino_snake)):
        if len(domino_snake) > 6:
            i = 0
            for i in range(3):
                snake += f"{domino_snake[i]}"
            snake += "..."
            i = len(domino_snake) - 3
            for i in range(len(domino_snake) - 3, len(domino_snake)):
                snake += f"{domino_snake[i]}"
            break
        else:
            snake += f"{domino_snake[i]}"
    print(snake)


stock_pieces, computer_pieces, player_pieces = generate_stock_computer_player()
next_player, domino_snake = find_snake(computer_pieces, player_pieces)

snake = ""
flag = True
while flag:
    print_all(stock_pieces, domino_snake, computer_pieces, player_pieces)
    flag = check_win(computer_pieces, player_pieces, domino_snake, domino_snake)
    if flag == False:
        break
    if next_player == 'computer':
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        domino_snake, computer_pieces, player_pieces, stock_pieces, flag = player_move(domino_snake, computer_pieces,
                                                                                       player_pieces, stock_pieces)
        next_player = "player"
    else:
        print("\nStatus: It's your turn to make a move. Enter your command.")
        domino_snake, computer_pieces, player_pieces, stock_pieces, flag = player_move(domino_snake, computer_pieces,
                                                                                       player_pieces, stock_pieces)
        next_player = "computer"
