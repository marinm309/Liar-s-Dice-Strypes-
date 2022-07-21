import random
import time


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.dices = [random.randint(1, 6) for _ in range(5)]

    def roll_the_dices(self):
        return [random.randint(1, 6) for _ in range(len(self.dices))]


def generate_all_bids(players):
    total_dices = 0
    for player in players:
        total_dices += len(player.dices)
    list_of_bids = [f'{x}:{y}' for x in range(1, 7) for y in range(1, total_dices + 1)]
    return list_of_bids


def create_players(player_name, n):
    players_object_list = [Player(1, player_name), ]
    for player_number in range(1, n):
        players_object_list.append(Player(player_number + 1, f'Bot: {player_number}'))
    return players_object_list


def wild_activation():
    print(f"Press 1 for 'Wild game', press 2 for normal game!")
    command = ''
    while command != '1' and command != '2':
        command = input()
    return True if command == '1' else False


def higher_the_bid(bids, player=0):
    if player != 0:
        first_call_wall = int(int(bids[-1][2:]) * random.uniform(0.12, 0.4))
        second_call_wall = int(int(bids[-1][2:]) * random.uniform(0.25, 0.6))
        for i in bids:
            if second_call_wall < int(i[2:]) < first_call_wall or second_call_wall > int(i[2:]) > first_call_wall:
                call = i
                print(f'{call}')
                bids = bids[bids.index(call) + 1:]
                return bids, call
        call = bids[0]
        print(f'{call}')
        bids = bids[bids.index(call) + 1:]
        return bids, call
    while True:
        print(f'Choose higher then dice value: {bids[0][0]} or higher amount between: {bids[0][2:]} - {bids[-1][2:]}')
        dice_value = input('Dice value: ')
        dice_amount = input('Dice amount: ')
        call = dice_value + ':' + dice_amount
        if call in bids:
            bids = bids[bids.index(call) + 1:]
            return bids, call


def print_all_players_dices(all_players, player):
    print(f'{all_players[player].name} won!')
    print('-------------------- Dices reveal')
    for p in all_players:
        print(f"{p.name}'s dices: {p.dices}")
    print('---------------------------------')


def play_again(player_name):
    players = create_players(player_name, __number_of_players)
    list_of_bids = generate_all_bids(players)
    print(f'Press 1 to play again, press 2 to exit!')
    command = ''
    while command != '1' and command != '2':
        command = input()
    if command == '1':
        play(list_of_bids, players)
    exit()


def check_for_winner(players):
    if len(players) == 1:
        print(f'The winner is {players[0].name} !!!')
        play_again(players[0].name)


def new_roll(players):
    for p in players:
        p.dices = p.roll_the_dices()


def challenge(player, prev_player, all_players, current_bid, wild):
    print(f'{all_players[player].name} challenges {all_players[prev_player].name}')
    total_dices = 0
    dice = int(current_bid[0])
    last_call_amount = int(current_bid[2:])
    for i in all_players:
        for j in i.dices:
            if j == dice or j == 1 and wild:
                total_dices += 1
    if total_dices >= last_call_amount:
        print_all_players_dices(all_players, prev_player)
        all_players[player].dices.pop()
        if not all_players[player].dices:
            print(f'{all_players[player].name} is out!')
            if all_players[player].name == all_players[0].name:
                play_again(all_players[0].name)
            all_players.pop(player)
        return all_players, player, '1:1'
    else:
        print_all_players_dices(all_players, player)
        all_players[prev_player].dices.pop()
        if not all_players[prev_player].dices:
            print(f'{all_players[prev_player].name} is out!')
            if all_players[prev_player].name == all_players[0].name:
                play_again(all_players[0].name)
            all_players.pop(prev_player)
        return all_players, prev_player, '1:1'


def make_turn(current_player_turn, players_left, list_of_bids, current_bid, first_turn, wild):
    if current_player_turn == 0:
        print(f"Your dices: {players_left[0].dices}")
        turn_command = '1' if first_turn else ''
        while turn_command != '1' and turn_command != '2':
            turn_command = input('Press 1 for higher bid\n'
                                 'Press 2 to call previous player a liar')
        if turn_command == '1':
            list_of_bids, current_bid = higher_the_bid(list_of_bids)
            return current_player_turn + 1, players_left, list_of_bids, current_bid, False
        else:
            players_left, current_player_turn, current_bid = challenge(current_player_turn, current_player_turn - 1,
                                                                       players_left,
                                                                       current_bid, wild)
            new_roll(players_left)
            return current_player_turn, players_left, generate_all_bids(players_left), current_bid, True
    else:
        if int(current_bid[2:]) >= int(int(list_of_bids[-1][2:]) * random.uniform(0.25, 0.6)) and not first_turn:
            players_left, current_player_turn, current_bid = challenge(current_player_turn, current_player_turn - 1,
                                                                       players_left,
                                                                       current_bid, wild)
            new_roll(players_left)
            return current_player_turn, players_left, generate_all_bids(players_left), current_bid, True
        else:
            list_of_bids, current_bid = higher_the_bid(list_of_bids, current_player_turn)
            return current_player_turn + 1, players_left, list_of_bids, current_bid, False


def play(list_of_bids, players):
    current_bid = ''
    current_player = 0
    first_turn = True
    wild = wild_activation()
    while True:
        current_player, players, list_of_bids, current_bid, first_turn = make_turn(current_player, players,
                                                                                   list_of_bids,
                                                                                   current_bid, first_turn, wild)
        check_for_winner(players)
        time.sleep(1)
        if current_player >= len(players) or current_player < -1:
            current_player = 0


__number_of_players = 7
players = create_players('Marin', __number_of_players)
list_of_bids = generate_all_bids(players)

play(list_of_bids, players)
