import random

class GuessingGame:
    def __init__(self):
        self.guesses = 0
        self.number = random.randint(1, 9)


if __name__ == '__main__':
    exit = False

    while not exit:
        game = GuessingGame()
        print('==================================================================================')
        print('Welcome to the guessing game.\nYou will need to guess the number I have chosen from 1-9.')

        correct = False
        while not correct:
            valid = False
            while not valid:
                guess = input('Enter your guess: ')

                if guess.isdigit():
                    guess = int(guess)
                    valid = True

                else:
                    print('That is an invalid guess, please enter a number between 1-9.')

            game.guesses += 1

            if game.number == guess:
                print(f'Congratulations! You have guessed the number {game.number} correctly. You took {game.guesses} guesses.')
                correct = True

            else:
                if game.number > guess:
                    print('Incorrect, my number is higher!')

                elif game.number < guess:
                    print('Incorrect, my number is lower!')

        valid = False
        while not valid:
            selection = input('Would you like to play again? ')

            if selection.lower() == 'no':
                print('Thank you for playing the guessing game.')
                valid = True
                exit = True

            elif selection.lower() == 'yes':
                valid = True
                print('Game will now restart.')

            else:
                print('Please enter either yes or no.')

