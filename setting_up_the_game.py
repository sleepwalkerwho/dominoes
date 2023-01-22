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
        player.remove(domino[0])
    else:
        domino.append(computer_max)
        player_turn = 'player'
        computer.remove(domino[0])
    return player_turn, domino

if __name__ == "__main__":
    stock_pieces, computer_pieces, player_pieces = generate_stock_computer_player()
    next_player, domino_snake = find_snake(computer_pieces, player_pieces)
    print(f"Stock pieces: {stock_pieces}")
    print(f"Computer pieces: {computer_pieces}")
    print(f"Player pieces: {player_pieces}")
    print(f"Domino snake: {domino_snake}")
    print(f"Status: {next_player}")
