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


def player_input_check(stock, domino, computer, player, next_player):
    p_move = ""
    ok = True
    while ok:
        p_move = input()
        try:
            player[abs(int(p_move)) - 1]
            p_move = int(p_move)
            ok = False
        except:
            print("Invalid input. Please try again.")
            print_all(stock, domino, computer, player, next_player)
    return p_move


def check_negative(number, player):
    if number > 0:
        return False
    elif number < 0:
        number = -number
        if number > len(player):
            return True
        elif number <= len(player):
            return False

def check_player_move(domino, move, player, stock, computer, next_player):
    move_list = player[move-1]
    if domino[-1][-1] == move_list[0]:
        return move_list, player.index(move_list), True
    elif domino[-1][-1] == move_list[-1]:
        return move_list.reverse(), player.index(move_list), True
    else:
        print("Illegal move. Please try again.")
        #print_all(stock,domino,computer,player,next_player)
        return move_list, player.index(move_list), False


def player_move(stock, domino, computer, player, next_player):
    move = player_input_check(stock, domino, computer, player, next_player)
    if move < 0 and -move > len(player):
        return 1
    elif move > 0 and move <= len(player):
        move_list, index, is_ok = check_player_move(domino, move, player, stock, computer, next_player)
        if is_ok is False:
            move = player_input_check(stock, domino, computer, player, next_player)
        else:
            domino.append(player[index])
            player.remove(player[index])
    elif move < 0 and (len(player) + move > 0):
        move = -move
        domino.insert(0, player[move - 1])
        player.remove(player[move - 1])
    elif move == 0 and len(stock) > 0:
            stock, player = take_from_stock(stock, player)
    return domino, computer, player, stock, flag


def computer_move(computer, player, domino, stock):
    move = input()
    flag = True
    if len(computer) > 0:
        move = random.randint(0, len(computer) - 1)
        domino.append(computer[move])
        computer.remove(computer[move])
    if len(computer) == 0:
        flag = check_win(computer, player, domino, stock)
    return computer, player, domino, stock, flag


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
            print_all(stock, snake, computer, player, next_player)
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


def print_all(stock, domino, computer, player, next_player):
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
    if next_player == 'player':
        print("\nStatus: It's your turn to make a move. Enter your command.")
    elif next_player == 'computer':
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")


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
flag = True
while flag:
    print_all(stock_pieces, domino_snake, computer_pieces, player_pieces, next_player)
    flag = check_win(computer_pieces, player_pieces, domino_snake, domino_snake)
    if flag == False:
        break
    if next_player == 'computer':
        computer_pieces, player_pieces, domino_snake, stock_pieces, flag = computer_move(computer_pieces, player_pieces, domino_snake, stock_pieces)
        next_player = "player"
    else:
        domino_snake, computer_pieces, player_pieces, stock_pieces, flag = player_move(stock_pieces, domino_snake, computer_pieces, player_pieces, next_player)
        next_player = "computer"
