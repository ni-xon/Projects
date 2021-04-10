import random


class RPS:
    def __init__(self, winning_score):
        self.player1_score = self.player2_score = 0
        self.winning_score = int(winning_score)
        self.selections = ['rock', 'paper', 'scissors']
        self.game_over = False

    def compare(self, player1_input, player2_input):
        if player1_input == player2_input:
            return 'Draw -- No score'

        elif player1_input == 'paper' and player2_input == 'rock':
            return 'Paper beats Rock -- You win'

        elif player1_input == 'rock' and player2_input == 'paper':
            return 'Paper beats Rock -- Computer wins'

        elif player1_input == 'scissors' and player2_input == 'paper':
            return 'Scissors beats paper -- You win'

        elif player1_input == 'paper' and player2_input == 'scissors':
            return 'Scissors beats Paper -- Computer wins'

        elif player1_input == 'rock' and player2_input == 'scissors':
            return 'Rock beats Scissors -- You win'

        elif player1_input == 'scissors' and player2_input == 'rock':
            return 'Rock beats Scissors -- Computer wins'

    def play(self):
        while not self.game_over:
            player2_input = self.selections[random.randrange(len(self.selections))]

            while True:
                print('==================================================================================')
                player1_input = input('Rock, paper or scissors? ')
                player1_input = player1_input.lower()
                if player1_input in self.selections:
                    break

                else:
                    print('Invalid input, please try again')

            print(f'Computer: {player2_input}')

            result = self.compare(player1_input, player2_input)
            if 'You win' in result:
                self.player1_score += 1

            elif 'Computer wins' in result:
                self.player2_score += 1

            print(result)
            print(f'\nScores:\nPlayer: {self.player1_score}\nComputer: {self.player2_score}')
            print('==================================================================================')
            if self.player1_score == self.winning_score or self.player2_score == self.winning_score:
                self.game_over = True

        if self.player1_score == self.winning_score:
            print('Player wins the game!')

        else:
            print('Computer wins the game!')


if __name__ == '__main__':
    rounds = ''
    while not rounds.isdigit():
        rounds = input('Enter the score required to win the game: ')

        if not rounds.isdigit():
            print('Invalid input, please try again')

    game = RPS(rounds)
    game.play()
