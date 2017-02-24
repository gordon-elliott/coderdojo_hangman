__copyright__ = 'Copyright(c) Gordon Elliott 2017'

import argparse
import os

from hangman.secret_word import SecretWord
from hangman.guesses import letters_from_player
from hangman.gallows import CLASSIC_GALLOWS


SECRET_WORDS_FILENAME = os.path.join(os.path.dirname(__file__), 'secret_words.txt')


def start_hangman(secret_words_filename):
    """ Start the game

        pick secret word to guess
        for each letter from user
            record guess
            if letter is not in secret word
                display gallows
            display any correct guesses so far
            if all letters found
                player wins
            if gallows complete
                player loses
    """

    secret_word = SecretWord(secret_words_filename)
    secret_word.pick_word()

    for guess, guessed_letters in letters_from_player():
        if not secret_word.contains(guess):
            CLASSIC_GALLOWS.build()
            print(CLASSIC_GALLOWS.reveal())

        matches = secret_word.matching_guesses(guessed_letters)
        print(' '.join(matches))

        if secret_word.last_guess_was_correct:
            print('Correct. You win with {} guesses'.format(len(guessed_letters)))
            break

        if CLASSIC_GALLOWS.is_complete:
            print('You lose. You guessed {}. The secret word was "{}".'.format(
                ' '.join(guessed_letters),
                secret_word
            ))
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--secret_words',
        type=str,
        default=SECRET_WORDS_FILENAME
    )
    args = parser.parse_args()

    start_hangman(args.secret_words)