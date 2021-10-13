import getpass
def first_player():
    symbols = ['STONE', 'SCISSORS', 'PAPER']
    answer1 = ''

    while answer1 not in symbols:

        answer1 = getpass.getpass("First Player please choose among: Stone, Scissors, Paper ").upper()
        if answer1 in symbols:
            print('You successfully chose the symbol!')

    return answer1
def second_player():
    symbols = ['STONE', 'SCISSORS', 'PAPER']
    answer2 = ''

    while answer2 not in symbols:

        answer2 = getpass.getpass("Second Player please choose among: Stone, Scissors, Paper ").upper()

        if answer2 in symbols:
            print('You successfully chose the symbol!')

    return answer2

def comparison(first_player, answer2):
    if answer1 == 'PAPER' and answer2 == 'STONE':
            print('First Player Won!!!')
    elif answer1 == 'STONE' and answer2 == 'SCISSORS':
            print('First Player Won!!!')
    elif answer1 == 'SCISSORS' and answer2 == 'PAPER':
            print('First Player Won!!!')
    elif answer1 == answer2:
            print('Nobody won!')
    else:
            print('Second Player Won!!!')

answer1 = first_player()

answer2 = second_player()

comparison(answer1, answer2)
